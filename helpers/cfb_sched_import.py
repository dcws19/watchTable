import cfbd

# Starting guide at https://blog.collegefootballdata.com/introduction-to-cfb-analytics/
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'Kz3FIyreYHzvIBkdFxEowdPiEVY7dEnRnhDVya5Rrd6drE1UaA262N7+ZGtC0mal'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_config = cfbd.ApiClient(configuration)

# Set up games api, then pull in week 1 (+week 0) info
games_api = cfbd.GamesApi(api_config)
rankings_api = cfbd.RankingsApi(api_config)  # work in progress
ratings_api = cfbd.RatingsApi(api_config)  # work in progress
