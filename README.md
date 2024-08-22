# watchTable

Creating personalized recommendations
for the most watchable college football games.

Currently, it can send an email of the top X best games per viewing window using manual processes.

I would like to automatically send recommendations each Friday morning to each person with a profile. (Github actions?)

In the future, I'd like to create a DashApp where users can input their preferences and view their recommendations.

Thank you to collegefootballdata.com for the wonderful API.
# Features

Preferred conferences
- SEC #1
- ACC #2
- B1G #3, etc.

Preferred teams
- Mizzou #1
- VT #2
- Army #3, etc.

Close games 
- ELO difference

Best teams
- ELO added up

TV/Web channels available
- Network TV (ABC, NBC, FOX, CBS)
- Individ. cable (SECN, B1GTV, ESPN, etc.)
- Individ. web (ESPN+, Peacock, etc.)

### Break up by viewing windows
- Non-Saturdays
- noon-2
- 3-5
- 6-9
- 10+

### UPCOMING: Choose weights for each option
- Teams 50 %
- Close 25 %
- Confs 15 %
- Best 10 %
- Include only TV/Web available
