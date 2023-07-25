#!/bin/bash

TEMP_FILE=$(mktemp)
echo "Temporary file: $TEMP_FILE"

poetry export --without-urls --without-hashes -f requirements.txt --output "$TEMP_FILE"

# read from TEMP_FILE, split by , and write first column to requirements.txt
awk -F';' '{print $1}' "$TEMP_FILE" > requirements.txt