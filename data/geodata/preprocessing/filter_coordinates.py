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
        return "All items are None in list."
    else:
        none_items = [i for i, val in enumerate(column_as_list) if val == None]
        if not none_items:
            return "There are not None values in list."
        else:
            print(f"None items: {none_items}")
            return none_items


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
    uncertainity = column_to_list(df, "coordinate_uncertainty")

    coordinates_df = pd.DataFrame({"species_name": species_name, 
                                   "latitude": latitude,
                                   "longitude": longitude,
                                   "uncertainity": uncertainity
                                  }) 

    # Find empty coordinates
    print(which_none(latitude))
    print(which_none(longitude))
    print(which_none(uncertainity))

    # Low precission (100 km)

