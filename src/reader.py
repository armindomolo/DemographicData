import json
from math import e

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


# read csv
def read_csv(filename: str, path = "data/") -> pd.DataFrame:
    try:
        df = pd.read_csv(path + filename)
        print(f"Data loaded successfully from {filename}")
        return df
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# read json
def read_json(filename: str, path = "data/") -> pd.DataFrame:
    try:
        with open(path + filename, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"Data loaded successfully from {filename}")
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

