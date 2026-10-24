#!/usr/bin/env python3
"""Create bounded DOCX tracked replacements with verified accept/reject text views.

Requires lxml. Complex targets and documents with existing revisions are rejected.
No rendering or semantic validation is performed here.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree
from audit_revision import load_records

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
Q = lambda name: f"{{{W}}}{name}"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
REVISION_TAGS = {"ins", "del", "moveFrom", "moveTo", "cellIns", "cellDel", "cellMerge"}


def parse(data):
    parser = etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    root = etree.fromstring(data, parser)
    if root.getroottree().docinfo.doctype:
        raise ValueError("DTD declarations are not supported")
    return root


def serialize(root):
    return etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone=True)


def load_docx(path):
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [x.filename for x in infos]
        if len(set(names)) != len(names):
            raise ValueError("Duplicate ZIP entries are not supported")
        if sum(x.file_size for x in infos) > 256*1024*1024:
            raise ValueError("Package exceeds the 256 MiB uncompressed limit")
        if archive.testzip() is not None:
            raise ValueError("Corrupt ZIP package")
        files = {x.filename: archive.read(x) for x in infos}
    if "word/document.xml" not in files:
        raise ValueError("DOCX document.xml is missing")
    if any(name.startswith("_xmlsignatures/") for name in files):
        raise ValueError("Signed packages require an application workflow")
    return files, infos


def paragraphs(root):
    return root.xpath("/w:document/w:body//w:p", namespaces=NS)


def view(paragraph, accept):
    result = []
    for node in paragraph.xpath(".//w:t|.//w:delText", namespaces=NS):
        ancestors = {etree.QName(p).localname for p in node.iterancestors()}
        if accept and "del" in ancestors:
            continue
        if not accept and "ins" in ancestors:
            continue
        result.append(node.text or "")
    return "".join(result)


def existing_revisions(files):
    found = []
    for name, data in files.items():
        if not name.startswith("word/") or not name.endswith(".xml"):
            continue
        root = parse(data)
        for node in root.iter():
            if not isinstance(node.tag, str):
                continue
            tag = etree.QName(node)
            if tag.namespace == W and (tag.localname in REVISION_TAGS or tag.localname.endswith("Change") or tag.localname.startswith("moveFrom") or tag.localname.startswith("moveTo")):
                found.append(name)
                break
    return found


def inspect(path):
    files, _ = load_docx(path)
    root = parse(files["word/document.xml"])
    return {"sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            "revision_parts": existing_revisions(files),
            "paragraphs": [{"paragraph_index": i, "text": view(p, True)} for i, p in enumerate(paragraphs(root))],
            "scope": "Body and table paragraphs only; headers and footnotes are not editable by this helper"}


def simple_runs(paragraph):
    ancestors = list(paragraph.iterancestors())
    ordinary_containers = {Q(name) for name in ("body", "tc", "tr", "tbl", "document")}
    if (not ancestors or ancestors[0].tag not in {Q("body"), Q("tc")}
            or any(node.tag not in ordinary_containers for node in ancestors)
            or ancestors[-1].tag != Q("document")):
        raise ValueError("Text boxes, content controls and other nested targets require Word/WPS")
    runs, offset = [], 0
    for child in paragraph:
        if child.tag == Q("pPr"):
            continue
        if child.tag == Q("proofErr"):
            continue
        if child.tag != Q("r"):
            raise ValueError("Target paragraph contains a bookmark, hyperlink or other complex element")
        if any(c.tag not in {Q("rPr"), Q("t")} for c in child):
            raise ValueError("Target run contains a field, break, drawing or other non-text element")
        texts = child.findall(Q("t"))
        if len(texts) != 1 or not texts[0].text:
            raise ValueError("Target paragraph contains an empty or compound text run")
        value = texts[0].text
        runs.append((offset, offset+len(value), child, value))
        offset += len(value)
    return runs


def source_slice(runs, start, end):
    output = []
    for lo, hi, run, value in runs:
        a, b = max(lo, start), min(hi, end)
        if a >= b:
            continue
        copy = deepcopy(run)
        text = copy.find(Q("t"))
        text.text = value[a-lo:b-lo]
        text.set(XML_SPACE, "preserve")
        output.append(copy)
    return output


def style_key(run):
    props = run.find(Q("rPr"))
    return b"" if props is None else etree.tostring(props, method="c14n")


def apply(source, manifest, destination, author):
    source, destination = Path(source), Path(destination)
    if not author or not author.strip():
        raise ValueError("An explicitly supplied reviewer name is required")
    if source.resolve() == destination.resolve() or destination.exists():
        raise ValueError("Output must be a new path distinct from the source")
    records = load_records(manifest)
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    files, infos = load_docx(source)
    if existing_revisions(files):
        raise ValueError("Existing revisions found; use Word/WPS without accepting others' changes")
    if "word/settings.xml" not in files:
        raise ValueError("settings.xml is missing; use a document application")
    root = parse(files["word/document.xml"])
    ps = paragraphs(root)
    old_views = [view(p, True) for p in ps]
    expected = list(old_views)
    grouped = {}
    for i, edit in enumerate(records):
        index = edit.get("paragraph_index")
        if type(index) is not int or not 0 <= index < len(ps):
            raise ValueError(f"Invalid paragraph_index in record {i}")
        before = old_views[index]
        original = edit["original"]
        if "start" in edit:
            start = edit["start"]
            if type(start) is not int or start < 0:
                raise ValueError("start must be a nonnegative Unicode character offset")
        else:
            matches = [j for j in range(len(before)) if before.startswith(original, j)]
            if len(matches) != 1:
                raise ValueError("Original text is missing or ambiguous; supply verified start")
            start = matches[0]
        end = start + len(original)
        if before[start:end] != original:
            raise ValueError("Stale original text or wrong offset")
        if original == edit["revised"]:
            raise ValueError("Unchanged text does not need tracked replacement")
        if any(c in edit["revised"] for c in "\r\n\t"):
            raise ValueError("Paragraph or tab changes require a document application")
        grouped.setdefault(index, []).append((start, end, edit))
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    numeric_ids = [int(v) for v in root.xpath("//@w:id", namespaces=NS) if v.isdigit()]
    next_id = max(numeric_ids + [0]) + 1
    revision_ids = []

    def wrapper(kind, runs):
        nonlocal next_id
        node = etree.Element(Q(kind), {Q("id"): str(next_id), Q("author"): author, Q("date"): stamp})
        revision_ids.append(next_id)
        next_id += 1
        for run in runs:
            if kind == "del":
                for t in run.findall(Q("t")):
                    t.tag = Q("delText")
            node.append(run)
        return node

    for index, edits in grouped.items():
        edits.sort(key=lambda x: x[0])
        if any(a[1] > b[0] for a, b in zip(edits, edits[1:])):
            raise ValueError("Overlapping replacements are not supported")
        p = ps[index]
        runs = simple_runs(p)
        content, cursor, expected_text = [], 0, []
        for start, end, edit in edits:
            selected = [r for lo, hi, r, _ in runs if lo < end and hi > start]
            if not selected or len({style_key(r) for r in selected}) != 1:
                raise ValueError("Replacement spans multiple text formats; use Word/WPS")
            content.extend(source_slice(runs, cursor, start))
            content.append(wrapper("del", source_slice(runs, start, end)))
            inserted = deepcopy(selected[0])
            inserted.find(Q("t")).text = edit["revised"]
            inserted.find(Q("t")).set(XML_SPACE, "preserve")
            content.append(wrapper("ins", [inserted]))
            expected_text.extend([old_views[index][cursor:start], edit["revised"]])
            cursor = end
        content.extend(source_slice(runs, cursor, len(old_views[index])))
        expected_text.append(old_views[index][cursor:])
        expected[index] = "".join(expected_text)
        for child in list(p):
            if child.tag != Q("pPr"):
                p.remove(child)
        p.extend(content)
    if [view(p, False) for p in ps] != old_views or [view(p, True) for p in ps] != expected:
        raise ValueError("Accept/reject verification failed")
    settings = parse(files["word/settings.xml"])
    track = settings.find(Q("trackRevisions"))
    if track is None:
        track = etree.SubElement(settings, Q("trackRevisions"))
    track.set(Q("val"), "true")
    output = dict(files)
    output["word/document.xml"] = serialize(root)
    output["word/settings.xml"] = serialize(settings)
    # Exclusive creation also protects an output created after the initial check.
    with destination.open("xb") as stream:
        with ZipFile(stream, "w", compression=ZIP_DEFLATED) as archive:
            for info in infos:
                archive.writestr(info, output[info.filename])
    readback, _ = load_docx(destination)
    rb = paragraphs(parse(readback["word/document.xml"]))
    if [view(p, True) for p in rb] != expected or [view(p, False) for p in rb] != old_views:
        raise ValueError("Saved file failed accept/reject validation; do not deliver it")
    if not all(readback[n] == b for n, b in files.items() if n not in {"word/document.xml", "word/settings.xml"}):
        raise ValueError("Unexpected package changes; do not deliver the output")
    if hashlib.sha256(source.read_bytes()).hexdigest() != source_hash:
        raise ValueError("Source changed during the operation; verify versions before delivery")
    return {"output": str(destination), "reviewer": author, "replacements": len(records),
            "revision_ids": revision_ids, "accept_reject_text_verified": True,
            "other_parts_byte_preserved": True, "source_sha256": source_hash,
            "rendered": False, "semantic_review_required": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    read = commands.add_parser("inspect")
    read.add_argument("source")
    write = commands.add_parser("apply")
    write.add_argument("source")
    write.add_argument("manifest")
    write.add_argument("destination")
    write.add_argument("--author", required=True)
    args = parser.parse_args()
    try:
        result = inspect(args.source) if args.command == "inspect" else apply(args.source, args.manifest, args.destination, args.author)
    except (ValueError, OSError, etree.XMLSyntaxError) as error:
        parser.exit(2, f"Cannot process document: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
