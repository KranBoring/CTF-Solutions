import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_writeups.py"
SPEC = importlib.util.spec_from_file_location("sync_writeups", SCRIPT)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class WriteupContentTests(unittest.TestCase):
    def test_empty_heading_and_placeholders_are_not_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "write-up.md"
            path.write_text("\ufeff# Title\n\nTODO\n<!-- note -->\n", encoding="utf-8")
            self.assertFalse(sync.meaningful(path))
            path.write_text("# Title\n\nRecovered flag: example\n", encoding="utf-8")
            self.assertTrue(sync.meaningful(path))

    def test_name_normalization_handles_spaces_punctuation_and_case(self):
        self.assertEqual(sync.norm("Modular Exponentiation"), sync.norm("MODULAR_Exponentiation"))
        self.assertEqual(sync.norm("Modular-Exponentiation!"), sync.norm("Modular Exponentiation"))


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.base = self.root / "Platform" / "Crypto"
        self.base.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_index(self, table):
        path = self.base / "README.md"
        path.write_bytes(table.encode("utf-8"))
        return path

    def test_extra_columns_nested_folder_and_crlf_are_preserved(self):
        writeup = self.base / "Exercises" / "Modular_Exponentiation" / "write-up.md"
        writeup.parent.mkdir(parents=True)
        writeup.write_text("Solved with modular arithmetic.\n", encoding="utf-8")
        original = (
            "| ID | Challenge Name | Points | Write-up |\r\n"
            "| --- | --- | --- | --- |\r\n"
            "| 314 | [Modular Exponentiation](https://example.test/modular-exponentiation?id=314) | 20 | Chưa có write-up |\r\n"
        )
        readme = self.write_index(original)
        done, total, issues, changed = sync.process(readme, self.root, dry=False)
        result = readme.read_bytes()
        self.assertEqual((done, total, issues, changed), (1, 1, [], True))
        self.assertIn(b"[Modular Exponentiation](https://example.test/modular-exponentiation?id=314)", result)
        self.assertIn(b"| 314 |", result)
        self.assertIn("[Đọc write-up](Exercises/Modular_Exponentiation/write-up.md)".encode("utf-8"), result)
        self.assertNotRegex(result.decode("utf-8"), r"(?<!\r)\n")
        self.assertEqual(original.splitlines()[0].split(" | ")[:3], readme.read_text(encoding="utf-8").splitlines()[0].split(" | ")[:3])

    def test_approved_alias_uses_readme_and_challenge_id(self):
        writeup = self.base / "Legacy_Power_Task" / "write-up.md"
        writeup.parent.mkdir()
        writeup.write_text("solution", encoding="utf-8")
        (self.root / "challenge-aliases.csv").write_text(
            "readme,challenge_id,challenge,directory\n"
            "Platform/Crypto/README.md,77,Modular Exponentiation,Platform/Crypto/Legacy_Power_Task\n",
            encoding="utf-8",
        )
        readme = self.write_index(
            "| ID | Challenge | Write-up |\n| --- | --- | --- |\n"
            "| 77 | [Modular Exponentiation](https://example.test/77) | Chưa có write-up |\n"
        )
        _, _, issues, _ = sync.process(readme, self.root, dry=False)
        self.assertEqual(issues, [])
        self.assertIn("[Đọc write-up](Legacy_Power_Task/write-up.md)", readme.read_text(encoding="utf-8"))

    def test_duplicate_normalized_folder_names_are_left_unchanged(self):
        for name in ("Alpha-Beta", "Alpha_Beta"):
            folder = self.base / name
            folder.mkdir()
            (folder / "write-up.md").write_text("solution", encoding="utf-8")
        original = "| Challenge | Write-up |\n| --- | --- |\n| [Alpha Beta](https://example.test/alpha-beta) | Chưa có write-up |\n"
        readme = self.write_index(original)
        _, _, issues, changed = sync.process(readme, self.root, dry=False)
        self.assertFalse(changed)
        self.assertEqual(readme.read_text(encoding="utf-8"), original)
        self.assertTrue(any("ambiguous" in issue for issue in issues))

    def test_cryptohack_challenge_points_to_course_writeup(self):
        course = self.root / "Cryptohack" / "Course" / "Modular_Arithmetic"
        challenge = self.root / "Cryptohack" / "Challenges" / "Mathematics"
        (course / "Modular_Exponentiation").mkdir(parents=True)
        challenge.mkdir(parents=True)
        (course / "Modular_Exponentiation" / "write-up.md").write_text("solution", encoding="utf-8")
        (course / "README.md").write_text(
            "| Challenge | Write-up |\n| --- | --- |\n"
            "| [Modular Exponentiation](https://example.test/course) | [Read](./Modular_Exponentiation/write-up.md) |\n",
            encoding="utf-8",
        )
        readme = challenge / "README.md"
        readme.write_text(
            "| Challenge | Write-up |\n| --- | --- |\n"
            "| [Modular Exponentiation](https://example.test/challenge) | Chưa có write-up |\n",
            encoding="utf-8",
        )
        sync.process(readme, self.root, dry=False)
        self.assertIn("Đang nằm ở course", readme.read_text(encoding="utf-8"))
        self.assertEqual(sync.row_completion(readme, self.root), (1, 1))


    def test_navigation_readme_does_not_import_nested_event_challenges(self):
        parent = self.root / "Others-Events"
        nested = parent / "2026" / "ExampleEvent"
        readme = parent / "README.md"
        nested.mkdir(parents=True)
        readme.write_text("# Events\n\n- [2026](./2026/README.md)\n", encoding="utf-8")
        (parent / "2026" / "README.md").write_text("# 2026\n\n- [ExampleEvent](./ExampleEvent/README.md)\n", encoding="utf-8")
        (nested / "README.md").write_text("# ExampleEvent\n", encoding="utf-8")
        challenge = nested / "Crypto" / "Easy" / "Nested_Challenge"
        challenge.mkdir(parents=True)
        (challenge / "write-up.md").write_text("solution", encoding="utf-8")
        self.assertFalse(sync.create_others_event_table(readme, self.root, dry=True))
        self.assertFalse(sync.create_others_event_table(parent / "2026" / "README.md", self.root, dry=True))
        self.assertFalse(readme.exists() and readme.read_text(encoding="utf-8").count("| Challenge |"))

    def test_invalid_alias_manifest_fails_instead_of_silently_ignoring(self):
        (self.root / "challenge-aliases.csv").write_text("name,path\n", encoding="utf-8")
        readme = self.write_index(
            "| Challenge | Write-up |\n| --- | --- |\n"
            "| [Unknown](https://example.test/unknown) | Chưa có write-up |\n"
        )
        with self.assertRaisesRegex(ValueError, "requires columns"):
            sync.process(readme, self.root, dry=True)

    def test_others_events_creates_a_table_when_missing(self):
        event = self.root / "Others-Events" / "SpringCTF"
        readme = event / "README.md"
        challenge = event / "Crypto" / "Easy" / "Challenge_One"
        challenge.mkdir(parents=True)
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text("# SpringCTF\n", encoding="utf-8")
        (challenge / "write-up.md").write_text("Recovered the flag.", encoding="utf-8")
        self.assertTrue(sync.create_others_event_table(readme, self.root, dry=False))
        content = readme.read_text(encoding="utf-8")
        self.assertIn("| Challenge | Write-up |", content)
        self.assertIn("Challenge_One", content)
        self.assertIn("[Đọc write-up]", content)


if __name__ == "__main__":
    unittest.main()