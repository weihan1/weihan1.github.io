import os
import subprocess

# Define scenes and methods
scenes = ["pi_rose"]
# scenes = ["clematis"]

# Stacking order: ours, Dynamic3DGS, 4dgs, 4dgaussians
stacking_order = ['ours', 'Dynamic3DGS', '4dgs', '4dgaussians']

# Base path (adjust this to your actual path structure)
base_path = './captured'

# ====================================================================
# --- SPEED CONTROL ---
# Set the speed multiplier for the final output video
# 1.0 = normal speed
# 0.5 = half speed (slower)
# 0.25 = quarter speed (much slower)
# 2.0 = double speed (faster)
SPEED_MULTIPLIER = 0.6  # Adjust this value to control playback speed
# ====================================================================

# ====================================================================
# --- CROP SPECIFICATIONS (Per-Method) ---
# Format: 'method': (x0, y0, x1, y1)
# x0, y0: Top-left corner coordinates
# x1, y1: Bottom-right corner coordinates
# The crop is applied to the area defined by (x1-x0) width and (y1-y0) height.

# Define a default crop (e.g., for methods not explicitly listed)
DEFAULT_CROP = (150, 600, 1050, 1200)

METHOD_CROP_SPECS = {
}
# ====================================================================

print("\n" + "=" * 60)
print("STEP 1: Stacking videos horizontally with per-method crop")
print(f"Speed multiplier: {SPEED_MULTIPLIER}x")
print("=" * 60)

for scene in scenes:
    # Create concat directory
    concat_dir = os.path.join(base_path, scene, 'spacetime_viz', 'concat')
    os.makedirs(concat_dir, exist_ok=True)
    
    # Collect all video paths in the correct order
    video_inputs = []
    
    # Store the actual methods found and their calculated crop parameters
    active_methods = []
    crop_params_list = [] # Stores (crop_width, crop_height, crop_x, crop_y) for each video
    
    for method in stacking_order:
        video_path = os.path.join(base_path, scene, 'spacetime_viz', method, 'output.mp4')
        
        if os.path.exists(video_path):
            video_inputs.append(video_path)
            active_methods.append(method)
            
            # Get crop specs: (x0, y0, x1, y1)
            x0, y0, x1, y1 = METHOD_CROP_SPECS.get(method, DEFAULT_CROP)
            
            # Calculate the required FFmpeg parameters: width, height, x, y (starting point)
            crop_w = x1 - x0
            crop_h = y1 - y0
            crop_x = x0
            crop_y = y0
            
            crop_params_list.append((crop_w, crop_h, crop_x, crop_y))
        else:
            print(f"⚠️ Missing video for stacking: {video_path}")
    
    if len(video_inputs) == 0:
        print(f"⚠️ No videos found for {scene}, skipping...")
        continue
    
    # Output stacked video
    output_stacked = os.path.join(concat_dir, 'all_methods_stacked.mp4')
    
    # Build ffmpeg command
    cmd = ['ffmpeg']
    
    # Add all input files
    for video in video_inputs:
        cmd.extend(['-i', video])
    
    # Build filter complex: crop each input, then stack, then adjust speed
    num_videos = len(video_inputs)
    filter_stages = []
    stack_inputs = []
    
    print(f"\n--- Individual Crop Details for {scene} ---")
    
    for i in range(num_videos):
        method = active_methods[i]
        crop_w, crop_h, crop_x, crop_y = crop_params_list[i]
        
        print(f"[{i: <2}] {method: <15}: Cropping {crop_w}x{crop_h} at ({crop_x}, {crop_y})")
        
        # Apply Crop: [i:v] -> crop=w:h:x:y -> [cropped_i]
        crop_filter = f'[{i}:v]crop={crop_w}:{crop_h}:{crop_x}:{crop_y}[cropped_{i}]'
        filter_stages.append(crop_filter)
        
        # Collect the cropped stream for stacking
        stack_inputs.append(f'[cropped_{i}]')
    
    print("------------------------------------------")
    
    # Stack all cropped videos horizontally
    hstack_filter = f'{"".join(stack_inputs)}hstack=inputs={num_videos}[stacked]'
    filter_stages.append(hstack_filter)
    
    # Apply speed adjustment using setpts
    # PTS (Presentation TimeStamp) multiplier: higher = slower, lower = faster
    # For 0.5x speed (slower), use PTS*2
    # For 2x speed (faster), use PTS*0.5
    pts_multiplier = 1.0 / SPEED_MULTIPLIER
    speed_filter = f'[stacked]setpts={pts_multiplier}*PTS[output]'
    filter_stages.append(speed_filter)
    
    filter_complex = ';'.join(filter_stages)
    
    cmd.extend([
        '-filter_complex', filter_complex,
        '-map', '[output]',
        '-y', # Overwrite output files without asking
        output_stacked
    ])
    
    print(f"\nBuilding stacked video for: {scene} ({num_videos} videos)")
    print(f"Order: {' | '.join(active_methods)}")
    print(f"Speed: {SPEED_MULTIPLIER}x")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ Created custom-cropped stacked video: {output_stacked}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error stacking {scene}: {e}")
        print("💡 NOTE: FFmpeg hstack requires all input streams to have the same dimensions.")
        print(f"💡 Ensure that the resulting WxH ({crop_w}x{crop_h}) is the same for all methods.")
        print(f"FFmpeg stdout: {e.stdout.decode()}")
        print(f"FFmpeg stderr: {e.stderr.decode()}")
        print(f"Command was: {' '.join(cmd)}")

print("\n" + "=" * 60)
print("✓ All done!")
print("=" * 60)