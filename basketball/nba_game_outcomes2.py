import requests
from bs4 import BeautifulSoup
import os
import csv

# First function takes NBA team as input ("DEN"), scrapes game outcome data for a given season, and outputs a CSV

def scrape_game_outcomes(team):
    season = "2023"
    url= f'https://www.basketball-reference.com/teams/{team}/{season}_games.html'
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table that contains the box score data
        table = soup.find('table', {'id': 'games'})

        if table:
            # Extract the data from the table
            rows = table.find_all('tr')
            data = []
            for row in rows[1:]:
                # Grab the following columns and process the data
                columns = row.find_all('td')
                if len(columns) >= 5:
                    game_date = columns[0].text
                    start_time = columns[1].text
                    location_value = columns[4].text
                    if location_value == "@":
                        location = "Away"
                    else: location = "Home"
                    opponent = columns[5].text
                    outcome_value = columns[6].text
                    if outcome_value == "L":
                        outcome = "Loss"
                    elif outcome_value == "W":
                        outcome = "Win"
                    else: outcome = "..."
                    game_length_value = columns[7].text
                    if game_length_value == "OT":
                        game_length = "Overtime"
                    else: game_length = "Normal"
                    team_score = columns[8].text
                    opponent_score = columns[9].text
                    total_wins = columns[10].text
                    total_losses = columns[11].text
                    win_loss_streak = columns[12].text
                    
                    # Add the data to the list
                    data.append([season, team, game_date, start_time, location, opponent, outcome, game_length, team_score, opponent_score, total_wins, total_losses, win_loss_streak])
            
            # Define location and file name for data output CSV files
            folder_path = 'C:\\Users\\gusca\\Code Outputs\\Basketball\\Game Outcomes'
            file_name = f'{team} {season} Regular Season.csv'
            file_path = os.path.join(folder_path, file_name)

            # Write the data to a CSV file
            #file_path = f'{player_name} {season} Regular Season.csv'
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Season", "Team", "Game Date", "Start Time", "Location", "Opponent","Outcome", "Game Length", "Team Score", "Opponent Score", "Wins", "Losses", "Win/Loss Streak"])
                writer.writerows(data)

            print(f"Data saved to {file_path}.")
            
        else:
            print(f"Couldn't find game outcomes for {team}.")
    else:
        print(f"Website wasn't up when searching for {team} game outcomes.")

# scrape_game_outcomes("LAC")

# Second function generates a list of NBA teams and iterates the values of that list through the scraper function above

def generate_team_list(team_list_file_path):
    with open(team_list_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            team = row[0]  # Assuming the team name is in the first column
            scrape_game_outcomes(team)

# Define location and file name for list of NBA teams.
folder_path = 'C:\\Users\\gusca\\Code Outputs\\Basketball'
file_name = 'nba_teams.csv'
team_list_file_path = os.path.join(folder_path, file_name)

team = generate_team_list(team_list_file_path)