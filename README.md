# OnePlus 15 (infiniti) OrangeFox device tree

This tree's build metadata and vendor target are aligned with the connected device's current Android 17 system build. The device reports system API 37, vendor API 36, and first API level 36. The vendor interface is still API 36, so the recovery product targets VNDK 36.

The available OrangeFox sync script currently builds from its `fox_16.0` source branch, which it labels super experimental. This is an Android 17 device-tree adaptation using that recovery base; it is not an Android 17 OrangeFox common-source branch.

## GitHub Actions build

Pushing to `fox_16.0` starts the cloud build. The workflow syncs OrangeFox sources, overlays this device tree, applies the splash and timezone defaults, patches MinUI's conditionally unused framebuffer argument, aligns update_engine with the SnapshotManager API in the synced source tree, declares the vold fscrypt header dependency for the OrangeFox GUI, and uploads the AVB-transplanted `recovery.img` as an Actions artifact. No local build is needed.

The splash defaults are Google Dark (`#202124`), the dark OrangeFox logo, and the “OrangeFox Recovery” text unchecked. The UTC+8 option uses standard time without a daylight-saving rule, and the “Use DST” setting starts unchecked, so Beijing time is not shifted one hour ahead.

## AVB note

The workflow reuses the 2,240-byte vbmeta block extracted from the supplied `recovery_fox.img`, then applies it to each new image with `tools/transplant_avb.sh`. This automates the fake-relock procedure you confirmed on the device. If the official recovery's AVB data changes after an OTA, replace `avb/recovery-vbmeta.bin` with the block from the new working image.

This reuses the existing signed block; it does not create a new OnePlus signature or recalculate its recovery descriptor. AOSP AVB descriptors bind vbmeta metadata to image data, so the resulting artifact should be understood as the tested fake-relock output, not as a newly OEM-signed image. See the [AVB hash descriptor definition](https://android.googlesource.com/platform/external/avb/+/refs/heads/main/libavb/avb_hash_descriptor.h).

Successful compilation does not confirm boot, decryption, or touch behavior on the Android 17 device. Those require a recovery boot and on-device checks.
