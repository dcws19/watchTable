import pandas as pd
from helpers import cfb_sched_import, get_week_num
from helpers.process_dates import process_dates

this_week = get_week_num.get_week_number()

# Import games and pull right columns
week_json = cfb_sched_import.games_api.get_games(year=2024, division='fbs', week=this_week)
week_df = pd.DataFrame.from_records([dict(home_team=w.home_team,
                                          away_team=w.away_team,
                                          home_conference=w.home_conference,
                                          away_conference=w.away_conference,
                                          home_elo=w.home_pregame_elo,
                                          away_elo=w.away_pregame_elo,
                                          start_date=w.start_date,
                                          start_time_tbd=w.start_time_tbd)
                                     for w in week_json])

# Create date and time columns separated
week_df = process_dates(week_df)

# Create this_week df, dropping games w/o start_times & in week 0 (if needed)
week_df_stamped = week_df
week_df_stamped['date'] = pd.to_datetime(week_df_stamped['date'])
week_df_stamped = week_df_stamped[week_df_stamped['start_time_tbd'] == False]
week_df_stamped.drop(columns=['start_time_tbd'], inplace=True)
week_df_stamped.drop(week_df_stamped[week_df_stamped['date'] == '2024-08-24'].index,inplace=True)

# Run in python console w/ Opt+Shift+E
file_path = f'/Users/JMM/Documents/GitHub/watchTable/outputs/full{this_week}.csv'
week_df_stamped.to_csv(file_path, index=False)
