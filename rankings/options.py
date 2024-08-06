from data import elos_preseason, weeks_2Plus

# Define the user's preferences
preferred_teams = ['Missouri', 'Virginia Tech', 'Army']
preferred_conferences = {'SEC': 1, 'ACC': 2, 'B1G': 3}
weights = {'teams': 50, 'close': 15, 'conferences': 15, 'best': 20}

# Add ELO ratings
elo_rates = elos_preseason.elos
elo_ratings = elo_rates.set_index('team')['elo'].to_dict()
week14_df = weeks_2Plus.week14_df
week14_df['home_elo'] = week14_df['home_team'].map(elo_ratings)
week14_df['away_elo'] = week14_df['away_team'].map(elo_ratings)

# Calculate the ELO difference for close games
week14_df['elo_diff'] = abs(week14_df['home_elo'] - week14_df['away_elo'])


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
    best_team_score = (row['home_elo'] + row['away_elo']) / 2
    score += best_team_score / max(elo_ratings.values()) * weights['best']

    return score


# Apply the scoring function to each game
week14_df['score'] = week14_df.apply(score_game, axis=1)

# Sort the dataframe by date and score
week14_df = week14_df.sort_values(by=['date', 'time (et)', 'score'], ascending=[True, True, False])

# Display the top and bottom 5 games for a quick overview
top_5_games = week14_df.head(5)
bottom_5_games = week14_df.tail(5)

print(top_5_games, bottom_5_games)

# Define viewing windows
viewing_windows = {
    'Thursday': ('2024-11-28', '11:00', '23:59'),
    'Friday': ('2024-11-29', '11:00', '23:59'),
    'Sat Noon': ('2024-11-30', '11:00', '14:29'),
    'Sat Afternoon': ('2024-11-30', '14:30', '17:59'),
    'Sat Evening': ('2024-11-30', '18:00', '20:59'),
    'Sat Late Night': ('2024-11-30', '21:00', '23:59')
}


# Function to filter dataframe based on date and time range
def filter_by_time(df, date, start_time, end_time):
    mask = (df['date'] == date) & (df['time (et)'] >= start_time) & (df['time (et)'] <= end_time)
    return df[mask]


# Create a dictionary to hold dataframes for each viewing window
viewing_dfs = {window: filter_by_time(week14_df, date, start, end)
               for window, (date, start, end) in viewing_windows.items()}

print(viewing_dfs['Thursday'].head(10))
