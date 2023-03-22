from __future__ import annotations

import argparse
from typing import Sequence

from project import Project


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bspy")
    parser.add_argument(
        "project_name",
        help="The name of the project to create",
        type=str,
    )
    args = parser.parse_args(argv)
    project = Project(args.project_name)
    project.create_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
