import tensorflow as tf
import os
import errno
import shutil
from PIL import Image


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


def jpg_to_tensor(source_dir, image_file):
    """
    Given a path to an image,
    return a 3-D tensor.
    """
    try:
        return tf.image.decode_jpeg(tf.io.read_file(f"{source_dir}/{image_file}"), channels=3)
    except:
        return print(f"Unable to open image {image_file}.")


def crop_image(tensor, image_file):
    """
    Crop image at a fixed position.
    Documentation: https://www.tensorflow.org/api_docs/python/tf/image/crop_to_bounding_box
    """
    ## Set the variable values here
    # Offset variables values (top-left corner)
    offset_height= 400 # Vertical coordinate 
    offset_width = 200 # Horizontal coordinate
    # Target variables values 
    target_height = 200 # Height of the result
    target_width = 200 # Width of the result
    try:
        return tf.image.crop_to_bounding_box(tensor, offset_height, offset_width, target_height, target_width)
    except:
        return print(f"Unable to crop image {image_file}.")


def crop_image_pil(source_dir, destination_dir, image_file):
    left = 200
    top = 400
    right = 400
    bottom = 200
    try:
        source_image = Image.open(os.path.join(source_dir, image_file))  
        try:
            cropped_image = source_image.crop((200,400,400, 200))
            try:
                if not os.path.exists(destination_dir):
                    os.mkdir(destination_dir)
                cropped_image.save(os.path.join(destination_dir,image_file)) 
            except: 
                return print(f"Unable to save image {image_file}.")
        except:
            return print(f"Unable to crop image {image_file}.")
    except:
        print(f"Unable to open image {image_file}.")


def resize_image(tensor, image_file):
    """
    Given an image stored as tensor,
    scale to a fixed pixel number.
    (From documentation: "Resizes an image to a target width and height
    by keeping the aspect ratio the same without distortion. 
    If the target dimensions don't match the image dimensions, 
    the image is resized and then padded with zeroes 
    to match requested dimensions.)
    """
    size = [100,100]
    try:
        return tf.image.resize_images(tensor, size,  method=tf.image.ResizeMethod.BILINEAR)
    except:
        return print(f"Unable to resize image {image_file}.")


def tensor_to_jpg(tensor, destination_dir, image_file):
    """
    Given a 3-D tensor
    return a .jpg image and save it to destination.
    """
    try:
        output_image = tf.image.encode_jpeg(tensor)
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)
        # Create a constant as filename
        image_path = os.path.join(destination_dir, image_file)
        file_name = tf.constant(image_path)
        tf.io.write_file(file_name, output_image)
    except:
        print(f"Unable to save image {image_file}.")
    else:
        print(f"{image_file} saved to {image_path}.")


def crop_all(source_dir, destination_dir):
    """
    Apply crop_image() to every image in the source directory.
    The source directory must have subfolders for each of the classes.
    """
    if os.path.exists(source_dir):
        for species_folder in os.listdir(source_dir):
            for image_file in os.listdir(os.path.join(source_dir, species_folder)):
                #image = jpg_to_tensor(os.path.join(source_dir, species_folder), image_file)
                #image = resize_image(image, image_file)
                #image = crop_image(image, image_file)
                #tensor_to_jpg(image, os.path.join(destination_dir, species_folder), image_file)
                crop_image_pil(os.path.join(source_dir, species_folder),
                               os.path.join(destination_dir, species_folder),
                               image_file
                               )
    else:
        print(f"Folder {source_dir} not found.")
    print("End.")


if __name__ == "__main__":

    # Create destination directory for the cropped images
    base_path = "data/images/image_preprocessing/"
    directory = "cropped_images"
    destination_dir = create_empty_dir(base_path, directory)

    # Crop all images in the directory
    source_dir = "data/images/image_preprocessing/resized_images/"
    crop_all(source_dir, destination_dir) 