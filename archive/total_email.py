import pandas as pd
import glob
import os
from helpers import get_week_num, send_email

# Directory where CSV files are stored
csv_directory = os.path.join('/outputs')

# Get a list of all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

viewing_order = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat Noon', 'Sat Afternoon', 'Sat Evening', 'Sat Late Night', 'Sun', 'Mon']

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

# Delete the original full file
try:
    # Iterate over all files in the specified directory
    for filename in os.listdir(csv_directory):
        # Check if "full" is in the file name
        if "full" in filename:
            file_path = os.path.join(csv_directory, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"Skipped: {filename} (no 'full' in name)")
except Exception as e:
    print(f"Error processing directory: {csv_directory}. Error: {e}")

for csv_file in csv_files:
    # Extract the viewing window name from the filename
    viewing_window = os.path.basename(csv_file).replace('.csv', '')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Sort DataFrame by game score
    df_sorted = df.sort_values(by='score', ascending=False).head(5)

    # Store the top 5 games in the dictionary
    top_games[viewing_window] = df_sorted

# TODO: Add index instead of score
# Now generate the HTML content based on the desired viewing order
for window in viewing_order:
    if window in top_games:
        df_sorted = top_games[window]

        # Create an HTML table for the viewing window
        html_content += f"<h2>Viewing Window: {window}</h2>"
        html_content += "<table>"
        html_content += "<tr><th>score</th><th>home_team</th><th>away_team</th><th>date</th><th>time (et)</th><th>outlet</th></tr>"

        for index, row in df_sorted.iterrows():
            html_content += f"<tr><td>{row['score']}</td><td>{row['home_team']}</td><td>{row['away_team']}</td><td>{row['date']}</td><td>{row['time (et)']}</td><td>{row['outlet']}</td></tr>"

        html_content += "</table>"

# Close the HTML tags
html_content += """
</body>
</html>
"""

# Specify the file path for the HTML file
this_week = get_week_num.get_week_number()
print(this_week)
html_path = f'/Users/JMM/Documents/GitHub/watchTable/outputs/week{this_week}_report.html'
sub = f'Week {this_week} NCAAF Watch Tables'
email = 'jack@morrisroe.org'

# Write the HTML content to the file
with open(html_path, 'w') as file:
    file.write(html_content)

print(f"HTML file created at: {html_path}")

send_email.send_email(html_file_path=html_path, subject=sub, to_email=email)
