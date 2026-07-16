"""
cli.py - Scaffold a new CMake project from the bundled template.
"""

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent / "template"


def _validate_name(name: str) -> str:
    """Ensure the project name is safe for use in CMake and as a directory."""
    if not name:
        raise argparse.ArgumentTypeError("Project name cannot be empty.")
    if not name[0].isalpha() and name[0] != "_":
        raise argparse.ArgumentTypeError(
            f"Project name must start with a letter or underscore: '{name}'"
        )
    forbidden = set(name) & set(" .!@#$%^&*()[]{}|\\;:'\",<>?/~`")
    if forbidden:
        raise argparse.ArgumentTypeError(
            f"Project name contains invalid characters: {forbidden}"
        )
    return name


def create_project(project_name: str, target_dir: Path) -> None:
    """Copy the template into *target_dir* and customise it for *project_name*."""
    if target_dir.exists():
        print(f"Error: '{target_dir}' already exists.")
        sys.exit(1)

    print(f"Creating project '{project_name}' in '{target_dir}' ...")

    # Copy template
    shutil.copytree(str(TEMPLATE_DIR), str(target_dir))

    # Make everything writable (template may be read-only)
    for path in target_dir.rglob("*"):
        path.chmod(0o755)

    # ── Patch CMakeLists.txt ──
    cmake = target_dir / "CMakeLists.txt"
    if cmake.exists():
        text = cmake.read_text()
        text = text.replace("project(App)", f"project({project_name})")
        text = text.replace("add_executable(app ", f"add_executable({project_name} ")
        text = text.replace(
            "target_include_directories(app ",
            f"target_include_directories({project_name} ",
        )
        cmake.write_text(text)

    # ── Patch .zed/debug.json ──
    debug_json = target_dir / ".zed" / "debug.json"
    if debug_json.exists():
        text = debug_json.read_text()
        text = text.replace("/build/app", f"/build/{project_name}")
        debug_json.write_text(text)

    print(f"Done! Project created at '{target_dir}'")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="mklab",
        description="Scaffold a new CMake project from a template.",
    )
    parser.add_argument(
        "project_name",
        type=_validate_name,
        help="Name of the project (used in CMakeLists.txt)",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Directory to create the project in (default: ./<project-name>)",
    )

    args = parser.parse_args(argv)
    target = args.target_dir or Path(args.project_name)
    create_project(args.project_name, target)
