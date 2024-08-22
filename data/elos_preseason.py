import pandas as pd

# Import df with elos
# TODO: Search for week 1 and its ELOs for testing purposes
elo_path = '/Users/JMM/Documents/GitHub/watchTable/outputs/full1.csv'
df = pd.read_csv(elo_path)
home = df[['home_team', 'home_elo']]
away = df[['away_team', 'away_elo']]

home.rename(columns={'home_team': 'team', 'home_elo': 'elo'}, inplace=True)
away.rename(columns={'away_team': 'team', 'away_elo': 'elo'}, inplace=True)

elos = pd.concat([home, away])
elos.dropna(inplace=True)
