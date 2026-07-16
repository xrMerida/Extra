"""
cli.py - Interactive terminal UI for cleanwork.

Interaction model is inspired by `git rebase -i`:
  For each file you see a prompt where you type an action key.
  Actions are processed in order, and a final summary is shown.
"""

import os
import subprocess
from pathlib import Path

from .core import (
    Action,
    FileEntry,
    ScanResult,
    apply_actions,
    clean_directory,
    load_manifest,
    preview_file,
    scan_directories,
    undo_last,
)

# ── ANSI helpers (no external deps) ──────────────────────────────────────────

_BOLD = "\033[1m"
_DIM = "\033[2m"
_RESET = "\033[0m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_BLUE = "\033[34m"
_MAGENTA = "\033[35m"
_CYAN = "\033[36m"
_WHITE = "\033[97m"
_BG_GREEN = "\033[42m"
_BG_RED = "\033[41m"
_BG_YELLOW = "\033[43m"
_BG_BLUE = "\033[44m"


def _clear():
    """Clear terminal screen."""
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True, check=False)


def _color(text: str, code: str) -> str:
    return f"{code}{text}{_RESET}"


def _bold(text: str) -> str:
    return _color(text, _BOLD)


def _dim(text: str) -> str:
    return _color(text, _DIM)


def _header(text: str) -> str:
    return _color(f" {text} ", _BOLD + _BG_BLUE + _WHITE)


def _success(text: str) -> str:
    return _color(text, _GREEN)


def _warn(text: str) -> str:
    return _color(text, _YELLOW)


def _error(text: str) -> str:
    return _color(text, _RED)


# ── Display ──────────────────────────────────────────────────────────────────

ACTION_COLORS = {
    Action.PICK: _GREEN,
    Action.RENAME: _CYAN,
    Action.DELETE: _RED,
    Action.SKIP: _DIM,
    Action.VIEW: _MAGENTA,
}

ACTION_LABELS = {
    Action.PICK: "PICK",
    Action.RENAME: "RENAME",
    Action.DELETE: "DELETE",
    Action.SKIP: "SKIP",
    Action.VIEW: "VIEW",
}


def _banner():
    print()
    print(_header("cleanwork"))
    print(
        _dim("  Interactive file cleanup — sort ~/Desktop & ~/Downloads → ~/Documents")
    )
    print()


def _file_status_icon(entry: FileEntry) -> str:
    """Return a colored status tag for a resolved file."""
    if not entry.resolved:
        return _dim("  ○ pending")
    color = ACTION_COLORS.get(entry.action, "")
    label = ACTION_LABELS.get(entry.action, "?")
    extra = ""
    if entry.action == Action.RENAME and entry.new_name:
        extra = f" → {entry.new_name}"
    return f"  {_color(label, color + _BOLD)}{extra}"


def _show_file_list(result: ScanResult):
    """Print the numbered file list with status."""
    print(_bold("  #   Source       Size      File"))
    print(_dim("  " + "─" * 62))

    for i, entry in enumerate(result.files, 1):
        src_color = _YELLOW if entry.source_dir == "Desktop" else _CYAN
        src = _color(f"{entry.source_dir:<10}", src_color)
        size = _dim(f"{entry.display_size:>8}")
        name = entry.display_name
        status = _file_status_icon(entry)
        print(f"  {_bold(str(i)):>4}  {src}  {size}  {name}{status}")

    print(_dim("  " + "─" * 62))
    print()


def _show_actions_menu():
    """Print the action help."""
    print(_bold("  Actions:"))
    actions = [
        ("1-9", "jump — type a number to jump to that file", _WHITE),
        ("p", "pick — move to ~/Documents", _GREEN),
        ("r", "rename — move with a new name", _CYAN),
        ("d", "delete — remove permanently", _RED),
        ("v", "view — preview file contents", _MAGENTA),
        ("s", "skip — leave in place (default)", _DIM),
        ("u", "undo — revert last resolved file", _YELLOW),
        ("a", "accept all — pick all remaining", _GREEN),
        ("x", "skip all remaining", _DIM),
        ("q", "quit — finish and apply", _BOLD),
        ("l", "list — show files again", _WHITE),
    ]
    for key, desc, color in actions:
        print(f"    {_color(key, color + _BOLD)}  {_dim(desc)}")
    print()


