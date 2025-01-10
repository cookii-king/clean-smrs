#!/bin/bash

# Check if a directory is passed as an argument
if [ -z "$1" ]; then
  echo "No directory provided. Please enter a directory path:"
  read -r DIRECTORY
else
  DIRECTORY="$1"
fi

# Check if the directory exists
if [ ! -d "$DIRECTORY" ]; then
  echo "Error: '$DIRECTORY' is not a valid directory."
  exit 1
fi

# Output file name
OUTPUT_FILE="directory_structure_and_files.txt"

# Predefined paths to exclude, including .DS_Store and .sqlite3 files
EXCLUDED_PATHS=("*/__pycache__/*" "*/.git/*" "*.log" "*.tmp" "*.sqlite3" "*.DS_Store" "*/images/*" "*/videos/*" "*.png" "*.jpg" "*/staticfiles/*" "*/static/*" "*__pycache__*")

# Ask the user if they want to add more paths to exclude
echo "Do you want to exclude additional files or directories? (y/n)"
read -r ADD_EXCLUSIONS

if [[ "$ADD_EXCLUSIONS" =~ ^[Yy]$ ]]; then
  echo "Enter paths or patterns to exclude (one per line). Type 'done' when finished:"
  while true; do
    read -r PATH_TO_EXCLUDE
    if [[ "$PATH_TO_EXCLUDE" == "done" ]]; then
      break
    fi
    EXCLUDED_PATHS+=("$PATH_TO_EXCLUDE")
  done
fi

# Display the list of exclusions
echo "Excluding the following paths:"
for path in "${EXCLUDED_PATHS[@]}"; do
  echo "- $path"
done

# Create or overwrite the output file
echo "Directory structure and file contents for: $DIRECTORY" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Generate the directory tree structure, excluding specific paths, and append to the output file
echo "Generating directory structure..." >> "$OUTPUT_FILE"
tree "$DIRECTORY" -I "$(IFS='|'; echo "${EXCLUDED_PATHS[*]}")" >> "$OUTPUT_FILE" 2>/dev/null || echo "tree command failed. Please install it." >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Add file contents below the tree structure
echo "Appending file contents..." >> "$OUTPUT_FILE"

# Use find to exclude unwanted paths and process the files
FIND_EXCLUDE_ARGS=""
for path in "${EXCLUDED_PATHS[@]}"; do
  FIND_EXCLUDE_ARGS="$FIND_EXCLUDE_ARGS -not -path \"$path\""
done

eval find "$DIRECTORY" -type f $FIND_EXCLUDE_ARGS | while read -r FILE; do
  echo "File: $FILE" >> "$OUTPUT_FILE"
  echo "----------------------------------------" >> "$OUTPUT_FILE"
  cat "$FILE" >> "$OUTPUT_FILE" 2>/dev/null || echo "Error reading $FILE" >> "$OUTPUT_FILE"
  echo -e "\n\n" >> "$OUTPUT_FILE"
done

echo "Done! Output saved to $OUTPUT_FILE"
