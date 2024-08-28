#!/bin/bash

selected_simulated_scenes=("chair_two_views" "hotdog_three_views" "ficus_five_views")
selected_captured_scenes=("chef_two_views" "carving_three_views" "cinema_five_views") 

# Loop over all simulated scenes
for scene in "${selected_simulated_scenes[@]}"
do
  remote_path="/scratch/ondemand28/weihanluo/TransientNeRF/results/${scene}/movies/${scene}.mp4"
  remote_dir="tyche:${remote_path}"
  destination_dir="./simulated/transientnerf/"
  rsync -avz --progress "${remote_dir}" "${destination_dir}"
done


# Loop over all simulated scenes
for scene in "${selected_captured_scenes[@]}"
do
  remote_path="/scratch/ondemand28/weihanluo/TransientNeRF/results/${scene}/movies/${scene}.mp4"
  remote_dir="tyche:${remote_path}"
  destination_dir="./simulated/transientnerf/"
  rsync -avz --progress "${remote_dir}" "${destination_dir}"
done


