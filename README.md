# DREAM MATCH STREAMLIT APP
In this study, it is aimed to predict which team will win the match between two randomly formed teams, 
whose team captains will be NBA legends and the remaining players will be from NBA, Euroleague and Eurocup leagues, 
and the statistics of the players in this match. The project was also imported into the prod environment via steramlit.

## Dataset Description
- League: League

- Season: Season

- Player: Player

- Team: Team

- GP: Games Played

- MIN: Minutes Played

- birth_year: Birth Year

- birth_month: Birth Month

- birth_date: Birth Date

- height: Height

- height_cm: Height (cm)

- weight: Weight

- weight_kg: Weight (kg)

- nationality: Nationality

- high_school: High School

- FGM: Field Goals Made

- FGA: Field Goals Attempted

- 3PM: 3-Point Field Goals Made

- 3PA: 3-Point Field Goals Attempted

- FTM: Free Throws Made

- FTA: Free Throws Attempted

- TOV: Turnovers

- PF: Personal Fouls

- ORB: Offensive Rebounds

- DRB: Defensive Rebounds

- REB: Total Rebounds

- AST: Assists

- STL: Steals

- BLK: Blocks

- PTS: Points

- draft_round: Draft Round

- draft_pick: Draft Pick

- draft_team: Draft Team

- 3PR: 3-Point Field Goal Percentage

- FGR: Field Goal Percentage

- PPM: Points Per Minute

- RPM: Rebounds Per Minute

- SPM: Steals Per Minute

- APM: Assists Per Minute

- BPM: Blocks Per Minute

- MPM: Minutes Per Game

## Methodology
1. **Exploratory Data Analysis (EDA):** Reviewing the complete dataset involves identifying both numerical and categorical variables, and conducting an analysis on their distribution.
2. **Feature Engineering:** Missing and outlier values ​​were edited. New variables have been created. Encoding operations have been completed.
3. **Model Building:** Modeling was done and the section up to this point was converted into a pkl file.
4. **Streamlit:** The necessary functions for establishing teams and playing the match were written and the application was brought to the live environment with streamlit.

## Streamlit App
You can also select teams and start a match via the link below.

https://dreammatch.streamlit.app/
