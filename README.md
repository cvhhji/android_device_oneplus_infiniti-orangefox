# OnePlus 15 (infiniti) OrangeFox device tree

This tree's build metadata and vendor target are aligned with the connected device's current Android 17 system build. The device reports system API 37, vendor API 36, and first API level 36. The vendor interface is still API 36, so the recovery product targets VNDK 36.

The available OrangeFox sync script currently builds from its `fox_16.0` source branch, which it labels super experimental. This is an Android 17 device-tree adaptation using that recovery base; it is not an Android 17 OrangeFox common-source branch.

## GitHub Actions build

Pushing to `fox_16.0` starts the cloud build. The workflow syncs OrangeFox sources, overlays this device tree, applies the splash defaults, and uploads `recovery.img` as an Actions artifact. No local build is needed.

The splash defaults are Google Dark (`#202124`), the dark OrangeFox logo, and the “OrangeFox Recovery” text unchecked.

## AVB note

The supplied shell script copies a vbmeta block and checks only the `AVB0`/`AVBf` magic. It does not verify the descriptor digest against the recovery image. In the supplied `recovery_fox.img`, the signed recovery descriptor digest does not match the image payload, so carrying that block into new builds cannot establish that a locked bootloader will accept them. The Actions artifact is the built recovery image; it is not re-signed with OnePlus's private key.

Successful compilation does not confirm boot, decryption, or touch behavior on the Android 17 device. Those require a recovery boot and on-device checks.
