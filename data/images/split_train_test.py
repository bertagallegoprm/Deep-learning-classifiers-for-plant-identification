import os
import random
from data.config import SplitImageDataset as sid


if __name__ == "__main__":
    # Parameters configured in SplitImageDataset 
    raw_image_dir = sid.raw_image_dir
    train_dir = sid.train_dir
    test_dir = sid.test_dir
    train_size = sid.train_size
    test_size = sid.test_size
    seed = sid.seed
    ############################################
    # Create train and test folders
    if not os.path.exists(train_dir):
        os.system(f"mkdir {train_dir}")
    if not os.path.exists(test_dir):
        os.system(f"mkdir {test_dir}")
    # Separate images in train and test folders
    for folder in os.listdir(raw_image_dir):
        if os.path.isfile(os.path.join(raw_image_dir, folder)):
            # Rename species folder with underscores
            species_words = folder.split(" ")
            species_folder = '_'.join(species_words)
            os.rename(os.path.join(raw_image_dir, folder), os.path.join(raw_image_dir, species_folder) )
            if (species_folder != "train") and (species_folder != "test"):
                # List all files in each species folder
                species_files = os.listdir((os.path.join(raw_image_dir, species_folder)))
                # Get train and test sizes per species folder
                n_train = round(len(species_files)*(train_size/100))
                n_test = round(len(species_files)*(test_size/100))
                # Select train and test files and move to folders
                random.seed(seed)
                train_files = random.sample(species_files, n_train)
                test_files = list(set(species_files) - set(train_files))
                for file in train_files:
                    if not os.path.exists(f"{train_dir}/{species_folder}"):
                        os.system(f"mkdir {train_dir}/{species_folder}")
                    os.rename(os.path.join(raw_image_dir, species_folder, file), os.path.join(train_dir, species_folder, file))
                for file in test_files:
                    if not os.path.exists(f"{test_dir}/{species_folder}"):
                        os.system(f"mkdir {test_dir}/{species_folder}")
                    os.rename(os.path.join(raw_image_dir, species_folder, file), os.path.join(test_dir, species_folder, file))            
            # Remove empty folders
            if len(os.listdir(os.path.join(raw_image_dir, species_folder))) == 0:
                os.remove(os.path.join(raw_image_dir, species_folder))



