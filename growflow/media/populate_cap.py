#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

# Define lists
scenes = ["pi_rose"]
scenes = ["pi_corn_full_subset4"]
# types = ["point_clouds", "renders"]
types = ["renders", "point_clouds"]
# types = ["point_clouds"]
# types = ["spacetime_viz"]
methods = ["4dgaussians", "4dgs", "Dynamic3DGS", "gt", "ours"]
methods = ["gt"]

angles = ["r_0", "r_1", "r_2", "r_3", "r_4", "r_5", "r_6"]
# Base source directory
base_src = Path("../../../captured")
base_dest = Path("./captured")
# Loop over each scene
for scene in scenes:
    print(f"Processing scene: {scene}")
    
    # Loop over each type (point_clouds and renders)
    for type_name in types:
        print(f"  Processing type: {type_name}")
        
        # Loop over each method
        for method in methods:
            print(f"    Processing method: {method}")
            
            # Determine source file and destination based on type
            for angle in angles:
                if type_name == "renders":
                    src_file = base_src / scene / method / angle / "imgs.mp4"
                    dest_dir = base_dest / scene /"renders"/ method / angle
                elif type_name == "point_clouds":  # point_clouds
                    #NOTE: no gt point clouds 
                    src_file = base_src / scene / method / f"point_cloud_gs_color_animation_{angle}.mp4"
                    dest_dir = base_dest / scene /"point_clouds"/ method / angle
                elif type_name == "spacetime_viz":
                    src_file = base_src / scene /method/"space_time_viz"/"output.mp4"
                    dest_dir = base_dest / scene / "spacetime_viz" / method
                
                # Create destination directory if it doesn't exist
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy the file if it exists
                if src_file.exists():
                    dest_file = dest_dir / src_file.name
                    shutil.copy2(src_file, dest_file)
                    print(f"      ✓ Copied to {dest_dir}/")
                else:
                    print(f"      ✗ Source file not found: {src_file}")
        
    print()

print("Done!")