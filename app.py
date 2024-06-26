# imorting
import pandas as pd
import streamlit as st
import random
import pickle

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 500)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

# Page Title and Page Icon
st.set_page_config(layout= "wide", page_title= "DREAM MATCH", page_icon= "🏀")


# Page Header
st.markdown("<h1 style='text-align: center;'>🏀 <font color='red'>DREAM MATCH</font> 🏀</h1>", unsafe_allow_html=True)

# Page Arrangement
main_tab = st.tabs(["Home"])
home_content = main_tab[0]
left_main_col, right_main_col = home_content.columns(2)

# Loading Python Objects
with open("df.pkl","rb") as file:
    df = pickle.load(file)

with open("dt.pkl","rb") as file:
    dt = pickle.load(file)


# This function allows the creation of two teams of 12 players, with the team captain being an NBA star.
def team_selection(df):
    df_star_player = df.loc[(df["League"] == "NBA") & (df["PPM"] > 30)]
    captains = df_star_player["index"].drop_duplicates().sample(n=2)
    captains_list = captains.tolist()

    other_players = df[~df["index"].isin(captains_list)]
    other_players_1 = other_players["index"].drop_duplicates().sample(n=11)
    other_players_2 = other_players["index"].drop_duplicates().sample(n=11)

    team_a = [captains.iloc[0]] + other_players_1.tolist()
    team_b = [captains.iloc[1]] + other_players_2.tolist()
    return team_a, team_b

team_a,team_b = team_selection(df)

# This function shows the teams
def show_teams(team_a, team_b):
    team_a_players = dt.iloc[team_a].reset_index().drop(columns=["index"])
    team_a_players = team_a_players.rename(columns={"Season-Player": "TEAM A"})

    team_b_players = dt.iloc[team_b].reset_index().drop(columns=["index"])
    team_b_players = team_b_players.rename(columns={"Season-Player": "TEAM B"})
    return team_a_players, team_b_players
team_a_players, team_b_players = show_teams(team_a, team_b)

# It allows each player's time to be adjusted to a minimum of 10 and a maximum of 40 minutes. It also ensures that the total time of each team's players is 200 minutes.
def player_times(team_a,team_b):
    
    total_time = 200
    min_time = 10
    max_time = 40
    team_a_df = pd.DataFrame({"index": team_a})
    team_a_df["MP"] = 0

    while True:
        
        team_a_df["MP"] = [random.randint(min_time, max_time) for _ in range(len(team_a))]

        
        if team_a_df["MP"].sum() == total_time:
            break

    team_b_df = pd.DataFrame({"index": team_b})
    team_b_df["MP"] = 0

    while True:
        
        team_b_df["MP"] = [random.randint(min_time, max_time) for _ in range(len(team_b))]

       
        if team_b_df["MP"].sum() == total_time:
            break

    return team_a_df, team_b_df

team_a_df, team_b_df = player_times(team_a,team_b)

# Makes edits to team dataframes
def last_team_app(team_a,team_b):
    
    team_a = df.loc[team_a]
    team_b = df.loc[team_b]


    team_a.reset_index(inplace=True)
    team_b.reset_index(inplace=True)

    team_a = pd.concat([team_a, team_a_df], axis=1)
    team_b = pd.concat([team_b, team_b_df], axis=1)

    team_a.drop(columns=["index"], inplace=True)
    team_b.drop(columns=["index"], inplace=True)

    team_a = team_a.rename(columns={'level_0': 'index'})
    team_b = team_b.rename(columns={'level_0': 'index'})

    return team_a, team_b

team_a,team_b = last_team_app(team_a, team_b)

# Creates the statistics of the players in this match.
def game_stats(team_a, team_b):
    team_a["MatchPoint"] = ((team_a["MP"] * (team_a["y_pred_point"])) / team_a["y_pred_minute"]).astype(
        int)
    team_b["MatchPoint"] = ((team_b["MP"] * (team_b["y_pred_point"])) / team_b["y_pred_minute"]).astype(
        int)

    team_a["MatchRebound"] = ((team_a["MP"] * (team_a["y_pred_rebound"])) / team_a["y_pred_minute"]).astype(
        int)
    team_b["MatchRebound"] = ((team_b["MP"] * (team_b["y_pred_rebound"])) / team_b["y_pred_minute"]).astype(
        int)

    team_a["MatchAsist"] = ((team_a["MP"] * (team_a["y_pred_asist"])) / team_a["y_pred_minute"]).astype(
        int)
    team_b["MatchAsist"] = ((team_b["MP"] * (team_b["y_pred_asist"])) / team_b["y_pred_minute"]).astype(
        int)

    team_a["MatchBlock"] = ((team_a["MP"] * (team_a["y_pred_block"])) / team_a["y_pred_minute"]).astype(int)
    team_b["MatchBlock"] = ((team_b["MP"] * (team_b["y_pred_block"])) / team_b["y_pred_minute"]).astype(int)

    team_a["MatchTOV"] = ((team_a["MP"] * (team_a["y_pred_tov"])) / team_a["y_pred_minute"]).astype(int)
    team_b["MatchTOV"] = ((team_b["MP"] * (team_b["y_pred_tov"])) / team_b["y_pred_minute"]).astype(int)

    team_a["MatchSteal"] = ((team_a["MP"] * (team_a["y_pred_steal"])) / team_a["y_pred_minute"]).astype(int)
    team_b["MatchSteal"] = ((team_b["MP"] * (team_b["y_pred_steal"])) / team_b["y_pred_minute"]).astype(int)

    team_a["MatchFoul"] = ((team_a["MP"] * (team_a["y_pred_foul"])) / team_a["y_pred_minute"]).astype(
        int)
    team_b["MatchFoul"] = ((team_b["MP"] * (team_b["y_pred_foul"])) / team_b["y_pred_minute"]).astype(
        int)

    return team_a, team_b
