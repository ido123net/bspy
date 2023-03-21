import datetime
import os
import subprocess

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


def create_project(project_name):
    # Create project directory
    os.makedirs(project_name)

    # Create src directory
    src_dir = os.path.join(project_name, "src", project_name)
    os.makedirs(src_dir)

    # Create project.toml file
    toml_path = os.path.join(project_name, "project.toml")
    with open(toml_path, "w") as f:
        f.write('[project]\nname = "{}"\n'.format(project_name))

    # Create README.md file
    readme_path = os.path.join(project_name, "README.md")
    with open(readme_path, "w") as f:
        f.write(f"# {project_name}\n")

    # Create .gitignore file
    gitignore_path = os.path.join(project_name, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write(".vscode\n*.pyc\nvenv\n")

    # Create LICENSE file
    license_path = os.path.join(project_name, "LICENSE")
    with open(license_path, "w") as f:
        f.write(MIT_LICENSE.format(datetime.datetime.now().year))

    create_pre_commit_config(project_name)

    # Initialize Git repository
    subprocess.run(["git", "init"], cwd=project_name)
    subprocess.run(["virtualenv", "venv"], cwd=project_name)


def create_pre_commit_config(project_name):
    pre_commit_config_path = os.path.join(project_name, ".pre-commit-config.yaml")
    with open(pre_commit_config_path, "w") as f:
        f.write("repos:\n")
        f.write("-   repo: https://github.com/psf/black\n")
        f.write("    rev: 23.1.0\n")
        f.write("    hooks:\n")
        f.write("    -   id: black\n")
        f.write("-   repo: https://github.com/PyCQA/flake8\n")
        f.write("    rev: 6.0.0\n")
        f.write("    hooks:\n")
        f.write("    -   id: flake8\n")
        f.write("-   repo: https://github.com/pycqa/isort\n")
        f.write("    rev: 5.11.2\n")
        f.write("    hooks:\n")
        f.write("    -   id: isort\n")
        f.write("-   repo: https://github.com/asottile/pyupgrade\n")
        f.write("    rev: v3.3.1\n")
        f.write("    hooks:\n")
        f.write("    -   id: pyupgrade\n")
        f.write("        args: [--py38-plus]\n")


if __name__ == "__main__":
    create_project("my_project")
