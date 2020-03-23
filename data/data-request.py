import requests

def get_data():
    """
    Get data from GBIF using its API
    """
    response = requests.get(
        "https://api.gbif.org/v1/occurrence/search?year=1800,1899",
        params={"q":})
    if response.status_code == 200:
        #print(response.headers["Date"])
        print(response.json())
    elif response.status_code == 404:
        print('404: Page not found.')
    else:
        print(":(")

if __name__ == "__main__":
    get_data()