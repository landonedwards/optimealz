const form = document.querySelector("#mealForm");
const results = document.querySelector("#results");

function renderWeek(data) {
  results.innerHTML = "";

  // use data.week because of how the FastAPI response is structured
  const plan = data.week;

  Object.entries(plan).forEach(([day, meals]) => {
    const daySection = document.createElement("div");
    daySection.classList.add("day");

    daySection.innerHTML = `<h2>${day}</h2>`;

    meals.forEach((meal, index) => {
      const mealDiv = document.createElement("div");
      mealDiv.classList.add("meal");

      if (!meal || !meal.name) {
        mealDiv.textContent = "No meal planned";
      } else {
        mealDiv.innerHTML = `
          <strong>${meal.name}</strong><br>
          Calories: ${meal.calories}
        `;
      }

      daySection.appendChild(mealDiv);
    });

    results.appendChild(daySection);
  });
}

form.addEventListener("submit", async (event) => {
    // prevents page from refreshing upon submitting
    event.preventDefault();

    const calories = document.querySelector("#calories").value;
    const budget = document.querySelector("#budget").value;
    const diet = document.querySelector("#diet").value;

    let url = `http://127.0.0.1:8000/generate-plan`;

    // create an object matching the Constraints model
    const constraints = {
        max_calories: Number(calories),
        max_budget: Number(budget),
        max_cook_time: 60,              // required now
        dietary_restriction: diet || null,
        meals_per_week: 7
    };

    try {
        // sends request to FastAPI server using the POST method
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(constraints)
        });

        const data = await response.json();
        renderWeek(data);
    } catch (error) {
        results.textContent = "Error generating meal plan.";
        console.error("Error:", error)
    }
});