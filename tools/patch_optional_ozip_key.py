#!/usr/bin/env python3
"""Give the optional OZIP action an empty key when a device has no OZIP key."""

from pathlib import Path
import sys


ANCHOR = "int GUIAction::ozip_decrypt(string zip_path)\n{"
DEFAULT = (
    "#ifndef TW_OZIP_DECRYPT_KEY\n"
    '#define TW_OZIP_DECRYPT_KEY ""\n'
    "#endif\n\n"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <gui/action.cpp>")

    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"OrangeFox GUI action source not found: {path}")

    text = path.read_text(encoding="utf-8")
    if DEFAULT in text:
        print("Optional OZIP key already has an empty default.")
        return

    if text.count(ANCHOR) != 1 or "TW_OZIP_DECRYPT_KEY" not in text:
        raise SystemExit("Could not identify the expected unguarded OZIP action")

    path.write_text(text.replace(ANCHOR, DEFAULT + ANCHOR, 1), encoding="utf-8", newline="\n")
    print("Added an empty fallback for the optional TW_OZIP_DECRYPT_KEY macro.")


if __name__ == "__main__":
    main()
