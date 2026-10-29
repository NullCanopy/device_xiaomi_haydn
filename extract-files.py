#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# Copyright (C) 2021 The LineageOS Project
#           (C) 2026 Paranoid Android
#
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/qcom/common/vendor/telephony',
    'hardware/qcom/wlan/qcwcn',
    'hardware/xiaomi',
    'vendor/qcom/common/vendor/adreno/r',
    'vendor/qcom/common/vendor/display/5.4',
    'vendor/qcom/common/vendor/gps-legacy',
    'vendor/qcom/common/vendor/media/5.4',
    'vendor/qcom/common/vendor/perf',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/init/vendor.xiaomi.hardware.citsensorservice@1.1-service.rc': blob_fixup()
        .add_line_if_missing('    task_profiles ServiceCapacityLow'),
    ('vendor/etc/media_lahaina/video_system_specs.json', 'vendor/etc/media_shima_v1/video_system_specs.json', 'vendor/etc/media_yupik_v1/video_system_specs.json'): blob_fixup()
        .regex_replace('"max_retry_alloc_output_timeout": 10000,', '"max_retry_alloc_output_timeout": 0,'),
    ('vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/lib64/android.hardware.secure_element@1.0-impl.so': blob_fixup()
        .remove_needed('android.hidl.base@1.0.so'),
    'vendor/lib64/libmisight.so': blob_fixup()
        .add_needed('libjsoncpp_shim.so'),
    'vendor/etc/camera/pureShot_parameter.xml': blob_fixup()
        .regex_replace(r'=(\d+)>', r'="\1">'),
    'vendor/lib/libaudioroute_ext.so': blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .binary_regex_replace(b'\x73\x74\x5F\x6C\x69\x63\x65\x6E\x73\x65\x2E\x6C\x69\x63', b'\x63\x61\x6D\x65\x72\x61\x5F\x63\x6E\x66\x2E\x74\x78\x74')
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/hw/camera.xiaomi.so': blob_fixup()
        .sig_replace('52 07 00 94', '1F 20 03 D5'),
    'vendor/lib64/hw/com.qti.chi.override.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/vendor.xiaomi.hardware.cameraperf@1.0-impl.so': blob_fixup()
        .sig_replace('21 00 80 52 7c 00 00 94', '21 00 80 52 1F 20 03 D5'),
    ('vendor/lib64/libalAILDC.so', 'vendor/lib64/libalLDC.so', 'vendor/lib64/libalhLDC.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    ('vendor/lib64/libarcsoft_hdrplus_hvx_stub.so', 'vendor/lib64/libarcsoft_super_night_raw.so', 'vendor/lib64/libellc.so',
    'vendor/lib64/libmialgo_pureShot.so', 'vendor/lib64/libmialgo_vn_clk.so', 'vendor/lib64/libmiphone_preview_bokeh.so'): blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open')
        .clear_symbol_version('remote_handle64_close')
        .clear_symbol_version('remote_handle64_invoke')
        .clear_symbol_version('remote_handle64_open')
        .clear_symbol_version('remote_register_buf_attr'),
}

module = ExtractUtilsModule(
    'haydn',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
