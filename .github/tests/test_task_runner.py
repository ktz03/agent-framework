# Copyright (c) Microsoft. All rights reserved.

"""Regression tests for workspace package selector matching."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))

from scripts.task_runner import project_filter_matches


class ProjectSelectorTests(unittest.TestCase):
    def assert_selected(self, selector: str, expected: list[str]) -> None:
        projects = [Path("packages/core"), Path("packages/openai")]
        selected = [
            project.as_posix()
            for project in projects
            if project_filter_matches(project, selector, aliases=[f"agent-framework-{project.name}"])
        ]
        self.assertEqual(selected, expected)

    def test_short_name(self) -> None:
        self.assert_selected("core", ["packages/core"])

    def test_short_name_with_forward_trailing_separator(self) -> None:
        self.assert_selected("core/", ["packages/core"])

    def test_short_name_with_backslash_trailing_separator(self) -> None:
        self.assert_selected("core\\", ["packages/core"])

    def test_workspace_path(self) -> None:
        self.assert_selected("packages/core", ["packages/core"])

    def test_workspace_path_with_forward_trailing_separator(self) -> None:
        self.assert_selected("packages/core/", ["packages/core"])

    def test_windows_workspace_path(self) -> None:
        self.assert_selected("packages\\core", ["packages/core"])

    def test_windows_workspace_path_with_trailing_separator(self) -> None:
        self.assert_selected("packages\\core\\", ["packages/core"])

    def test_relative_path_with_forward_trailing_separator(self) -> None:
        self.assert_selected("./packages/core/", ["packages/core"])

    def test_relative_path_with_mixed_trailing_separator(self) -> None:
        self.assert_selected("./packages\\core\\", ["packages/core"])

    def test_distribution_alias(self) -> None:
        self.assert_selected("agent-framework-core", ["packages/core"])

    def test_forward_glob(self) -> None:
        self.assert_selected("packages/*", ["packages/core", "packages/openai"])

    def test_windows_glob_with_trailing_separator(self) -> None:
        self.assert_selected("packages\\*\\", ["packages/core", "packages/openai"])


if __name__ == "__main__":
    unittest.main()
