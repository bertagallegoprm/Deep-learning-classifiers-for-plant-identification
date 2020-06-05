import pandas as pd
import os
import matplotlib.pyplot as plt
from data.search import filter_hash
from data.config import geodata_filter, species_list
from data.file_handler import create_dataframe_from_csv, column_to_list
from data.geodata.plot_coordinates import plot_occurrences_map, plot_coordinates_frequency
from data.geodata.plot_coordinates_per_species import plot_coordenates_count, unique, get_species_list, get_occurrence_count

def which_none(column_as_list):
    """
    Return the position of elements in a list that are None
    or inform if all elements are None 
    or there are not None values. 
    """
    series = pd.Series(column_as_list)
    series_none = series.isna()
    if all(series_none):
        print("All items are None in list.") # then column should be dropped
        return
    else:
        index_list = []
        for i in range(0,len(series_none)):
            if series_none[i]:
                index_list.append(i)
            else:
                continue
        if len(index_list)==0:
            print("There are not None values in list.")
            return 
        else:
            print(f"{len(index_list)} None items.") # then rows should be dropped
            return index_list


def which_low_precision(column_as_list, max_uncertainty):
    """
    Return the position of elements in a list 
    for uncertainty greater than 
    """
    unprecise_occurrences = [i for i, val in enumerate(column_as_list) if val > max_uncertainty] 
    print(f"{len(unprecise_occurrences)} occurrences have uncertainty above {max_uncertainty} m.")
    return unprecise_occurrences
    

def drop_rows_by_index(coordinates_df, rows):
    """
    Drop rows in the dataframe that have None values.
    """
    filtered_df = coordinates_df
    if rows is not None:
        for row in rows:
            filtered_df = filtered_df.drop(row)
            print(f"Row {row} removed from data set.")
        return filtered_df
    else:
        print("No rows to remove.")
        return coordinates_df


def drop_duplicate_coordinates(coordinates_df):
    """
    Return a dataframe with no duplicates coordinates 
    for the same species name.
    """
    no_duplicates = coordinates_df.drop_duplicates(["species_name","longitude", "latitude"])
    print(f"Removed {len(coordinates_df)-len(no_duplicates)} duplicated rows.")
    return no_duplicates





if __name__ == "__main__":

    # Open CSV file with the occurrences data.
    base_path = "data/geodata/request/outputs/"
    filter_hash = filter_hash(geodata_filter, species_list.species_list)
    csv_file_name = filter_hash + "_geodata.csv"
    df = create_dataframe_from_csv(base_path+csv_file_name)

    # Extract list with coordinates
    latitude = column_to_list(df, "decimal_latitude")
    longitude = column_to_list(df, "decimal_longitude")
    species_name = column_to_list(df, "species_name")
    uncertainty = column_to_list(df, "coordinate_uncertainty")

    coordinates_df = pd.DataFrame({"species_name": species_name, 
                                   "latitude": latitude,
                                   "longitude": longitude,
                                   "coordinate_uncertainty": uncertainty
                                  }) 

    # Find empty coordinates
    filtered_df = coordinates_df
    print("Filter latitude:")
    filtered_df = drop_rows_by_index(filtered_df, which_none(latitude))
    print("Filter longitude:")
    filtered_df = drop_rows_by_index(filtered_df, which_none(longitude))
    print("Filter uncertainty:")
    filtered_df = drop_rows_by_index(filtered_df, which_none(uncertainty))

    # Low precission (10 000 m)
    max_uncertainty = 10000
    which_low_precision(uncertainty, max_uncertainty)
    filtered_df = drop_rows_by_index(filtered_df, which_low_precision(uncertainty, max_uncertainty) )

    # Duplicates
    filtered_df = drop_duplicate_coordinates(filtered_df)

    # Filtered rows
    print(f"{len(coordinates_df)-len(filtered_df)} rows removed from geodata data set.")

    # Save filtered CSV
    save_dir = "data/geodata/preprocessing/outputs"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    csv_file_name = os.path.join(save_dir, "filtered_coordinates.csv")
    filtered_df.to_csv(csv_file_name, sep = ",", header = True, index = None, encoding="utf-8")
    print(f"{csv_file_name} created.")

    # Plot filtered occurrences location
    destination_path = os.path.join(save_dir, "filtered_occurrences_per_class.png")
    shape_file = "data/geodata/uk_maps/GBR_adm0.shp" # UK map
    plot_occurrences_map(filtered_df, shape_file, destination_path)

    # Plot occurrence count
    path_to_plot = os.path.join(save_dir, "filtered_distribution_map.png")
    geodata = filtered_df
    species_name = unique(get_species_list(geodata))
    occurrence_count = get_occurrence_count(get_species_list(geodata))   
    plot_coordenates_count(occurrence_count, species_name, path_to_plot)

    # Plot coordinates histogram
    destination_path = os.path.join(save_dir, "filtered_histogram.png")
    plot_coordinates_frequency(coordinates_df, destination_path)

