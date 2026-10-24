from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/superhumanizer/scripts"
sys.path.insert(0, str(SCRIPTS))
import audit_revision as audit
import docx_revisions as docx
from lxml import etree


def make_fixture(path, first="Before alpha after.", table="Second paragraph.", special=None):
    root = etree.Element(docx.Q("document"), nsmap={"w": docx.W})
    body = etree.SubElement(root, docx.Q("body"))
    p = etree.SubElement(body, docx.Q("p"))
    for value in (first[:7], first[7:]):
        if not value:
            continue
        r = etree.SubElement(p, docx.Q("r"))
        etree.SubElement(r, docx.Q("t")).text = value
    tbl = etree.SubElement(body, docx.Q("tbl"))
    row = etree.SubElement(tbl, docx.Q("tr"))
    cell = etree.SubElement(row, docx.Q("tc"))
    p2 = etree.SubElement(cell, docx.Q("p"))
    etree.SubElement(etree.SubElement(p2, docx.Q("r")), docx.Q("t")).text = table
    settings = etree.Element(docx.Q("settings"), nsmap={"w": docx.W})
    etree.SubElement(settings, docx.Q("trackRevisions"), {docx.Q("val"): "false"})
    if special:
        special(root)
    files = {
        "[Content_Types].xml": b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
        "word/document.xml": docx.serialize(root),
        "word/settings.xml": docx.serialize(settings),
        "word/header1.xml": b'<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:t>Untouched header</w:t></w:r></w:p></w:hdr>',
        "word/media/opaque.bin": b"\x00\x01preserve bytes\xff",
    }
    with ZipFile(path, "w") as z:
        for name, data in files.items():
            z.writestr(name, data)
    return files


class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.source = self.base / "original.docx"
        self.output = self.base / "revised.docx"
        self.manifest = self.base / "edits.json"

    def tearDown(self):
        self.tmp.cleanup()

    def run_edit(self, records, author="Test Reviewer"):
        self.manifest.write_text(json.dumps({"revisions": records}, ensure_ascii=False), encoding="utf-8")
        return docx.apply(self.source, self.manifest, self.output, author)

    def test_round_trip_preserves_original_unselected_text_and_binary_parts(self):
        files = make_fixture(self.source)
        original_bytes = self.source.read_bytes()
        result = self.run_edit([{"id":"R1", "paragraph_index":0, "original":"alpha", "revised":"beta"}])
        saved, _ = docx.load_docx(self.output)
        root = docx.parse(saved["word/document.xml"])
        ps = docx.paragraphs(root)
        self.assertEqual(docx.view(ps[0], True), "Before beta after.")
        self.assertEqual(docx.view(ps[0], False), "Before alpha after.")
        self.assertEqual(docx.view(ps[1], True), "Second paragraph.")
        self.assertEqual(original_bytes, self.source.read_bytes())
        self.assertEqual(saved["word/media/opaque.bin"], files["word/media/opaque.bin"])
        self.assertEqual(saved["word/header1.xml"], files["word/header1.xml"])
        wrappers = root.xpath("//w:ins|//w:del", namespaces=docx.NS)
        self.assertEqual(len(wrappers), 2)
        self.assertEqual({x.get(docx.Q("author")) for x in wrappers}, {"Test Reviewer"})
        self.assertEqual(len({x.get(docx.Q("id")) for x in wrappers}), 2)
        self.assertEqual(docx.parse(saved["word/settings.xml"]).find(docx.Q("trackRevisions")).get(docx.Q("val")), "true")
        self.assertTrue(result["accept_reject_text_verified"])
        self.assertFalse(result["rendered"])

    def test_multiple_edits_use_original_offsets(self):
        make_fixture(self.source, first="alpha and omega.")
        self.run_edit([
            {"id":"R2", "paragraph_index":0, "original":"omega", "revised":"the final item"},
            {"id":"R1", "paragraph_index":0, "original":"alpha", "revised":"the first item"},
        ])
        self.assertEqual(docx.inspect(self.output)["paragraphs"][0]["text"], "the first item and the final item.")

    def test_unicode_table_replacement(self):
        make_fixture(self.source, table="项目可能有效。")
        self.run_edit([{"paragraph_index":1, "start":2, "original":"可能有效", "revised":"或许有效"}])
        self.assertEqual(docx.inspect(self.output)["paragraphs"][1]["text"], "项目或许有效。")

    def test_ambiguous_text_requires_start(self):
        make_fixture(self.source, first="alpha alpha")
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            self.run_edit([{"paragraph_index":0, "original":"alpha", "revised":"beta"}])
        self.assertFalse(self.output.exists())
        self.run_edit([{"paragraph_index":0, "start":6, "original":"alpha", "revised":"beta"}])
        self.assertEqual(docx.inspect(self.output)["paragraphs"][0]["text"], "alpha beta")

    def test_stale_text_and_overlapping_spans_rejected(self):
        make_fixture(self.source)
        with self.assertRaisesRegex(ValueError, "Stale"):
            self.run_edit([{"paragraph_index":0, "start":0, "original":"alpha", "revised":"beta"}])
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            self.run_edit([
                {"id":"a", "paragraph_index":0, "original":"alpha", "revised":"beta"},
                {"id":"b", "paragraph_index":0, "original":"alpha after", "revised":"gamma"},
            ])
        self.assertFalse(self.output.exists())

    def test_existing_revisions_in_header_rejected(self):
        files = make_fixture(self.source)
        files["word/header1.xml"] = b'<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:ins/></w:p></w:hdr>'
        with ZipFile(self.source, "w") as z:
            for n,b in files.items():
                z.writestr(n,b)
        with self.assertRaisesRegex(ValueError, "Existing revisions"):
            self.run_edit([{"paragraph_index":0, "original":"alpha", "revised":"beta"}])

    def test_hyperlink_target_rejected(self):
        def mutate(root):
            p=docx.paragraphs(root)[0]
            node=p[0]
            p.remove(node)
            h=etree.SubElement(p, docx.Q("hyperlink"))
            h.append(node)
        make_fixture(self.source, special=mutate)
        with self.assertRaisesRegex(ValueError, "complex element"):
            self.run_edit([{"paragraph_index":0, "original":"alpha", "revised":"beta"}])

    def test_mixed_text_formats_rejected(self):
        def mutate(root):
            run=docx.paragraphs(root)[0][1]
            props=etree.Element(docx.Q("rPr"))
            etree.SubElement(props, docx.Q("b"))
            run.insert(0, props)
        make_fixture(self.source, special=mutate)
        with self.assertRaisesRegex(ValueError, "multiple text formats"):
            self.run_edit([{"paragraph_index":0, "original":"Before alpha", "revised":"Before beta"}])

    def test_tables_in_complex_containers_rejected(self):
        for container in ("sdt", "customXml", "txbxContent", "AlternateContent"):
            with self.subTest(container=container):
                def mutate(root):
                    body = root.find(docx.Q("body"))
                    table = body.find(docx.Q("tbl"))
                    body.remove(table)
                    if container == "AlternateContent":
                        tag = "{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"
                    else:
                        tag = docx.Q(container)
                    wrapper = etree.SubElement(body, tag)
                    if container == "sdt":
                        props = etree.SubElement(wrapper, docx.Q("sdtPr"))
                        etree.SubElement(props, docx.Q("lock"), {docx.Q("val"): "sdtContentLocked"})
                        etree.SubElement(props, docx.Q("dataBinding"), {docx.Q("xpath"): "/data/value"})
                        wrapper = etree.SubElement(wrapper, docx.Q("sdtContent"))
                    wrapper.append(table)
                make_fixture(self.source, special=mutate)
                source_bytes = self.source.read_bytes()
                with self.assertRaisesRegex(ValueError, "nested targets"):
                    self.run_edit([{"paragraph_index":1, "original":"Second", "revised":"Changed"}])
                self.assertFalse(self.output.exists())
                self.assertEqual(self.source.read_bytes(), source_bytes)

    def test_ordinary_nested_table_remains_supported(self):
        def mutate(root):
            cell = root.find(".//" + docx.Q("tc"))
            paragraph = cell.find(docx.Q("p"))
            cell.remove(paragraph)
            table = etree.SubElement(cell, docx.Q("tbl"))
            row = etree.SubElement(table, docx.Q("tr"))
            nested_cell = etree.SubElement(row, docx.Q("tc"))
            nested_cell.append(paragraph)
        make_fixture(self.source, special=mutate)
        self.run_edit([{"paragraph_index":1, "original":"Second", "revised":"Changed"}])
        self.assertEqual(docx.inspect(self.output)["paragraphs"][1]["text"], "Changed paragraph.")

    def test_author_and_output_protection(self):
        make_fixture(self.source)
        records=[{"paragraph_index":0, "original":"alpha", "revised":"beta"}]
        with self.assertRaisesRegex(ValueError, "reviewer"):
            self.run_edit(records, author=" ")
        self.output.write_text("Keep this existing file")
        with self.assertRaisesRegex(ValueError, "new path"):
            self.run_edit(records)
        self.assertEqual(self.output.read_text(), "Keep this existing file")

    def test_same_source_destination_rejected(self):
        make_fixture(self.source)
        original=self.source.read_bytes()
        self.manifest.write_text(json.dumps([{"paragraph_index":0, "original":"alpha", "revised":"beta"}]))
        with self.assertRaisesRegex(ValueError, "new path"):
            docx.apply(self.source, self.manifest, self.source, "Reviewer")
        self.assertEqual(original, self.source.read_bytes())


