const form = document.querySelector("#mealForm");
const results = document.querySelector("#results");

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
        // prints results and formats it for readability
        results.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        results.textContent = "Error generating meal plan.";
        console.error("Error:", error)
    }
});