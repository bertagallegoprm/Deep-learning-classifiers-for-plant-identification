import requests
import urllib.request
import os
import pandas as pd
import hashlib
import pdb
from data.species_names import native_trees_list
from data.storage_handler import stop_if_size
from data.file_handler import image_result_to_csv, open_filter_report
from data.common_api_request import get_taxon_key, get_occurence_key
from data.config import images_filter, species_list
from data.search import filter_hash


def get_occurrence_image(species_occurrences_keys, folder):
    """
    Download image for the occurrences of the given species.
    Image naming format: 
        taxon key + occurrence key + occurrence number
        example: 2878688_1056970865_1.jpg
    """
    base_url = "https://api.gbif.org/v1/"
    has_image_dict = {}
    for species_name, occurrences in species_occurrences_keys.items(): 
        taxon_key = species_taxon_key[species_name] 
        species_words = species_name.split(" ")
        species_class = '_'.join(species_words)   
        current_folder = folder+"/"+species_class 
        for occurrence in range(0,(len(occurrences))):          
            occurrence_key = occurrences[occurrence]                
            response = requests.get(f"{base_url}occurrence/{occurrence_key}")
            if response.status_code == 200:
                occurrence_result = response.json()
                try:
                    occurrence_url = occurrence_result["media"][0]["identifier"] 
                    try:
                        # Create folder where to store images
                        if not os.path.exists(current_folder):
                            os.makedirs(current_folder)            
                        # Name and download file 
                        image_path = f"{current_folder}/{species_class}_{occurrence_key}.jpg"
                        urllib.request.urlretrieve(occurrence_url, image_path) 
                        has_image_dict[occurrence_key]= "1"
                        stop_if_size(10)
                    except:
                        # urlretrieve fails              
                        has_image_dict[occurrence_key]= "0"
                except:
                        # parsing request result fails
                        has_image_dict[occurrence_key]= "0"
            elif response.status_code == 404:
                print('Error 404: Page not found.')
            else:
                print("Error. Undetermined status code.")  
    return has_image_dict                                                   


def species_without_speciesKey(species_list,species_taxon_key):
    species_with_taxon_keys = list(species_taxon_key.keys())
    diff = list(set(species_list) - set(species_with_taxon_keys))
    if len(diff)==0:
        print("All species have a speciesKey.")
    else:
        print(f"Species without a speciesKey:{diff}")
    return diff


def get_results_table(species_occurrences_keys, occurrence_has_image):
    """
    Return a data frame with:
    - Species names.
    - Species keys (speciesKey/taxonKey)
    - Occurrences keys (key/gbifID)
    - Information about if the image has been downloaded (0 or 1)
    """   
    column_names = ["species_name", "taxon_key", "occurrence_key", "has_image"]
    df = pd.DataFrame(columns = column_names) 
    for species_name, occurrences in species_occurrences_keys.items():      
        for occurrence in range(0,(len(occurrences))):
            taxon_key = species_taxon_key[species_name]
            data_in_row = []
            data_in_row.extend([species_name,taxon_key, occurrences[occurrence], ""])         
            new_row = pd.DataFrame([data_in_row], columns=column_names)
            df = df.append(new_row, ignore_index = True)
    for occurence_key, has_image in occurrence_has_image.items():
        df.loc[df["occurrence_key"] == occurence_key, ["has_image"]] = has_image
    df.sort_values(by=["taxon_key", "occurrence_key"])
    return df


if __name__ == "__main__":

    # 1- Customize search parameters 
    # Species input
    species_list = species_list.species_list
    ###### Edit in config file   ##################
    # Search name
    search_name = images_filter.search_name 
    # Filter parameters
    media_type =  images_filter.media_type
    country = images_filter.country
    has_coordinate = images_filter.has_coordinate 
    kingdom = images_filter.kingdom  
    basis_of_record = images_filter.basis_of_record
    institution_code = images_filter.institution_code
    ###############################################

    # 2- Handle filter parameters
    filter = {"mediaType": media_type, "country": country, "hasCoordinate": has_coordinate, "kingdom": kingdom, "basisOfRecord": basis_of_record, "institutionCode": institution_code}
    filter_information = images_filter.filter_information()
    ## Hash the filter information + species list string to use it for naming the results file
    filter_hash = filter_hash(images_filter, species_list)     
    print(f"Starting request '{search_name}' identified by: {filter_hash}.")

    # 3- Get species keys (same as taxon key) 
    species_taxon_key = get_taxon_key(species_list)
    ## Check if all species entered have a taxon key
    species_without_speciesKey(species_list,species_taxon_key)

    # 4- Get occurrences keys 
    species_occurrences_keys = get_occurence_key(species_taxon_key, filter)

    # 5- Get images from occurrences
    folder = "data/images/image_request/"+filter_hash + "_images"
    occurrence_has_image = get_occurrence_image(species_occurrences_keys, folder)

    # 6-  Save results information for the applied filter
    ## Save results summary to csv file
    result_df = get_results_table(species_occurrences_keys, occurrence_has_image)
    image_result_to_csv(result_df, filter_hash)
    ## Save filter and species information to text file
    save_filter = open_filter_report(filter_hash)
    save_filter.write(f"{search_name}\n")
    save_filter.write(f"{str(filter_information)}\n\n")
    save_filter.write("Input species list:\n")
    for species in species_list:
        save_filter.write(f"{species}\n")
    save_filter.close()
