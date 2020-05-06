import os
import random
from data.config import SplitImageDataset as sid


if __name__ == "__main__":
    # Parameters in SplitImageDataset
    # Image directories
    raw_image_dir = sid.raw_image_dir
    train_dir = sid.train_dir
    val_dir = sid.val_dir
    test_dir = sid.test_dir
    # Train and test sizes
    train_size = sid.train_size
    val_size = sid.val_size
    test_size = sid.test_size
    # Seed for the random image sampling
    seed = sid.seed
    ###########################################
    # Create train, validation and test folders
    if not os.path.exists(train_dir):
        os.system(f"mkdir {train_dir}")
    if not os.path.exists(val_dir):
        os.system(f"mkdir {val_dir}")
    if not os.path.exists(test_dir):
        os.system(f"mkdir {test_dir}")
    # Separate images in train and test folders
    for folder in os.listdir(raw_image_dir):
        # Rename species folder with underscores
        species_words = folder.split(" ")
        species_folder = '_'.join(species_words)
        os.rename(os.path.join(raw_image_dir, folder), os.path.join(raw_image_dir, species_folder))
        if os.path.exists(os.path.join(raw_image_dir, species_folder)):
            if (species_folder != "train") and (species_folder != "val") and (species_folder != "test"):
                # List all files in each species folder
                species_files = os.listdir((os.path.join(raw_image_dir, species_folder)))
                # Get train and test sizes per species folder
                n_train = round(len(species_files)*(train_size/100))
                n_val = round(len(species_files)*(val_size/100))
                n_test = round(len(species_files)*(test_size/100))
                # Select train and test files 
                random.seed(seed)
                train_files = random.sample(species_files, n_train)
                val_files = random.sample((list(set(species_files) - set(train_files))),n_val)
                test_files = list(set(species_files) - set(train_files) - set(val_files))
                # Move files to folders
                for file in train_files:
                    if not os.path.exists(f"{train_dir}/{species_folder}"):
                        os.system(f"mkdir {train_dir}/{species_folder}")
                    os.rename(os.path.join(raw_image_dir, species_folder, file), os.path.join(train_dir, species_folder, file))
                for file in val_files:
                    if not os.path.exists(f"{val_dir}/{species_folder}"):
                        os.system(f"mkdir {val_dir}/{species_folder}")
                    os.rename(os.path.join(raw_image_dir, species_folder, file), os.path.join(val_dir, species_folder, file))
                for file in test_files:
                    if not os.path.exists(f"{test_dir}/test"):
                        os.system(f"mkdir {test_dir}/test")
                    os.rename(os.path.join(raw_image_dir, species_folder, file), os.path.join(test_dir, "test", file))      
                # Remove empty folders
                os.rmdir(os.path.join(raw_image_dir, species_folder))
                print(f"{species_folder} files splitted.")
        else:
            print(f"Path not found: {os.path.join(raw_image_dir, folder)}")



