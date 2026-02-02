import os
import subprocess

# Define scenes and methods
# scenes = ["pi_rose"]
scenes = ["pi_corn_full_subset4"]

# Stacking order: gt, ours, Dynamic3DGS, 4dgs, 4dgaussians
stacking_order = ['gt', 'ours', 'Dynamic3DGS', '4dgs', '4dgaussians']

# Define angles
angles = ["r_0", "r_1", "r_2", "r_3", "r_4", "r_5", "r_6"]
angles = ["r_2"]
# Base path (adjust this to your actual path structure)
base_path = './captured'

# Step 1: Crop all videos
print("=" * 60)
print("STEP 1: Cropping videos")
print("=" * 60)

for scene in scenes:
    if scene == "pi_rose":
        slow_down_factor = 0.36
        inverse = 1/slow_down_factor
        crop_params = {
            "r_0": (150, 600, 600, 1200),
            "r_1": (390, 600, 840, 1200),
            "r_2": (570, 600, 1020, 1200),
            "r_3": (540, 600, 990, 1200),
            "r_4": (420, 600, 870, 1200),
            "r_5": (150, 600, 600, 1200),
            "r_6": (150, 600, 600, 1200),
        }
    else:
        slow_down_factor = 0.36
        inverse = 1/slow_down_factor
        crop_params = {
            "r_2": (620, 250, 1030, 1200),
        }
        
    for method in stacking_order:
        for angle in angles:
            # Get crop parameters for this angle
            crop_x0, crop_y0, crop_x1, crop_y1 = crop_params[angle]
            crop_width = crop_x1 - crop_x0
            crop_height = crop_y1 - crop_y0
            
            # Construct input and output paths
            input_path = os.path.join(base_path, scene, 'renders', method, angle, 'imgs.mp4')
            output_path = os.path.join(base_path, scene, 'renders', method, angle, 'imgs_cropped.mp4')
            
            # Check if input file exists
            if not os.path.exists(input_path):
                print(f"⚠️  Skipping (file not found): {input_path}")
                continue
            
            # Run ffmpeg command to crop
            cmd = [
                'ffmpeg',
                '-i', input_path,
                # Combine all video filters into one string for -filter:v
                '-filter:v', f'crop={crop_width}:{crop_height}:{crop_x0}:{crop_y0},pad=ceil(iw/2)*2:ceil(ih/2)*2,setpts={inverse:.2f}*PTS',
                '-c:v', 'libx264',
                '-crf', '18',
                '-y',
                output_path
            ]
            
            print(f"Cropping: {scene}/{method}/{angle} - Region: ({crop_x0}, {crop_y0}) to ({crop_x1}, {crop_y1})")
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✓ Created: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"✗ Error cropping {input_path}: {e}")

# Step 2: Stack videos horizontally for each scene
print("\n" + "=" * 60)
print("STEP 2: Stacking videos horizontally for each scene and angle (with reverse)")
print("=" * 60)

for scene in scenes:
    for angle in angles:
        # Create concat directory for this angle
        concat_dir = os.path.join(base_path, scene, 'renders', 'concat', angle)
        os.makedirs(concat_dir, exist_ok=True)
        
        # Collect all video paths in the correct order
        video_inputs = []
        for method in stacking_order:
            video_path = os.path.join(base_path, scene, 'renders', method, angle, 'imgs_cropped.mp4')
            
            if os.path.exists(video_path):
                video_inputs.append(video_path)
            else:
                print(f"⚠️  Missing video for stacking: {video_path}")
        
        if len(video_inputs) == 0:
            print(f"⚠️  No videos found for {scene}/{angle}, skipping...")
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
        
        print(f"\nStacking videos for: {scene}/{angle} ({num_videos} videos)")
        print(f"Order: {' | '.join(stacking_order[:num_videos])}")
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Created stacked video: {output_stacked}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error stacking {scene}/{angle}: {e}")
            print(f"Command was: {' '.join(cmd)}")

print("\n" + "=" * 60)
print("✓ All done!")
print("=" * 60)