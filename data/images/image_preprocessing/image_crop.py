import tensorflow as tf
import os
import errno
import shutil


def create_empty_dir(base_path, directory):
    """
    Create a new directory.
    If it already exists, it deletes it and all its contents.
    It returns the new directory path.
    """
    full_path = base_path + directory
    print(f"Creating directory: {full_path}")
    try:
        shutil.rmtree(full_path)
    except:
        pass
    finally:
        os.mkdir(full_path)
        print (f"Created directory {full_path}.")
        return full_path


def crop_image(source_dir, destination_dir, image_file):
    """
    Crop image at a fixed position.
    Documentation: https://www.tensorflow.org/api_docs/python/tf/image/crop_to_bounding_box
    """
    ## Set the variable values here
    # Offset variables values (top-left corner)
    offset_height= 400 # Vertical coordinate 
    offset_width = 200 # Horizontal coordinate
    # Target variables values 
    target_height = 100 # Height of the result
    target_width = 100 # Width of the result

    # Import the image
    try:
        image = tf.image.decode_png(tf.io.read_file(f"{source_dir}/{image_file}"), channels=3)
        # Crop the image as per the parameters
        try:
            cropped_image_tensor = tf.image.crop_to_bounding_box(image, offset_height, offset_width, target_height, target_width)
            output_image = tf.image.encode_png(cropped_image_tensor)
            # Save image
            try:
                # Create species folder if it does not exist
                if not os.path.exists(destination_dir):
                    os.mkdir(destination_dir)
                # Create a constant as filename
                image_crop_path = os.path.join(destination_dir, image_file)
                file_name = tf.constant(image_crop_path)
                tf.io.write_file(file_name, output_image)
                #print(f"{image_file} cropped.")
            except:
                return print(f"Unable to save image {image_file}.")
        except:
            return print(f"Unable to crop image {image_file}.")
    except:
        return print(f"Unable to open image {image_file}.")


def crop_all_raw_images(source_dir, destination_dir):
    """
    Apply crop_image() to every image in the source directory.
    The source directory must have subfolders for each of the classes.
    """
    if os.path.exists(source_dir):
        for species_folder in os.listdir(source_dir):
            for image_file in os.listdir(os.path.join(source_dir, species_folder)):
                try:
                    crop_image(os.path.join(source_dir, species_folder), os.path.join(destination_dir, species_folder), image_file)
                except:
                    pass
    else:
        print(f"Folder {source_dir} not found.")
    print("End.")


if __name__ == "__main__":

    # Create destination directory for the cropped images
    base_path = "data/images/image_preprocessing/"
    cropped_directory = "cropped_images"
    destination_dir = create_empty_dir(base_path, cropped_directory)

    # Delte invalid files
    #os.remove(f"{source_dir}/Crataegus_monogyna/Crataegus_monogyna_1258956705.jpg)

    # Crop all images in the raw_images directory
    source_dir = "data/images/raw_images/"
    crop_all_raw_images(source_dir, destination_dir) 
