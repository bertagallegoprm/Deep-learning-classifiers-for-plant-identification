import os
import random
from data.file_handler import copy_dir


def split_train_test(directory, train_size, test_size):
    train_dir = os.path.join(directory, "train")
    test_dir = os.path.join(directory, "test")
    # Create train, validation and test folders
    if not os.path.exists(train_dir):
        os.system(f"mkdir {train_dir}")

    if not os.path.exists(test_dir):
        os.system(f"mkdir {test_dir}")
    # Separate images in train and test folders
    for folder in os.listdir(directory):
        # Rename species folder with underscores
        species_words = folder.split(" ")
        species_folder = '_'.join(species_words)
        os.rename(os.path.join(directory, folder), os.path.join(directory, species_folder))
        if os.path.exists(os.path.join(directory, species_folder)):
            if (species_folder != "train") and (species_folder != "test"):
                # List all files in each species folder
                species_files = os.listdir((os.path.join(directory, species_folder)))
                # Get train and test sizes per species folder
                n_train = round(len(species_files)*(train_size/100))
                n_test = round(len(species_files)*(test_size/100))
                # Select train and test files 
                random.seed(seed)
                train_files = random.sample(species_files, n_train)
                test_files = list(set(species_files) - set(train_files))
                # Move files to folders
                for file in train_files:
                    if not os.path.exists(f"{train_dir}/{species_folder}"):
                        os.system(f"mkdir {train_dir}/{species_folder}")
                    os.rename(os.path.join(directory, species_folder, file), os.path.join(train_dir, species_folder, file))
                for file in test_files:
                    if not os.path.exists(f"{test_dir}"):
                        os.system(f"mkdir {test_dir}")
                    os.rename(os.path.join(directory, species_folder, file), os.path.join(test_dir, file))      
                # Remove empty folders
                os.rmdir(os.path.join(directory, species_folder))
                print(f"{species_folder} files splitted.")
        else:
            print(f"Path not found: {os.path.join(directory, folder)}")


if __name__ == "__main__":
    # CONFIGURATION
    # Image directories
    base_path = "data/images/image_preprocessing/"
    ##############################################
    src_directory = "cropped_images"
    dest_directory = "processed_images_train_test"
    src_path = os.path.join(base_path, src_directory)
    dest_path = os.path.join(base_path, dest_directory)
    #################################################
    # Train and test sizes
    train_size = 90
    test_size = 10
    # Seed for the random image sampling
    seed = 1234
    ###########################################

    # Copy source dir to empty destination dir
    copy_dir(src_path, dest_path)

    # Split images dataset
    split_train_test(dest_path, train_size, test_size)


