import pandas as pd
from data import cfb_sched_import
from helpers.process_dates import process_dates

# Dictionary to store DataFrames for each week
weeks_dfs = {}

# Loop through weeks 2 to 14
for week in range(2, 15):
    week_json = cfb_sched_import.games_api.get_games(year=2024, division='fbs', week=week)
    week_df = pd.DataFrame.from_records([dict(home_team=w.home_team,
                                              away_team=w.away_team,
                                              home_conference=w.home_conference,
                                              away_conference=w.away_conference,
                                              home_elo=w.home_pregame_elo,
                                              away_elo=w.away_pregame_elo,
                                              start_date=w.start_date)
                                         for w in week_json])

    # Convert the 'start_date' column to datetime format
    week_df['start_date'] = pd.to_datetime(week_df['start_date'])

    # Store the DataFrame in the dictionary with the week number as the key
    weeks_dfs[week] = week_df

# Create separate DataFrame variables for each week
for week, df in weeks_dfs.items():
    globals()[f'week{week}_df'] = df
    df = process_dates(df)

# Example of accessing the DataFrame for week 2
# print(week2_df)

# Run in python console w/ Opt+Shift+E
