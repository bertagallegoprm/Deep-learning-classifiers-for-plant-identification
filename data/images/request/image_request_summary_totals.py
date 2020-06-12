import pandas as pd
from data.file_handler import create_dataframe_from_csv


if __name__ == "__main__":
    path_to_file = input("Enter file name (summary.csv, full path): ") 
    summary = create_dataframe_from_csv(path_to_file)
    total_species = int(summary.shape[0])
    print(f"Total number of species: {total_species}")
    # Total number of occurrences
    total_occurrences = int(summary[["occurrence_count"]].sum())
    print(f"Total number of occurrences: {total_occurrences}")
    # Total number of images
    total_images = int(summary[["image_count"]].sum())
    print(f"Total number of images: {total_images}")