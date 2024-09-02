from flask import Flask, render_template, request, jsonify
from main import *

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    team1 = request.json["team1"]
    team2 = request.json["team2"]
    print(f"Teams received: {team1}, {team2}")

    prediction = main(team1, team2)  # OpenAI API response given the 2 team names
    return jsonify({"prediction": prediction})  # Convert to JSON for HTML representation


if __name__ == "__main__":
    app.run(debug=True)
