#
# Copyright (C) 2026 Paranoid Android
#
# SPDX-License-Identifier: Apache-2.0
#

LOCAL_PATH := $(call my-dir)

ifneq ($(TARGET_PREBUILT_KERNEL),)
# The QTI HALs built from source pick the UAPI headers up from the kernel
# build output, which doesn't exist with a prebuilt kernel. Stage the
# prebuilt headers there instead.
HAYDN_KERNEL_HEADERS_OUT := $(TARGET_OUT_INTERMEDIATES)/KERNEL_OBJ/usr
HAYDN_KERNEL_HEADERS := $(shell find $(TARGET_BOARD_KERNEL_HEADERS) -type f)

$(HAYDN_KERNEL_HEADERS_OUT): $(HAYDN_KERNEL_HEADERS)
	$(hide) rm -rf $@
	$(hide) mkdir -p $@/include
	$(hide) cp -r $(TARGET_BOARD_KERNEL_HEADERS)/. $@/include/
endif
