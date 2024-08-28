import os
import cv2

def save_transition_video(filename, img_dir, save_format="mp4", fps=30):
    '''
    Create a transition video where we first show more of image sets 1, then a line wipes through those images
    and show more of image sets 2. 
    
    '''
    output_filename = img_dir.split("/")[-1].split("_")[0]
    mesh_images = [cv2.imread(f"{img_dir}/")]
    normal_images = []
    N = len(mesh_images)
    H,W = mesh_images[0].shape
    for f in os.listdir(img_dir)
        if mesh_matcher_compiled.search(f):
            mesh_images.append(f)
        elif mesh_matcher_compiled.search(f):
            normal_images.append(f)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (W, H))
    transition_duration = fps * 2
    for frame_index in range(transition_duration):
        alpha = frame_index / (transition_duration - 1)
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        
        for i in range(N):
            # Line position for the current frame
            line_position = int(W * alpha)
            
            # Create the transition frame
            left_part = images_set1[i][:, :line_position]
            right_part = images_set2[i][:, line_position:]
            
            # Combine the parts
            frame[:, :line_position] = left_part
            frame[:, line_position:] = right_part
            
            # Write the frame to the video
            video_writer.write(frame)
    video_writer.release()
