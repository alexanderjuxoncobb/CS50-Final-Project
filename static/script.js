document
  .getElementById("prediction-form")
  .addEventListener("submit", async function (e) {
    // Allows program to run whilst waiting for the data to come back
    e.preventDefault(); // Prevents default behaviour which is the reload the page (allowing you to enter custom behaviour)
    document.getElementById("result-card").style.display = "none";

    const submitButton = document.querySelector(".btn-predict"); // querySelector because it is using a CSS class
    const loading = document.getElementById("loading");

    submitButton.style.display = "none"; // Same as style="diaply: none;" from the CSS
    loading.style.display = "flex";

    // Reset the visibility of all elements before processing the new prediction
    document.getElementById("no-game").style.display = "none";
    document.getElementById("game-details").style.display = "none";
    document.getElementById("reasons-list").style.display = "none";
    document.getElementById("reasons-list").innerHTML = ""; // Clear previous reasons

    const selectedOption1 =
      document.getElementById("team1-select").options[
        document.getElementById("team1-select").selectedIndex
      ];
    const selectedOption2 =
      document.getElementById("team2-select").options[
        document.getElementById("team2-select").selectedIndex
      ];

    const team1 = selectedOption1.text;
    const team2 = selectedOption2.text;

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        // await means the script will run below whilst waiting (allowing the loading animation to show)
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ team1: team1, team2: team2 }),
      });

      console.log("Response received:", response);
      const data = await response.json();
      console.log("Parsed JSON data:", data);

      const prediction = JSON.parse(data.prediction);

      // Check if the game is not scheduled
      if (prediction.date === "No game scheduled") {
        document.getElementById("no-game").textContent =
          "No game scheduled. Pick another matchup.";
        document.getElementById("no-game").style.display = "block";
        document.getElementById("game-details").style.display = "none";
        document.getElementById("reasons-list").style.display = "none";
      } else {
        document.getElementById("game-details").style.display = "block";
        document.getElementById("reasons-list").style.display = "block";

        document.getElementById("match-date").textContent = prediction.date;
        document.getElementById("home-team").textContent = prediction.home;
        document.getElementById("winner").textContent = prediction.winner;

        const winnerElement = document.getElementById("winner");
        winnerElement.textContent = prediction.winner;
        winnerElement.classList.add("bg-success"); // Add the 'bg-success' class to highlight the winner green

        // Clear any previous responses and populate the reasons list
        const reasonsList = document.getElementById("reasons-list");
        reasonsList.innerHTML = "";
        if (prediction.reason && prediction.reason.length > 0) {
          prediction.reason.forEach((reason) => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = reason;
            li.style.listStyleType = "none";
            reasonsList.appendChild(li);
          });
          reasonsList.style.display = "block"; // Show the reasons list if there are reasons
        } else {
          reasonsList.style.display = "none"; // Hide the reasons list if there are no reasons
        }
      }
      document.getElementById("result-card").style.display = "block";
    } catch (error) {
      console.error("Error:", error);
    } finally {
      loading.style.display = "none";
      document.getElementById("result-card").style.display = "block";
    }
  });

document
  .getElementById("team1-select")
  .addEventListener("change", function (e) {
    const submitButton = document.querySelector(".btn-predict"); // querySelector because it is using CSS class
    submitButton.style.display = "block";
    document.getElementById("new-one").style.margin = "0 auto"; // Center it horizontally
  });

document
  .getElementById("team2-select")
  .addEventListener("change", function (e) {
    document.getElementById("new-one").style.display = "block"; // Can call via id too (which you had to make becuause it is NOT submit, that is the type)
    document.getElementById("new-one").style.margin = "0 auto"; // Center it horizontally
  });
