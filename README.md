# CS50 Final Project

Demo Video URL: https://youtu.be/pvGclr8v-_s?si=L8Eoug4kJaxsbLFH

TL;DR:

A webapp that scrapes the internet to make an informed decision on who will win an upcoming football match in the premier league. I parse information from sources such as the current table rankings alongside recent BBC articles and YouTube comments for the two teams selected. This is then sent to the OpenAI API, which returns the match date, who is playing at home, the predicted winner and 3 reasons for making this prediction.

Full Description:

I wanted to practice techniques such as webscaping and making an API call, so I decided on making a prediction tool for the english premier league. Users must select 2 teams from a dropdown and then click 'Get Prediction'. There is some error catching in place incase a match is not scheduled in the near future (and therefore not being picked up when scraping the fixtures from Sky Sports) or the same team selected in both dropdowns. The webpage is written in index.html and uses bootstrap and some custom CSS for the styling.

Once 'Get Prediction' is submited, my script.js file sends a request to app.py, where my flask @app.route() routing is writen. Going through the '/predict' route (which is called via fetch("http://127.0.0.1:5000/predict") in my script.js) calls main.py which is where the scraping and OpenAI API call takes place. In main.py I call multiple functions from helpers.py which return important information such as current rankings and ELO ratings, alongside content from recent BBC articles and the top comments under Sky Sports Premier League YouTube videos mentioning either team. This is then passed into a dictionary 'final_data' which is sent to the OpenAI API along with the some prompting that it is a professional football analyst who has been tasked with predicting the outcome of an upcoming match, based on the information provided.

Once the JSON response has been received it is passed back to script.js, which has been waiting for the response using async / await functionality. Script.js changes the display of some HTML elements (from "none" to "block" AKA visible) and passes in the relevant information from the JSON response. A user can then, once they read this information, change the team in the dropdown menu to reveal the 'Get Prediction' button again and re-run the script with different teams.

A slight caveat of this project is its lack of refinement--the information being scraped is surface level and the biggest predictor of a winner is the ELO rating. Additionally, betting sites have much more refined models so simply returning their odds would enhance (and probably dominate) my predictions. However, the aim of this project wasn't to beat the market! It was to practice the ideas I learnt in CS50 and apply them to build a real-world piece of software. In this regard, it's been a great success and I've learnt a lot.
