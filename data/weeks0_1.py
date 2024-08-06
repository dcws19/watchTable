import pandas as pd
from data import cfb_sched_import
from helpers.process_dates import process_dates

# Import games and pull right columns
week0_1_json = cfb_sched_import.games_api.get_games(year=2024, division='fbs', week=1)
week0_1_df = pd.DataFrame.from_records([dict(home_team=w.home_team,
                                             away_team=w.away_team,
                                             home_conference=w.home_conference,
                                             away_conference=w.away_conference,
                                             home_elo=w.home_pregame_elo,
                                             away_elo=w.away_pregame_elo,
                                             start_date=w.start_date,
                                             start_time_tbd=w.start_time_tbd)
                                        for w in week0_1_json])

# Create date and time columns separated
week0_1_df = process_dates(week0_1_df)

# Create week 0 and week 1 dfs, dropping games w/o start_times
week0_1_df_stamped = week0_1_df
week0_1_df_stamped['date'] = pd.to_datetime(week0_1_df_stamped['date'])
week0_1_df_stamped = week0_1_df_stamped[week0_1_df_stamped['start_time_tbd'] == False]
week0_1_df_stamped.drop(columns=['start_time_tbd'], inplace=True)
ts = pd.Timestamp('2024-08-27')
week0_df = week0_1_df_stamped[week0_1_df_stamped['date'] < ts]
week1_df = week0_1_df_stamped[week0_1_df_stamped['date'] > ts]

# Run in python console w/ Opt+Shift+E
