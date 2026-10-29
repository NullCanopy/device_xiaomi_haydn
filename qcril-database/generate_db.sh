#!/bin/bash
#
# Copyright (C) 2024 The LineageOS Project
#           (C) 2026 Paranoid Android
#
# SPDX-License-Identifier: Apache-2.0
#

set -e

if [[ $# -le 2 ]]; then
    echo "syntax: generate_db.sh sqlite3 target_db sql_file0 sql_file1..."
    exit 1
fi

SQLITE=$1
if [[ ! -x "$SQLITE" ]]; then
    echo "sqlite binary not found or not executable: $SQLITE"
    exit 1
fi

TARGET_DB=$2

shift 2

# Split the config sql and ecc sql files
for file in "$@"; do
    if [[ $file == *_config.sql ]]; then
        CONFIG_SQL_FILES+=("$file")
    else
        ECC_SQL_FILES+=("$file")
    fi
done

# Sort the files by the version in their name, as they come from both the
# device and vendor trees
sort_by_version() {
    for file in "$@"; do
        printf '%s\t%s\n' "$(basename "$file")" "$file"
    done | sort -V -k1,1 | cut -f2
}

IFS=$'\n' CONFIG_SQL_FILES=($(sort_by_version "${CONFIG_SQL_FILES[@]}"))
IFS=$'\n' ECC_SQL_FILES=($(sort_by_version "${ECC_SQL_FILES[@]}"))
unset IFS

# Config migrations should be applied after ecc migrations
ORDERED_MIGRATIONS=("${ECC_SQL_FILES[@]}" "${CONFIG_SQL_FILES[@]}")

# The migrations use double-quoted string literals, which sqlite3 only
# accepts when built with SQLITE_DQS, so convert them to single quotes.
rm -f "$TARGET_DB"
{
    echo ".bail on"
    echo "BEGIN TRANSACTION;"
    for file in "${ORDERED_MIGRATIONS[@]}"; do
        sed "s/\"/'/g" "$file"
    done
    echo "COMMIT TRANSACTION;"
} | $SQLITE "$TARGET_DB"
