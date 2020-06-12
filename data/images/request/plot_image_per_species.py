from matplotlib import pyplot as plt
import pandas as pd


def get_summary_csv():
    path_to_file = input("Enter file name (summary.csv, full path): ") 
    return pd.read_csv(path_to_file, sep=",", encoding="utf-8")


def get_species_list(df):
    return df["species_name"].tolist()


def get_image_count(df):
    return df["image_count"].tolist()


def plot_image_count(image_count, species_name):
    """
    Plot number of images per class.
    """
    image_count = list(reversed(image_count))
    species_name = list(reversed(species_name))
    plt.figure(figsize=(10,10)) 
    plt.barh(species_name, image_count, color="#7cd9b7", height=0.8, edgecolor="grey")
    plt.title("Number of images per class")
    # x axis, species
    xint = range(0,(max(image_count)+1))
    plt.xticks(xint)
    plt.xlabel("Number of images")
    # y axis, image count
    plt.ylabel("Species", rotation="vertical")
    plt.yticks(fontsize=8)
    # save file
    plt.savefig("data/images/image_request/request_reports/images_per_species.png")

if __name__ == "__main__":
    summary = get_summary_csv()
    species_name = get_species_list(summary)
    image_count = get_image_count(summary)   
    plot_image_count(image_count, species_name)


    
