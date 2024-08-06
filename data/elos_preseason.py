import pandas as pd
from data import weeks0_1

# Import df with elos
df = weeks0_1.week0_1_df
home = df[['home_team', 'home_elo']]
away = df[['away_team', 'away_elo']]

home.rename(columns={'home_team': 'team', 'home_elo': 'elo'}, inplace=True)
away.rename(columns={'away_team': 'team', 'away_elo': 'elo'}, inplace=True)

elos = pd.concat([home, away])
elos.dropna(inplace=True)
