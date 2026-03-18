# package imports:
import functools
import io
import json
import re
import time
from site import check_enableusersite
from typing import Callable

import pandas as pd
import requests
from tabulate import tabulate

"""This script is responsible for fetching data from the UNICEF API, processing it, and saving the relevant information to a CSV file. The script includes error handling to manage potential issues during data retrieval and processing."""

# reader in resquests
header: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


# Function to request data from the UNICEF API and check the response status
def load_data(url: str) -> pd.DataFrame | None:

    if url is not None:
        response: requests.Response = requests.get(url, headers=header)
        try:
            response.raise_for_status()
            if "csv" in url:
                print("Loading data from CSV response...")
                print("Data loaded successfully from CSV.")
                return pd.read_csv(io.StringIO(response.text))  # type: ignore
            else:
                print("Loading data from JSON response...")
                print("Data loaded successfully from JSON.")
                return pd.json_normalize(response.json()["features"])  # type: ignore
        except requests.exceptions.HTTPError as e:
            print(f"Connection failed with status code: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


def load_data_unicef(
    country_id: str, group_indicator: str | None, indicator: str | None
) -> pd.DataFrame | None:
    url_unicef: str = url_all_indicator_unicef(country_id)
    groupIndicator: list[str] | None = (
        string_for_list(group_indicator) if group_indicator else None
    )
    indicatorlist: list[str] | None = string_for_list(indicator) if indicator else None
    if country_id:
        db: pd.DataFrame | None = load_data(url=url_unicef)  # type: ignore
        # time.sleep(1)  # Sleep for 1 second to avoid overwhelming the API
        if db is not None:
            if group_indicator:
                db = db[db["INDICATOR"].str.contains("|".join(groupIndicator))].reset_index(drop=True)  # type: ignore
            if indicator:
                return db[db["Indicator"].str.contains("|".join(indicatorlist))].reset_index(drop=True)  # type: ignore
        return db
    return None


# url_unicef = f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/AGO..?format=csv&labels=both"
def url_all_indicator_unicef(country_id: str) -> str:
    return f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/{country_id}..?format=csv&labels=both"


# transform string in list to string with + separator for url query parameters
def string_for_list(string: str) -> list[str]:
    if "," in string:
        return [s for s in string.split(",")]
    return [string]

# Function to filter a DataFrame based on multiple criteria and return a list of unique values from a specified column
def list_from_database(db: pd.DataFrame, column: str, *args) -> list[str]:
    if args is None or len(args) == 0:
        return db[column].dropna().unique().tolist()
    else:
        for arg in args:
            if arg is not None:
                db = db[db[column].str.contains(arg)].reset_index(drop=True)  # type: ignore
        return db[column].dropna().unique().tolist()

if __name__ == "__main__":
    pass
