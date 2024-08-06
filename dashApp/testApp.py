import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

# Load data
file_path = 'outputs/full.csv'
data = pd.read_csv(file_path)

# Initialize the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('College Football Games'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        page_size=10,
        sort_action='native',  # Enable sorting
        filter_action='native'  # Enable filtering
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
