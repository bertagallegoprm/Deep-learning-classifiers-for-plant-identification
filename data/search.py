import hashlib


class SearchFilter(object):
    """
    Search parameters in GBIF API.
    """
    def __init__(self, search_name, media_type, country, has_coordinate, kingdom, basis_of_record, institution_code):
        self.search_name = search_name
        self.media_type = media_type  
        self.country = country
        self.has_coordinate = has_coordinate # True/False
        self.kingdom = kingdom  # Plantae
        self.basis_of_record = basis_of_record
        self.institution_code = institution_code # K (RBG Kew)

    def filter_information(self):
        """
        Return the filter information to add to the filter text file
        and to form the filter identifier.
        """
        return f"""
    Filters:
    mediaType: {self.media_type}
    country: {self.country}
    hasCoordinate: {self.has_coordinate}
    kingdom:{self.kingdom}
    basisOfRecord: {self.basis_of_record}
    institutionCode: {self.institution_code}
        """ 


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