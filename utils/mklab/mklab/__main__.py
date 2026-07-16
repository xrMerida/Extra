"""
mklab - Scaffold new CMake projects from a template.

Usage:
    python -m mklab <project-name> [target-dir]
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
