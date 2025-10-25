#!/bin/bash

# Run with: bash .\compress.bash

# Directory containing folders to compress
BASE_DIR="Magi-Labyrinth-of-Magic-Scrapping"

# Output directory for archives
OUTPUT_DIR="zipped_archives"
mkdir -p "$OUTPUT_DIR"

# Loop through each folder in BASE_DIR
for folder in "$BASE_DIR"/*/; do
    # Remove trailing slash and get folder name
    folder_name=$(basename "$folder")
    # Create archive
    "/c/Program Files/7-Zip/7z.exe" a "$OUTPUT_DIR/${folder_name}.7z" "$folder"
done
