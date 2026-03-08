from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time


# Function to get the URL for a specific indicator and source
def get_url(indicator, source):
    if source in urls and indicator in urls[source]:
        return urls[source][indicator]
    else:
        print(f"URL not found for indicator '{indicator}' and source '{source}'.")
        return None

print("Scraping UNICEF data..")
print()

# Check the status of the response and print appropriate message
def check_status(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            print("Connection successful!")
            return response
        else:
            print(f'Connnection failed with status code:{response.status_code if response else "NO RESPONSE"}')
    return wrapper        
# Function to make a GET request to the URL and return the response
@check_status
def request(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        #response.raise_for_status()  # Check if the request was successful
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Function load data
def db(request,url):
    if url.find("csv") != -1:
        data_json = request.json()
        data_json = json.loads(request.text)
        db = pd.json_normalize(data_json['features'])
        return db
    else:
        db = pd.read_csv(request)
        return db

# Function to save JSON data to a file
def save_json(request, fil_path):
    try:
        data_json = request.json()
        with open(fil_path, 'w') as json_file:
            json.dump(data_json, json_file, indent=4)
        print("Data saved to JSON file successfully!")  
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")    

# Function to read JSON data from a file and convert it to a DataFrame       
def json_to_dataframe(request):
    data_json = request.json()        
    data_json = json.loads(request.text)
    dataframe = pd.json_normalize(data_json[1])      
    return dataframe

def save_csv(dataframe, file_path):
    try:
        dataframe.to_csv(file_path, index=False)
        print("Data saved to CSV file successfully!")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

if __name__ == "__main__":
    
    url_geral_unicef_ex = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/BRA..?format=csv&labels=both"
    #file_path = 'data/raw/url_child_mortality.json'
    #file_path_csv = 'data/raw/url_child_mortality.csv'
    data_response = request(url_geral_unicef_ex)
    db = pd.read_csv(url_geral_unicef_ex)
    print(db.head())
    print()
    print([x for x in db.columns])
    #save_json(data_response, file_path)
    """    education_data = json_to_dataframe(data_response)
    save_csv(education_data, file_path_csv)
    print(education_data.info())
    """
