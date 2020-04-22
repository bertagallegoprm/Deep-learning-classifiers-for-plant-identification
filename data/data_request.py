import requests
import urllib.request
import os
import pandas as pd
from species_names import native_trees_list
from storage_handler import stop_if_size
from file_handler import open_report_file

def get_taxon_key(species_list, report):
    """
    Get the GBIF taxon key for a given species name
    using its API.
    Return a dictionary for the species in the list passed as argument. 
    """
    report.write("\nSPECIES TAXON KEY\n")
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
                report.write(f"{species_name}: {species_key}.\n")
            except:
                print(f"Unable to find speciesKey for {species_name}.")
                report.write(f"Unable to find speciesKey for {species_name}.\n")
                pass
        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")
    return species_dict


def get_occurence_key(taxon_key_dict, filter, report):
    """
    Get data from GBIF using its API
    """
    report.write("\nSPECIES OCCURRENCES\n")
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
        report.write(f"{species_name}: {occurrences['count']}\n")
    return occurences_dict


def get_occurrence_image(taxon_key_dict, report):
    """
    Download image for the occurrences of the given species.
    Image naming format: 
        taxon key + occurrence key + occurrence number
        example: 2878688_1056970865_1.jpg
    """
    report.write("\nOCCURRENCE IMAGES\n")
    base_url = "https://api.gbif.org/v1/"
    # "institutionCode": "K"
    filter = {"mediaType": "StillImage", "country": "GB", "hasCoordinate": "True", "kingdom": "Plantae", "basisOfRecord": "PRESERVED_SPECIMEN"}
    for species_name, taxon_key in taxon_key_dict.items():
        filter["taxonKey"]=taxon_key
        response = requests.get(f"{base_url}occurrence/search", params=filter)
        if response.status_code == 200:
            occurrences = response.json()
            for occurrence_no in range(0, len(occurrences)):
                try:
                    occurrence_url = occurrences["results"][occurrence_no]["media"][0]["identifier"]
                    occurrence_key = occurrences["results"][occurrence_no]["key"]
                    folder = "images"
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    image_path = f"{folder}/{taxon_key}_{occurrence_key}_{occurrence_no}.jpg"
                    urllib.request.urlretrieve(occurrence_url, image_path) 
                    stop_if_size(10)
                except:
                    print(f"{species_name}: Occurrence {occurrence_key} not downloaded.")                
                    report.write(f"{species_name}: {occurrence_key} not downloaded.\n")
        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")                                                     


def species_without_speciesKey(species_list,taxon_key_dict):
    species_with_taxon_keys = list(taxon_key_dict.keys())
    diff = list(set(species_list) - set(species_with_taxon_keys))
    if len(diff)==0:
        print("All species have a speciesKey.")
    else:
        print(f"Species without a speciesKey:{diff}")
    return diff



if __name__ == "__main__":
    # Open report file
    report = open_report_file()
    report.write("DATA REQUEST FOR SPECIES IN GBIF\n")

    # Write filter  
    media_type = "StillImage"  
    country = "GB"
    has_coordinate = "True"
    kingdom = "Plantae"
    basis_of_record = "PRESERVED_SPECIMEN"
    filter = {"mediaType": media_type, "country": country, "hasCoordinate": has_coordinate, "kingdom": kingdom, "basisOfRecord": basis_of_record}
    report.write(f"""
    Filters:
    mediaType: {media_type},
    country = {country}
    hasCoordinate = {has_coordinate}
    kingdom = {kingdom}
    basisOfRecord = {basis_of_record}
    """)

    # Input species 
    species_list = native_trees_list()
    

    # Get GBIF keys for the given species
    taxon_key_dict = get_taxon_key(species_list[:5], report)
    report.write(f"Species list and key:{str(taxon_key_dict)}\n")
    report.write(f"Species without a speciesKey: {str(species_without_speciesKey(species_list,taxon_key_dict))}\n")


    # Apply filter to find species occurrences
    occurrences_key = get_occurence_key(taxon_key_dict, filter, report)
    report.write(f"Occurrences by species: {str(occurrences_key)}\n")
    #occurrence_key = "2013665032"
    
    # Download images for species occurrences
    #get_occurrence_image(taxon_key_dict, report)
    
    # Close text file
    report.close()
    
    # Get dataframe with results
    column_names = ["species_name", "taxon_key", "occurrence_key"]
    df = pd.DataFrame(columns = column_names) 
    for species_name, occurrences in occurrences_key.items():      
        for i in range(0,(len(occurrences)-1)):
            taxon_key = taxon_key_dict[species_name]
            data_in_row = []
            data_in_row.extend([species_name,taxon_key, occurrences[i]])         
            new_row = pd.DataFrame([data_in_row], columns=column_names)
            df = df.append(new_row, ignore_index=True)
    print(df)

