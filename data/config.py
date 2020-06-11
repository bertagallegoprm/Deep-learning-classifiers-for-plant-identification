from data.search import SearchFilter, Species
from data.image import ImageDimension
from data.filters import get_filter_str_or_bool, get_filter_int, get_species_list


# SEARCH FILTERS #################################################
images_filter = SearchFilter(
    search_name = get_filter_str_or_bool("search_name"),
    media_type = get_filter_str_or_bool("media_type"),  
    country = get_filter_str_or_bool("country"),
    has_coordinate = get_filter_str_or_bool("has_coordinate"),
    kingdom = get_filter_str_or_bool("kingdom"), 
    basis_of_record = get_filter_str_or_bool("basis_of_record"),
    institution_code = get_filter_str_or_bool("institution_code"), 
    limit = get_filter_int("limit")
) 
geodata_filter = SearchFilter(
    search_name = get_filter_str_or_bool("search_name"),
    media_type = get_filter_str_or_bool("media_type"),  
    country = get_filter_str_or_bool("country"),
    has_coordinate = get_filter_str_or_bool("has_coordinate"),
    kingdom = get_filter_str_or_bool("kingdom"), 
    basis_of_record = get_filter_str_or_bool("basis_of_record"),
    institution_code = get_filter_str_or_bool("institution_code"), 
    limit = get_filter_int("limit")
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
