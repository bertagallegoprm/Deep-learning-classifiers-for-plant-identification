from datetime import datetime
import os
import pandas as pd


def get_timestamp():
    """Get date and time for naming the files"""
    timestamp = datetime.now()
    timestamp_iso = timestamp.isoformat()
    timestamp_iso_seconds = timestamp_iso[:-7] 
    return timestamp_iso_seconds


def open_filter_report(filter_hashed):
    """
    Open a text file with the following naming format:
    md5hash_request_filter.txt
    Example: 2020-03-31T22:00:00_request_summary.txt
    """
    folder = "request_reports"
    if not os.path.exists(folder):
        os.makedirs(folder)
    text_file_name = f"{folder}/{filter_hashed}_request_filter.txt"
    print(f"{text_file_name} file created.")
    return open(text_file_name, "w")


def request_result_to_csv(df, filter_hash):
    """
    Create a CSV file with the results
    of the data request to GBIF
    and name it with a hash of the filter applied.
    Results from different filters 
    are stored in a new file, while results
    from the same filter are overwriten.
    """
    folder = "request_reports"
    if not os.path.exists(folder):
        os.makedirs(folder)
    csv_file_name = f"{folder}/{filter_hash}_request_results.csv"
    df.to_csv(csv_file_name, sep = ",", header = True, index = None, encoding="utf-8") 
    print(""+csv_file_name+" file created.")


def read_csv_name():
    """
    Prompt user for file path and name.
    """
    return input("Enter file name (full path): ") 


def create_dataframe_from_csv(path_to_csv):
    """
    Given a full path, open a CSV file
    and store it into a data frame object.
    """
    try:
        df = pd.read_csv(""+path_to_csv+"", sep=",", encoding="utf-8") # Change to utf-8 if CSV has this encoding
    except:
        raise
    return df
    


