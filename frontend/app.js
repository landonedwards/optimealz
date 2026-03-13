const form = document.querySelector("#mealForm");
const results = document.querySelector("#results");
const mealPlan = document.querySelector("#mealPlan");
const groceryDiv = document.querySelector("#groceryList");

// stored as a global variable so it is destroyed before a redrawing
let macroChartInstance = null

function renderGroceryList(data) {
  groceryDiv.innerHTML = "<h2>Grocery List</h2>";

  data.grocery_list.forEach(item => {
    const listItem = document.createElement("p");
    listItem.textContent = `${item.name}: ${item.amount} ${item.unit}`;
    groceryDiv.appendChild(listItem);
  });
}

function renderMacroChart(allMeals) {
  const totalProtein = allMeals.reduce(
    (sum, meal) => sum + (meal.nutrition.protein || 0),
    0,
  );
  const totalCarbs = allMeals.reduce(
    (sum, meal) => sum + (meal.nutrition.carbs || 0),
    0,
  );
  const totalFat = allMeals.reduce(
    (sum, meal) => sum + (meal.nutrition.fat || 0),
    0,
  );

  if (macroChartInstance) {
    // destroy previous chart before redrawing to prevent canvas stacking
    macroChartInstance.destroy();
  }

  const ctx = document.querySelector("#nutritionChart").getContext("2d");
  macroChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Protein", "Carbs", "Fat"],
      datasets: [
        {
          data: [
            Math.round(totalProtein),
            Math.round(totalCarbs),
            Math.round(totalFat),
          ],
          backgroundColor: ["#f97316", "#fbbf24", "#fed7aa"],
          borderWidth: 0,
          hoverOffset: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 16,
            usePointStyle: true, // circle markers instead of square boxes
            font: { size: 13 },
          },
        },
        tooltip: {
          callbacks: { label: (item) => `${item.label}: ${item.parsed}g` },
        },
      },
    },
  });
}

function renderPlan(data) {
  mealPlan.innerHTML = "";

  // use data.week because of how the FastAPI response is structured
  const plan = data.week;
  const allMeals = Object.values(plan).flat().filter(Boolean);

  Object.entries(plan).forEach(([day, meals]) => {
    const dayCard = document.createElement("div");
    dayCard.classList.add("dayCard");

    dayCard.innerHTML = `<h2>${day}</h2>`;

    meals.forEach(meal => {
      const mealDiv = document.createElement("div");
      mealDiv.classList.add("meal");

      if (!meal || !meal.name) {
        mealDiv.textContent = "No meal planned";
      } else {
        mealDiv.innerHTML = `
          <a href="${meal.source_url}" target="_blank"><strong>${meal.name}</strong></a><br>
          Calories: ${meal.calories} | 
          Cook Time: ${meal.cook_time} min | 
          Cost: $${meal.cost.toFixed(2)}
        `;
      }

      dayCard.appendChild(mealDiv);
    });

    mealPlan.appendChild(dayCard);
  });

  renderGroceryList(data);
  renderMacroChart(allMeals);
}

function validateConstraints(data) {
  if (data.max_calories <= 0) {
    alert("Calories must be greater than 0.");
    return false;
  }

  if (data.max_budget <= 0) {
    alert("Budget must be greater than 0.");
    return false;
  }

  if (data.max_cook_time <= 0) {
    alert("Cooking time must be greater than 0.");
    return false;
  }

  return true;
}

form.addEventListener("submit", async (event) => {
    // prevents page from refreshing upon submitting
    event.preventDefault();

    const calories = document.querySelector("#calories").value;
    const budget = document.querySelector("#budget").value;
    const cookingTime = document.querySelector("#cooking-time").value;
    const diet = document.querySelector("#diet").value;
    const protein = document.querySelector("#protein").value;
    const carbs = document.querySelector("#carbs").value;
    const fat = document.querySelector("#fat").value;
    const mealsPerDay = document.querySelector("#meals-per-day").value;
    // may want to ask how many meals per day
    // ask whether they'd like a different set of meals with a checkbox

    let url = `http://127.0.0.1:8000/generate-plan`;

    const mealsPerDayNumber = Number(mealsPerDay) || 3;
    // create an object matching the Constraints model
    const constraints = {
        max_calories: Number(calories) * 7,
        max_budget: Number(budget) * 7,
        max_cook_time: Number(cookingTime),    
        dietary_restriction: diet || null,

        target_protein: Number(protein) * 7 || null,
        target_carbs: Number(carbs) * 7 || null,
        target_fat: Number(fat) * 7 || null,

        meals_per_day: Number(mealsPerDay) || 3,
        meals_per_week: mealsPerDayNumber * 7 
    };

    // if constraints are not valid, return early
    if (!validateConstraints(constraints)) {
      return;
    }

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
        renderPlan(data);
    } catch (error) {
        results.textContent = "Error generating meal plan.";
        console.error("Error:", error)
    }
});