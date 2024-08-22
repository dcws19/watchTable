import os
import pandas as pd
from archive import this_week_games
from helpers import cfb_media_import, viewing_windows
# TODO: Split scores for teams, conferences, predicted close games, and predicted best teams to check algorithm


def generate_viewing_schedule(prefs):
    # Extract user preferences
    name = prefs["name"]
    email = prefs["email"]
    preferred_teams = prefs["preferred_teams"]
    preferred_conferences = prefs["preferred_conferences"]
    weights = prefs["weights"]
    channels = prefs["channels"]

    # Pre-define categories of game media
    broadcast = ['ABC', 'CBS', 'NBC', 'FOX']
    cable = ['CBSSN', 'ESPN', 'FS1', 'ESPNU', 'ACCN', 'BTN', 'SECN', "SEC NETWORK", "ACC NETWORK", "BIG10", "TruTV"]
    web = ['ESPN+', 'SECN+', 'BIG12|ESPN+', 'ACCNX', "ACC Extra"]

    # Merge user channels with the pre-defined ones
    all_channels = []
    if "broadcast" in channels:
        all_channels.extend(broadcast)
    if "cable" in channels:
        all_channels.extend(cable)
    if "web" in channels:
        all_channels.extend(web)

    # Add ELO ratings
    # elo_rates = elos_preseason.elos
    # elo_ratings = elo_rates.set_index('team')['elo'].to_dict()
    week_df = this_week_games.week_df_stamped
    # week_df['home_elo'] = week_df['home_team'].map(elo_ratings)
    # week_df['away_elo'] = week_df['away_team'].map(elo_ratings)
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

        # Preferred conferences
        home_conf_score = preferred_conferences.get(row['home_conference'], 0)
        away_conf_score = preferred_conferences.get(row['away_conference'], 0)
        conference_score = max(home_conf_score, away_conf_score)
        score += conference_score * weights['conferences']

        # Close games
        close_game_score = 1 / (1 + row['elo_diff'])  # Inverse of the ELO difference for closeness
        score += close_game_score * weights['close']

        # Best teams
        max_elo = max(week_df['home_elo'].max(), week_df['away_elo'].max())
        best_team_score = (row['home_elo'] + row['away_elo']) / 2
        score += best_team_score / max_elo * weights['best']

        # Zero out game if it doesn't have a channel in user's list
        if not any(channel in row['outlet'] for channel in all_channels):
            score = 0

        return round(score, 2)

    # Apply the scoring function to each game
    week_df['score'] = week_df.apply(score_game, axis=1)

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
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    for name, df in viewing_dfs.items():
        filename = f"{name}.csv"
        file_path = os.path.join(output_dir, filename)
        df.to_csv(file_path, index=False)


# Example: Load user preferences from JSON
# with open('project/profiles/this_profile.json', 'r') as f:
#     user_preferences = json.load(f)

# Generate the viewing schedule
# generate_viewing_schedule(user_preferences)
