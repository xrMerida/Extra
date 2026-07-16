"""
core.py - File scanning, preview, and manipulation operations.
"""

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path

MANIFEST_PATH = Path.home() / ".cleanwork_last_session.json"
TRASH_DIR = Path.home() / "Documents" / ".cleanwork_trash"


class Action(Enum):
    """Available actions for each file."""

    PICK = auto()  # Move to ~/Documents as-is
    RENAME = auto()  # Move to ~/Documents with a new name
    DELETE = auto()  # Delete the file
    SKIP = auto()  # Leave it where it is
    VIEW = auto()  # View contents (doesn't consume the action)


@dataclass
class FileEntry:
    """Represents a file found in Desktop or Downloads."""

    path: Path
    source_dir: str  # "Desktop" or "Downloads"
    action: Action = Action.SKIP
    new_name: str = ""  # Set when action is RENAME
    resolved: bool = False  # True once the user has decided on an action

    @property
    def display_size(self) -> str:
        """Human-readable file size."""
        try:
            size = self.path.stat().st_size
        except OSError:
            return "?"
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024:
                return f"{size:.1f}{unit}" if unit != "B" else f"{size}B"
            size /= 1024
        return f"{size:.1f}PB"

    @property
    def display_name(self) -> str:
        """Filename for display."""
        return self.path.name

    @property
    def dest_path(self) -> Path:
        """Determine destination in ~/Documents."""
        docs = Path.home() / "Documents"
        if self.action == Action.RENAME and self.new_name:
            return docs / self.new_name
        return docs / self.path.name


@dataclass
class ScanResult:
    """Result of scanning Desktop and Downloads."""

    files: list[FileEntry] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.files)

    @property
    def pending(self) -> list[FileEntry]:
        return [f for f in self.files if not f.resolved]

    @property
    def picked(self) -> list[FileEntry]:
        return [f for f in self.files if f.action in (Action.PICK, Action.RENAME)]

    @property
    def deleted(self) -> list[FileEntry]:
        return [f for f in self.files if f.action == Action.DELETE]

    @property
    def skipped(self) -> list[FileEntry]:
        return [f for f in self.files if f.action == Action.SKIP]

    @property
    def desktop_files(self) -> list[FileEntry]:
        return [f for f in self.files if f.source_dir == "Desktop"]

    @property
    def downloads_files(self) -> list[FileEntry]:
        return [f for f in self.files if f.source_dir == "Downloads"]


def scan_directories() -> ScanResult:
    """Scan ~/Desktop and ~/Downloads for files."""
    result = ScanResult()
    sources = [
        (Path.home() / "Desktop", "Desktop"),
        (Path.home() / "Downloads", "Downloads"),
    ]

    for source_dir, label in sources:
        if not source_dir.exists():
            continue
        try:
            for entry in sorted(source_dir.iterdir()):
                if entry.is_file() and not entry.name.startswith("."):
                    result.files.append(FileEntry(path=entry, source_dir=label))
        except PermissionError:
            continue

    return result


def preview_file(entry: FileEntry, max_lines: int = 80) -> str:
    """
    Return a text preview of a file's contents.
    For binary files, returns a hex dump header instead.
    """
    try:
        raw = entry.path.read_bytes()
    except OSError as e:
        return f"[error reading file: {e}]"

    # Check if binary
    if b"\x00" in raw[:512]:
        return _hex_preview(raw, max_lines)

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = raw.decode("latin-1")
        except Exception:
            return _hex_preview(raw, max_lines)

    lines = text.splitlines(keepends=True)[:max_lines]
    preview = "".join(lines)
    if len(text.splitlines()) > max_lines:
        preview += f"\n... ({len(text.splitlines()) - max_lines} more lines)"
    return preview


def _hex_preview(data: bytes, max_lines: int) -> str:
    """Create a hex dump preview for binary files."""
    lines = []
    for offset in range(0, min(len(data), max_lines * 16), 16):
        chunk = data[offset : offset + 16]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{offset:08x}  {hex_part:<48s}  {ascii_part}")
    return "\n".join(lines)


