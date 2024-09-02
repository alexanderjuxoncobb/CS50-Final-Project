import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import openai
from googleapiclient.errors import HttpError


# API keys removed for security
YOUTUBE_API_KEY = "YOUTUBE_API_KEY"
openai.api_key = "OPENAI_API_KEY"


# Since different sites refer to teams with different names and nicknames
team_name_variations = {
    "Arsenal": ["Arsenal"],
    "Aston Villa": ["Aston Villa", "Villa"],
    "AFC Bournemouth": ["Bournemouth", "AFC Bournemouth"],
    "Brighton and Hove Albion": ["Brighton", "Brighton & Hove Albion"],
    "Brentford": ["Brentford"],
    "Burnley": ["Burnley"],
    "Chelsea": ["Chelsea"],
    "Crystal Palace": ["Crystal Palace", "Palace"],
    "Everton": ["Everton"],
    "Fulham": ["Fulham"],
    "Liverpool": ["Liverpool"],
    "Luton Town": ["Luton", "Luton Town"],
    "Manchester City": ["Manchester City", "Man City", "MCFC"],
    "Manchester United": ["Manchester United", "Man Utd", "Man United"],
    "Newcastle United": ["Newcastle United", "Newcastle"],
    "Nottingham Forest": ["Nottingham Forest", "Nottm Forest"],
    "Sheffield United": ["Sheffield United", "Sheff Utd"],
    "Tottenham Hotspur": ["Tottenham Hotspur", "Tottenham", "Spurs"],
    "West Ham United": ["West Ham United", "West Ham"],
    "Wolverhampton Wanderers": ["Wolverhampton Wanderers", "Wolves"],
}


def next_game(team1, team2):
    url = "https://www.skysports.com/premier-league-fixtures"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    fixtures = soup.find_all("div", class_="fixres__item")

    for fixture in fixtures:
        teams_in_fixture = fixture.find_all("span", class_="swap-text__target")

        team1_in_fixture = teams_in_fixture[0].text
        team2_in_fixture = teams_in_fixture[1].text
        home = team1_in_fixture

        # If both teams are mentioned in the same element there must be a fixture
        if (team1_in_fixture == team1 and team2_in_fixture == team2) or (
            team1_in_fixture == team2 and team2_in_fixture == team1
        ):
            date_parent = fixture.find_previous(
                "h4", class_="fixres__header2"
            )  # Access the parent element to get the date
            if date_parent:
                match_date = date_parent.get_text()
                return match_date, home

    return None


def scrape_bbc_sport(team1, team2):
    url = "https://www.bbc.com/sport/football"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    def get_BBC_article_text(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the article's main text
        paragraphs = soup.find_all("p", class_="ssrcss-1q0x1qg-Paragraph e1jhz7w10")
        article_text = "\n".join([para.text for para in paragraphs])
        return article_text

    # Articles on the homepage in different positions have different classes
    article_links_1 = soup.find_all("a", class_="ssrcss-vdnb7q-PromoLink exn3ah91")
    article_links_2 = soup.find_all("a", class_="ssrcss-zmz0hi-PromoLink exn3ah91")
    article_links_3 = soup.find_all("a", class_="ssrcss-1b1mki6-PromoHeadline exn3ah96")
    articles = article_links_1 + article_links_2 + article_links_3

    selected_articles = []
    if articles:
        team1_vars = team_name_variations[team1]
        team2_vars = team_name_variations[team2]

        for article in articles:
            title = article.text.strip()
            found_match = False

            # Check if either team's name is in the title
            for team1_var in team1_vars:
                for team2_var in team2_vars:
                    if team1_var.lower() in title.lower() or team2_var.lower() in title.lower():
                        link = "https://www.bbc.com" + article["href"]
                        article_text = get_BBC_article_text(
                            link
                        )  # Get the full article text, using the helper function above
                        selected_articles.append({"title": title, "link": link, "text": article_text})
                        found_match = True
                        break
                if found_match:
                    break  # Break out of the outer loop
            if found_match:
                break  # Break out of the main article loop after the first match

        return selected_articles


def EPL_table():
    url = "https://www.skysports.com/premier-league-table"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    teams = soup.find_all("a", class_="standing-table__cell--name-link")

    # Points not directly accessible on Sky Sports
    points = []
    i = 1
    while i <= 20:
        points.append(soup.find("td", class_="standing-table__cell", attrs={"data-sort-value": f"{i}"}))
        i += 1

    rankings = {}
    for team, point in zip(teams, points):
        rankings[team.text] = int(point.text)

    return rankings


def ELO():
    url = "http://clubelo.com/ENG"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="ranking")  # Use only the table with the ELO rankings in it

    if table:
        rows = table.find_all("tr")  # Find the relevant rows in the table

        elo_dict = {}
        for row in rows:
            columns = row.find_all("td")
            if len(columns) > 0:  # Extract data from each row and create the dictionary
                team_name = columns[1].find("a").text.strip()  # Team name is in the 2nd column within an <a> tag
                elo_rating = columns[2].text.strip()  # ELO rating is in the 3rd column
                elo_dict[team_name] = int(elo_rating)
        return elo_dict

    return None  # Incase the table is not found or the website HTML changes


def youtube_comments(team1, team2):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    channel_id = "UCNAf1k0yIjyGu3k9BwAg3lg"  # Channel ID for sky sports prem

    def get_recent_videos(channel_id, team_name_variations, max_results=10):
        videos = []
        for team_name in team_name_variations:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=max_results,
                order="date",
                q=f'"{team_name}"',  # String in string, otherwise it will just treat it as a string literal
            )
            response = request.execute()
            videos.extend(  # Extend adds a list one by one instead of append which adds the list as a list
                response.get("items", [])  # [] is the default value
            )
        return videos

    def get_top_comments(video_id, max_results=10):
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                order="relevance",  # Retrieve top comments
                textFormat="plainText",
            )
            response = request.execute()  # Execute the list() to actually retrieve it

            comments = []
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            return comments

        except HttpError:
            return None

    # Handle any team name abbreviations
    def match_teams_in_title(title, team_variations):
        for (
            team,
            variations,
        ) in team_variations.items():  # For each team = key in the matching list
            for variation in variations:
                if variation.lower() in title.lower():
                    return team  # Return the official name to compare it with what the user enters
        return None

    team1_videos = get_recent_videos(channel_id, team_name_variations[team1])
    team2_videos = get_recent_videos(channel_id, team_name_variations[team2])

    team1_video_comments = {}
    for team1_video in team1_videos:
        title = team1_video["snippet"]["title"]

        # Check if the result is a video before trying to access 'videoId'
        if team1_video["id"]["kind"] == "youtube#video":
            video_id = team1_video["id"]["videoId"]
        else:
            # Handle the case where the result is not a video
            print(f"No videoId found for {team1}, result type was {team1_video['id']['kind']}")
            return None

        matched_team = match_teams_in_title(title, team_name_variations)
        if matched_team == team1:
            comments = get_top_comments(video_id)
            team1_video_comments[title] = comments

    team2_video_comments = {}
    for team2_video in team2_videos:
        title = team2_video["snippet"]["title"]

        if team2_video["id"]["kind"] == "youtube#video":
            video_id = team2_video["id"]["videoId"]
        else:
            print(f"No videoId found for {team2}, result type was {team2_video['id']['kind']}")
            return None

        matched_team = match_teams_in_title(title, team_name_variations)
        if matched_team == team2:
            comments = get_top_comments(video_id)
            team2_video_comments[title] = comments

    return team1_video_comments, team2_video_comments
