import pandas as pd 
import argparse
import sys


def get_df_from_csv():
    """
    Return a data frame object
    given a path to a CSV
    """
    parser = argparse.ArgumentParser(prog = "Get data request filter", usage = "Given a CSV with filter parameters, extract their values individually. Example: python3 -m data.filter data/sample_inputs/image_filter.csv")
    parser.add_argument('src_path', type=str,  help = "path to the CSV file with the species names. Example: data/inputs/species_list.csv")
    arg = parser.parse_args()
    src_path = arg.src_path
    df = pd.read_csv(""+src_path+"", sep=",", encoding="utf-8")
    return df.where(df.notnull(), None)


def get_species_list():
    """Return a list of species"""
    df = get_df_from_csv()
    first_column = df.columns[0] 
    result = df[first_column].tolist()
    if result is not None:
        return result
    else:
        print("You must enter at least one species name in the first column.")


def get_filter_str_or_bool(filter_parameter):
    """Return a string or a boolean with the result of the filter parameter"""
    df = get_df_from_csv()
    result = df[filter_parameter].tolist()[0]
    if result is None:
        return ""
    else:
        return result

def get_filter_int(filter_parameter):
    """Return an integer with the result of the filter parameter"""
    df = get_df_from_csv()
    result = int(df[filter_parameter].tolist()[0])
    if result is None:
        return ""
    else:
        return result


if __name__ == "__main__":
    print(f'species list: {get_species_list()}')
    print(f'search_name: {get_filter_str_or_bool("search_name")}')
    print(f'media_type: {get_filter_str_or_bool("media_type")}')
    print(f'country: {get_filter_str_or_bool("country")}')
    print(f'has_coordinate: {get_filter_str_or_bool("has_coordinate")}')
    print(f'basis_of_record: {get_filter_str_or_bool("basis_of_record")}')
    print(f'institution_code: {get_filter_str_or_bool("institution_code")}')
    print(f'limit: {get_filter_int("limit")}')


