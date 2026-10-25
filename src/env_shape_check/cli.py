
"""Command-line interface for env-shape-check."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class EnvFileError(ValueError):
    """An environment file could not be read or parsed safely."""


def read_names(path: Path) -> set[str]:
    """Read assignment names only; never retain or return assignment values."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise EnvFileError(f"cannot read {path}: {exc}") from exc

    names: set[str] = set()
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        if "=" not in line:
            raise EnvFileError(f"{path}:{line_number}: expected NAME=value assignment")

        name = line.split("=", maxsplit=1)[0].strip()
        if not _NAME.fullmatch(name):
            raise EnvFileError(f"{path}:{line_number}: invalid variable name")
        names.add(name)
    return names


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="env-shape-check",
        description="Compare environment variable names without displaying values.",
    )
    parser.add_argument(
        "--example",
        type=Path,
        default=Path(".env.example"),
        help="template file (default: .env.example)",
    )
    parser.add_argument(
        "--env",
        type=Path,
        default=Path(".env"),
        help="local environment file (default: .env)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        expected = read_names(args.example)
        actual = read_names(args.env)
    except EnvFileError as exc:
        print(f"env-shape-check: {exc}", file=sys.stderr)
        return 2

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if not missing and not extra:
        print("Environment variable names match.")
        return 0

    if missing:
        print(f"Missing from {args.env}: {', '.join(missing)}")
    if extra:
        print(f"Extra in {args.env}: {', '.join(extra)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