def apply_actions(result: ScanResult, docs: Path | None = None) -> dict:
    """
    Execute all queued actions and return a summary.

    Writes a manifest to ~/.cleanwork_last_session.json so changes can be
    undone with ``undo_last()``.

    Returns a dict with counts: moved, renamed, deleted, skipped, errors.
    """
    if docs is None:
        docs = Path.home() / "Documents"
    docs.mkdir(parents=True, exist_ok=True)
    TRASH_DIR.mkdir(parents=True, exist_ok=True)

    summary = {"moved": 0, "renamed": 0, "deleted": 0, "skipped": 0, "errors": []}
    manifest_entries: list[dict] = []

    for entry in result.files:
        if entry.action == Action.VIEW:
            summary["skipped"] += 1
            continue

        if entry.action == Action.SKIP:
            summary["skipped"] += 1
            continue

        if entry.action == Action.DELETE:
            trash_dest = TRASH_DIR / entry.path.name
            # Avoid collision in trash
            if trash_dest.exists():
                stem, suffix = trash_dest.stem, trash_dest.suffix
                counter = 1
                while trash_dest.exists():
                    trash_dest = TRASH_DIR / f"{stem}_{counter}{suffix}"
                    counter += 1
            try:
                shutil.move(str(entry.path), str(trash_dest))
                manifest_entries.append(
                    {
                        "original_path": str(entry.path),
                        "destination_path": str(trash_dest),
                        "action": "delete",
                        "source_dir": entry.source_dir,
                    }
                )
                summary["deleted"] += 1
            except OSError as e:
                summary["errors"].append(f"Delete {entry.path.name}: {e}")
            continue

        if entry.action in (Action.PICK, Action.RENAME):
            dest = entry.dest_path
            # Handle name collisions by appending a number
            if dest.exists():
                stem, suffix = dest.stem, dest.suffix
                counter = 1
                while dest.exists():
                    dest = docs / f"{stem}_{counter}{suffix}"
                    counter += 1
            try:
                shutil.move(str(entry.path), str(dest))
                manifest_entries.append(
                    {
                        "original_path": str(entry.path),
                        "destination_path": str(dest),
                        "action": "move",
                        "source_dir": entry.source_dir,
                    }
                )
                if entry.action == Action.RENAME:
                    summary["renamed"] += 1
                else:
                    summary["moved"] += 1
            except OSError as e:
                summary["errors"].append(f"Move {entry.path.name}: {e}")
            continue

        summary["skipped"] += 1

    # Persist manifest for undo
    if manifest_entries:
        _save_manifest(manifest_entries)

    return summary


def prompt_clean_source(source_dir: Path) -> bool:
    """Ask the user whether to delete all remaining files in a source directory.
    Returns True if confirmed."""
    if not source_dir.exists():
        return False

    remaining = [
        f for f in source_dir.iterdir() if f.is_file() and not f.name.startswith(".")
    ]
    if not remaining:
        return False

    # We return the count; the caller handles the prompt
    return True  # Signal that there are files to clean


def clean_directory(source_dir: Path) -> int:
    """Delete all files in a directory. Returns number deleted."""
    count = 0
    if not source_dir.exists():
        return 0
    for entry in source_dir.iterdir():
        if entry.is_file() and not entry.name.startswith("."):
            try:
                entry.unlink()
                count += 1
            except OSError:
                continue
    return count


# ── Manifest / Undo ────────────────────────────────────────────────────────


def _save_manifest(entries: list[dict]) -> None:
    """Persist a session manifest to disk."""
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }
    MANIFEST_PATH.write_text(json.dumps(data, indent=2))


def load_manifest() -> dict | None:
    """Load and return the last session manifest, or None."""
    if not MANIFEST_PATH.exists():
        return None
    try:
        return json.loads(MANIFEST_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def undo_last() -> dict:
    """
    Reverse the operations recorded in the last session manifest.

    Returns a summary dict with: undone, errors.
    """
    manifest = load_manifest()
    if manifest is None:
        return {"undone": 0, "errors": ["No previous session found."]}

    summary = {"undone": 0, "errors": []}

    # Process in reverse order so later moves don't shadow earlier ones
    for entry in reversed(manifest.get("entries", [])):
        orig = Path(entry["original_path"])
        dest = Path(entry["destination_path"])

        if not dest.exists():
            summary["errors"].append(
                f"{dest.name}: file not found at destination, nothing to undo"
            )
            continue

        # Ensure the original directory still exists
        orig.parent.mkdir(parents=True, exist_ok=True)

        # Handle name collision at the original location
        target = orig
        if target.exists():
            stem, suffix = target.stem, target.suffix
            counter = 1
            while target.exists():
                target = orig.parent / f"{stem}_{counter}{suffix}"
                counter += 1

        try:
            shutil.move(str(dest), str(target))
            summary["undone"] += 1
        except OSError as e:
            summary["errors"].append(f"{dest.name}: {e}")

    # Clean up trash dir if empty, remove manifest
    try:
        if TRASH_DIR.exists() and not any(TRASH_DIR.iterdir()):
            TRASH_DIR.rmdir()
    except OSError:
        pass

    try:
        MANIFEST_PATH.unlink(missing_ok=True)
    except OSError:
        pass

    return summary
