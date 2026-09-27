#!/usr/bin/env python3
"""Expose TWRP's vold fscrypt policy headers to the OrangeFox GUI target."""

from pathlib import Path
import sys


MODULE = 'cc_library_static {\n    name: "libguitwrp",'
DEFAULTS = '    defaults: ["libguitwrp_defaults", "twrp_defaults"],\n'
HEADER_LIB = '    header_libs: ["libvold_headers"],\n'


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <orangefox-source-root>")

    root = Path(sys.argv[1])
    header = root / "system/vold/fscrypt_policy.h"
    vold_bp = root / "system/vold/Android.bp"
    gui_bp = root / "bootable/recovery/gui/Android.bp"

    for path in (header, vold_bp, gui_bp):
        if not path.is_file():
            raise SystemExit(f"Required fscrypt compatibility input not found: {path}")

    vold_text = vold_bp.read_text(encoding="utf-8")
    if 'name: "libvold_headers"' not in vold_text or "recovery_available: true" not in vold_text:
        raise SystemExit("libvold_headers is not exported for recovery by system/vold")

    text = gui_bp.read_text(encoding="utf-8")
    if text.count(MODULE) != 1:
        raise SystemExit(
            f"Expected one libguitwrp cc_library_static block, found {text.count(MODULE)}"
        )

    start = text.index(MODULE)
    end = text.find("\n}", start)
    if end < 0:
        raise SystemExit("Could not locate the end of the libguitwrp module")
    block = text[start:end]

    if HEADER_LIB.strip() in block:
        print("libguitwrp already exports the vold fscrypt header dependency.")
        return

    if block.count(DEFAULTS) != 1:
        raise SystemExit("Expected one libguitwrp defaults property to anchor the patch")

    patched = text[:start] + block.replace(DEFAULTS, DEFAULTS + HEADER_LIB, 1) + text[end:]
    gui_bp.write_text(patched, encoding="utf-8", newline="\n")
    print("Added libvold_headers to the libguitwrp Soong header dependencies.")


if __name__ == "__main__":
    main()
