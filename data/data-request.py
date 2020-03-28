import requests


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


def get_data():
    """
    Get data from GBIF using its API
    """
    base_url = "https://api.gbif.org/v1/"
    # "institutionCode": "K"
    filter = {"mediaType": "StillImage", "country": "GB", "hasCoordinate": "True", "kingdom": "Plantae", "basisOfRecord": "PRESERVED_SPECIMEN", "taxonKey": "328"}
    response = requests.get(f"{base_url}occurrence/search", params=filter)
    if response.status_code == 200:
        #print(response.headers["Date"])
        occurrences = response.json()
        print(f"Keys: {occurrences.keys()}")
        print(f"Results: {occurrences['results']}")
        print(f"Number of occurrences: {occurrences['count']}")
    elif response.status_code == 404:
        print('404: Page not found.')
    else:
        print(":(")

if __name__ == "__main__":
    species_list = ("quercus robur", "taxus baccata")
    print(get_taxon_key(species_list))
    #get_data()