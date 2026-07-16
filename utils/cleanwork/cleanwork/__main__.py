"""
cleanwork - Interactive file cleanup CLI.

Usage:
    python -m cleanwork           # interactive mode
    python -m cleanwork --undo    # reverse last session
    cleanwork                     # if installed via pip
    cleanwork --undo
"""

import sys

from .cli import run_interactive, run_undo


def main():
    try:
        if "--undo" in sys.argv:
            run_undo()
        else:
            run_interactive()
    except KeyboardInterrupt:
        print("\n  Interrupted. No changes were made.\n")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
