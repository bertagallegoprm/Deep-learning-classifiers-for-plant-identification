import requests
import urllib.request
import os
import pandas as pd
import hashlib
import pdb
from data.common_api_request import get_taxon_key, get_occurence_key
from data.config import geodata_filter, species_list
from data.search import filter_hash

def get_occurrence_data(species_occurrences_keys):
    """
    Given the species occurrence key
    return a data frame with a series of geographical parameters
    associated to the occurrence.
    """
    base_url = "https://api.gbif.org/v1/"
    column_names = ["species_name", "taxon_key", "occurrence_key", "basis_of_record", "institution_code","coordinate_system", "decimal_longitude", "decimal_latitude", "coordinate_uncertainty","elevation", "date", "issues"]
    df = pd.DataFrame(columns = column_names) 
    count_species = 1
    for species_name, occurrences in species_occurrences_keys.items(): 
        taxon_key = species_taxon_key[species_name]     
        for occurrence in range(0,(len(occurrences))):          
            occurrence_key = occurrences[occurrence]                
            response = requests.get(f"{base_url}occurrence/{occurrence_key}")
            if response.status_code == 200:
                occurrence_result = response.json()
                try:
                    basis_of_record = occurrence_result["basisOfRecord"]
                except:
                    basis_of_record = ""
                    pass
                try:
                    institution_code = occurrence_result["institutionCode"]
                except:
                    institution_code = ""
                    pass
                try:
                    coordinate_system = occurrence_result["geodeticDatum"]
                except:
                    coordinate_system = ""
                    pass
                try:
                    decimal_longitude = occurrence_result["decimalLongitude"]
                except:
                    decimal_longitude = ""
                    pass
                try:
                    decimal_latitude = occurrence_result["decimalLatitude"]
                except:
                    decimal_latitude = ""
                    pass
                try:
                    coordinate_uncertainty = occurrence_result["coordinateUncertaintyInMeters"]
                except:
                    coordinate_uncertainty = ""
                    pass
                try:
                    elevation = occurrence_result["elevation"]
                except:
                    elevation = ""
                    pass
                try:
                    date = occurrence_result["eventDate"]
                except:
                    date = ""
                    pass
                try:
                    issues = occurrence_result["issues"]
                except:
                    issues = ""
                    pass
                data_in_row = []
                data_in_row.extend([species_name,taxon_key, occurrences[occurrence], basis_of_record,institution_code, coordinate_system, decimal_longitude, decimal_latitude, coordinate_uncertainty, elevation, date, issues])         
                new_row = pd.DataFrame([data_in_row], columns=column_names)
                df = df.append(new_row, ignore_index = True)
            elif response.status_code == 404:
                print('Error 404: Page not found.')
            else:
                print("Error. Undetermined status code.")  
    return df


if __name__ == "__main__":

    # 1- Import search parameters 
    # Species input
    species_list = species_list.species_list 
    # Search name
    search_name = geodata_filter.search_name 
    # Filter parameters
    media_type =  geodata_filter.media_type
    country = geodata_filter.country
    has_coordinate = geodata_filter.has_coordinate 
    kingdom = geodata_filter.kingdom  
    basis_of_record = geodata_filter.basis_of_record
    institution_code = geodata_filter.institution_code
    limit = geodata_filter.limit
    ###############################################

    # 2- Handle filter parameters
    filter = {"mediaType": media_type, "country": country, "hasCoordinate": has_coordinate, "kingdom": kingdom, "basisOfRecord": basis_of_record, "institutionCode": institution_code, "limit":limit}
    filter_information = geodata_filter.filter_information()
    ## Hash the filter information + species list string to use it for naming the results file
    filter_hash = filter_hash(geodata_filter, species_list)     
    print(f"Starting request '{search_name}' identified by: {filter_hash}.")    

    # 3- Save filter and species information to text file
    folder = "data/geodata/request/outputs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    text_file_name = f"{folder}/{filter_hash}_geodata_filter.txt"
    save_filter = open(text_file_name, "w")
    save_filter.write(f"{search_name}\n")
    save_filter.write(f"{str(filter_information)}\n")
    save_filter.write(f"Records download limit: {limit}\n\n")
    save_filter.write("Input species list:\n")
    for species in species_list:
        save_filter.write(f"{species}\n")
    save_filter.close()

    # 4- Get species keys (same as taxon key) 
    species_taxon_key = get_taxon_key(species_list)

    # 5- Get occurrences keys 
    species_occurrences_keys = get_occurence_key(species_taxon_key, filter)

    # 6- Get occurrence data into a CSV file
    save_dir = "data/geodata/request/outputs"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    occurrence_data_table = get_occurrence_data(species_occurrences_keys)
    csv_file_name = "data/geodata/request/outputs/"+filter_hash+"_geodata.csv" 
    occurrence_data_table.to_csv(csv_file_name, sep = ",", header = True, index = None, encoding="utf-8")