#
# Copyright (C) 2025 The Android Open Source Project
# Copyright (C) 2025 SebaUbuntu's TWRP device tree generator
#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2024 The OrangeFox Recovery Project
# SPDX-License-Identifier: GPL-3.0-or-later
#

LOCAL_PATH := device/oneplus/infiniti

# Shipping API level
BOARD_SHIPPING_API_LEVEL := 36
PRODUCT_SHIPPING_API_LEVEL := 36
PRODUCT_TARGET_VNDK_VERSION := 36

# Dynamic partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

PRODUCT_PACKAGES += \
    lpflash \
    lpmake \
    lpunpack \
    fox_thermal_guard \
    wpa_cli \
    wpa_supplicant

# Package the Wi-Fi control client and vendor supplicant in the recovery ramdisk.
TW_RECOVERY_ADDITIONAL_RELINK_BINARY_FILES += \
    $(TARGET_OUT_VENDOR_EXECUTABLES)/wpa_cli
TW_RECOVERY_ADDITIONAL_RELINK_VENDOR_HW_BINARY_FILES += \
    $(TARGET_OUT_VENDOR_EXECUTABLES)/hw/wpa_supplicant

# OTA certs
PRODUCT_EXTRA_RECOVERY_KEYS += \
	$(LOCAL_PATH)/security/local_OTA \
	$(LOCAL_PATH)/security/special_OTA

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += $(LOCAL_PATH)

# some OrangeFox-specific settings
$(call inherit-product, $(LOCAL_PATH)/fox_infiniti.mk)
#
