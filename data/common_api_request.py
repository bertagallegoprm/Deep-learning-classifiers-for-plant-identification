import requests
import urllib.request
import os
import pandas as pd


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