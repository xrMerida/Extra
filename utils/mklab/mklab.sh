#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
TEMPLATE="$SCRIPT_DIR/Template"

usage() {
    echo "Usage: mklab.sh <destination> [name]"
    echo
    echo "  destination  Path to create the new project at"
    echo "  name         Project name — replaces 'App' in template files"
    exit 1
}

[[ $# -lt 1 ]] && usage

DEST="$1"
NAME="${2:-}"

if [[ -d "$DEST" ]]; then
    echo "Error: destination '$DEST' already exists" >&2
    exit 1
fi

cp -r "$TEMPLATE" "$DEST"

if [[ -n "$NAME" ]]; then
    LOWER="$(echo "$NAME" | tr '[:upper:]' '[:lower:]')"

    find "$DEST" -type f -exec sed -i "s/App/$NAME/g" {} +
    find "$DEST" -type f -exec sed -i "s/app/$LOWER/g" {} +

    # Rename include/App -> include/$LOWER
    if [[ -d "$DEST/include/App" ]]; then
        mv "$DEST/include/App" "$DEST/include/$LOWER"
    fi

    # Clean up placeholder
    rm -f "$DEST/include/$LOWER/.gitkeep"
fi

echo "Created project at $DEST"
