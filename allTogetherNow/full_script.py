import os
import json
from data import function_this_week_games
from rankings import function_this_week_rankings
from emails import function_total_email

# Directory containing user profiles
profiles_dir = 'profiles/'

# Load and process each user profile
for profile_file in os.listdir(profiles_dir):
    if profile_file.endswith('.json'):
        profile_path = os.path.join(profiles_dir, profile_file)

        # Load user preferences
        with open(profile_path, 'r') as f:
            user_preferences = json.load(f)

        # Clear files in outputs
        outputs_dir = 'outputs/'
        try:
            # Iterate over all files in the specified directory
            for filename in os.listdir(outputs_dir):
                file_path = os.path.join(outputs_dir, filename)
                # Check if it's a file (and not a subdirectory)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error processing directory: {outputs_dir}. Error: {e}")

        # Create data for rankings
        function_this_week_games.create_weekly_game_csv(output_dir='/Users/JMM/Documents/GitHub/watchTable/outputs')
        # Run data for this_week and personalized rankings based on profile
        function_this_week_rankings.generate_viewing_schedule(prefs=user_preferences)
        # Build and send personalized recommendations via email
        function_total_email.generate_and_send_report(
            csv_directory='outputs/',
            email=user_preferences['email'],
            user=user_preferences['name']
        )
        print(f"Generated and sent {user_preferences['name']}'s cfb viewing recommendations")

        # Run the rest of your script using these preferences
        # For example, call a function:
        # run_schedule_script(preferred_teams, preferred_conferences, weights, channels)
