# these three import commands below envoke functionality from python libraries.
# in the case of the bs4 library, we are importing a specific part, "BeautifulSoup."
# by using the from command with the import command, we no longer need to prefix
# commands from the bs4 library with the "bs4." prefix. we will still need to do that 
# for commands from the requests and csv libraries. using from to eliminate prefixes
# is dangerous to do too much though, as some libraries may have identical commands
# so lopping off their prefixes can introduce ambiguity and bonk your code.

import requests
from bs4 import BeautifulSoup
import os
import csv

def scrape_game_log(player_name):
    season = "2023"
    player_lastname_initial = player_name[0].lower()
    last_name, first_name = player_name.split(", ")
    last_name_first_five = last_name[:5].lower()
    first_name_first_two = first_name[:2].lower()
    player_id = last_name_first_five + first_name_first_two + "01"
    url = f'https://www.basketball-reference.com/players/{player_lastname_initial}/{player_id}/gamelog/{season}/'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table that contains the box score data
        table = soup.find('table', {'id': 'pgl_basic'})

        if table:
            # Extract the data from the table
            rows = table.find_all('tr')
            data = []
            for row in rows[1:]:
                # Grab the following columns and process the data
                columns = row.find_all('td')
                if len(columns) >= 29:
                    game_count = columns[0].text
                    date = columns[1].text
                    player_age = columns[2].text
                    team = columns[3].text
                    
                    location_value = columns[4].text
                    if location_value == "@":
                        location = "Away"
                    else:
                        location = "Home"
                        
                    opponent = columns[5].text
                    streak = columns[6].text
                    
                    game_entrance_value = columns[7].text
                    if game_entrance_value == "1":
                        game_entrance = "Starter"
                    else:
                        game_entrance = "Off Bench"
                    
                    player_minutes = columns[8].text
                    field_goals_made = columns[9].text
                    field_goals_attempted = columns[10].text
                    field_goal_percentage = columns[11].text
                    three_pointers_made = columns[12].text
                    three_pointers_attempted = columns[13].text
                    three_point_percentage = columns[14].text
                    free_throws_made = columns[15].text
                    free_throws_attempted = columns[16].text
                    free_throw_percentage = columns[17].text
                    rebounds_offensive = columns[18].text
                    rebounds_defensive = columns[19].text
                    rebounds_total = columns[20].text
                    assists = columns[21].text
                    steals = columns[22].text
                    blocks = columns[23].text
                    turnovers = columns[24].text
                    personal_fouls = columns[25].text
                    points = columns[26].text
                    hollinger_score = columns[27].text
                    plus_minus = columns[28].text
                    
                    # Add the data to the list
                    data.append([season, player_name, game_count, date, player_age, team, location, opponent, streak, game_entrance, player_minutes, field_goals_made, field_goals_attempted, field_goal_percentage, three_pointers_made, three_pointers_attempted, three_point_percentage, free_throws_made, free_throws_attempted, free_throw_percentage, rebounds_offensive, rebounds_defensive, rebounds_total, assists, steals, blocks, turnovers, personal_fouls, points, hollinger_score, plus_minus])
            
            # Change this folder path to make sense on whatever computer you're running this code on.
            folder_path = 'C:\\Users\\gcaravalho\\Code\\Python\\Basketball\\Game Log CSVs'
            file_name = f'{player_name} {season} Regular Season.csv'

            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)

            # Write the data to a CSV file
            #file_path = f'{player_name} {season} Regular Season.csv'
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Season", "Player", "Game Count","Date","Player Age", "Team", "Location", "Opponent", "Streak", "Game Entrance", "Player Minutes", "Field Goals Made", "Field Goals Attempted", "Field Goal Percentage", "Three Pointers Made", "Three Pointers Attempted", "Three Point Percentage", "Free Throws Made", "Free Throws Attempted", "Free Throw Percentage", "Rebounds Offensive", "Rebounds Defensive", "Rebounds Total", "Assists", "Steals", "Blocks", "Turnovers", "Personal Fouls", "Points", "Hollinger Score", "Plus Minus"])
                writer.writerows(data)

            print(f"Data saved to {file_path}.")
        else:
            print("Game log table not found.")
    else:
        print("Website broke.")

# Call the function with the player's name
scrape_game_log("Butler, Jimmy")