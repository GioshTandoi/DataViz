from typing import List, Dict
import pandas as pd
from pandas.core.series import Series
from utils.raw_data import raw_data


MIN_DATE = '2020-01-01'
MAX_DATE = '2021-02-16'

def fill_zero_days(data):
    idx = pd.date_range(MIN_DATE, MAX_DATE)
    return data.reindex(idx, fill_value=0)

def apply_filters(series, data, filters):
    if not filters:
        return data

    for dimension, values in filters.items():
        column = data_structure[series]["filter"][dimension]["column"]
        data = data[data[column].isin(values)]

    return data

def get_daily_cases(data, filters = None, transform=None):
    series = data['cases_national'].copy()
    series = apply_filters("cases", series, filters)
    series = series.groupby(by=series['Date_statistics']).count()
    series = series.rename(columns={'Date_file': "series"})
    series = fill_zero_days(series)

    if transform:
        series = data_structure["cases"]["transformers"][transform](series)

    return series["series"]

def get_daily_tests(data, filters = None, transform=None):
    series = data['tests'].copy()
    series = apply_filters("tests", series, filters)
    series = series.groupby(by=series['Date_statistics']).sum()
    series = series.rename(columns={'Tested_with_result': "series"})
    series = fill_zero_days(series)

    if transform:
        series = data_structure["tests"]["transformers"][transform](series)

    return series["series"]

def get_daily_icu_admissions(data, filters = None, transform=None):
    series = data['icu'].copy()
    series = series.groupby(by=series['Date_statistics']).sum()
    series = series.rename(columns={'IC_admission': "series"})
    series = fill_zero_days(series)

    if transform:
        series = data_structure["ICU admissions"]["transformers"][transform](series)

    return series["series"]


def trans_seven_day_average(series, **kwargs):
    return series.rolling(window=7).mean()

def trans_tests_per_positive(series, **kwargs):
    series["series"] = series["series"]/series["Tested_positive"]
    return series


data_structure = {
    "cases": {
        "getter": get_daily_cases,
        "filter": {
            "Sex": {
                "column": "Sex",
                "type": "category",
                "values": ["Male", "Female"],
            },
            "Region": {
                "column": "Province",
                "type": "category",
                "values": raw_data['cases_national']["Province"].unique(),
            },
            "Age group": {
                "column": "Agegroup",
                "type": "category",
                "values": raw_data['cases_national']["Agegroup"].unique(),
            },
        },
        "transformers": {
            "Seven Day Average": trans_seven_day_average,
        },
    },
    "Tests": {
        "getter": get_daily_tests,
        "filter": {
            "Region": {
                "column": "Security_region_name",
                "type": "category",
                "values": raw_data['tests']["Security_region_name"].unique(),
            },
        },
        "transformers": {
            "Seven Day Average": trans_seven_day_average,
            "Per Positive result": trans_tests_per_positive,
        },
    },
    "ICU admissions": {
        "getter": get_daily_icu_admissions,
        "filter": {
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

    if series_2:
        s2 = data_structure[series_2]["getter"](
            raw_data, filters=filters_2, transform=transform_2)
        data["series_2"] = s2

    return data


if __name__ == '__main__':

    print(get_data(series_1="cases", filters_1={"Sex": ["Male"]},
        series_2="cases", transform_2="Seven Day Average").tail(20))

    print(get_data(series_1="cases", filters_1={"Sex": ["Male"], "Region": ["Groningen"]},
        series_2="cases", transform_2="Seven Day Average").tail(20))

    print(get_data(series_1="tests",
        series_2="tests", transform_2="Seven Day Average").tail(20))

    print(get_data(series_1="tests",
        series_2="tests", transform_2="Per Positive result").tail(20))

    print(get_data(series_1="ICU admissions",
        series_2="ICU admissions", transform_2="Seven Day Average").tail(20))