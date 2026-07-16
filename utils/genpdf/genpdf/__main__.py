"""
genpdf - Interactive PDF generator for lab assignments.

Usage:
    python -m genpdf [project_dir]
"""

from .cli import main


def run():
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        raise SystemExit(1)


if __name__ == "__main__":
    run()
