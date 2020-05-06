import os
import random

if __name__ == "__main__":
    # Parameters ##############################
    # Image directories
    raw_image_dir = "data/images/raw_images/"
    train_dir = raw_image_dir + "train"
    val_dir = raw_image_dir + "val"
    test_dir = raw_image_dir + "test"
    # Train and test sizes
    train_size = 60
    val_size = 20
    test_size = 20
    # Seed for the random image sampling
    seed = 1234
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
        if os.path.exists(os.path.join(raw_image_dir, folder)):
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
                    os.rename(os.path.join(raw_image_dir, species_folder, file), os.path.join(test_dir, file))      
                # Remove empty folders
                os.rmdir(os.path.join(raw_image_dir, species_folder))
                print(f"{species_folder} files splitted.")
        else:
            print(f"Path not found: {os.path.join(raw_image_dir, folder)}")



