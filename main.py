import json
import openai
import json
from helpers import *


def main(team1, team2):
    match_date = next_game(team1, team2)

    # Handle scenario where there is no scheduled match found
    if not match_date:
        return json.dumps(
            {
                "date": "No game scheduled",
                "home": None,
                "winner": None,
                "reason": [None, None, None],
            }
        )

    # Call the functions in helpers.py
    rankings = EPL_table()
    ELOs = ELO()
    BBC_articles = scrape_bbc_sport(team1, team2)
    comments = youtube_comments(team1, team2)

    # Handle not having any comments (due to no videos with a team's name in the title).
    if comments is None:
        comments = ([], [])

    # Add the match information to the data
    match_info = {
        "team1": team1,
        "team2": team2,
        "date": match_date[0],
        "home team": match_date[1],
    }

    final_data = {
        "match_info": match_info,
        "rankings": rankings,
        "ELOs": ELOs,
        "articles": BBC_articles,
        "team1 comments": comments[0],
        "team2 comments": comments[1],
    }

    # Convert to JSON for easy parsing in the next step
    json_data = json.dumps(final_data, indent=2)

    # Send prompt to OpenAI API with relevant information provided at the end
    messages = [
        {
            "role": "system",
            "content": """You are a professional football analyst who has an ability to predict the result of football matches in the premier league. You do this by analysing both of the teams playing, looking at their ranking, ELO, home vs away, and sentiment for how the team is performing which you glean from youtube comments. \n
         
         Work through the information given to you and us it to make an informed decision for who you think will win the match between 'team1' and 'team2'. Give your answer as a JSON response with 4 keys: date, home, winner, reason. The value for date should be solely the date that the match is scheduled to take place. The value for home team should be the team playing at home. The value for winner should solely return the name of the team that you think will win the match. The value for the reasons should be a list of three items which are the top 3 reasons for you making the decision that you did. Please be as specific as possible, and ensure that you verify any reason with the data that you have been provided. Do not make any false claims with respect to the data.

         Make sure to ONLY provide the JSON response as specified. There should be no additional content.
         """,
        },
        {
            "role": "user",
            "content": f"""The match data will be given to you in the following format. Firstly you will be given some information about the match, tagged 'match_info'. Then you will be given an up to date dictionary with key value pair of a team's name followed by their current points in the league (where more points = higher position in the league). This is acurate data so treat it as legitimate. Next you will be given each team's ELO rating, again in a dictionary pair where the key is the team name and the value is their ELO. Be aware that being the home team increases your ELO by 55 points. Additionally, a higher ELO rating indicates a better team. You should bear this in mind for your analysis. Next you will be given some BBC articles about each of the teams, which will give you information about current transfers within each of the clubs. Finally you will be given 'team1 comments' and 'team2 comments' which is the top 10 comments from the top 10 youtube videos for each of the clubs playing. You can use these comments to guage how positive fans are for each club, as this will represent their respective form. \n
        
        Here is the Match Data: {json_data}.""",
        },
    ]

    print("Sending request to OpenAI API...")
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=500)
    print("Response received from OpenAI API")

    reply = response.choices[0].message.content.strip()  # strip() removes trailing and starting whitespace
    return reply
