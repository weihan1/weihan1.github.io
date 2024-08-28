#!/bin/bash

selected_simulated_scenes=("chair-two-views" "hotdog-three-views" "ficus-five-views")
selected_captured_scenes=("chef-two-views" "carving-three-views" "cinema-five-views") 
baselines=("monosdf_with_mask-baseline" "neuralangelo-baseline" "regnerf-baseline" "transient-neuralangelo")

  # Loop over all simulated scenes
#for baseline in "${baselines[@]}"
#do
#  for scene in "${selected_simulated_scenes[@]}"
#  do
#    first_word=$(echo "$scene" | cut -d'-' -f1)
#    echo "the first word is $first_word"
#    remote_path="/scratch/ondemand28/weihanluo/transientangelo/movies/${baseline}-blender-${first_word}/${scene}/save/it0-test.mp4"
#    remote_dir="tyche:${remote_path}"
#    destination_dir="simulated/${baseline}/${scene}.mp4"
#    echo "rsyncing from ${remote_dir} to ${destination_dir}"
#    rsync -avz --progress "${remote_dir}" "${destination_dir}"
#  done
#done

# Loop over all captured scenes
for baseline in "${baselines[@]}"
do
  for scene in "${selected_captured_scenes[@]}"
  do
      first_word=$(echo "$scene" | cut -d'-' -f1)
      echo "the first word is $first_word"
      remote_path="/scratch/ondemand28/weihanluo/transientangelo/movies/${baseline}-captured-${first_word}/${scene}/save/it0-test.mp4"
      remote_dir="tyche:${remote_path}"
      destination_dir="captured/${baseline}/${scene}.mp4"
      echo "rsyncing from ${remote_dir} to ${destination_dir}"
      rsync -avzn --progress "${remote_dir}" "${destination_dir}"
  done
done

