#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

# Define lists
scenes = ["clematis", "plant_1", "plant_2", "plant_3", "plant_4", "plant_5", "tulip"]
# types = ["point_clouds", "renders"]
# types = ["renders"]
types = ["point_clouds"]
methods = ["4dgaussians", "4dgs", "Dynamic3DGS", "gt", "ours"]
data_type = "synthetic"

# Base source directory
base_src = Path("../../../simulated_demo/white")

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
            if type_name == "renders":
                src_file = base_src / scene / method / "r_0" / "imgs.mp4"
                dest_dir = data_type / Path(scene) / type_name / method
            else:  # point_clouds
                if method != "gt":
                    #NOTE: no gt point clouds 
                    src_file = base_src / scene / method / "point_cloud_gs_color_animation_r_0.mp4"
                    dest_dir = data_type / Path(scene) / type_name / method
            
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