team_a, team_b = game_stats(team_a, team_b)

# Shows the statistics of the players in this match.
def match_stats(team_a, team_b):

    team_a_indexes = team_a["index"].to_list()
    team_b_indexes = team_b["index"].to_list()
    team_A = pd.DataFrame(dt.iloc[team_a_indexes]["Season-Player"]).reset_index()
    team_B = pd.DataFrame(dt.iloc[team_b_indexes]["Season-Player"]).reset_index()

    match_stats_team_a = pd.concat([team_A[['Season-Player']], team_a[['MP', 'MatchPoint', 'MatchRebound', 'MatchAsist', 'MatchBlock', 'MatchTOV', 'MatchSteal', 'MatchFoul']]], axis=1)
    match_stats_team_b = pd.concat([team_B[['Season-Player']], team_b[['MP', 'MatchPoint', 'MatchRebound', 'MatchAsist', 'MatchBlock', 'MatchTOV', 'MatchSteal', 'MatchFoul']]], axis=1)

    column_names = {'Season-Player': 'PLAYER', 'MP': 'MINUTE', 'MatchPoint': 'POINT', 'MatchRebound': 'REBOUND', 'MatchAsist': 'ASSIST', 'MatchBlock': 'BLOCK', 'MatchTOV': 'TURNOVER', 'MatchSteal': 'STEAL', 'MatchFoul': 'FOUL'}
    match_stats_team_a = match_stats_team_a.rename(columns=column_names)
    match_stats_team_b = match_stats_team_b.rename(columns=column_names)

    return  match_stats_team_a, match_stats_team_b


team_a_stats, team_b_stats = match_stats(team_a, team_b)


# Shows the total points of the teams in this match.
def team_points(team_a, team_b):
    team_a_total_point = team_a["MatchPoint"].sum()
    team_b_total_point = team_b["MatchPoint"].sum()
    return team_a_total_point, team_b_total_point

team_a_total_point,team_b_total_point=team_points(team_a, team_b)

# Shows the winning team
def winner_loser(team_a_total_point, team_b_total_point):
    if team_a_total_point > team_b_total_point:
        return ("TEAM A WON!\n\n" +
                "TEAM A : " + str(team_a_total_point) + "  -  " "TEAM B : " + str(team_b_total_point))
    elif team_a_total_point < team_b_total_point:
        return ("TEAM B WON!\n\n" +
                "TEAM A : " + str(team_a_total_point) + "  -  " "TEAM B : " + str(team_b_total_point))
    else:
        team_b_total_point += 1
        return ("TEAM B WON!\n\n" +
                "TEAM A : " + str(team_a_total_point) + "  -  " "TEAM B : " + str(team_b_total_point)) 



result= winner_loser(team_a_total_point, team_b_total_point)




def main():

    session_state = st.session_state
    
    if 'team_a' not in session_state:
        session_state.team_a = None
    if 'team_b' not in session_state:
        session_state.team_b = None

   # Creation of "SELECT TEAMS" button 
    if left_main_col.button("SELECT TEAMS"):
        team_a, team_b = team_selection(df)  
        team_a_players, team_b_players = show_teams(team_a, team_b)  
        session_state.a_takimi = team_a 
        session_state.team_b = team_b  

       
        teams_col1, teams_col2 = st.columns(2)
        with teams_col1:
            st.write(team_a_players)
        with teams_col2:
            st.write(team_b_players)



    # Creation of "START MATCH" button 
    if right_main_col.button("START MATCH"):
        team_a = session_state.a_takimi 
        team_b = session_state.team_b 
        if team_a is not None and team_b is not None:
            team_a_df, team_b_df = player_times(team_a, team_b)
            team_a, team_b = last_team_app(team_a, team_b)
            team_a, team_b = game_stats(team_a, team_b)
            team_a_total_point, team_b_total_point = team_points(team_a, team_b)
            result = winner_loser(team_a_total_point, team_b_total_point)
            st.write(result)
            team_a, team_b = game_stats(team_a, team_b)
            team_a_stats, team_b_stats = match_stats(team_a, team_b)

            
            stats_col1, stats_col2 = st.columns(2)
            with stats_col1:
                st.write(team_a_stats)
            with stats_col2:
                st.write(team_b_stats)


if __name__ == "__main__":
    main()









