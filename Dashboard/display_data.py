from typing import List, Dict
import pandas as pd
from raw_data import raw_data


MIN_DATE = '2020-01-01'
MAX_DATE = '2020-02-01'

def fill_zero_days(data):
    idx = pd.date_range(MIN_DATE, MAX_DATE)
    return data.reindex(idx, fill_value=0)

def apply_filters(data, filters):
    if not filters:
        return data

    for column, values in filters.items():
        data = data[data[column].isin(values)]

    return data

def get_daily_cases(data, filters = None, transform=None):
    series = data['cases_national'].copy()
    series = apply_filters(series, filters)
    series = series.groupby(by=series['Date_statistics']).count()
    series = series.rename(columns={'Date_file': "series"})
    series = series["series"]
    series = fill_zero_days(series)

    return series

def trans_seven_day_average(series, **kwargs):
    pass


data_structure = {
    "cases": {
        "getter": get_daily_cases,
        "filter": {
            "Sex": {
                "type": "category",
                "values": ["Male", "Female"],
            },
        },
        "transformers": {
            "Seven Day Average": trans_seven_day_average,
        },
    },
}

def get_data(
    series_1=None, filters_1=None, transform_1=None,
    series_2=None, filters_2=None, transform_2=None):
    idx = pd.date_range(MIN_DATE, MAX_DATE)
    data = pd.DataFrame(index=idx)

    if series_1:
        s1 = data_structure[series_1]["getter"](
            raw_data, filters=filters_1, transform=transform_1)
        data["series_1"] = s1

    if series_1:
        s2 = data_structure[series_1]["getter"](
            raw_data, filters=filters_2, transform=transform_2)
        data["series_2"] = s2

    return data

if __name__ == '__main__':
    print('daily cases')
    cases = get_daily_cases(raw_data)
    print(cases.tail(60))

    cases = get_daily_cases(raw_data, filters={"Sex": ["Male"]})
    print(cases.tail(60))

    print(get_data(series_1="cases", filters_1={"Sex": ["Male"]}, series_2="cases"))