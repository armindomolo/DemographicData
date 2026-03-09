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


  # type: ignore

# Function to request data from the UNICEF API and check the response status
def handle_request(func) -> Callable[..., requests.Response | None]:
    @functools.wraps(func)
    def wrapper(url: str, *args, **kwargs) -> pd.DataFrame | None:
        try:
            response: requests.Response = requests.get(
                url, headers={"User-Agent": "Mozilla/5.0"}
            )
            time.sleep(1)  # Sleep for 1 second to avoid overwhelming the API
            response.raise_for_status()  # Check if the request was successful
            return func(response, url, *args, **kwargs)
        except requests.exceptions.HTTPError as e:
            print(f"Connection failed with status code: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    return wrapper  # type: ignore


@handle_request
def load_data(
    response: requests.Response, url: str, *args, **kwargs
) -> pd.DataFrame | None:
    if response is not None:
        if "csv" in url:
            print("Loading data from CSV response...")
            print("Data loaded successfully from CSV.")
            return pd.read_csv(io.StringIO(response.text))
        data_json: dict = response.json()
        return pd.json_normalize(data_json["features"])
    return None


def load_data_unicef(
    country_id: str, group_indicator: str | None, indicator: str| None
) -> pd.DataFrame | None:
    url_unicef: str = build_url(country_id)
    groupIndicator:list[str] | None   = string_for_list(group_indicator) if group_indicator else None
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
def build_url(country_id: str) -> str:
    return f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/{country_id}..?format=csv&labels=both"

# transform string in list to string with + separator for url query parameters
def string_for_list(string: str) -> list[str]:
    if "," in string:
        return [s for s in string.split(",")]
    return [string]


if __name__ == "__main__":
    pass
