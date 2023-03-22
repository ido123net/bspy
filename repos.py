from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class Hook:
    id: str
    alias: str | None = None
    name: str | None = None
    languge_version: str | None = None
    files: str | None = None
    exclude: str | None = None
    types: str | None = None
    types_or: str | None = None
    exclude_types: str | None = None
    args: list[str] | None = None
    stages: list[str] | None = None
    additional_dependencies: list[str] | None = None
    always_run: bool | None = None
    verbose: bool | None = None
    log_file: str | None = None

    def __iter__(self):
        for field in dataclasses.fields(self):
            attr = getattr(self, field.name)
            if attr is not None:
                yield field.name, attr

    def asdict(self) -> dict[str, Any]:
        return dict(self)


@dataclasses.dataclass
class Repo:
    repo: str
    rev: str
    hooks: list[Hook]

    def __iter__(self):
        for field in dataclasses.fields(self):
            attr = getattr(self, field.name)
            if attr is not None:
                yield field.name, attr

    def asdict(self) -> dict[str, Any]:
        d = dict(self)
        d["hooks"] = [hook.asdict() for hook in self.hooks]
        return d


@dataclasses.dataclass
class Repos:
    repos: list[Repo]
    default_install_hook_types: str | None = None
    default_language_version: dict[str, str] | None = None
    default_stages: list[str] | None = None
    files: str | None = None
    exclude: str | None = None
    fail_fast: bool | None = None
    minimum_pre_commit_version: str | None = None

    def __iter__(self):
        for field in dataclasses.fields(self):
            attr = getattr(self, field.name)
            if attr is not None:
                yield field.name, attr

    def asdict(self) -> dict[str, Any]:
        d = dict(self)
        d["repos"] = [repo.asdict() for repo in self.repos]
        return d


DEFAULT_REPOS = Repos(
    repos=[
        Repo(
            repo="https://github.com/psf/black",
            rev="23.1.0",
            hooks=[
                Hook(
                    id="black",
                )
            ],
        ),
        Repo(
            repo="https://github.com/PyCQA/flake8",
            rev="6.0.0",
            hooks=[
                Hook(
                    id="flake8",
                )
            ],
        ),
        Repo(
            repo="https://github.com/pycqa/isort",
            rev="5.11.2",
            hooks=[
                Hook(
                    id="isort",
                )
            ],
        ),
        Repo(
            repo="https://github.com/asottile/pyupgrade",
            rev="v3.3.1",
            hooks=[
                Hook(
                    id="pyupgrade",
                    args=["--py38-plus"],
                )
            ],
        ),
    ]
)
