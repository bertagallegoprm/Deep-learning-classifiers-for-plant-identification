from matplotlib import pyplot as plt
import pandas as pd


def get_geodata_csv():
    path_to_file = input("Enter file name (geodata.csv, full path): ") 
    return pd.read_csv(path_to_file, sep=",", encoding="utf-8")


def get_species_list(df):
    return df["species_name"].tolist()


def unique(item_list):
    unique_list = []
    for item in item_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def get_occurrence_count(item_list):
    item_count = []
    unique_items = unique(item_list)
    for item in unique_items:
        item_count.append(item_list.count(item))
    return item_count


def plot_coordenates_count(occurrence_count, species_name, path_to_plot):
    """
    Plot number of coordenates per class.
    """
    occurrence_count = list(reversed(occurrence_count))
    species_name = list(reversed(species_name))
    plt.figure(figsize=(10,10)) 
    plt.barh(species_name, occurrence_count, color="#7cd9b7", height=0.8, edgecolor="grey")
    plt.title("Number of georeferences per class")
    # x axis, species
    xint = range(0,(max(occurrence_count)+1))
    plt.xticks(xint)
    plt.xlabel("Number of georeferences")
    # y axis, image count
    plt.ylabel("Species", rotation="vertical")
    plt.yticks(fontsize=8)
    # save file
    plt.savefig(path_to_plot)

if __name__ == "__main__":
    path_to_plot = "data/geodata/request_reports/georeference_per_species.png"
    geodata = get_geodata_csv()
    species_name = unique(get_species_list(geodata))
    occurrence_count = get_occurrence_count(get_species_list(geodata))   
    plot_coordenates_count(occurrence_count, species_name)