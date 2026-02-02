import os

def create_folder_structure():
    # Base directory
    base_dir = "./captured"
    
    # Main plant folders
    plant_folders = ["pi_rose"]
    
    # Type of visuals
    type_of_vis = ["renders", "point_clouds"]
    
    # Subdirectories for each plant folder
    subdirectories = ["4dgaussians", "4dgs", "Dynamic3DGS", "gt", "ours"]
    angles = ["r_0", "r_1", "r_2", "r_3", "r_4", "r_5", "r_6"] 
    # Create base directory if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)
    
    # Create each plant folder and its subdirectories
    for plant in plant_folders:
        plant_path = os.path.join(base_dir, plant)
        
        # Create the main plant directory
        os.makedirs(plant_path, exist_ok=True)
        print(f"Created directory: {plant_path}")
        for viz in type_of_vis :
            viz_path =  os.path.join(plant_path, viz)
            os.makedirs(viz_path, exist_ok=True)
            print(f"  Created subdirectory: {viz_path}")

            for subdir in subdirectories:
                subdir_path = os.path.join(viz_path, subdir)
                os.makedirs(subdir_path, exist_ok=True)
                print(f"  Created subdirectory: {subdir_path}")
                for angle in angles:
                    angle_path = os.path.join(subdir_path, angle)
                    os.makedirs(angle_path, exist_ok=True)
                    print(f"  Created subdirectory: {angle_path}")
    
    print("\nFolder structure created successfully!")

if __name__ == "__main__":
    create_folder_structure()