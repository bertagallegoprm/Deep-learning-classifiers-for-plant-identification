import requests
import urllib.request
import os


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
            species = response.json()
            species_key = species["speciesKey"]
            species_dict[species_name] = species_key
        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")
    return species_dict


def get_occurence_key(taxon_key_dict):
    """
    Get data from GBIF using its API
    """
    base_url = "https://api.gbif.org/v1/"
    # "institutionCode": "K"
    filter = {"mediaType": "StillImage", "country": "GB", "hasCoordinate": "True", "kingdom": "Plantae", "basisOfRecord": "PRESERVED_SPECIMEN"}
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


def get_occurrence_image(taxon_key_dict):
    """
    Download image for the occurrences of the given species.
    Image naming format: 
        taxon key + occurrence key + occurrence number
        example: 2878688_1056970865_1.jpg
    """
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
                except:
                    print(f"Occurrence {occurrence_key} not downloaded for {species_name}")

        elif response.status_code == 404:
            print('Error 404: Page not found.')
        else:
            print("Error. Undetermined status code.")                                                     


if __name__ == "__main__":
    species_list = ("quercus robur", "taxus baccata")
    taxon_key_dict = get_taxon_key(species_list)
    print(taxon_key_dict)
    print(get_occurence_key(taxon_key_dict))
    #occurrence_key = "2013665032"
    get_occurrence_image(taxon_key_dict)