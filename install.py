#!/usr/bin/env python3
"""
Install nautilus-trader-cython-stubs to a target directory.

Usage:
    python install.py <target_path>

Example:
    python install.py /path/to/python/site-packages/nautilus_trader
"""

import argparse
import shutil
import sys
from pathlib import Path


def install(target: Path) -> None:
    stubs_dir = Path(__file__).parent / "stubs"

    if not stubs_dir.exists():
        print(f"Error: stubs directory not found at {stubs_dir}", file=sys.stderr)
        sys.exit(1)

    if not target.exists():
        print(f"Error: target directory does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    copied = 0

    for src in stubs_dir.rglob("*"):
        if not src.is_file():
            continue

        rel = src.relative_to(stubs_dir)
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
        print(f"  copied: {rel}")

    print(f"\nDone. {copied} file(s) installed to {target}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install nautilus-trader-cython-stubs into a nautilus_trader package directory."
    )
    parser.add_argument(
        "target_path",
        help="Path to the nautilus_trader package directory "
             "(e.g. {python_path}/lib/{python_version}/site-packages/nautilus_trader)",
    )
    args = parser.parse_args()

    install(Path(args.target_path).expanduser().resolve())


if __name__ == "__main__":
    main()
