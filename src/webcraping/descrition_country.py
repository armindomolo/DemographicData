import json
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

print("Scraping description of countries data..")
print()


# Check the status of the response and print appropriate message
def check_status(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            print("Connection successful!")
            return response
        else:
            print(
                f'Connnection failed with status code:{response.status_code if response else "NO RESPONSE"}'
            )

    return wrapper


# Function to make a GET request to the URL and return the response
@check_status
def request(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        # response.raise_for_status()  # Check if the request was successful
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Function to read JSON data from a file and convert it to a DataFrame
def db_from_json(request):
    try:
        data_json = request.json()
        ##data_json = json.loads(request.text)
        db = pd.json_normalize(data_json["features"])
        return db
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# Function to save DataFrame to a CSV file
def db_save_csv(db, file_path):
    try:
        db.to_csv(file_path, index=False)
        print("Data saved to CSV file successfully!")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")


# Function to save JSON data to a file

# Function to save DataFrame to a CSV file


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    url_geral = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/AGO..?format=csv&labels=both"

    data = request(url)
    db = db_from_json(data)
    # db_save_csv(db, "data/raw/countries_description.csv")
    id_country = list(db["id"].unique())
    print()

    # Download data unicef
    """    for i, id in enumerate(id_country):
        url_geral = f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/{id}..?format=csv&labels=both"
        data_response = request(url_geral)
        if data_response is not None:
            file_path_csv = f"data/raw/unicef_data/unicef_data_{id}.csv"
            try:
                db_csv = pd.read_csv(url_geral)
                if db_csv is not None:
                    db_save_csv(db_csv, file_path_csv)
                    print(f"Downloading data for country: {id}...")
            except Exception as e:
                print(f"Error processing data for country {id}: {e}")
        print()
        time.sleep(2)  # Sleep for 1 second between requests to avoid overwhelming the server
  """

    url_geral = f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/AGO?format=csv&labels=both"
    data_response = request(url_geral)
    if data_response is not None:
        file_path_csv = f"data/raw/unicef_data_all.csv"
        try:
            db_csv = pd.read_csv(url_geral, low_memory=False)
            """
            if db_csv is not None:
                db_save_csv(db_csv, file_path_csv)
                print(f"Downloading data for all countries...")
            """
        except Exception as e:
            print(f"Error processing data for all countries: {e}")
    # %%
    db_csv
