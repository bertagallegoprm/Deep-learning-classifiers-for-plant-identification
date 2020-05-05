import os
import random

if __name__ == "__main__":
    raw_image_dir = "data/images/raw_images/"
    train_dir = raw_image_dir + "train"
    test_dir = raw_image_dir + "test"
    train_size = 80
    test_size = 20
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
                print(len(species_files))
                # Get train and test sizes per species folder
                n_train = round(len(species_files)*(train_size/100))
                n_test = round(len(species_files)*(test_size/100))
                # Select train and test files and move to folders
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



