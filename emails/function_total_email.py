import pandas as pd
import glob
import os
import shutil
from helpers import get_week_num, send_email


def generate_and_send_report(csv_directory, email, user):
    # Define the viewing order for the week
    viewing_order = ['Tue', 'Wed', 'Thu', 'Fri',
                     'Sat Noon', 'Sat Afternoon', 'Sat Evening', 'Sat Late Night', 'Sun', 'Mon']

    # Initialize HTML content
    html_content = """
    <html>
    <head>
        <style>
            table {width: 100%; border-collapse: collapse; margin-bottom: 20px;}
            th, td {border: 1px solid black; padding: 8px; text-align: left;}
            th {background-color: #f2f2f2;}
            h2 {font-family: Arial, sans-serif; color: #333;}
        </style>
    </head>
    <body>
    """

    # Dictionary to store top 5 games from each viewing window
    top_games = {}

    # Stash away the full file in archive
    dest_directory = '/Users/JMM/Documents/GitHub/watchTable/archive/fullFiles'

    # Delete the original full file
    try:
        # Iterate over all files in the specified directory
        for filename in os.listdir(csv_directory):
            # Check if "full" is in the file name
            if "full" in filename:
                file_path = os.path.join(csv_directory, filename)
                destination_path = os.path.join(dest_directory, filename)
                shutil.move(file_path, destination_path)
                print(f"Moved: {file_path} to {destination_path}")
            else:
                print(f"Skipped: {filename} (no 'full' in name)")
    except Exception as e:
        print(f"Error processing directory: {csv_directory}. Error: {e}")

    # Get a list of all CSV files in the directory
    csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

    # Process each CSV file to find the top 5 games
    for csv_file in csv_files:
        # Extract the viewing window name from the filename
        viewing_window = os.path.basename(csv_file).replace('.csv', '')

        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Sort DataFrame by game score
        df_sorted = df.sort_values(by='score', ascending=False).head(5)

        # Store the top 5 games in the dictionary
        top_games[viewing_window] = df_sorted

    # Generate the HTML content based on the desired viewing order
    for window in viewing_order:
        if window in top_games:
            df_sorted = top_games[window]

            # Create an HTML table for the viewing window
            html_content += f"<h2>Viewing Window: {window}</h2>"
            html_content += "<table>"
            html_content += "<tr><th>Score</th><th>Home Team</th><th>Away Team</th><th>Date</th><th>Time (ET)</th><th>Outlet</th></tr>"

            for index, row in df_sorted.iterrows():
                html_content += f"<tr><td>{row['score']}</td><td>{row['home_team']}</td><td>{row['away_team']}</td><td>{row['date']}</td><td>{row['time (et)']}</td><td>{row['outlet']}</td></tr>"

            html_content += "</table>"

    # Close the HTML tags
    html_content += """
    </body>
    </html>
    """

    # Get the current week number
    this_week = get_week_num.get_week_number()
    print(this_week)

    # Specify the file path for the HTML file
    html_path = os.path.join(csv_directory, f'week{this_week}_report.html')
    subject = f'Week {this_week} CFB Watch Tables for {user}'

    # Write the HTML content to the file
    with open(html_path, 'w') as file:
        file.write(html_content)

    print(f"HTML file created at: {html_path}")

    # Send the email with the generated HTML report
    send_email.send_email(html_file_path=html_path, subject=subject, to_email=email)


# Example function call
"""generate_and_send_report(
    csv_directory='/Users/JMM/Documents/GitHub/watchTable/outputs',
    email='jack@morrisroe.org',
    user='Jack'
)"""
