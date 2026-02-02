import os
import subprocess

# Define scenes and methods
scenes = ["pi_rose"]
scenes = ["pi_corn_full_subset4"]
# Stacking order: ours, Dynamic3DGS, 4dgs, 4dgaussians
stacking_order = ['ours', 'Dynamic3DGS', '4dgs', '4dgaussians']

# Base path (adjust this to your actual path structure)
base_path = './captured'

# ====================================================================
# --- CROP SPECIFICATIONS (Per-Method) ---
# Format: 'method': (x0, y0, x1, y1)
# x0, y0: Top-left corner coordinates
# x1, y1: Bottom-right corner coordinates
# The crop is applied to the area defined by (x1-x0) width and (y1-y0) height.

# Define a default crop (e.g., for methods not explicitly listed)
DEFAULT_CROP = (200, 200, 400, 400)

# ====================================================================

print("\n" + "=" * 60)
print("STEP 1: Stacking videos horizontally with per-method crop and reverse")
print("=" * 60)

for scene in scenes:
    if scene == "pi_rose":
        METHOD_CROP_SPECS = {
            # Method 1: 'ours' will crop from (200, 200) to (800, 600) -> 600x400 output
            'ours': (200, 150, 520, 375), 
            
            # Method 2: 'Dynamic3DGS' will crop from (100, 150) to (700, 550) -> 600x400 output
            'Dynamic3DGS': (200, 150, 520, 375), 
            
            # Method 3: '4dgs' is not explicitly listed, so it will use the DEFAULT_CROP.
            '4dgs': (200, 175, 520, 400), 
            # Method 4: '4dgaussians' will crop a smaller, more focused area 
            # from (300, 300) to (500, 500) -> 200x200 output
            '4dgaussians': (200, 175, 520, 400), 
            
        }
    else:
        METHOD_CROP_SPECS = {
            'ours': (200, 150, 400, 375), 
            
            # Method 2: 'Dynamic3DGS' will crop from (100, 150) to (700, 550) -> 600x400 output
            'Dynamic3DGS': (200, 150, 400, 375), 
            
            # Method 3: '4dgs' is not explicitly listed, so it will use the DEFAULT_CROP.
            '4dgs': (200, 175, 400, 400), 
            # Method 4: '4dgaussians' will crop a smaller, more focused area 
            # from (400, 300) to (300, 500) -> 200x200 output
            '4dgaussians': (200, 175, 400, 400), 
            
        }
        
    # Create concat directory
    concat_dir = os.path.join(base_path, scene, 'point_clouds', 'concat')
    os.makedirs(concat_dir, exist_ok=True)
    
    # Collect all video paths in the correct order
    video_inputs = []
    
    # Store the actual methods found and their calculated crop parameters
    active_methods = []
    crop_params_list = [] # Stores (crop_width, crop_height, crop_x, crop_y) for each video
    
    for method in stacking_order:
        if scene == "pi_rose":
            angle = "r_0"
        else:
            angle = "r_2"
        video_path = os.path.join(base_path, scene, 'point_clouds', method, angle, f'point_cloud_gs_color_animation_{angle}.mp4')
        
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
    
    # Build filter complex: crop each input, reverse, then stack
    num_videos = len(video_inputs)
    filter_stages = []
    stack_inputs = []
    
    print(f"\n--- Individual Crop Details for {scene} ---")
    
    for i in range(num_videos):
        method = active_methods[i]
        crop_w, crop_h, crop_x, crop_y = crop_params_list[i]
        
        print(f"[{i: <2}] {method: <15}: Cropping {crop_w}x{crop_h} at ({crop_x}, {crop_y})")
        
        # 1. Apply Crop: [i:v] -> crop=w:h:x:y -> [cropped_i]
        # Note: We must ensure all resulting cropped videos have the same width and height 
        # before hstack, or it will fail. If they are different, 
        # you might need a scale/pad filter before hstack.
        crop_filter = f'[{i}:v]crop={crop_w}:{crop_h}:{crop_x}:{crop_y}[cropped_{i}]'
        filter_stages.append(crop_filter)
        
        # 2. Apply Reverse: [cropped_i] -> reverse -> [rv_i]
        reverse_filter = f'[cropped_{i}]reverse[rv{i}]'
        filter_stages.append(reverse_filter)
        
        # Collect the reversed stream for stacking
        stack_inputs.append(f'[rv{i}]')
    
    print("------------------------------------------")
    
    # 3. Stack all reversed streams: [rv0][rv1]... -> hstack -> (final output)
    hstack_filter = f'{"".join(stack_inputs)}hstack=inputs={num_videos}'
    filter_stages.append(hstack_filter)
    
    filter_complex = ';'.join(filter_stages)
    
    cmd.extend([
        '-filter_complex', filter_complex,
        '-y', # Overwrite output files without asking
        output_stacked
    ])
    
    print(f"\nBuilding stacked video for: {scene} ({num_videos} videos)")
    print(f"Order: {' | '.join(active_methods)}")
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ Created custom-cropped and stacked video: {output_stacked}")
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
