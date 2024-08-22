import os
import pandas as pd
from data import elos_preseason
from archive import this_week_games
from helpers import cfb_media_import, viewing_windows

# Pre-define categories of game media
broadcast = ['ABC', 'CBS', 'NBC', 'FOX']
# TODO: Auto lookup channels
cable = ['CBSSN', 'ESPN', 'FS1', 'ESPNU', 'ACCN', 'BTN', 'SECN', "SEC NETWORK", "ACC NETWORK", "BIG10"]
web = ['ESPN+', 'SECN+', 'BIG12|ESPN+', 'ACCNX', "ACC Extra"]

# Define the user's preferences
preferred_teams = ["Missouri", "Ohio State", "Oregon", "Texas"]
preferred_conferences = {'SEC': 1, 'Big 10': 2}
weights = {'teams': 40, 'close': 20, 'conferences': 5, 'best': 35}
channels = broadcast + cable + web  # + ['ESPN+']

# Add ELO ratings
elo_rates = elos_preseason.elos
elo_ratings = elo_rates.set_index('team')['elo'].to_dict()
week_df = this_week_games.week_df_stamped
week_df['home_elo'] = week_df['home_team'].map(elo_ratings)
week_df['away_elo'] = week_df['away_team'].map(elo_ratings)
week_df[['home_elo', 'away_elo']] = week_df[['home_elo', 'away_elo']].fillna(1000)

# Calculate the ELO difference for close games
week_df['elo_diff'] = abs(week_df['home_elo'] - week_df['away_elo'])

# Add media info
week1_media = cfb_media_import.this_week_media
week_df = pd.merge(week_df, week1_media, how='outer', left_on=['home_team', 'away_team'],
                   right_on=['homeTeam', 'awayTeam'])
cols_to_drop = ['id', 'season', 'week', 'seasonType', 'startTime', 'isStartTimeTBD', 'homeTeam',
                'homeConference', 'awayTeam', 'awayConference', 'mediaType']
week_df.drop(cols_to_drop, axis=1, inplace=True)
week_df.dropna(axis=0, how='any', inplace=True)
cols_to_keep = ['home_team', 'away_team', 'home_conference', 'away_conference',
                'home_elo', 'away_elo', 'date', 'time (et)', 'elo_diff']
week_df = week_df.groupby(cols_to_keep, as_index=False).agg({
    'outlet': list})


# Function to score the games based on the user's criteria
def score_game(row):
    score = 0

    # Preferred teams
    if row['home_team'] in preferred_teams or row['away_team'] in preferred_teams:
        score += weights['teams']

    # Preferred conferences (don't weight ACC over SEC?)
    home_conf_score = preferred_conferences.get(row['home_conference'], 0)
    away_conf_score = preferred_conferences.get(row['away_conference'], 0)
    conference_score = max(home_conf_score, away_conf_score)
    score += conference_score * weights['conferences']

    # Close games
    close_game_score = 1 / (1 + row['elo_diff'])  # Inverse of the ELO difference for closeness
    score += close_game_score * weights['close']

    # Assume max ELO rating in the dataframe for the 'best' team scoring
    elo_ratings = {'max_elo': max(week_df['home_elo'].max(), week_df['away_elo'].max())}

    # Best teams
    best_team_score = (row['home_elo'] + row['away_elo']) / 2
    score += best_team_score / elo_ratings['max_elo'] * weights['best']

    # Zero out game if it doesn't have a channel in user's list
    if not any(channel in row['outlet'] for channel in channels):
        score = 0

    return round(score, 2)


# Apply the scoring function to each game, then round score
week_df['score'] = week_df.apply(score_game, axis=1)

# Output a full dataframe of all viewing windows, if desired
"""
output_dir = 'outputs'
filename1 = "full.csv"
file_path1 = os.path.join(output_dir, filename1)
week1_df.to_csv(file_path1, index=False)
"""

# Define viewing windows
view_windows = viewing_windows.create_dynamic_viewing_windows(this_week_games.file_path)


# Function to filter dataframe based on date and time range
def filter_by_time(df, date, start_time, end_time):
    mask = (df['date'] == date) & (df['time (et)'] >= start_time) & (df['time (et)'] <= end_time)
    filtered_df = df[mask]

    # Sort the filtered DataFrame by 'score' column
    sorted_df = filtered_df.sort_values(by='score', ascending=False)

    return sorted_df


# Create a dictionary to hold dataframes for each viewing window
viewing_dfs = {window: filter_by_time(week_df, date, start, end)
               for window, (date, start, end) in view_windows.items()}

# Save each DataFrame to a separate CSV file
for name, df in viewing_dfs.items():
    output_dir = 'outputs'
    filename = f"{name}.csv"
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, index=False)
