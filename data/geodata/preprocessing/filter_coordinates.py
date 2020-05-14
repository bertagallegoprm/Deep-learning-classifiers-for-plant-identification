import pandas as pd
from data.search import filter_hash
from data.config import geodata_filter, species_list
from data.file_handler import create_dataframe_from_csv, column_to_list


def which_none(column_as_list):
    """
    Return the position of elements in a list that are None
    or inform if all elements are None 
    or there are not None values. 
    """
    if all(column_as_list) is None:
        print("All items are None in list.") # then column should be dropped
        return
    else:
        none_items = [i for i, val in enumerate(column_as_list) if val == None]
        if not none_items:
            print("There are not None values in list.")
            return 
        else:
            print(f"None items: {none_items}") # then rows should be dropped
            return none_items


def which_low_precision(column_as_list, max_uncertainty):
    """
    Return the position of elements in a list 
    for uncertainty greater than 
    """
    unprecise_occurrences = [i for i, val in enumerate(column_as_list) if val > max_uncertainty] 
    print(f"{len(unprecise_occurrences)} occurrences have uncertainty above {max_uncertainty} m.")
    return unprecise_occurrences
    

def drop_none_rows(coordinates_df, rows):
    """
    Drop rows in the dataframe that have None values.
    """
    filtered = coordinates_df
    if rows is not None:
        for row in rows:
            filtered = filtered.drop(row)
            print(f"Row {row} removed from data set")
        return filtered
    else:
        print("No rows to remove.")


if __name__ == "__main__":

    # Open CSV file with the occurrences data.
    base_path = "data/geodata/request_reports/"
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
                                   "uncertainty": uncertainty
                                  }) 

    # Find empty coordinates
    print("Filter latitude:")
    drop_none_rows(coordinates_df, which_none(latitude))
    print("Filter longitude:")
    drop_none_rows(coordinates_df, which_none(longitude))
    print("Filter uncertainty:")
    drop_none_rows(coordinates_df, which_none(uncertainty))


    # Low precission (10 000 m)
    max_uncertainty = 10000
    print(which_low_precision(uncertainty, max_uncertainty))
    filtered_df = drop_none_rows(coordinates_df, which_low_precision(uncertainty, max_uncertainty) )
