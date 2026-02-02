import os
import subprocess

# Define scenes and methods
scenes = ['clematis', 'plant_1', 'plant_2', 'plant_3', 'plant_4', 'plant_5', 'tulip']
# scenes = ["clematis"]

# Stacking order: gt, ours, Dynamic3DGS, 4dgs, 4dgaussians
#NOTE: skip gt here
# stacking_order = ['gt', 'ours', 'Dynamic3DGS', '4dgs', '4dgaussians']
stacking_order = ['ours', 'Dynamic3DGS', '4dgs', '4dgaussians']

# Base path (adjust this to your actual path structure)
base_path = './synthetic'

# Step 2: Stack videos horizontally for each scene
print("\n" + "=" * 60)
print("STEP 1: Stacking videos horizontally for each scene (with reverse)")
print("=" * 60)

for scene in scenes:
    # Create concat directory
    concat_dir = os.path.join(base_path, scene, 'point_clouds', 'concat')
    os.makedirs(concat_dir, exist_ok=True)
    
    # Collect all video paths in the correct order
    video_inputs = []
    for method in stacking_order:
        video_path = os.path.join(base_path, scene, 'point_clouds', method, 'point_cloud_gs_color_animation_r_0.mp4')
        
        if os.path.exists(video_path):
            video_inputs.append(video_path)
        else:
            print(f"⚠️  Missing video for stacking: {video_path}")
    
    if len(video_inputs) == 0:
        print(f"⚠️  No videos found for {scene}, skipping...")
        continue
    
    # Output stacked video
    output_stacked = os.path.join(concat_dir, 'all_methods_stacked.mp4')
    
    # Build ffmpeg command for horizontal stacking with reverse
    cmd = ['ffmpeg']
    
    # Add all input files
    for video in video_inputs:
        cmd.extend(['-i', video])
    
    # Build filter complex: reverse each input then stack
    num_videos = len(video_inputs)
    reverse_filters = ';'.join([f'[{i}:v]reverse[rv{i}]' for i in range(num_videos)])
    stack_inputs = ''.join([f'[rv{i}]' for i in range(num_videos)])
    filter_complex = f'{reverse_filters};{stack_inputs}hstack=inputs={num_videos}'
    
    cmd.extend([
        '-filter_complex', filter_complex,
        '-y',
        output_stacked
    ])
    
    print(f"\nStacking videos for: {scene} ({num_videos} videos)")
    print(f"Order: {' | '.join(stacking_order[:num_videos])}")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ Created stacked video: {output_stacked}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error stacking {scene}: {e}")
        print(f"Command was: {' '.join(cmd)}")

print("\n" + "=" * 60)
print("✓ All done!")
print("=" * 60)