

class SplitImageDataset:
    """
    Set up parameters to configure image location
    and how to split into train and test datasets.
    """
    # Image directories
    raw_image_dir = "data/images/raw_images/"
    train_dir = raw_image_dir + "train"
    test_dir = raw_image_dir + "test"
    # Train and test sizes
    train_size = 80
    test_size = 20
    # Seed for the random image sampling
    seed = 1234


class TensorRescale:
    """
    """
    batch_size = 128
    epochs = 15
    IMG_HEIGHT = 150
    IMG_WIDTH = 150