import requests
import urllib.request
import os
import pandas as pd
from species_names import native_trees_list
from storage_handler import stop_if_size
from file_handler import request_result_to_csv

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
                print(f"Unable to find speciesKey for {species_name}.")
                pass
        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")
    return species_dict


def get_occurence_key(taxon_key_dict, filter):
    """
    Get data from GBIF using its API
    """
    base_url = "https://api.gbif.org/v1/"
    # "institutionCode": "K"
    occurences_dict = {}
    for species_name, taxon_key in taxon_key_dict.items():
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
        print(f"Number of occurrences for {species_name}: {occurrences['count']}")
    return occurences_dict


def get_occurrence_image(taxon_key_dict, filter):
    """
    Download image for the occurrences of the given species.
    Image naming format: 
        taxon key + occurrence key + occurrence number
        example: 2878688_1056970865_1.jpg
    """
    base_url = "https://api.gbif.org/v1/"
    has_image_dict = {}
    occurrences_key = get_occurence_key(taxon_key_dict, filter)
    for species_name, occurrences in occurrences_key.items(): 
        taxon_key = taxon_key_dict[species_name]     
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
                        image_path = f"{folder}/{taxon_key}_{occurrence_key}_{occurrence}.jpg"
                        urllib.request.urlretrieve(occurrence_url, image_path) 
                        has_image_dict[occurrence_key]= "1"
                        stop_if_size(10)
                    except:
                        print(f"{species_name}: Occurrence {occurrence_key} not downloaded.")                
                        has_image_dict[occurrence_key]= "x"
                except:
                        print(f"{species_name}: Occurrence {occurrence_key} does not have a valid url.")
                        has_image_dict[occurrence_key]= "0"
                #except:
                #    print(f"{species_name}: Unable to get occurrence key.")
            elif response.status_code == 404:
                print('Error 404: Page not found.')
            else:
                print("Error. Undetermined status code.")  
    return has_image_dict                                                   


def species_without_speciesKey(species_list,taxon_key_dict):
    species_with_taxon_keys = list(taxon_key_dict.keys())
    diff = list(set(species_list) - set(species_with_taxon_keys))
    if len(diff)==0:
        print("All species have a speciesKey.")
    else:
        print(f"Species without a speciesKey:{diff}")
    return diff


def get_results_table(species_list, filter):
    """
    Return a data frame with the 
    """
    taxon_key_dict = get_taxon_key(species_list[:3])
    occurrences_key = get_occurence_key(taxon_key_dict, filter)
    occurrence_has_image = get_occurrence_image(taxon_key_dict, filter)
    column_names = ["species_name", "taxon_key", "occurrence_key", "has_image"]
    df = pd.DataFrame(columns = column_names) 
    for species_name, occurrences in occurrences_key.items():      
        for occurrence in range(0,(len(occurrences))):
            taxon_key = taxon_key_dict[species_name]
            data_in_row = []
            data_in_row.extend([species_name,taxon_key, occurrences[occurrence], ""])         
            new_row = pd.DataFrame([data_in_row], columns=column_names)
            df = df.append(new_row, ignore_index = True)
    for occurence_key, has_image in occurrence_has_image.items():
        df.loc[df["occurrence_key"] == occurence_key, ["has_image"]] = has_image
    df.sort_values(by=["taxon_key", "occurrence_key"])
    return df





if __name__ == "__main__":

    # 1- Handle filter information  

    ###### Edit for a different search ############
    media_type = "StillImage"  
    country = "GB"
    has_coordinate = "False"
    kingdom = "Plantae"
    basis_of_record = "PRESERVED_SPECIMEN"
    #############################################

    filter = {"mediaType": media_type, "country": country, "hasCoordinate": has_coordinate, "kingdom": kingdom, "basisOfRecord": basis_of_record}
    filter_information = f"""
    Filters:
    mediaType: {media_type},
    country: {country},
    hasCoordinate: {has_coordinate},
    kingdom:{kingdom},
    basisOfRecord: {basis_of_record}.
    """
    print(filter_information)

    ## Hash the filter information string to use it for naming the results file
    filter_hash = hashlib.md5(str.encode(filter_information)).hexdigest()

    # Input species 
    species_list = native_trees_list()
    

    # Get GBIF keys for the given species
    #taxon_key_dict = get_taxon_key(species_list[:3])


    # Apply filter to find species occurrences
    #occurrences_key = get_occurence_key(taxon_key_dict, filter)
    #occurrence_key = "2013665032"
    
    # Download images for species occurrences
    #occurrence_has_image = get_occurrence_image(taxon_key_dict, filter)
    
    result_df = get_results_table(species_list, filter)
    request_result_to_csv(result_df, filter_hash)

