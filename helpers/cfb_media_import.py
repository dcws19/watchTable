import requests
import pandas as pd
from io import StringIO
from helpers import get_week_num

url = "https://api.collegefootballdata.com/games/media"

this_week = get_week_num.get_week_number()
print(this_week)

querystring = {"year": "2024", "week": str(this_week)}

payload = ""
headers = {"Authorization": "Bearer Kz3FIyreYHzvIBkdFxEowdPiEVY7dEnRnhDVya5Rrd6drE1UaA262N7+ZGtC0mal"}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

json_data = StringIO(response.text)

this_week_media = pd.read_json(json_data)
