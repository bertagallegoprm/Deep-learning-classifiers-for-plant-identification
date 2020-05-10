import tensorflow as tf
import os


def crop_image(folder_path, image_file):
    """
    Documentation: https://www.tensorflow.org/api_docs/python/tf/image/crop_to_bounding_box
    """
    # Import the image
    image = tf.image.decode_png(tf.io.read_file(f"{folder_path}{image_file}"), channels=3)
    ## Set the variable values here
    # Offset variables values (top-left corner)
    offset_height= 400 # Vertical coordinate 
    offset_width = 200 # Horizontal coordinate
    # Target variables values 
    target_height = 800 # Height of the result
    target_width = 500 # Width of the result
    try:
        # Crop the image as per the parameters
        cropped_image_tensor = tf.image.crop_to_bounding_box(image, offset_height, offset_width, target_height, target_width)
        output_image = tf.image.encode_png(cropped_image_tensor)
        # Create a constant as filename
        image_crop_path = "data/images/image_preprocessing/cropped_images/"+image_file
        file_name = tf.constant(image_crop_path)
        tf.io.write_file(file_name, output_image)
        print(f"{image_file} cropped.")
    except:
        print(f"Error: image {image_file}")


if __name__ == "__main__":
    # Get file names from the folder 
    folder_path = "data/images/sample_images/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image_file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, image_file)):
            crop_image(folder_path, image_file)