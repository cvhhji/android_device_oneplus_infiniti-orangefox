#
# Copyright (C) 2025 The Android Open Source Project
# Copyright (C) 2025 SebaUbuntu's TWRP device tree generator
#
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2024 The OrangeFox Recovery Project
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Configure base.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)

# Configure core_64_bit_only.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)

# Configure virtual_ab compression.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota/compression.mk)

# Configure emulated_storage.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/emulated_storage.mk)

# Configure twrp common.mk
$(call inherit-product, vendor/twrp/config/common.mk)

# Configure full_base_telephony.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)


# Inherit from dodge device
$(call inherit-product, device/oneplus/infiniti/device.mk)

PRODUCT_DEVICE := infiniti
PRODUCT_NAME := twrp_infiniti
PRODUCT_BRAND := oneplus
PRODUCT_MODEL := OnePlus 15
PRODUCT_MANUFACTURER := oneplus

PRODUCT_GMS_CLIENTID_BASE := android-oplus

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRIVATE_BUILD_DESC="qssi-user 17 CP2A.260605.016 1789230075256 release-keys"

BUILD_FINGERPRINT := OnePlus/PLK110/OP60FFL1:17/CP2A.260605.016/B.3e2f3d0-1859d0c-1859d08:user/release-keys

# Theme
TW_STATUS_ICONS_ALIGN := center
