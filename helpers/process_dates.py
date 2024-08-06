import pandas as pd


def process_dates(df):
    """
    Convert start_date to datetime, convert to Eastern time,
    and extract date and time components.
    """
    df['datetime'] = pd.to_datetime(df['start_date'])
    df['datetime_edt'] = df['datetime'].dt.tz_convert('US/Eastern')
    df['date'] = df['datetime_edt'].dt.date
    df['time (et)'] = df['datetime_edt'].dt.strftime('%H:%M')
    df.drop(columns=['start_date', 'datetime', 'datetime_edt'], inplace=True)
    return df
