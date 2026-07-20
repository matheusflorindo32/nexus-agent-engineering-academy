"""Behavioral regression tests for the repository validator."""
from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("validate_repository.py")
SPEC = spec_from_file_location("nexus_repository_validator", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def frontmatter(doc_id: str, *, slug: str | None = None, prerequisites: str | None = None) -> str:
    fields = [
        "---",
        f"id: {doc_id}",
        "title: Test document",
        "lang: pt-BR",
        "status: draft",
    ]
    if slug is not None:
        fields.append(f"slug: {slug}")
    if prerequisites is not None:
        fields.append(f"prerequisites: {prerequisites}")
    return "\n".join([*fields, "---", "", "# Test document", ""])


class ValidatorBehaviorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory(prefix="nexus-validator-test-")
        self.root = Path(self.temporary_directory.name)
        self.root_patch = patch.object(VALIDATOR, "ROOT", self.root)
        self.root_patch.start()

    def tearDown(self) -> None:
        self.root_patch.stop()
        self.temporary_directory.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def test_rejects_missing_frontmatter(self) -> None:
        path = self.write("docs/missing.md", "# Missing frontmatter\n")
        errors: list[str] = []
        VALIDATOR.check_frontmatter([path], errors)
        self.assert_error(errors, "frontmatter YAML ausente")

    def test_rejects_duplicate_id(self) -> None:
        first = self.write("docs/first.md", frontmatter("docs.duplicate"))
        second = self.write("docs/second.md", frontmatter("docs.duplicate"))
        errors: list[str] = []
        VALIDATOR.check_frontmatter([first, second], errors)
        self.assert_error(errors, "id duplicado")

    def test_rejects_duplicate_explicit_slug(self) -> None:
        first = self.write("docs/first.md", frontmatter("docs.first", slug="same-slug"))
        second = self.write("docs/second.md", frontmatter("docs.second", slug="same-slug"))
        errors: list[str] = []
        VALIDATOR.check_frontmatter([first, second], errors)
        self.assert_error(errors, "slug duplicado")

    def test_derived_slugs_include_repository_path(self) -> None:
        first = self.write("course/README.md", frontmatter("course.index"))
        second = self.write("docs/README.md", frontmatter("docs.index"))
        errors: list[str] = []
        VALIDATOR.check_frontmatter([first, second], errors)
        self.assertFalse(any("slug duplicado" in error for error in errors), errors)

    def test_rejects_missing_prerequisite(self) -> None:
        path = self.write(
            "course/module.md",
            frontmatter("course.module.current", prerequisites="[course.module.missing]"),
        )
        errors: list[str] = []
        VALIDATOR.check_frontmatter([path], errors)
        self.assert_error(errors, "pré-requisito inexistente")

    def test_accepts_existing_prerequisite(self) -> None:
        first = self.write("course/first.md", frontmatter("course.module.first"))
        second = self.write(
            "course/second.md",
            frontmatter("course.module.second", prerequisites="[course.module.first]"),
        )
        errors: list[str] = []
        VALIDATOR.check_frontmatter([first, second], errors)
        self.assertFalse(any("pré-requisito" in error for error in errors), errors)

    def test_rejects_broken_internal_link(self) -> None:
        path = self.write("docs/source.md", frontmatter("docs.source") + "[Missing](missing.md)\n")
        errors: list[str] = []
        VALIDATOR.check_links([path], errors)
        self.assert_error(errors, "link interno quebrado")

    def test_rejects_duplicate_module_number(self) -> None:
        body = "\n".join(
            [*VALIDATOR.REQUIRED_MODULE_SECTIONS, "## Laboratório", "## Avaliação", ""]
        )
        self.write("course/modules/00-first/README.md", body)
        self.write("course/modules/00-second/README.md", body)
        errors: list[str] = []
        VALIDATOR.check_modules(errors)
        self.assert_error(errors, "número de módulo duplicado 00")

    def test_rejects_missing_required_module(self) -> None:
        errors: list[str] = []
        VALIDATOR.check_modules(errors)
        self.assert_error(errors, "módulos obrigatórios ausentes")

    def test_rejects_duplicate_lab_number(self) -> None:
        body = "\n".join([*VALIDATOR.REQUIRED_LAB_SECTIONS, "## Procedimento", ""])
        self.write("labs/LAB-101-first.md", body)
        self.write("labs/LAB-101-second.md", body)
        errors: list[str] = []
        VALIDATOR.check_labs(errors)
        self.assert_error(errors, "número de laboratório duplicado 101")

    def test_rejects_missing_required_lab(self) -> None:
        errors: list[str] = []
        VALIDATOR.check_labs(errors)
        self.assert_error(errors, "laboratórios obrigatórios ausentes")

    def test_secret_scan_includes_env_and_aws_access_key(self) -> None:
        self.write(".env", "OPENAI_API_KEY=sk-" + "A" * 24 + "\n")
        aws_access_key = "AKIA" + "IOSFODNN7EXAMPLE"
        self.write("settings.py", f'AWS_ACCESS_KEY_ID = "{aws_access_key}"\n')
        errors: list[str] = []
        VALIDATOR.check_secrets(errors)
        self.assert_error(errors, "OpenAI-style key")
        self.assert_error(errors, "AWS access key ID")

    def test_secret_scan_avoids_short_placeholders(self) -> None:
        self.write(".env.example", "OPENAI_API_KEY=sk-example\n")
        self.write("settings.py", 'AWS_ACCESS_KEY_ID = "AKIAEXAMPLE"\n')
        errors: list[str] = []
        VALIDATOR.check_secrets(errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
