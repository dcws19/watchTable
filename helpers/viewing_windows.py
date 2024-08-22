import pandas as pd


def create_dynamic_viewing_windows(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df['time (et)'] = pd.to_datetime(df['time (et)'], format='%H:%M').dt.time

    # Find the date for Saturday
    saturday_date = df[df['date'].dt.strftime('%A') == 'Saturday']['date'].unique()
    if len(saturday_date) > 0:
        saturday_date = str(saturday_date[0].date())
    else:
        saturday_date = 'Saturday'  # Default if no Saturday date found

    # Define base viewing windows for Saturday with the dynamic date
    base_windows = {
        'Sat Noon': (saturday_date, '11:00', '14:29'),
        'Sat Afternoon': (saturday_date, '14:30', '17:59'),
        'Sat Evening': (saturday_date, '18:00', '20:59'),
        'Sat Late Night': (saturday_date, '21:00', '23:59')
    }

    # Create dynamic viewing windows for other days with games, excluding Saturday
    dynamic_windows = {
        date.strftime('%a'): (str(date.date()), '11:00', '23:59')
        for date in df['date'].unique() if date.strftime('%A') in ['Thursday', 'Friday', 'Sunday',
                                                                   'Monday', 'Tuesday', 'Wednesday']
    }

    # To create a list of all viewing windows
    all_windows = {**dynamic_windows, **base_windows}

    return all_windows


'''
    # Filter and concatenate games within the viewing windows
    filtered_games = []
    for date, start, end in dynamic_windows.values():
        filtered_games.append(df[(df['date'] == pd.to_datetime(date)) &
                                 (df['time (et)'] >= pd.to_datetime(start).time()) &
                                 (df['time (et)'] <= pd.to_datetime(end).time())])

    for time_window, (day, start, end) in base_windows.items():
        filtered_games.append(df[(df['date'].dt.strftime('%A') == day) &
                                 (df['time (et)'] >= pd.to_datetime(start).time()) &
                                 (df['time (et)'] <= pd.to_datetime(end).time())])

    return pd.concat(filtered_games).reset_index(drop=True)[['home_team', 'away_team', 'date', 'time (et)']]
'''

full_path = '/outputs/full1.csv'

# print(create_dynamic_viewing_windows(full_path))
