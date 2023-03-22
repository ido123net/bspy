from __future__ import annotations

import argparse
import datetime
import pathlib
import subprocess
import yaml
from typing import Sequence

from repos import Repos
from repos import DEFAULT_REPOS


MIT_LICENSE = """\
MIT License

Copyright (c) {} Ido Frenkel

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


def create_project(project_name: pathlib.Path) -> None:
    # Create project directory
    project_name.mkdir()

    # Create src directory
    src_dir = project_name / "src" / project_name.name.replace("-", "_")
    src_dir.mkdir(parents=True)

    # Create project.toml file
    toml_path = project_name / "project.toml"
    toml_path.write_text('[project]\n')
    toml_path.write_text(f'name = "{project_name}"\n')

    # Create README.md file
    readme_path = project_name / "README.md"
    readme_path.write_text(f"# {project_name}\n")

    # Create .gitignore file
    gitignore_path = project_name / ".gitignore"
    gitignore_path.write_text(".vscode\n")
    gitignore_path.write_text("*.pyc\n")
    gitignore_path.write_text("venv\n")

    # Create LICENSE file
    license_path = project_name / "LICENSE"
    license_path.write_text(MIT_LICENSE.format(datetime.datetime.now().year))

    create_pre_commit_config(project_name)

    # Initialize Git repository
    subprocess.run(["git", "init"], cwd=project_name)
    subprocess.run(["virtualenv", "venv"], cwd=project_name)


def create_pre_commit_config(
    project_path: pathlib.Path,
    repos: Repos = DEFAULT_REPOS,
) -> None:
    pre_commit_config_path = project_path / ".pre-commit-config.yaml"
    with pre_commit_config_path.open("w") as f:
        yaml.dump(repos.asdict(), f)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bspy")
    parser.add_argument(
        "project_name",
        help="The name of the project to create",
        type=pathlib.Path,
    )
    args = parser.parse_args(argv)
    create_project(args.project_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
