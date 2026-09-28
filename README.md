# OnePlus 15 (infiniti) OrangeFox device tree

This tree's build metadata and vendor target are aligned with the connected device's current Android 17 system build. The device reports system API 37, vendor API 36, and first API level 36. The vendor interface is still API 36, so the recovery product targets VNDK 36.

The available OrangeFox sync script currently builds from its `fox_16.0` source branch, which it labels super experimental. This is an Android 17 device-tree adaptation using that recovery base; it is not an Android 17 OrangeFox common-source branch.

## GitHub Actions build

Pushing to `fox_16.0` starts the cloud build. The workflow syncs OrangeFox sources, overlays this device tree, sets Simplified Chinese, Beijing time (UTC+8 without daylight saving), and the 24-hour clock as defaults, applies the splash defaults, patches MinUI's conditionally unused framebuffer argument, aligns update_engine with the SnapshotManager API in the synced source tree, declares the vold fscrypt header dependency for the OrangeFox GUI, defaults the unused OZIP key to an empty value, aligns the pre-decrypt keystore database sync call with the synced `system/vold` API, limits the 16 KiB prebuilt ELF-check exemption to MagiskBoot, and uploads the AVB-transplanted `recovery.img` as an Actions artifact. No local build is needed.

The OnePlus SM8850 Canoe kernel build configuration uses 4 KiB pages. The workflow therefore exempts only the existing 4 KiB MagiskBoot prebuilt from the 16 KiB ELF check; it keeps the check enabled for the other prebuilts. If the recovery switches to a 16 KiB kernel, replace MagiskBoot with a 16 KiB-aligned binary instead of retaining this exemption. See the [OnePlus kernel build configuration](https://github.com/OnePlusOSS/android_kernel_oneplus_sm8850/blob/oneplus/sm8850_b_16.0.0_oneplus_15/build.config.msm.canoe).

The splash defaults are Google Dark (`#202124`), the dark OrangeFox logo, and the “OrangeFox Recovery” text unchecked. The default zone is `TAIST-8;` (UTC+8 without a daylight-saving rule), the “Use DST” setting starts unchecked, and the clock uses 24-hour time, so Beijing time is not shifted one hour ahead.

## Wi-Fi

The existing “Start WLAN” menu entry now mounts `/vendor` and `/vendor_dlkm` through OrangeFox, then calls a device-tree script to load the Qualcomm WLAN modules, signal CNSS `fs_ready`, wait for `wlan0`, and start `wpa_supplicant`. Wi-Fi modules remain out of `TW_LOAD_VENDOR_MODULES`, and the existing `post.decrypt.modules=true` init trigger is retained so recovery startup does not load WLAN drivers early.

## AVB note

The workflow reuses the 2,240-byte vbmeta block extracted from the supplied official `recovery.img`, then applies it to each new image with `tools/transplant_avb.sh`. The block is byte-identical to the one in the supplied older `recovery_fox.img`. If the official recovery's AVB data changes after an OTA, replace `avb/recovery-vbmeta.bin` with the block from the new official image.

This reuses the existing signed block; it does not create a new OnePlus signature or recalculate its recovery descriptor. AOSP AVB descriptors bind vbmeta metadata to image data, so the resulting artifact should be understood as the tested fake-relock output, not as a newly OEM-signed image. See the [AVB hash descriptor definition](https://android.googlesource.com/platform/external/avb/+/refs/heads/main/libavb/avb_hash_descriptor.h).

Successful compilation does not confirm boot, decryption, touch, or Wi-Fi operation on the Android 17 device. Those require a recovery boot and on-device checks.
