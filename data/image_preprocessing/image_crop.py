import tensorflow as tf

# Tutorial: https://www.tensorflow.org/api_docs/python/tf/image/crop_to_bounding_box
# Import the image
image = tf.image.decode_png(tf.io.read_file("../ef1a27f6cfc1b4755c1c380f9a54ee9c_images/2684709_910347906.jpg"), channels=3)

## Set the variable values here
# Offset variables values (top-left corner)
offset_height= 400 # Vertical coordinate 
offset_width = 200 # Horizontal coordinate
# Target variables values 
target_height = 800 # Height of the result
target_width = 500 # Width of the result
# Crop the image as per the parameters
cropped_image_tensor = tf.image.crop_to_bounding_box(image, offset_height, offset_width, target_height, target_width)

output_image = tf.image.encode_png(cropped_image_tensor)

# Create a constant as filename
file_name = tf.constant("ouput_image.jpg")
file = tf.io.write_file(file_name, output_image)

print("Image Saved!")