"""This file contains the code to load all raw data and provide it for further 
processing steps. 
"""
from pathlib import Path
import pandas as pd

data_folder = Path("Data")

files = {
    "aggregated_cases_municipality": "COVID-19_aantallen_gemeente_cumulatief.csv",
    "handicaped": "COVID-19_gehandicaptenzorg.csv",
    "tests": "COVID-19_uitgevoerde_testen.csv",
    "daily_cases_municiplaity": "COVID-19_aantallen_gemeente_per_dag.csv",
    "icu": "COVID-19_ic_opnames.csv",
    "nursing_homes": "COVID-19_verpleeghuizen.csv",
    "cases_national": "COVID-19_casus_landelijk.csv",
    "water": "COVID-19_rioolwaterdata.csv",
    "hospital": "COVID-19_ziekenhuisopnames.csv",
    "bahaviour": "COVID-19_gedrag.csv",
    "seventy_plus": "COVID-19_thuiswonend_70plus.csv",
}

raw_data = {}

for key, file in files.items():
    print(f"loading... {file}")
    raw_data[key] = pd.read_csv(data_folder / file, sep=";")