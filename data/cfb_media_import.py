import requests
import pandas as pd
from io import StringIO

url = "https://api.collegefootballdata.com/games/media"

querystring = {"year": "2024", "week": "1"}

payload = ""
headers = {"Authorization": "Bearer Kz3FIyreYHzvIBkdFxEowdPiEVY7dEnRnhDVya5Rrd6drE1UaA262N7+ZGtC0mal"}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

json_data = StringIO(response.text)

week1_media = pd.read_json(json_data)
