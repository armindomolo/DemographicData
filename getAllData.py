import functools

import pandas as pd
import requests

"""
This script is responsible for fetching data from the UNICEF API, processing it, and saving the relevant information to a CSV file. The script includes error handling to manage potential issues during data retrieval and processing."""
""""""


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


# decorator to create the filter indicators function
def filter_indicators(func):
    @functools.wraps(func)
    def wrapper(*args, group_indicators=None, indicators=None):
        df = func(*args)

        if df is None:
            print("No data to filter.")
            return None

        if group_indicators:
            df = df[df["INDICATOR"].isin(group_indicators)].reset_index(drop=True)

        if indicators is not None:
            return df[df["Indicator"].isin(indicators)].reset_index(drop=True)
        return df

    return wrapper


# get data from url:
@filter_indicators
def unicef_data(country_id) -> pd.DataFrame | None:
    url = f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/{country_id}..?format=csv&labels=both"
    data_respond = request(url)
    try:
        db_csv = pd.read_csv(data_respond)
        return db_csv
    except Exception as e:
        print(f"Error processing data for country {country_id}: {e}")
        return None


if __name__ == "_main__":
    print("Fetching data from UNICEF API for Angola...")
    df_ango = unicef_data("AGO", group_indicators="DM_POP_TOT")
    print(df_ango.head())
    df_ango.to_csv("data/raw/data_ango_DM_POP_TOT.csv", index=False)
