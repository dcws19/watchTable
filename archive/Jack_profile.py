# Pre-define categories of game media
broadcast = ['ABC', 'CBS', 'NBC', 'FOX']
cable = ['CBSSN', 'ESPN', 'FS1', 'ESPNU', 'ACCN', 'BTN', 'SECN']
web = ['ESPN+', 'SECN+', 'BIG12|ESPN+', 'ACCNX']

# Define the user's preferences
preferred_teams = ['Missouri', 'Virginia Tech', 'Army']
preferred_conferences = {'SEC': 1}
weights = {'teams': 40, 'close': 20, 'conferences': 5, 'best': 35}
channels = broadcast + cable + web
