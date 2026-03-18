import io
import json
import os
import time
import typing
from ast import Call
from typing import Callable

import pandas as pd
import requests

from src import loader, saver

# Define json type for type hinting
Json = typing.Dict[str, typing.Any]


# Create class to ManageData
class ManageData:
    def __init__(self) -> None:
        self.response: requests.Response | None = None
        self.url: str | None = None
        self.data: Callable[..., pd.DataFrame | Json] | None = None
        self.header: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    # loard data from url return in json or csv format
    def load_data(self, url: str) -> pd.DataFrame | Json | None:
        self.url = url
        if self.url is not None:
            self.response = requests.get(self.url, headers=self.header)
            try:
                self.response.raise_for_status()
                if "csv" in self.url:
                    print("Loading data from CSV response...")
                    print("Data loaded successfully from CSV.")
                    self.data = self.response.text  # type: ignore
                    return pd.read_csv(io.StringIO(self.data))  # type: ignore
                else:
                    print("Loading data from JSON response...")
                    print("Data loaded successfully from JSON.")
                    self.data = self.response.json()
                    return pd.json_normalize(self.data["features"])  # type: ignore
            except requests.exceptions.HTTPError as e:
                print(f"Connection failed with status code: {e}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None
