
class ImageDimension(object):
    """
    Parameters related to image preprocessing.
    """
    def __init__(self, left, top, right, bottom, width, height):
        self.left = left
        self.top = top  
        self.right = right
        self.bottom = bottom 
        self.width = width
        self.height = height

    def coordinates(self):
        """
        Return a list with coordinates for area selection.
        """
        return (self.left, self.top, self.right, self.bottom)

    def image_size(self):
        """
        Return a list with width and height for area selection.
        """
        return (self.width, self.height)

         


class Species(object):
    """
    Species list used in the search.
    """
    def __init__(self, species_list):
        self.species_list = species_list


def filter_hash(search_filter, species_list):
    """
    Return an alphanumeric search identifier by combining:
    - Search filter.
    - Species list.
    """
    filter_information = search_filter.filter_information()
    filter_and_species_information = filter_information + str(species_list)
    return hashlib.md5(str.encode(filter_and_species_information)).hexdigest()