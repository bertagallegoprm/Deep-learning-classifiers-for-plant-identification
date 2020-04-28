import requests
import urllib.request
import os
import pandas as pd
import hashlib
import pdb
from species_names import native_trees_list
from image_request import 



if __name__ == "__main__":

    # 1- Customize search parameters 

    ###### Edit for a new search ##################
    # Search name
    search_name = "Occurrence data from native trees in GB"
    # Species input
    species_list = native_trees_list() 
    # Filter parameters
    media_type = ""  #StillImage
    country = "GB"
    has_coordinate = "True" # True/False
    kingdom = ""  # Plantae
    basis_of_record = ""
    institution_code = "" # K (RBG Kew)
    ###############################################

    # 2- Handle filter parameters
    filter = {"mediaType": media_type, "country": country, "hasCoordinate": has_coordinate, "kingdom": kingdom, "basisOfRecord": basis_of_record, "institutionCode": institution_code}
    filter_information = f"""
    Filters:
    mediaType: {media_type}
    country: {country}
    hasCoordinate: {has_coordinate}
    kingdom:{kingdom}
    basisOfRecord: {basis_of_record}
    institutionCode: {institution_code}
    """ 
    ## Hash the filter information + species list string to use it for naming the results file
    filter_and_species_information = filter_information + str(species_list)
    filter_hash = hashlib.md5(str.encode(filter_and_species_information)).hexdigest()     

    # 3- Get species keys (same as taxon key) 
    species_taxon_key = get_taxon_key(species_list)

    # 4- Get occurrences keys 
    species_occurrences_keys = get_occurence_key(species_taxon_key, filter)
