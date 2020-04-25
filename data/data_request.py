import requests
import urllib.request
import os
import pandas as pd
import hashlib
from species_names import native_trees_list
from storage_handler import stop_if_size
from file_handler import request_result_to_csv, open_filter_report

def get_taxon_key(species_list):
    """
    Get the GBIF taxon key for a given species name
    using its API.
    Return a dictionary for the species in the list passed as argument. 
    """
    base_url = "https://api.gbif.org/v1/"
    resource = "species/match"
    parameter = "name"
    species_dict = {}
    for species_name in species_list:
        response = requests.get(f"{base_url}{resource}?{parameter}={species_name}")
        if response.status_code == 200:
            try:
                species = response.json()
                species_key = species["speciesKey"]
                species_dict[species_name] = species_key
            except:
                #print(f"Unable to find speciesKey for {species_name}.")
                pass
        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")
    return species_dict


def get_occurence_key(species_taxon_key, filter):
    """
    Get data from GBIF using its API
    """
    base_url = "https://api.gbif.org/v1/"
    occurences_dict = {}
    for species_name, taxon_key in species_taxon_key.items():
        filter["taxonKey"]=taxon_key
        response = requests.get(f"{base_url}occurrence/search", params=filter)
        if response.status_code == 200:
            occurrences = response.json()
            occurrences_results = occurrences.get("results",{})
            species_occurence_dict = {}
            for occurrence_no in range(0, len(occurrences_results)):
                occurences_key = occurrences_results[occurrence_no].get("key")
                species_occurence_dict[occurrence_no] = occurences_key        
        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")
        occurences_dict[species_name]=species_occurence_dict
        #print(f"Number of occurrences for {species_name}: {occurrences['count']}")
    return occurences_dict


def get_occurrence_image(species_occurrences_keys, filter):
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
        for occurrence in range(0,(len(occurrences))):          
            occurrence_key = occurrences[occurrence]                
            filter["gbifID"]=occurrence_key
            response = requests.get(f"{base_url}occurrence/search", params=filter)
            if response.status_code == 200:
                occurrence_result = response.json()
                try:
                    occurrence_url = occurrence_result["results"][0]["media"][0]["identifier"]                  
                    try:
                        # Create folder where to store images
                        folder = "images"
                        if not os.path.exists(folder):
                            os.makedirs(folder)            
                        # Name and download file   
                        image_path = f"{folder}/{taxon_key}_{occurrence_key}.jpg"
                        urllib.request.urlretrieve(occurrence_url, image_path) 
                        has_image_dict[occurrence_key]= "1"
                        stop_if_size(10)
                    except:
                        #print(f"{species_name}: Occurrence {occurrence_key} not downloaded.")                
                        has_image_dict[occurrence_key]= "0"
                except:
                        #print(f"{species_name}: Occurrence {occurrence_key} does not have a valid url.")
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

    ###### Edit for a new search ##################
    # Search name
    search_name = "Herbarium specimens images from native trees in GB"
    # Species input
    species_list = native_trees_list() 
    # Filter parameters
    media_type = "StillImage"  
    country = "GB"
    has_coordinate = "" # True/False
    kingdom = ""  # Plantae
    basis_of_record = "PRESERVED_SPECIMEN"
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

    # 3- Get species keys (same as taxon key) 
    species_taxon_key = get_taxon_key(species_list)
    ## Check if all species entered have a taxon key
    species_without_speciesKey(species_list,species_taxon_key)

    # 4- Get occurrences keys 
    species_occurrences_keys = get_occurence_key(species_taxon_key, filter)

    # 5- Get images from occurrences
    occurrence_has_image = get_occurrence_image(species_occurrences_keys, filter)

    # 6-  Save results information for the applied filter
    ## Hash the filter information + species list string to use it for naming the results file
    filter_and_species_information = filter_information + str(species_list)
    filter_hash = hashlib.md5(str.encode(filter_and_species_information)).hexdigest()
    ## Save results summary to csv file
    result_df = get_results_table(species_occurrences_keys, occurrence_has_image)
    request_result_to_csv(result_df, filter_hash)
    ## Save filter and species information to text file
    save_filter = open_filter_report(filter_hash)
    save_filter.write(f"{search_name}\n")
    save_filter.write(f"{str(filter_information)}\n\n")
    save_filter.write("Input species list:\n")
    for species in species_list:
        save_filter.write(f"{species}\n")
    save_filter.close()
