# Copyright (c) Microsoft. All rights reserved.

from pathlib import Path
from unittest.mock import patch

from packaging.version import Version

from scripts.dependencies._dependency_bounds_upper_impl import _collect_development_pin_replacements
from scripts.dependencies.upgrade_dev_dependencies import (
    _apply_tool_requirement_replacements,
    _collect_tool_requirement_replacements,
)
from scripts.tool_requirements import load_requirements


class _VersionCatalog:
    def __init__(self, versions: dict[str, list[str]]) -> None:
        self._versions = versions

    def get(self, package_name: str) -> list[Version]:
        return [Version(version) for version in self._versions.get(package_name, [])]


def test_collect_tool_requirement_replacements_preserves_extras_and_markers(tmp_path: Path) -> None:
    requirements_file = tmp_path / "testing.txt"
    requirements_file.write_text('# Test tools\npytest==9.1.1\npytest-xdist[psutil]==3.8.0; python_version >= "3.10"\n')
    catalog = _VersionCatalog({
        "pytest": ["9.1.1", "9.2.0"],
        "pytest-xdist": ["3.8.0", "3.9.0"],
    })

    replacements = _collect_tool_requirement_replacements(requirements_file, catalog=catalog)  # type: ignore[arg-type]

    assert replacements == {
        "pytest==9.1.1": "pytest==9.2.0",
        'pytest-xdist[psutil]==3.8.0; python_version >= "3.10"': (
            'pytest-xdist[psutil]==3.9.0; python_version >= "3.10"'
        ),
    }


def test_collect_development_pins_skips_coordinated_uv_upgrade(tmp_path: Path) -> None:
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(
        """
[project]
name = "test-project"
version = "1.0.0"

[dependency-groups]
dev = ["uv==0.12.23", "poethepoet==0.48.0"]
"""
    )
    catalog = _VersionCatalog({
        "poethepoet": ["0.48.0", "0.49.0"],
        "uv": ["0.12.23", "0.12.24"],
    })

    replacements = _collect_development_pin_replacements(pyproject_file, catalog=catalog)  # type: ignore[arg-type]

    assert replacements == {"poethepoet==0.48.0": "poethepoet==0.49.0"}


def test_apply_tool_requirement_replacements_preserves_includes_and_comments(tmp_path: Path) -> None:
    requirements_file = tmp_path / "all.txt"
    requirements_file.write_text("# Shared tools\n-r runtime.txt\nruff==0.16.10\n")

    _apply_tool_requirement_replacements(requirements_file, {"ruff==0.16.10": "ruff==0.17.0"})

    assert requirements_file.read_text() == "# Shared tools\n-r runtime.txt\nruff==0.17.0\n"


def test_collect_tool_requirement_replacements_reads_utf8_comments(tmp_path: Path) -> None:
    requirements_file = tmp_path / "testing.txt"
    requirements_file.write_text("# 日本語 documentation\npytest==9.1.1\n", encoding="utf-8")
    catalog = _VersionCatalog({"pytest": ["9.1.1", "9.2.0"]})

    replacements = _collect_tool_requirement_replacements(requirements_file, catalog=catalog)  # type: ignore[arg-type]

    assert replacements == {"pytest==9.1.1": "pytest==9.2.0"}


def test_apply_tool_requirement_replacements_preserves_utf8_comments(tmp_path: Path) -> None:
    requirements_file = tmp_path / "all.txt"
    requirements_file.write_text("# 日本語 documentation\n-r runtime.txt\nruff==0.16.10\n", encoding="utf-8")

    _apply_tool_requirement_replacements(requirements_file, {"ruff==0.16.10": "ruff==0.17.0"})

    assert requirements_file.read_text(encoding="utf-8") == "# 日本語 documentation\n-r runtime.txt\nruff==0.17.0\n"


def test_load_requirements_reads_utf8_comments_in_included_files(tmp_path: Path) -> None:
    (tmp_path / "requirements-testing.txt").write_text("# Test tools\n-r runtime.txt\npytest==9.1.1\n", encoding="utf-8")
    (tmp_path / "runtime.txt").write_text("# 日本語 documentation\nrich==15.0.0\n", encoding="utf-8")

    with patch("scripts.tool_requirements.REQUIREMENTS_ROOT", tmp_path):
        assert load_requirements("testing") == ("rich==15.0.0", "pytest==9.1.1")
