import os
import pandas as pd
from data import elos_preseason, weeks0_1, cfb_media_import

# Pre-define categories of game media
broadcast = ['ABC', 'CBS', 'NBC', 'FOX']
cable = ['CBSSN', 'ESPN', 'FS1', 'ESPNU', 'ACCN', 'BTN', 'SECN']
web = ['ESPN+', 'SECN+', 'BIG12|ESPN+', 'ACCNX']

# Define the user's preferences
preferred_teams = ['Missouri', 'Virginia Tech', 'Penn State', 'West Virginia']
preferred_conferences = {'SEC': 1, 'ACC': 2}
weights = {'teams': 40, 'close': 20, 'conferences': 5, 'best': 35}
channels = broadcast + cable  # + ['ESPN+']

# Add ELO ratings
elo_rates = elos_preseason.elos
elo_ratings = elo_rates.set_index('team')['elo'].to_dict()
week1_df = weeks0_1.week1_df
week1_df['home_elo'] = week1_df['home_team'].map(elo_ratings)
week1_df['away_elo'] = week1_df['away_team'].map(elo_ratings)
week1_df[['home_elo', 'away_elo']] = week1_df[['home_elo', 'away_elo']].fillna(1000)

# Calculate the ELO difference for close games
week1_df['elo_diff'] = abs(week1_df['home_elo'] - week1_df['away_elo'])

# Add media info
week1_media = cfb_media_import.week1_media
week1_df = pd.merge(week1_df, week1_media, how='outer', left_on=['home_team', 'away_team'],
                    right_on=['homeTeam', 'awayTeam'])
cols_to_drop = ['id', 'season', 'week', 'seasonType', 'startTime', 'isStartTimeTBD', 'homeTeam',
                'homeConference', 'awayTeam', 'awayConference', 'mediaType', ]
week1_df.drop(cols_to_drop, axis=1, inplace=True)
week1_df.dropna(axis=0, how='any', inplace=True)
week1_df = week1_df.drop_duplicates()


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

    # Best teams
    best_team_score = (row['home_elo'] + row['away_elo']) / 2
    score += best_team_score / max(elo_ratings.values()) * weights['best']

    # Zero out game if it doesn't have a channel
    if row['outlet'] not in channels:
        score = 0

    return score


# Apply the scoring function to each game
week1_df['score'] = week1_df.apply(score_game, axis=1)
output_dir = 'outputs'
filename1 = "full.csv"
file_path1 = os.path.join(output_dir, filename1)
week1_df.to_csv(file_path1, index=False)
# week1_df_filtered = week1_df[week1_df['channel'].isin(channels)]

# Define viewing windows
# TODO: Automatically search for viewing windows dates for each week
# TODO: Automatically search for viewing windows outside of Saturday
viewing_windows = {
    # 'Week_0' : ('2024-08-24', '11:00', '23:59'),
    'Thursday': ('2024-08-29', '11:00', '23:59'),
    'Friday': ('2024-08-30', '11:00', '23:59'),
    'Sat Noon': ('2024-08-31', '11:00', '14:29'),
    'Sat Afternoon': ('2024-08-31', '14:30', '17:59'),
    'Sat Evening': ('2024-08-31', '18:00', '20:59'),
    'Sat Late Night': ('2024-08-31', '21:00', '23:59'),
    'Sunday': ('2024-09-01', '11:00', '23:59'),
    'Monday': ('2024-09-02', '11:00', '23:59')
}


# Function to filter dataframe based on date and time range
def filter_by_time(df, date, start_time, end_time):
    mask = (df['date'] == date) & (df['time (et)'] >= start_time) & (df['time (et)'] <= end_time)
    filtered_df = df[mask]

    # Sort the filtered DataFrame by 'score' column
    sorted_df = filtered_df.sort_values(by='score', ascending=False)

    return sorted_df


# Create a dictionary to hold dataframes for each viewing window
viewing_dfs = {window: filter_by_time(week1_df, date, start, end)
               for window, (date, start, end) in viewing_windows.items()}

# print(viewing_dfs['Sat Noon'].head(10))

# Save each DataFrame to a separate CSV file
for name, df in viewing_dfs.items():
    filename = f"{name}.csv"
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, index=False)
