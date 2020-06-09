from data.search import SearchFilter, Species
from data.species_list import get_species_list
from data.image import ImageDimension


# SEARCH FILTERS #################################################
images_filter = SearchFilter(
    search_name = "Herbarium specimens from British native tree species worldwide",
    media_type = "StillImage",  
    country = "",
    has_coordinate = "",
    kingdom = "", 
    basis_of_record = "PRESERVED_SPECIMEN",
    institution_code = "", 
    limit = "500"
) 
geodata_filter = SearchFilter(
    search_name = "Occurrence data from native trees in GB",
    media_type = "",  
    country = "GB",
    has_coordinate = "True",
    kingdom = "", 
    basis_of_record = "",
    institution_code = "",
    limit = "100"
)

species_list = Species(species_list = get_species_list())
####################################################################

# IMAGE PREPROCESSING ##############################################

cropping = ImageDimension(
    left = 200,
    top = 400,
    right = 950,
    bottom = 1250,
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
    batch_size = 3 
    epochs = 15                                     
    shuffle=True                                                               
    seed = 1234 