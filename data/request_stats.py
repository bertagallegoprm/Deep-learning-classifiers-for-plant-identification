import pandas as pd
from file_handler import read_csv_name, create_dataframe_from_csv


if __name__ == "__main__":

    # Open request_results into a data frame
    request_results = create_dataframe_from_csv(read_csv_name())

    # Table with Species name : Occurrences/species : Images/species
    ## List of species
    ## Number of occurences by species
    ## Number of images per species


    # Total number of different species
    # Total number of occurrences
    # Total number of images