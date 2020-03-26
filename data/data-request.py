import requests


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
    get_data()