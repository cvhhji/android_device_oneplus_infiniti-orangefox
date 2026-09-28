#!/usr/bin/env python3
"""Mount device vendor partitions from OrangeFox's WLAN start menu."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def patch_wlan_page(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    vendor_mount = '<action function="mount">/vendor</action>'
    vendor_dlkm_mount = '<action function="mount">/vendor_dlkm</action>'

    if vendor_mount in source or vendor_dlkm_mount in source:
        if vendor_mount in source and vendor_dlkm_mount in source:
            return False
        raise RuntimeError("WLAN start page has only one of the two mount actions")

    pattern = re.compile(
        r'(?P<start><listitem name="\{@wlan_start\}">.*?'
        r'<action function="overlay">console</action>)\s*'
        r'(?P<terminal><action function="terminalcommand">wlan_start</action>)',
        re.DOTALL,
    )
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one WLAN start action block, found {len(matches)}"
        )

    match = matches[0]
    indentation = re.search(
        r"\n([ \t]*)<action function=\"terminalcommand\">wlan_start",
        match.group(0),
    )
    indent = indentation.group(1) if indentation else "\t\t\t\t\t"
    replacement = (
        match.group("start")
        + "\n"
        + indent
        + vendor_mount
        + "\n"
        + indent
        + vendor_dlkm_mount
        + "\n"
        + indent
        + match.group("terminal")
    )
    path.write_text(source[: match.start()] + replacement + source[match.end() :], encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/gui/theme/portrait_hdpi/pages/wlan.xml", file=sys.stderr)
        return 2

    target = Path(sys.argv[1])
    if patch_wlan_page(target):
        print(f"Added on-demand vendor mounts to {target}")
    else:
        print(f"On-demand vendor mounts already present in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
