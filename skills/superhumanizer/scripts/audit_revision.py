#!/usr/bin/env python3
"""Literal and length checks. This program does not judge semantic equivalence."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

TOKEN = re.compile(r"[\u3400-\u9fff]|[^\W_]+(?:[’'\-][^\W_]+)*", re.UNICODE)
NUMBER = re.compile(r"(?<!\w)\d+(?:[,\.]\d+)*(?:%|‰)?")
CITATION = re.compile(r"\([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*\)|\[(?:\d+[,;\s–-]*)+\]")
URL = re.compile(r"https?://[^\s<>\"\)]+")


def count_units(value):
    # Each CJK character is one unit, each other contiguous word is one unit.
    spaced = re.sub(r"([\u3400-\u9fff])", r" \1 ", value)
    return len(TOKEN.findall(spaced))


def load_records(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    records = data.get("revisions") if isinstance(data, dict) else data
    if not isinstance(records, list) or not records:
        raise ValueError("Expected a nonempty list or an object with revisions")
    ids = set()
    for i, item in enumerate(records):
        if not isinstance(item, dict):
            raise ValueError(f"Record {i} must be an object")
        for field in ("original", "revised"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"Record {i} needs nonempty {field} text")
        key = item.get("id", str(i))
        if not isinstance(key, str) or key in ids:
            raise ValueError("Record IDs must be unique strings")
        ids.add(key)
        protected = item.get("protected", [])
        if not isinstance(protected, list) or any(not isinstance(x, str) or not x for x in protected):
            raise ValueError("protected must contain nonempty strings")
    return records


def audit(records, paragraph_tolerance=0.10, total_tolerance=0.05):
    rows = []
    total_before = total_after = 0
    for i, item in enumerate(records):
        before, after = item["original"], item["revised"]
        old, new = count_units(before), count_units(after)
        total_before += old
        total_after += new
        issues = []
        for label, pattern in (("numbers", NUMBER), ("citation_like_text", CITATION), ("urls", URL)):
            a, b = Counter(pattern.findall(before)), Counter(pattern.findall(after))
            if a != b:
                issues.append({"type": label, "removed": list((a-b).elements()), "added": list((b-a).elements())})
        for literal in item.get("protected", []):
            if literal not in before:
                issues.append({"type": "invalid_protected_literal", "value": literal})
            elif before.count(literal) != after.count(literal):
                issues.append({"type": "protected_literal_changed", "value": literal})
        rows.append({
            "id": item.get("id", str(i)), "before_units": old, "after_units": new,
            "change_percent": round(100*(new-old)/old, 2) if old else None,
            "length_warning": abs(new-old) > max(2, old*paragraph_tolerance),
            "literal_issues": issues,
        })
    return {
        "unit_definition": "CJK characters plus non-CJK words; not an AI score",
        "records": rows,
        "total_before_units": total_before, "total_after_units": total_after,
        "total_change_percent": round(100*(total_after-total_before)/total_before, 2) if total_before else None,
        "total_length_warning": abs(total_after-total_before) > max(2, total_before*total_tolerance),
        "literal_checks_passed": not any(r["literal_issues"] for r in rows),
        "semantic_review_required": True,
        "limitations": "Regex checks can miss citations, units, qualifiers and meaning changes. Review every claim manually.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--paragraph-tolerance", type=float, default=0.10)
    parser.add_argument("--total-tolerance", type=float, default=0.05)
    args = parser.parse_args()
    if not 0 <= args.paragraph_tolerance <= 1 or not 0 <= args.total_tolerance <= 1:
        parser.error("Tolerances must be between 0 and 1")
    try:
        result = audit(load_records(args.manifest), args.paragraph_tolerance, args.total_tolerance)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Cannot audit revisions: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["literal_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
