from __future__ import annotations

import datetime
import enum
import pathlib

import git
import virtualenv
import yaml

from bspy.repos import DEFAULT_REPOS, Repos

DEFAULT_GITIGNORE = [
    ".vscode",
    "*.pyc",
    "venv",
]
DEFAULT_TOML = """\
[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
authors = [
    {{name = "{name}", email = "{email}"}}
]
readme = "README.md"
requires-python = ">=3.8"
license = {{text = "LICENSE"}}
version = "0.0.1"

[tool.setuptools.packages.find]
where = ["src"]

[tool.isort]
profile = 'black'
"""
DEFAULT_FLAKE8 = """\
[flake8]
max-line-length = 88
extend-ignore = E203
"""
MIT_LICENSE = """\
MIT License

Copyright (c) {year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


class LicenseType(enum.Enum):
    MIT = enum.auto()


class Project:
    def __init__(self, name: str) -> None:
        self.name = name.replace("-", "_")
        self.project_p = pathlib.Path(name)
        self.repo = git.Repo.init(self.project_p)
        self.src_d = self.project_p / "src"
        self.toml_p = self.project_p / "pyproject.toml"
        self.flake8_p = self.project_p / ".flake8"
        self.readme_p = self.project_p / "README.md"
        self.gitignore_p = self.project_p / ".gitignore"
        self.license_p = self.project_p / "LICENSE"
        self.pre_commit_config_p = self.project_p / ".pre-commit-config.yaml"
        self.venv = self.project_p / "venv"

    def create_gitignore(self, ignore_patterns: list[str] = DEFAULT_GITIGNORE) -> None:
        with self.gitignore_p.open("w") as f:
            for ignore_pattern in ignore_patterns:
                f.write(f"{ignore_pattern}\n")

    def create_toml(self) -> None:
        git_config = self.repo.config_reader()
        name = git_config.get_value("user", "name")
        email = git_config.get_value("user", "email")
        text = DEFAULT_TOML.format(project_name=self.name, name=name, email=email)
        self.toml_p.write_text(text)

    def create_flake8(self, text: str = DEFAULT_FLAKE8) -> None:
        self.flake8_p.write_text(text)

    def create_readme(self) -> None:
        self.readme_p.write_text(f"# {self.name.replace('_', ' ')}\n")

    def create_license(self, license_type: str = "MIT") -> None:
        git_config = self.repo.config_reader()
        name = git_config.get_value("user", "name")
        year = datetime.datetime.now().year

        if license_type == "MIT":
            text = MIT_LICENSE.format(year=year, name=name)
        else:
            raise NotImplementedError

        self.license_p.write_text(text)

    def create_pre_commit_config(self, repos: Repos = DEFAULT_REPOS) -> None:
        with self.pre_commit_config_p.open("w") as f:
            yaml.safe_dump(repos.asdict(), f, sort_keys=False)

    def create_src(self) -> None:
        (self.src_d / self.name).mkdir(parents=True)
        (self.src_d / self.name / "__init__.py").touch()

    def create_venv(self) -> None:
        virtualenv.cli_run(["venv"])

    def create_all(self) -> None:
        self.create_gitignore()
        self.create_toml()
        self.create_flake8()
        self.create_readme()
        self.create_license()
        self.create_pre_commit_config()
        self.create_src()
        self.create_venv()
