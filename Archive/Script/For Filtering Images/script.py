import os
import shutil
import random

# Paths
train_dir = "C:/Users/sabar/Downloads/Dataset - Copy/train"
images_dir = os.path.join(train_dir, "images")
labels_dir = os.path.join(train_dir, "labels")

newtrain_dir = "C:/Users/sabar/Downloads/Dataset - Copy/trainnewtrain"
newtest_dir = "C:/Users/sabar/Downloads/Dataset - Copy/trainnewtest"

# Create new folders
for folder in [newtrain_dir, newtest_dir]:
    os.makedirs(os.path.join(folder, "images"), exist_ok=True)
    os.makedirs(os.path.join(folder, "labels"), exist_ok=True)

# Get all image filenames
all_images = os.listdir(images_dir)
random.shuffle(all_images)

# Split ratio 80-20
split_idx = int(len(all_images) * 0.8)
train_images = all_images[:split_idx]
test_images = all_images[split_idx:]

# Function to move files
def move_files(file_list, dest_dir):
    for fname in file_list:
        shutil.move(os.path.join(images_dir, fname), os.path.join(dest_dir, "images", fname))
        label_file = fname.replace(".jpg", ".txt")  # change extension if needed
        shutil.move(os.path.join(labels_dir, label_file), os.path.join(dest_dir, "labels", label_file))

# Move images
move_files(train_images, newtrain_dir)
move_files(test_images, newtest_dir)

# Optional: remove old empty train folder
shutil.rmtree(train_dir)
