from datetime import datetime
import os


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
    folder = "request_summary"
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
    folder = "request_summary"
    if not os.path.exists(folder):
        os.makedirs(folder)
    csv_file_name = f"{folder}/{filter_hash}_request_summary.csv"
    df.to_csv(csv_file_name, sep = ",", header = True, index = None, encoding="utf-8") 
    print(""+csv_file_name+" file created.")


if __name__ == "__main__":
    report = open_report_file()
    report.write("test")
    report.close()


    


