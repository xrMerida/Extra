"""
cli.py - Interactive prompts for building a lab-assignment PDF.
"""

import sys
from pathlib import Path

from .pdf import generate_pdf
from .utils import discover_files, get_clipboard_image


def pick_files(available: list[str], chosen_global: set[str]) -> list[str]:
    """Let the user pick files from the available list."""
    print("\nAvailable files:\n")
    added = [f for f in available if f in chosen_global]
    pending = [f for f in available if f not in chosen_global]
    ordered = added + pending
    for i, f in enumerate(ordered, 1):
        marker = "+" if f in chosen_global else "-"
        print(f"  {marker} {i:2d}. {f}")

    print("\nEnter numbers separated by commas (e.g. 1,3,4)")
    print("Or type 'all' to select everything\n")

    choice = input(" > ").strip()

    if choice.lower() == "all":
        return available

    selected = []
    for part in choice.split(","):
        part = part.strip()
        if not part.isdigit():
            continue
        idx = int(part) - 1
        if 0 <= idx < len(ordered):
            selected.append(ordered[idx])

    if not selected:
        print("No files selected.")
        return []

    print("\nSelected:")
    for f in selected:
        print(f"  + {f}")

    return selected


def collect_activities(project_root: Path) -> list[dict]:
    """Interactively collect activities and their files."""
    activities = []
    chosen_global: set[str] = set()

    while True:
        print("\n" + "=" * 40)
        name = input("Activity name: ").strip()
        if not name:
            break

        available = discover_files(project_root)
        chosen = pick_files(available, chosen_global)
        if chosen:
            chosen_global.update(chosen)
            activities.append({"name": name, "files": chosen})

        more = input("\nAdd another activity? (y/n): ").strip().lower()
        if more != "y":
            break

    return activities


def main():
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1]).resolve()
    else:
        project_root = Path.cwd()

    if not project_root.is_dir():
        print(f"[!] Directory not found: {project_root}")
        sys.exit(1)

    print("=" * 40)
    print("  PDF Generator - Source Code")
    print(f"  Directory: {project_root}")
    print("=" * 40)

    title = input("\nDocument title: ").strip()
    subtitle = input("Subtitle (Enter to skip): ").strip()

    activities = collect_activities(project_root)
    if not activities:
        print("\nNo activities added. Exiting.")
        return

    print("\nOutput image:")
    print("  - Enter a file path")
    print("  - Type 'clip' to paste from clipboard")
    print("  - Enter to skip")
    img_input = input("\n > ").strip()

    img_path = None
    if img_input.lower() == "clip":
        img_path = get_clipboard_image()
    elif img_input:
        img_path = Path(img_input)
        if not img_path.is_absolute():
            img_path = project_root / img_path
        if not img_path.exists():
            print(f"  [!] Image not found: {img_path}")
            img_path = None

    output_name = input("\nOutput filename (without .pdf): ").strip()
    if not output_name:
        output_name = "output"

    out = project_root / f"{output_name}.pdf"
    generate_pdf(project_root, title, activities, out, subtitle, img_path)
    print(f"\nGenerated: {out}")
