

class SplitImageDataset:
    """
    Set up parameters to configure image location
    and how to split into train and test datasets.
    """
    # Image directories
    raw_image_dir = "data/images/raw_images/"
    train_dir = raw_image_dir + "train"
    test_dir = raw_image_dir + "test"
    val_dir = raw_image_dir + "val"
    # Train and test sizes
    train_size = 60
    test_size = 20
    val_size = 20
    # Seed for the random image sampling
    seed = 1234


class ImageGenerator:
    """
    color_mode - "rgb" for 3 color channel, "grayscale" for black and white.
    class_mode - "binary" for 2 classes, "categoriacal" for more than 2, "input" for autoencoder.
    batch sixe - No. of images to be yielded from the generator per batch.
    epoch - 
    shuffle - True to shuffle the order of images being yielded. False otherwise.
    seed - seed for the random image augmentation
    """
    color_mode= "rgb"   
    img_height = 150 # if 50: pixels too big; if 250: too much noise
    img_width = 150   
    class_mode="categorical" 
    batch_size = 128 
    epochs = 15                                     
    shuffle=True                                                               
    seed = 1234 