import pandas as pd
from helpers import cfb_sched_import, get_week_num
from helpers.process_dates import process_dates


def create_weekly_game_csv(output_dir):
    # Get the current week number
    this_week = get_week_num.get_week_number()

    # Import games and pull the relevant columns
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

    # Process the dates to create separate date and time columns
    week_df = process_dates(week_df)

    # Filter the DataFrame to exclude games without start times and games in week 0
    week_df_stamped = week_df.copy()
    week_df_stamped['date'] = pd.to_datetime(week_df_stamped['date'])
    week_df_stamped = week_df_stamped[week_df_stamped['start_time_tbd'] == False]
    week_df_stamped.drop(columns=['start_time_tbd'], inplace=True)
    week_df_stamped.drop(week_df_stamped[week_df_stamped['date'] == '2024-08-24'].index, inplace=True)

    # Define the output file path
    file_path = f'{output_dir}/full{this_week}.csv'

    # Save the DataFrame to a CSV file
    week_df_stamped.to_csv(file_path, index=False)
    print(f"CSV file created at: {file_path}")

# Example function call
# create_weekly_game_csv(output_dir='/Users/JMM/Documents/GitHub/watchTable/outputs')
