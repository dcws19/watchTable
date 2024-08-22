


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