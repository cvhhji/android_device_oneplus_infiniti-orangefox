#!/usr/bin/env python3
"""Patch an upstream MinUI warning that fails Android 17 warnings-as-errors builds."""

from pathlib import Path
import sys


OLD = "static void fbdev_blank(minui_backend* backend __unused, bool blank)"
NEW = "static void fbdev_blank(minui_backend* backend __unused, bool blank __unused)"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <graphics_fbdev.cpp>")

    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"MinUI source file not found: {path}")

    text = path.read_text(encoding="utf-8")
    old_count = text.count(OLD)
    new_count = text.count(NEW)
    if old_count == 0 and new_count == 1:
        print("MinUI framebuffer parameter is already marked unused.")
        return
    if old_count != 1:
        raise SystemExit(
            "MinUI Android 17 patch expected one fbdev_blank definition "
            f"without __unused, found {old_count}"
        )

    path.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="\n")
    print("Marked fbdev_blank's conditionally unused parameter __unused.")


if __name__ == "__main__":
    main()
