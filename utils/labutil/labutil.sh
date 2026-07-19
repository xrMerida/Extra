#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

usage_() {
  echo "Usage: labutil.sh <operation> <name>"
  echo
  echo "Operations:"
  echo "  class   Creates a new .h and .cpp files in the current directory"
}

replace_names_() {
  local FILE="$1"
  sed --in-place "s/__NAME/$NAME/g" "$FILE"
  sed --in-place "s/__LNAME/$LNAME/g" "$FILE"
}

cmd_class_() {
  # .h file location
  local DOTH="./include/$LPROJ/$LNAME.h"
  # .cpp file location
  local DOTCPP="./src/$LNAME.cpp"

  # Create directories if they don't exitst
  mkdir -p "$(dirname "$DOTCPP")"
  mkdir -p "$(dirname "$DOTH")"

  # Create the empty files
  cp "$SCRIPT_DIR/cmd_class/__LNAME.h" "$DOTH"
  cp "$SCRIPT_DIR/cmd_class/__LNAME.cpp" "$DOTCPP"

  # Replace placeholders with actual values
  replace_names_ "$DOTCPP"
  replace_names_ "$DOTH"

  echo "Files $DOTCPP & $DOTH created succesfully"
}

# MAIN -------------
CMAKETXT="./CMakeLists.txt"
NAME="${2:-}"
if [[ -z "$NAME" ]]; then
  usage_ >&2
  exit 1
fi
LNAME="$(echo "$NAME" | tr '[:upper:]' '[:lower:]')"
if [[ ! -f $CMAKETXT ]]; then
  echo "Could not find $CMAKETXT"
  exit 1
fi
PROJ="$(grep -oPi '(?i)\bproject\(\K[^)]+' "$CMAKETXT")"
LPROJ="$(echo "$PROJ" | tr '[:upper:]' '[:lower:]')"

if [[ $# -lt 2 ]]; then
  usage_ >&2
  exit 1
fi

case "$1" in
	class)
	cmd_class_ "$@"
		;;
	*)
 usage_ >&2
 exit 1
		;;
esac
