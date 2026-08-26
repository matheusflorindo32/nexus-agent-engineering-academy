"""Validate the minimal Agent Skills contract used by NEXUS without YAML dependencies."""
from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


class SkillContractTests(unittest.TestCase):
    def test_skills_have_required_metadata(self) -> None:
        skill_files = sorted(SKILLS_ROOT.glob("*/SKILL.md"))
        self.assertTrue(skill_files, "at least one Skill must exist")
        for path in skill_files:
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
            self.assertIn("name", data, path)
            self.assertIn("description", data, path)
            self.assertTrue(NAME_RE.fullmatch(data["name"]), path)
            self.assertEqual(data["name"], path.parent.name, path)
            self.assertTrue(data["description"].strip(), path)
            self.assertLessEqual(len(data["name"]), 64, path)
            self.assertLessEqual(len(data["description"]), 1024, path)

    def test_skill_dirs_do_not_hide_executables(self) -> None:
        executable_suffixes = {".sh", ".bash", ".ps1", ".exe", ".bat", ".cmd"}
        for path in SKILLS_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in executable_suffixes:
                self.fail(f"executable requires explicit security review before inclusion: {path}")


if __name__ == "__main__":
    unittest.main()
