#!/bin/bash

# Directories containing datasets
dataset_dir=("simulated" "captured")

# Loop over all datasets
for dataset in "${dataset_dir[@]}"; do
  # Loop over all directories in the dataset
  for dir in "$dataset"/*/; do
    # Set video_dir to the current directory in the loop
    video_dir="$dir"
    
    # Loop over all video files in the current directory
    for video in "$video_dir"/*; do
      if [ -f "$video" ]; then
        echo "Opening $video"
        # Use 'xdg-open' for Linux or 'open' for macOS
        if command -v xdg-open > /dev/null; then
          xdg-open "$video"
        elif command -v open > /dev/null; then
          open "$video"
        else
          echo "No suitable command found to open video files."
          exit 1
        fi
        sleep 15
      fi
    done
  done
done
