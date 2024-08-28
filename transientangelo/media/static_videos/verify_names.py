import os

datasets = ["simulated", "captured"]
baselines = ["monosdf", "neuralangelo", "ours", "regnerf", "transientnerf"]
scenes = {
    "simulated": ["chair-two-views.mp4", "ficus-five-views.mp4", "hotdog-three-views.mp4"],
    "captured": ["carving-three-views.mp4", "chef-two-views.mp4", "cinema-five-views.mp4"]
}

for dataset in datasets:
    for scene in scenes[dataset]:
        for baseline in baselines:
            path_to_check = os.path.join(dataset, baseline, scene)
            if not os.path.exists(path_to_check):
                print(f"{path_to_check} video does not exist!!!")

print("search completed.")
