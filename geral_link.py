# %%
import json
import time

import pandas as pd
import requests
from rich.console import Console
from rich.table import Table

# Initialize Rich console for better output formatting
# %%
console = Console()


## Function to fetch UNICEF data for a specific country:
# %%
def unicef_data(country_id):
    url_geral = f"https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/{country_id}..?format=csv&labels=both"
    try:
        db_csv = pd.read_csv(url_geral)
        return db_csv
    except Exception as e:
        print(f"Error processing data for country {country_id}: {e}")
        return None


# %%
df_ango = unicef_data_all = unicef_data(
    "AGO"
)  # Example for Angola, replace "AGO" with the desired country code

# %%
df_ango.head()

# columns of the dataframe
# %%
print([column for column in df_ango.columns])

# select 2 columns
# %%
df_ango_selected = (
    df_ango[["INDICATOR", "Indicator"]].drop_duplicates().reset_index(drop=True)
)

# %%
df_ango_selected.to_csv("data/raw/indicator_data.csv", index=False)
# %%
