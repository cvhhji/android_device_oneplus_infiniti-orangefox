#!/usr/bin/env python3
"""Limit the 16 KiB prebuilt ELF exemption to magiskboot for this 4 KiB kernel."""

from pathlib import Path
import sys


MAGISKBOOT_MODULE = 'cc_prebuilt_binary {\n    name: "magiskboot",\n'
RECOVERY_PROPERTY = "    recovery: true,\n"
PAGE_SIZE_EXEMPTION = "    ignore_max_page_size: true,\n"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <orangefox-source-root>")

    root = Path(sys.argv[1])
    android_bp = root / "external/magisk-prebuilt/prebuilt/Android.bp"
    if not android_bp.is_file():
        raise SystemExit(f"MagiskBoot prebuilt module not found: {android_bp}")

    text = android_bp.read_text(encoding="utf-8")
    if text.count(MAGISKBOOT_MODULE) != 1:
        raise SystemExit("Could not identify exactly one MagiskBoot prebuilt module")

    start = text.index(MAGISKBOOT_MODULE)
    end = text.find("\n}", start)
    if end < 0:
        raise SystemExit("Could not locate the end of the MagiskBoot prebuilt module")
    block = text[start:end]

    if PAGE_SIZE_EXEMPTION in block:
        print("MagiskBoot already ignores the 16 KiB prebuilt alignment check.")
        return

    if block.count(RECOVERY_PROPERTY) != 1:
        raise SystemExit("Could not identify the recovery property in the MagiskBoot module")

    patched_block = block.replace(
        RECOVERY_PROPERTY, RECOVERY_PROPERTY + PAGE_SIZE_EXEMPTION, 1
    )
    patched = text[:start] + patched_block + text[end:]
    if patched.count(PAGE_SIZE_EXEMPTION) != 1:
        raise SystemExit("MagiskBoot page-size exemption was not applied exactly once")

    android_bp.write_text(patched, encoding="utf-8", newline="\n")
    print("Exempted only the 4 KiB MagiskBoot prebuilt from the 16 KiB ELF check.")


if __name__ == "__main__":
    main()