def _show_summary(result: ScanResult, summary: dict):
    """Print the final operation summary."""
    print()
    print(_header("SUMMARY"))
    print()

    picked = result.picked
    if picked:
        print(_success(f"  → {len(picked)} file(s) moved to ~/Documents:"))
        for entry in picked:
            dest_name = (
                entry.new_name if entry.action == Action.RENAME else entry.display_name
            )
            print(_success(f"      • {entry.display_name} → {dest_name}"))
        print()

    deleted = result.deleted
    if deleted:
        print(_error(f"  ✗ {len(deleted)} file(s) deleted:"))
        for entry in deleted:
            print(_error(f"      • {entry.display_name}"))
        print()

    skipped = result.skipped
    if skipped:
        print(_warn(f"  ○ {len(skipped)} file(s) left in place:"))
        for entry in skipped:
            print(_warn(f"      • {entry.display_name} [{entry.source_dir}]"))
        print()

    errors = summary.get("errors", [])
    if errors:
        print(_error("  Errors:"))
        for err in errors:
            print(_error(f"      • {err}"))
        print()


# ── Input helpers ────────────────────────────────────────────────────────────


def _input(prompt: str) -> str:
    """Read user input, stripping whitespace."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def _confirm(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question."""
    hint = _dim("[Y/n]") if default else _dim("[y/N]")
    answer = _input(f"  {prompt} {hint} ").lower()
    if not answer:
        return default
    return answer in ("y", "yes")


# ── Main interactive loop ───────────────────────────────────────────────────


def run_interactive():
    """Main entry point for the interactive CLI."""
    _clear()
    _banner()

    # ── Scan ──
    print(_dim("  Scanning ~/Desktop and ~/Downloads..."))
    result = scan_directories()

    if result.total == 0:
        print(_warn("  No files found in ~/Desktop or ~/Downloads. Nothing to do."))
        print()
        return

    print(_success(f"  Found {result.total} file(s)."))
    print(_success(f"    Desktop: {len(result.desktop_files)}"))
    print(_success(f"    Downloads: {len(result.downloads_files)}"))
    print()

    # ── Interactive loop ──
    _show_file_list(result)
    _show_actions_menu()

    while True:
        pending = result.pending
        if not pending:
            print(_success("  All files have been resolved."))
            break

        # Show the first unresolved file
        current = pending[0]
        idx = result.files.index(current) + 1
        print(
            _bold(f"  [{idx}/{result.total}] {current.display_name}")
            + _dim(f"  ({current.source_dir}, {current.display_size})")
        )

        action = _input("  action ▸ ").lower()

        # ── Numeric jump ──
        if action.isdigit():
            target_idx = int(action) - 1
            if (
                0 <= target_idx < len(result.files)
                and not result.files[target_idx].resolved
            ):
                entry = result.files.pop(target_idx)
                first_pending = next(
                    (i for i, f in enumerate(result.files) if not f.resolved),
                    len(result.files),
                )
                result.files.insert(first_pending, entry)
                print(_dim(f"    Jumped to #{target_idx + 1}"))
                print()
                continue
            else:
                print(_error(f"    Invalid or already resolved: #{action}"))
                print()
                continue

        # ── Undo last resolution ──
        if action in ("u", "undo"):
            resolved = [f for f in result.files if f.resolved]
            if not resolved:
                print(_dim("    Nothing to undo."))
                print()
                continue
            last = resolved[-1]
            last.resolved = False
            last.action = Action.SKIP
            last.new_name = ""
            print(
                _warn(
                    f"    Reverted #{result.files.index(last) + 1} {last.display_name}"
                )
            )
            print()
            continue

        if action in ("q", "quit", ""):
            if not _confirm("Finish and apply all actions now?"):
                continue
            break

        elif action in ("p", "pick"):
            current.action = Action.PICK
            current.resolved = True
            print(_success("    ✓ Will move to ~/Documents"))
            print()

        elif action in ("r", "rename"):
            new_name = _input("  new name ▸ ")
            if not new_name:
                print(_dim("    (cancelled)"))
                continue
            current.action = Action.RENAME
            current.new_name = new_name
            current.resolved = True
            print(_success(f"    ✓ Will rename to '{new_name}' and move"))
            print()

        elif action in ("d", "delete"):
            if _confirm(f"Really delete '{current.display_name}'?", default=False):
                current.action = Action.DELETE
                current.resolved = True
                print(_error("    ✗ Will delete"))
                print()
            else:
                print(_dim("    (cancelled)"))
                print()

        elif action in ("v", "view"):
            print()
            print(
                _color("  ┌─── Preview ───────────────────────────────────────", _CYAN)
            )
            content = preview_file(current)
            for line in content.splitlines()[:100]:
                print(f"  │ {line}")
            if content.count("\n") > 100:
                print(_dim("  │ ... (truncated)"))
            print(
                _color("  └──────────────────────────────────────────────────", _CYAN)
            )
            print()
            # VIEW doesn't consume — show the file again
            continue

        elif action in ("a", "accept", "accept-all"):
            for entry in result.pending:
                entry.action = Action.PICK
                entry.resolved = True
            print(_success("    ✓ All remaining files marked for pick"))
            print()
            break

        elif action in ("x", "skip-all"):
            for entry in result.pending:
                entry.action = Action.SKIP
                entry.resolved = True
            print(_warn("    ○ All remaining files marked for skip"))
            print()
            break

        elif action in ("l", "list"):
            _show_file_list(result)
            continue

        else:
            print(_error(f"    Unknown action: '{action}'. Type 'l' for help."))
            print()
            continue

    # ── Summary before applying ──
    print()
    print(_bold("  ══════════════════════════════════════════════════════"))
    print(_bold("  Pending changes:"))
    print(_bold("  ══════════════════════════════════════════════════════"))
    _show_file_list(result)

    if not _confirm("Apply these changes now?", default=True):
        print(_warn("  Aborted. No files were modified."))
        return

    # ── Apply ──
    print()
    print(_dim("  Applying changes..."))
    summary = apply_actions(result)
    _show_summary(result, summary)

    # ── Prompt to clean source dirs ──
    print(_bold("  ══════════════════════════════════════════════════════"))
    print(_bold("  Clean up source directories?"))
    print(_bold("  ══════════════════════════════════════════════════════"))
    print()

    home = Path.home()
    for dirname in ("Desktop", "Downloads"):
        source = home / dirname
        if not source.exists():
            continue
        remaining = [
            f for f in source.iterdir() if f.is_file() and not f.name.startswith(".")
        ]
        if not remaining:
            print(_dim("  ~/Desktop is already clean."))
            continue

        print(_warn(f"  {len(remaining)} file(s) remain in ~/{dirname}:"))
        for f in remaining[:10]:
            print(_warn(f"      • {f.name}"))
        if len(remaining) > 10:
            print(_warn(f"      ... and {len(remaining) - 10} more"))
        print()

        if _confirm(f"Delete ALL remaining files in ~/{dirname}?", default=False):
            count = clean_directory(source)
            print(_success(f"    ✓ Deleted {count} file(s) from ~/{dirname}"))
        else:
            print(_dim(f"    (kept ~/{dirname} as-is)"))
        print()

    # ── Done ──
    print(_header(" DONE "))
    print(_success("  Files have been sorted into ~/Documents."))
    print()

    if _confirm("Undo these changes?", default=False):
        run_undo()


