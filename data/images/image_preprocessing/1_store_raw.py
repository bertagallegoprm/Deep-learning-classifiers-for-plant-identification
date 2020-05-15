import os
import shutil
import errno
from data.search import filter_hash
from data.config import images_filter, species_list

def create_raw_images_dir(base_path):
    """
    Create the folder to store the raw images 
    so that the image preprocessing can be decoupled 
    from the image request.
    """
    raw_images_dir = "raw_images"
    path_raw = base_path + raw_images_dir
    print(f"Creating directory: {path_raw}")
    try:
        shutil.rmtree(path_raw)
    except OSError:
        raise
    else:
        os.mkdir(path_raw)
        print (f"Created directory {path_raw}.")
        return path_raw
        

def copy_directories(source_path, destination_path, symlinks=False, ignore=None):
    """
    Copy all directories and files from source to origin directory.
    """
    for item in os.listdir(source_path):
        source = os.path.join(source_path, item)
        destination = os.path.join(destination_path, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination, symlinks, ignore)
            print(f"Copied {item} directory into {destination_path}")
        else:
            shutil.copy2(source, destination)
    print("End.")

if __name__ == "__main__":
    # Base path
    base_path = "data/images/"
    # Source directory
    filter_hash = filter_hash(images_filter, species_list.species_list)    
    source_path = f"data/images/image_request/{filter_hash}_images"
    # Create destination directory and copy contents from source
    destination_path = create_raw_images_dir(base_path)
    copy_directories(source_path, destination_path)