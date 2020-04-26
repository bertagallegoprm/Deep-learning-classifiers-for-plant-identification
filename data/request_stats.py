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

def save_summary_as_csv(path_to_file):
    """
    Given the path to the CSV file with the results of the request
    creates a summary as a data frame object using get_summary_of_results()
    and saves it to the request_reports folders as a CSV.
    """
    summary = get_summary_of_results(path_to_file)
    file_name = path_to_file.split("/")[-1]
    filter_hash = file_name.split("_")[0]
    summary_file_name = "request_reports/" + filter_hash + "_summary.csv"
    summary.to_csv(summary_file_name)
    print(f"File {summary_file_name} created.")

if __name__ == "__main__":

    save_summary_as_csv(read_csv_name())

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