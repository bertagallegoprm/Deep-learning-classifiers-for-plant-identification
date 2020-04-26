import pandas as pd
from file_handler import read_csv_name, create_dataframe_from_csv


if __name__ == "__main__":

    # Open request_results into a data frame
    #request_results = create_dataframe_from_csv(read_csv_name())
    request_results = create_dataframe_from_csv("/home/berta/Repos/tfm/data/request_reports/ef1a27f6cfc1b4755c1c380f9a54ee9c_request_results.csv")

    # Table with Species name : Occurrences/species : Images/species
    ## List of species
    unique_taxon = request_results[["species_name", "taxon_key"]].drop_duplicates(["species_name", "taxon_key"])
    print(unique_taxon)
    ## Number of occurences by species
    occurrences_per_taxon = request_results.groupby("species_name")["taxon_key"].value_counts().reset_index(name="occurrence_count")
    ## Number of images per species
    images_per_taxon = request_results[request_results.has_image == 1].groupby("species_name")["taxon_key"].value_counts().reset_index(name="image_count")
    images_per_taxon = images_per_taxon.iloc[:,-1]


    # Total number of different species
    # Total number of occurrences
    # Total number of images