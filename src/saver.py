import functools
import io
import json
import os
import re
import time
from typing import Callable
from urllib import response

import geopandas as gpd
import pandas as pd
import requests


# Define a function to save the DataFrame to a CSV file
def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    try:
        df.to_csv(filename, index=False)
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")


# Save the DataFrame to a JSON file
def save_to_json(df: pd.DataFrame, filename: str) -> None:
    try:
        df.to_json(filename, orient="records", lines=True)
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")


# Save the GeoDataFrame to a Shapefile
def save_to_shapefile(
    gdf: gpd.GeoDataFrame,
    filename: str,
) -> None:
    try:
        gdf.to_file(filename, driver="ESRI Shapefile")
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to Shapefile: {e}")


# Save csv from url HTTP request:
# Function to request data from the UNICEF API and check the response status
def check_file_exists(filepath: str) -> bool:

    if not (os.path.exists(f"{filepath}.csv") or os.path.exists(f"{filepath}.json")):
        print(f"File '{filepath}.csv' or '{filepath}.json' does not exist.")
        return False
    else:
        print(f"File '{filepath}.csv' or '{filepath}.json' already exists.")
        return True


def save_data_request(
    url: str,
    file: str,
    path: str = "../data/raw",
    **kwargs,
) -> None:
    header: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Connection failed with status code: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    os.makedirs(path, exist_ok=True)
    filename: str = file if file is not None else url.split("/")[-1].split("?")[0]
    content_type: str = response.headers.get("Content-Type", "")
    is_csv: bool = "csv" in content_type or url.endswith(".csv")

    if is_csv:
        filepath: str = f"{path}/{filename}.csv"
        print("Loading data from CSV response...")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Data loaded successfully from CSV.")
    else:
        filepath = f"{path}/{filename}.json"
        print("Loading data from JSON response...")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response.json(), f)
        print("Data loaded successfully from JSON.")


if __name__ == "__main__":
    pass