# ── Standalone undo ────────────────────────────────────────────────────────


def run_undo():
    """Reverse the last applied session using the saved manifest."""
    _banner()

    manifest = load_manifest()
    if manifest is None:
        print(_warn("  No previous session to undo."))
        print()
        return

    ts = manifest.get("timestamp", "unknown")
    entries = manifest.get("entries", [])
    print(_dim(f"  Last session: {ts} ({len(entries)} operation(s))"))
    print()

    # Show what will be undone
    print(_bold("  Files to restore:"))
    for e in entries:
        action_label = (
            _color("move", _GREEN) if e["action"] == "move" else _color("delete", _RED)
        )
        orig = Path(e["original_path"])
        dest = Path(e["destination_path"])
        status = _success("✓") if dest.exists() else _error("?")
        print(
            f"    {status} {orig.name}  {_dim(f'← {dest.parent.name}/')}{action_label}"
        )
    print()

    if not _confirm("Undo all changes?", default=True):
        print(_warn("  Aborted. Nothing was undone."))
        print()
        return

    print(_dim("  Reversing changes..."))
    summary = undo_last()

    undone = summary.get("undone", 0)
    errors = summary.get("errors", [])

    if undone:
        print(_success(f"  ✓ Restored {undone} file(s) to their original locations."))
    if errors:
        print()
        for err in errors:
            print(_error(f"  ⚠ {err}"))
    if not undone and not errors:
        print(_warn("  Nothing to undo."))
    print()
