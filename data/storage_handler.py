import os
import subprocess

def get_images_size():
    """
    Return size of images folder in GB.
    """
    path = "images/"
    total_size = 0
    for root, directory, files in os.walk(path):  
        for file in files:
            file_size = subprocess.check_output(f"wc -c < {path}{file}", shell=True)
            file_size = int(file_size)
            total_size = total_size + file_size
    total_size_gb = round((((total_size/1024)/1024)/1024),6)
    return total_size_gb


def stop_if_size(max_size):
    """
    Rise AssertionError if image folder reached size limit.
    (I am using this as a security messure to not collapse
    the VM where I am working due to lack of space
    when downloading all the images).
    """
    assert get_images_size() < max_size, f"Image folder reached {max_size} GB."



if __name__ == "__main__":
    stop_if_size(10)