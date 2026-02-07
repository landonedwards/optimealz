const form = document.querySelector("#mealForm");
const results = document.querySelector("#results");

form.addEventListener("submit", async (event) => {
    // prevents page from refreshing upon submitting
    event.preventDefault();

    const calories = document.querySelector("#calories").value;
    const budget = document.querySelector("#budget").value;
    const diet = document.querySelector("#diet").value;

    let url = `http://127.0.0.1:8000/generate-plan?max_calories=${calories}&max_budget=${budget}`;

    if (diet) {
        url += `&dietary_restriction=${diet}`;
    }

    try {
        // sends request to FastAPI server using the GET method
        const response = await fetch(url, {
            method: "GET"
        });

        const data = await response.json();
        // prints results and formats it for readability
        results.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        results.textContent = "Error generating meal plan.";
    }
});