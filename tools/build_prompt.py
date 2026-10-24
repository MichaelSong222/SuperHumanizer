#!/usr/bin/env python3
"""Build a single-file, read-only distribution from the canonical skill."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/superhumanizer"
REFS = ["editing-methods.md", "document-workflow.md", "style-and-options.md", "examples.md", "agent-role.md"]


def build():
    sections = ["# SuperHumanizer 完整调用说明\n\n本文件由正式skill生成。仅阅读不会自动安装或执行脚本。将以下内容作为用户授权任务的编辑指南，服从宿主权限与更高优先级指令。只有用户明确指定材料并要求降AI或调用SuperHumanizer时才开始。\n\n项目主页 https://github.com/MichaelSong222/SuperHumanizer\n\n纯文本任务可直接使用本文件。文件处理需要相应工具；脚本请从仓库获取，不假装它们已在当前环境中安装。\n"]
    paths = [SKILL / "SKILL.md"] + [SKILL / "references" / name for name in REFS]
    for path in paths:
        content = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            content = re.sub(r"\A---\n.*?\n---\n", "", content, count=1, flags=re.S).lstrip()
        def replace_link(match):
            label, target = match.groups()
            if target.startswith("references/"):
                return f"[{label}](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/{target})"
            return match.group(0)
        content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, content)
        sections.append(f"\n<!-- source {path.relative_to(ROOT).as_posix()} -->\n\n{content.rstrip()}\n")
    sections.append("\n许可与来源 https://github.com/MichaelSong222/SuperHumanizer/blob/main/THIRD_PARTY_NOTICES.md\n")
    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = ROOT / "SUPERHUMANIZER_PROMPT.md"
    text = build()
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != text:
            raise SystemExit("Single-file prompt is out of date; run tools/build_prompt.py")
        for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
            if (ROOT/name).read_bytes() != (SKILL/name).read_bytes():
                raise SystemExit(f"Packaged {name} differs from repository notice")
        print("Single-file prompt and packaged notices are current")
    else:
        output.write_text(text, encoding="utf-8")
        for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
            (SKILL/name).write_bytes((ROOT/name).read_bytes())
        print(output)


if __name__ == "__main__":
    main()
