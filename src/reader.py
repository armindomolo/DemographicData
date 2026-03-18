import functools
import json
import os
import re
from functools import wraps
from math import e
from tkinter import NO

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


# read csv
def read_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding="utf-8")
        print(f"Data loaded successfully from {path}")
        return df
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# read json
def read_json(path) -> pd.DataFrame:
    try:
        with open(path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"Data loaded successfully from {path}")
        return df
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# convert DataFrame to GeoDataFrame
def df_to_gdf(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:
    try:
        geometry: list[Point] = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        print("DataFrame successfully converted to GeoDataFrame")
        return gdf
    except Exception as e:
        print(f"An error occurred while converting to GeoDataFrame: {e}")
        return gpd.GeoDataFrame()  # Return an empty GeoDataFrame in case of error

# read shapefile
def read_shapefile(filename: str, path = "data/") -> gpd.GeoDataFrame:
    try:
        gdf = gpd.read_file(path + filename)
        print(f"Shapefile loaded successfully from {filename}")
        return gdf
    except Exception as e:
        print(f"An error occurred while reading the shapefile: {e}")
        return gpd.GeoDataFrame()  # Return an empty GeoDataFrame in case of error

def is_in_directory(path: str) -> bool:
    return os.getcwd() == os.path.abspath(path)

#--------------------------------------------------------------------------------------
# Change_dir decorator to change the working directory for a function
def change_dir(path: str) -> None:
     def decoretor(func) -> function | None:
         @wraps(func)
         def wrapper(*args, **kwargs) -> function | None:
             orignal_dir: str = os.path.dirname(os.path.abspath(__file__))
             try:
                if not is_in_directory(path):
                    os.chdir(path)
                    return func(*args, **kwargs)
                else:
                    print(f"Already in directory: {path}")
                    return func(*args, **kwargs)
             except FileNotFoundError:
                print(f"Directory not found: {path}")
             finally:
                 os.chdir(orignal_dir)
         return wrapper # type: ignore
     return decoretor  # type: ignore

#--------------------------------------------------------------------------------------
# set_directory
def set_directory(path) -> None:
    try:
        if not is_in_directory(path):
            os.chdir(path)
        else:
            print(f"Already in directory: {path}")
    except FileNotFoundError:
        print(f"Directory not found: {path}")

# return in original directory
def return_filepath() -> None:
    original_dir: str = os.path.dirname(os.path.abspath(__file__))
    os.chdir(original_dir)


#--------------------------------------------------------------------------------------
