from data.search import SearchFilter, Species
from data.species_names import native_trees_list
from data.image import ImageDimension


# SEARCH FILTERS #################################################
images_filter = SearchFilter(
    search_name = "Herbarium specimens images from native trees in GB",
    media_type = "StillImage",  
    country = "GB",
    has_coordinate = "",
    kingdom = "", 
    basis_of_record = "PRESERVED_SPECIMEN",
    institution_code = "", 
    limit = "30"
) 
geodata_filter = SearchFilter(
    search_name = "Occurrence data from native trees in GB",
    media_type = "",  
    country = "GB",
    has_coordinate = "True",
    kingdom = "", 
    basis_of_record = "",
    institution_code = "",
    limit = "30"
)

species_list = Species(species_list = native_trees_list())
####################################################################

# IMAGE PREPROCESSING ##############################################

cropping = ImageDimension(
    left = 300,
    top = 400,
    right = 900,
    bottom = 1600,
    width = "",
    height = ""
)

resizing = ImageDimension(
    left = "",
    top = "",
    right = "",
    bottom = "",
    width = 1200,
    height = 2000
)


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