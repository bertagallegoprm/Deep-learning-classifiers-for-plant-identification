import pandas as pd
from file_handler import read_csv_name, create_dataframe_from_csv

def get_summary_of_results(path_to_file):
    """
    Given the path to the CSV file with the results of the request:
    Return a data frame with a summary of
    - Number of occurrences species
    - Number of images per species
    """
    request_results = create_dataframe_from_csv(path_to_file)
    occurrences_per_taxon = request_results.groupby("species_name")["taxon_key"].value_counts().reset_index(name="occurrence_count")
    images_per_taxon = request_results[request_results.has_image == 1].groupby("species_name")["taxon_key"].value_counts().reset_index(name="image_count")
    images_per_taxon = images_per_taxon.iloc[:,-1]
    return occurrences_per_taxon.join(images_per_taxon)

if __name__ == "__main__":

    # Open request_results into a data frame
    path_to_file = read_csv_name()
    summary = get_summary_of_results(path_to_file)

    summary = get_summary_of_results(request_results)
    # Total number of different species
    total_species = int(summary.shape[0])
    print(f"Total number of species: {total_species}")
    # Total number of occurrences
    total_occurrences = int(summary[["occurrence_count"]].sum())
    print(f"Total number of occurrences: {total_occurrences}")
    # Total number of images
    total_images = int(summary[["image_count"]].sum())
    print(f"Total number of images: {total_occurrences}")