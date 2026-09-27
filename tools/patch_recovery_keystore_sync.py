#!/usr/bin/env python3
"""Use the Android 16 keystore database sync API before OrangeFox decryption."""

from pathlib import Path
import re
import sys


OLD_CALL = "android::keystore::copySqliteDb();"
NEW_CALL = "android::keystore::syncKeystoreDb();"
CALL_BLOCK = re.compile(
    r"(#ifdef\s+TW_INCLUDE_CRYPTO\s*\n\s*)"
    + re.escape(OLD_CALL)
)
NEW_CALL_BLOCK = re.compile(
    r"#ifdef\s+TW_INCLUDE_CRYPTO\s*\n\s*"
    + re.escape(NEW_CALL)
)
HEADER_DECLARATION = re.compile(r"\bbool\s+syncKeystoreDb\s*\(\s*\)\s*;")
IMPLEMENTATION = re.compile(r"\bbool\s+syncKeystoreDb\s*\(\s*\)\s*\{")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <orangefox-source-root>")

    root = Path(sys.argv[1])
    recovery = root / "bootable/recovery/twrp.cpp"
    header = root / "system/vold/Decrypt.h"
    implementation = root / "system/vold/Decrypt.cpp"

    for path in (recovery, header, implementation):
        if not path.is_file():
            raise SystemExit(f"Required keystore sync source not found: {path}")

    header_text = header.read_text(encoding="utf-8")
    implementation_text = implementation.read_text(encoding="utf-8")
    if not HEADER_DECLARATION.search(header_text):
        raise SystemExit("system/vold/Decrypt.h does not declare syncKeystoreDb()")
    if not IMPLEMENTATION.search(implementation_text):
        raise SystemExit("system/vold/Decrypt.cpp does not implement syncKeystoreDb()")

    text = recovery.read_text(encoding="utf-8")
    old_calls = text.count(OLD_CALL)
    new_calls = text.count(NEW_CALL)

    if old_calls == 0 and new_calls == 1 and NEW_CALL_BLOCK.search(text):
        print("OrangeFox already calls the Android 16 keystore sync API.")
        return

    if old_calls != 1 or new_calls != 0 or not CALL_BLOCK.search(text):
        raise SystemExit(
            "Could not identify exactly one legacy keystore copy call under TW_INCLUDE_CRYPTO"
        )

    patched = CALL_BLOCK.sub(lambda match: match.group(1) + NEW_CALL, text, count=1)
    if patched.count(NEW_CALL) != 1 or OLD_CALL in patched:
        raise SystemExit("Keystore sync call replacement did not produce the expected source")

    recovery.write_text(patched, encoding="utf-8", newline="\n")
    print("Aligned OrangeFox's pre-decrypt keystore sync call with system/vold.")


if __name__ == "__main__":
    main()
