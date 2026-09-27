#!/usr/bin/env python3
"""Align update_engine with the SnapshotManager API in OrangeFox fox_16.0."""

from pathlib import Path
import sys


OLD = (
    "bool DynamicPartitionControlAndroid::UpdateUsesSnapshotCompression() {\n"
    "  return GetVirtualAbFeatureFlag().IsEnabled() &&\n"
    "         GetSnapshotManager()->UpdateUsesSnapuserd();\n"
    "}"
)
NEW = (
    "bool DynamicPartitionControlAndroid::UpdateUsesSnapshotCompression() {\n"
    "  return GetVirtualAbFeatureFlag().IsEnabled() &&\n"
    "         GetSnapshotManager()->UpdateUsesCompression();\n"
    "}"
)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            f"Usage: {sys.argv[0]} <dynamic_partition_control_android.cc>"
        )

    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"update_engine source file not found: {path}")

    text = path.read_text(encoding="utf-8")
    old_count = text.count(OLD)
    new_count = text.count(NEW)
    if old_count == 0 and new_count == 1:
        print("update_engine SnapshotManager API is already aligned.")
        return
    if old_count != 1 or new_count != 0:
        raise SystemExit(
            "SnapshotManager Android 17 patch expected one unpatched "
            f"UpdateUsesSnapshotCompression definition, found old={old_count}, "
            f"new={new_count}"
        )

    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
    print("Aligned update_engine with SnapshotManager::UpdateUsesCompression.")


if __name__ == "__main__":
    main()