class AuditTests(unittest.TestCase):
    def test_changed_numbers_citations_and_protected_words_are_flagged(self):
        result=audit.audit([{"original":"It may affect 10 cases (Sample, 2024).", "revised":"It will affect 20 cases (Sample, 2025).", "protected":["may"]}])
        self.assertFalse(result["literal_checks_passed"])
        kinds={x["type"] for x in result["records"][0]["literal_issues"]}
        self.assertEqual(kinds, {"numbers", "citation_like_text", "protected_literal_changed"})

    def test_semantics_are_not_claimed_by_literal_audit(self):
        result=audit.audit([{"original":"The policy may help.", "revised":"The policy will help."}])
        self.assertTrue(result["literal_checks_passed"])
        self.assertTrue(result["semantic_review_required"])

    def test_mixed_language_count_and_length_warning(self):
        self.assertEqual(audit.count_units("我们 test 2"), 4)
        result=audit.audit([{"original":"One brief sentence.", "revised":"This is a much longer sentence with several additional words."}])
        self.assertTrue(result["records"][0]["length_warning"])


class PackageTests(unittest.TestCase):
    def test_internal_markdown_links_resolve(self):
        for path in ROOT.rglob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((path.parent/target.split("#")[0]).exists(), f"{path} -> {target}")

    def test_no_private_files_or_paths_in_distribution(self):
        for path in ROOT.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or ".git" in path.parts:
                continue
            self.assertNotIn(path.suffix.lower(), {".docx", ".pdf", ".zip"})
            content=path.read_text(encoding="utf-8")
            self.assertNotIn("/Users/" + "apple/", content)
            self.assertNotIn("com.tencent." + "xinWeChat", content)


if __name__ == "__main__":
    unittest.main()
