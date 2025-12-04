import requests
from dotenv import load_dotenv
import os


load_dotenv()

api_base = os.getenv("base_url")

def api_call(endpoint, file_name):

    try:
        api = f'{api_base}/{endpoint}'

        response = requests.get(api)

        if response.status_code == 200:
            data = response.json()

            file_path = os.path.join("Datasets",file_name)

            with open(file_path, "wb") as file:
                file.write(data)
                
        else:
            print(f"Failed to fetch data from {endpoint}. Status code: {response.status_code}")
    except Exception as e:
        print(str(e))   

api_data = {
    'admissions': 'admissions.csv',
    'daily_metrics': 'daily_metrics.csv',
    'hospitals': 'hospitals.csv',
    'wards': 'wards.csv'
}