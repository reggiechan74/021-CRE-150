"""Install Python dependencies for the plugin on first run."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))


REQUIRED_IMPORTS = ("pydantic", "yaml", "openpyxl", "reportlab")


def is_bootstrapped(plugin_root: Path) -> bool:
    return (plugin_root / ".bootstrapped").exists()


def missing_modules() -> list[str]:
    missing: list[str] = []
    for module_name in REQUIRED_IMPORTS:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(module_name)
    return missing


def bootstrap(plugin_root: Path) -> None:
    marker = plugin_root / ".bootstrapped"
    missing = missing_modules()
    if not missing and marker.exists():
        return

    requirements = plugin_root / "requirements.txt"
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "-r", str(requirements)],
        check=True,
    )
    marker.write_text("ok\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap cam-reconciliation-cre dependencies.")
    parser.add_argument(
        "--plugin-root",
        default=Path(__file__).resolve().parent.parent,
        type=Path,
        help="Plugin root containing requirements.txt.",
    )
    args = parser.parse_args()
    bootstrap(args.plugin_root.resolve())


if __name__ == "__main__":
    main()
