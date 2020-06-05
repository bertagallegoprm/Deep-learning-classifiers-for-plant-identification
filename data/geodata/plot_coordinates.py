import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import shapely
from shapely.geometry import Point, Polygon
from shapely import geometry
from data.search import filter_hash
from data.config import geodata_filter, species_list
from data.file_handler import create_dataframe_from_csv, column_to_list


def plot_occurrences_map(coordinates_df, shape_file, destination_path):
    """
    Given a shape file for a geographical area
    and a dataframe with at least two columns:
    - latitude
    - longitde
    return an occurrences map in .png format
    """
    # Add a new column to the data frame with a combination of coordinates
    coordinate_pair = [Point(xy) for xy in zip(coordinates_df.longitude, coordinates_df.latitude)]
    coordinates_df['geometry'] = coordinate_pair
    coordinates_df.drop(['latitude','longitude'], axis = 1, inplace=True)
    crs = {'init': 'epsg:4326'}
    occurrences_loc = gpd.GeoDataFrame(coordinates_df, crs=crs, geometry=coordinate_pair)
    occurrences_loc.shape
 
    shape_map = gpd.read_file(shape_file)
    fig, ax = plt.subplots(figsize = (10,10))
    occurrences_loc.geometry.plot(marker="d", color="green", markersize=1, ax=ax, label = "Species occurrences")
    shape_map.plot(color="grey", ax=ax, alpha = 0.2)
   
    plt.title('Species distribution map')
    plt.legend()
    plt.savefig(destination_path)


def plot_coordinates_frequency(coordinates_df, destination_path):
    """
    Given a data frame with latitude and longitude
    return an histogram with the frequency of the coordinates.
    """
    latitude = column_to_list(coordinates_df, "latitude")
    longitude = column_to_list(coordinates_df, "longitude")
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True, figsize=(6, 6))
    #fig, axs = plt.subplots(2)
    fig.suptitle('Coordinates distribution')
    plt.subplot(2,1,1)
    plt.hist(latitude, bins = 40, alpha = 0.5, 
             color="lightgreen", 
             edgecolor="grey")
    plt.ylabel("Frequency", fontsize=8)
    plt.xlabel("Latitude (decimal degrees)", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.subplot(2,1,2)
    plt.hist(longitude, bins = 40, alpha = 0.5, 
            color="lightpink", 
            edgecolor="grey")
    plt.ylabel("Frequency", fontsize=8)
    plt.xlabel("Longitude (decimal degrees)", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend()
    plt.savefig(destination_path)


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
    coordinates_df = pd.DataFrame(list(zip(species_name, latitude, longitude)), 
    columns = ["species_name", "latitude", "longitude"])

    # Plot occurrences location
    destination_path = "data/geodata/outputs/occurrences_map.png"
    shape_file = "data/geodata/uk_maps/GBR_adm0.shp" # UK map
    plot_occurrences_map(coordinates_df, shape_file, destination_path)
