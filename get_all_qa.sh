#!/bin/bash

# Set base directory (default is current dir if not provided)
BASE_DIR="${1:-.}"

# Find all directories with 'qa' in the name
find "$BASE_DIR" -type d -name '*qa*' | while IFS= read -r qa_dir; do
    echo "Processing directory: $qa_dir"

    # Find .tar, .tar.gz, and .tgz files directly inside the qa_dir
    find "$qa_dir" -maxdepth 1 -type f \( -name "*.tar" -o -name "*.tar.gz" -o -name "*.tgz" \) | while IFS= read -r archive; do
        echo "  Extracting: $archive"
        tar -xzf "$archive" -C "$qa_dir"
    done
done

