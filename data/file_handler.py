from datetime import datetime
import os


def get_timestamp():
    """Get date and time for naming the files"""
    timestamp = datetime.now()
    timestamp_iso = timestamp.isoformat()
    timestamp_iso_seconds = timestamp_iso[:-7] 
    return timestamp_iso_seconds


def open_report_file():
    """
    Open a text file with the following naming format:
    datetime_request_summary.txt
    Example: 2020-03-31T22:00:00_request_summary.txt
    """
    folder = "request_summary"
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.now()
    timestamp_iso = timestamp.isoformat()
    timestamp_iso_seconds = timestamp_iso[:-7]
    text_file_name = f"{folder}/{timestamp_iso_seconds}_request_summary.txt"
    print(f"{text_file_name} file created.")
    return open(text_file_name, "w")


def request_result_to_csv(df):
    """
    Create a CSV file given a dataset
    stored into a data frame object.
    """
    timestamp = get_timestamp()
    folder = "request_summary"
    if not os.path.exists(folder):
        os.makedirs(folder)
    csv_file_name = f"{folder}/{timestamp}_request_summary.csv"
    df.to_csv(csv_file_name, sep = ",", header = True, index = None, encoding="utf-8") 
    print(""+csv_file_name+" file created.")


if __name__ == "__main__":
    report = open_report_file()
    report.write("test")
    report.close()


    


