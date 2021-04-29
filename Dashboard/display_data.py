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

def get_daily_cases(data, col_name='series_1', filters = None):
    series = data['cases_national'].copy()
    series = apply_filters(series, filters)
    series = series.groupby(by=series['Date_statistics']).count()
    series = series.rename(columns={'Date_file': col_name})
    series = series[col_name]
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

if __name__ == '__main__':
    print('daily cases')
    cases = get_daily_cases(raw_data)
    print(cases.tail(60))

    cases = get_daily_cases(raw_data, filters={"Sex": ["Male"]})
    print(cases.tail(60))