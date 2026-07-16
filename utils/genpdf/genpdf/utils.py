"""
utils.py - File discovery and clipboard helpers.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

IGNORE_DIRS = {".cache", ".git", ".zed", "build"}


def discover_files(project_root: Path) -> list[str]:
    """Find all source files in the project."""
    files = []
    for p in sorted(project_root.rglob("*")):
        if not p.is_file():
            continue
        if any(d in p.parts for d in IGNORE_DIRS):
            continue
        rel = p.relative_to(project_root)
        if rel.suffix in {".cpp", ".h", ".hpp", ".c"}:
            files.append(str(rel))
    return files


def get_clipboard_image() -> Path | None:
    """Grab an image from the clipboard (wl-paste or xclip)."""
    tmp = Path(tempfile.gettempdir()) / "clipboard_image.png"
    if shutil.which("wl-paste"):
        result = subprocess.run(
            ["wl-paste", "--type", "image/png"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    elif shutil.which("xclip"):
        result = subprocess.run(
            ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        print("  [!] Install wl-clipboard (wl-paste) or xclip")
        return None
    if result.returncode == 0 and result.stdout:
        tmp.write_bytes(result.stdout)
        print("  [i] Image captured from clipboard")
        return tmp
    print("  [!] No image found on clipboard")
    return None
