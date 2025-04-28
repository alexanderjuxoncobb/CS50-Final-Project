# CS50 Final Project: Premier League Prediction Tool

A web application that leverages web scraping and AI to predict outcomes of upcoming Premier League football matches.

## [Demo Video](https://youtu.be/pvGclr8v-_s?si=L8Eoug4kJaxsbLFH)

## Overview

This application scrapes multiple data sources to gather relevant information about selected Premier League teams, including:
- Current table rankings
- ELO ratings
- Recent BBC news articles
- YouTube comments from Sky Sports Premier League videos

The collected data is then processed through OpenAI's API to generate a prediction including:
- Match date
- Home team advantage
- Predicted winner
- Three supporting reasons for the prediction

## Technical Implementation

### Frontend
- HTML/CSS with Bootstrap for responsive design
- JavaScript for dynamic content and asynchronous API calls

### Backend
- Flask web framework for routing
- Python-based web scraping
- OpenAI API integration for prediction generation

### Project Structure
- `index.html` - Main user interface
- `script.js` - Handles user interactions and API requests
- `app.py` - Flask application with endpoint routing
- `main.py` - Core logic for scraping and API integration
- `helpers.py` - Contains utility functions for data gathering

## Development Notes

This project was created as a final project for CS50, with a focus on implementing web scraping techniques and API integration rather than building a statistically superior prediction model. While betting sites and professional analysts use more sophisticated models, this project serves as a practical application of programming concepts learned during the course.

Future improvements could include:
- Integration with betting odds data
- More sophisticated statistical analysis
- Additional data sources for more accurate predictions
