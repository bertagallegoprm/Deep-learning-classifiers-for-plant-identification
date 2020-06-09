import pandas as pd 
import argparse


def get_species_list():
    """
    Return a list of species 
    passing as an argument the path to a CSV file 
    where the first column stores de names of the species.
    """
    parser = argparse.ArgumentParser(prog = "Get species names list", usage = "Given a CSV with species names in the first column, get a list of the species. Example: python3 -m data.species_list data/sample_inputs/species_list.csv")
    parser.add_argument('src_path', type=str,  help = "path to the CSV file with the species names. Example: data/inputs/species_list.csv")
    arg = parser.parse_args()
    src_path = arg.src_path
    df = pd.read_csv(""+src_path+"", sep=",", encoding="utf-8")
    first_column = df.columns[0] 
    return df[first_column].tolist()

if __name__ == "__main__":
    print(get_species_list())

