#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
TEMPLATE="$SCRIPT_DIR/Template"

if [[ $# == 0 ]]; then
  echo "Usage: mklab.sh <destination> [name]"
  echo
  echo "  destination  Path to create the new project"
  echo "  name         Project name, uses destination if not provided"
  exit 1
fi

DEST="$1"
NAME="${2:-$DEST}"
LNAME="$(echo "$NAME" | tr '[:upper:]' '[:lower:]')"

if [[ -d "$DEST" ]]; then
  echo "Error: destination '$DEST' already exists" >&2
  exit 1
fi

# Project creation --------
cp -r "$TEMPLATE" "$DEST"

find "$DEST" -type f -exec sed -i "s/__NAME/$NAME/g" {} +
find "$DEST" -type f -exec sed -i "s/__LNAME/$LNAME/g" {} +

mkdir -p "$DEST/include/$LNAME"

echo "Created project at './$DEST' with name '$NAME'"
