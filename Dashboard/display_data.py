import pandas as pd
from raw_data import raw_data

def get_daily_cases(data, col_name='series_1'):
    series = data['cases_national'].copy()
    series = series.groupby(by='Date_statistics').count()
    series = series.rename(columns={'Date_file': col_name})

    return series[col_name]

if __name__ == '__main__':
    cases = get_daily_cases(raw_data)
    print(cases)