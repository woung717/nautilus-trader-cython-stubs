#!/usr/bin/env python3
"""
Install nautilus-trader-cython-stubs to a target directory.

Usage:
    python install.py [target_path]

    If target_path is omitted, the script searches for nautilus_trader
    directories and prompts you to choose one interactively.

Example:
    python install.py
    python install.py /path/to/python/site-packages/nautilus_trader
"""

import argparse
import shutil
import sys
from pathlib import Path


_SKIP_PARTS = {".cache", ".git", ".hg", ".svn", "__pycache__"}


def _is_excluded(path: Path) -> bool:
    return any(part in _SKIP_PARTS for part in path.parts)


def find_nautilus_trader_dirs() -> list[Path]:
    """Search for directories named 'nautilus_trader' in likely install locations."""
    candidates: list[Path] = []
    seen: set[Path] = set()

    is_windows = sys.platform == "win32"
    home = Path.home()

    def add(p: Path) -> None:
        if not p.is_dir() or _is_excluded(p):
            return
        resolved = p.resolve()
        if resolved not in seen:
            seen.add(resolved)
            candidates.append(p)

    def glob_add(base: Path, pattern: str) -> None:
        try:
            for found in base.glob(pattern):
                add(found)
        except PermissionError:
            pass

    # 1. Direct hits in sys.path (site-packages, etc.) — one level deep only
    for raw in sys.path:
        if not raw:
            continue
        root = Path(raw)
        if root.name == "nautilus_trader":
            add(root)
        else:
            add(root / "nautilus_trader")

    if is_windows:
        # 2a. Windows: system-wide Python installs (C:\PythonXY\)
        for drive in [Path("C:/"), Path("D:/")]:
            for version_dir in drive.glob("Python*/"):
                add(version_dir / "Lib" / "site-packages" / "nautilus_trader")

        # 2b. Windows: per-user Python installs
        appdata_local = Path(
            sys.platform == "win32"
            and __import__("os").environ.get("LOCALAPPDATA", str(home / "AppData" / "Local"))
            or str(home / "AppData" / "Local")
        )
        appdata_roaming = Path(
            sys.platform == "win32"
            and __import__("os").environ.get("APPDATA", str(home / "AppData" / "Roaming"))
            or str(home / "AppData" / "Roaming")
        )
        glob_add(
            appdata_local / "Programs" / "Python",
            "Python*/Lib/site-packages/nautilus_trader",
        )
        glob_add(
            appdata_roaming / "Python",
            "Python*/site-packages/nautilus_trader",
        )

        # 2c. Windows: Conda/Mamba environments
        for conda_root in [
            home / "anaconda3",
            home / "miniconda3",
            home / "mambaforge",
            home / "miniforge3",
            appdata_local / "anaconda3",
            appdata_local / "miniconda3",
            Path("C:/ProgramData/anaconda3"),
            Path("C:/ProgramData/miniconda3"),
        ]:
            add(conda_root / "Lib" / "site-packages" / "nautilus_trader")
            glob_add(conda_root / "envs", "*/Lib/site-packages/nautilus_trader")

        # 2d. Windows: virtual envs up to three project-dir levels under home
        # Windows venvs: {venv}\Lib\site-packages (no python version subdir)
        for venv_name in [".venv", "venv", "env"]:
            for prefix in ["*", "*/*", "*/*/*"]:
                glob_add(
                    home,
                    f"{prefix}/{venv_name}/Lib/site-packages/nautilus_trader",
                )

    else:
        # 3a. Linux/macOS: system-wide site-packages and dist-packages
        for system_root in [
            Path("/usr/lib"),
            Path("/usr/local/lib"),
            Path("/opt/homebrew/lib"),       # macOS Homebrew (Apple Silicon)
            Path("/usr/local/opt/python/lib"),  # macOS Homebrew (Intel)
        ]:
            for version_dir in system_root.glob("python*"):
                add(version_dir / "site-packages" / "nautilus_trader")
                add(version_dir / "dist-packages" / "nautilus_trader")  # Debian/Ubuntu

        # 3b. User site: ~/.local/lib (Linux) and ~/Library/Python (macOS)
        for base in [home / ".local" / "lib", home / "Library" / "Python"]:
            for version_dir in base.glob("python*"):
                add(version_dir / "site-packages" / "nautilus_trader")

        # 3c. Conda/Mamba environments (Linux/macOS)
        for conda_root in [
            home / "anaconda3",
            home / "miniconda3",
            home / "mambaforge",
            home / "miniforge3",
            home / "opt" / "anaconda3",
            home / "opt" / "miniconda3",
            Path("/opt/anaconda3"),
            Path("/opt/miniconda3"),
        ]:
            glob_add(conda_root / "lib", "python*/site-packages/nautilus_trader")
            glob_add(conda_root / "envs", "*/lib/python*/site-packages/nautilus_trader")

        # 3d. Virtual envs up to three project-dir levels under home
        for venv_name in [".venv", "venv", "env"]:
            for prefix in ["*", "*/*", "*/*/*"]:
                glob_add(
                    home,
                    f"{prefix}/{venv_name}/lib/python*/site-packages/nautilus_trader",
                )

    return candidates


def select_target() -> Path:
    """Find nautilus_trader directories and let the user pick one."""
    print("Searching for nautilus_trader directories...")
    dirs = find_nautilus_trader_dirs()

    if not dirs:
        print(
            "Error: no nautilus_trader directory found.\n"
            "Please provide the path explicitly:\n"
            "  python install.py <target_path>",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"\nFound {len(dirs)} nautilus_trader directory(s):\n")
    for i, d in enumerate(dirs, 1):
        print(f"  [{i}] {d}")

    print()
    while True:
        raw = input(f"Select a directory [1-{len(dirs)}] (or 'q' to quit): ").strip()
        if raw.lower() == "q":
            print("Aborted.")
            sys.exit(0)
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(dirs):
                chosen = dirs[idx - 1]
                print(f"\nInstalling to: {chosen}\n")
                return chosen
        print(f"  Please enter a number between 1 and {len(dirs)}.")


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
        nargs="?",
        default=None,
        help="Path to the nautilus_trader package directory "
             "(e.g. {python_path}/lib/{python_version}/site-packages/nautilus_trader). "
             "If omitted, the script searches automatically and prompts you to choose.",
    )
    args = parser.parse_args()

    if args.target_path is None:
        target = select_target()
    else:
        target = Path(args.target_path).expanduser().resolve()

    install(target)


if __name__ == "__main__":
    main()
