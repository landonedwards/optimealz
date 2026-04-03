const form = document.querySelector("#mealForm");
const results = document.querySelector("#results");
const mealPlan = document.querySelector("#mealPlan");
const groceryDiv = document.querySelector("#groceryList");

// stored as a global variable so it is destroyed before a redrawing
let macroChartInstance = null
// track per-day chart instances so we can destroy them before redrawing
let dayChartInstances = {};
// register data labels plugin
Chart.register(ChartDataLabels);

function renderGroceryList(data) {
  groceryDiv.innerHTML = "<h2>Grocery List</h2>";

  data.grocery_list.forEach(item => {
    const wrapper = document.createElement("div");
    wrapper.classList.add("groceryItem");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = `ingredient-${item.name}-${item.unit}`;  // links the label to the checkbox

    const label = document.createElement("label");
    label.htmlFor = `ingredient-${item.name}-${item.unit}`; // clicking the label toggles the checkbox
    label.textContent = `${item.name}: ${item.amount} ${item.unit}`;

    wrapper.appendChild(checkbox);
    wrapper.appendChild(label);
    groceryDiv.appendChild(wrapper);
  });

  // add total cost for all ingredients at bottom of grocery list
  const groceryTotal = document.createElement("div");
  groceryTotal.classList.add("groceryTotal");
  groceryTotal.innerHTML = `<hr> <strong>Total:</strong> $${data.totals.cost.toFixed(2)}`;
  groceryDiv.appendChild(groceryTotal);
}

function renderDayCharts(dayCard, meals, day, dailyCalorieTarget) {
  const validMeals = meals.filter(Boolean);

  // sum up macros and calories for this day's meals
  const dayCalories = validMeals.reduce((sum, meal) => sum + (meal.nutrition.calories || 0), 0);
  const dayProtein  = validMeals.reduce((sum, meal) => sum + (meal.nutrition.protein  || 0), 0);
  const dayCarbs    = validMeals.reduce((sum, meal) => sum + (meal.nutrition.carbs    || 0), 0);
  const dayFat      = validMeals.reduce((sum, meal) => sum + (meal.nutrition.fat      || 0), 0);

  // container for both charts side by side
  const chartRow = document.createElement("div");
  chartRow.classList.add("chartRow");

  // -- macro pie chart --
  const pieWrapper = document.createElement("div");
  pieWrapper.classList.add("pieWrapper");

  const pieCanvas = document.createElement("canvas");
  pieCanvas.id = `macroChart-${day}`;
  pieWrapper.appendChild(pieCanvas);

  // -- calorie progress bar --
  const progressWrapper = document.createElement("div");
  progressWrapper.classList.add("progressWrapper");

  const percentage = dailyCalorieTarget
    ? Math.round((dayCalories / dailyCalorieTarget) * 100)
    : 0;

  const barColor = percentage >= 90 ? "#86efac" : percentage >= 60 ? "#fbbf24" : "#f97316";

  progressWrapper.innerHTML = `
    <p class="calorieHeader">
      Calories: <strong>${Math.round(dayCalories)}</strong> / ${dailyCalorieTarget ?? "—"} kcal
    </p>
    <div class="barWrapper">
      <div class="progressBar"></div>
    </div>
    <p class="caloriePercentage">${percentage}% of daily target</p>
  `;

  // grab progress bar after it has been created and apply variable styles to it
  const progressBar = progressWrapper.querySelector(".progressBar");
  progressBar.style.width = `${percentage}%`;
  progressBar.style.background = barColor;

  chartRow.appendChild(pieWrapper);
  chartRow.appendChild(progressWrapper);
  dayCard.appendChild(chartRow);

  // destroy previous chart for this day if it exists
  if (dayChartInstances[day]) {
    dayChartInstances[day].destroy();
  }

  // draw the macro pie
  dayChartInstances[day] = new Chart(pieCanvas.getContext("2d"), {
    type: "pie",
    data: {
      labels: ["Protein", "Carbs", "Fat"],
      datasets: [{
        data: [Math.round(dayProtein), Math.round(dayCarbs), Math.round(dayFat)],
        backgroundColor: ["#f97316", "#fbbf24", "#fed7aa"],
        borderWidth: 0,
        hoverOffset: 4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        datalabels: {
          formatter: (value, context) => {
            const total = context.dataset.data.reduce((sum, v) => sum + v, 0);
            const pct = Math.round((value / total) * 100);
            return total > 0 ? `${value}g\n${pct}%` : "";
          },
          color: "#fff",
          font: { size: 10, weight: "bold" },
          display: (context) => {
            const total = context.dataset.data.reduce((sum, v) => sum + v, 0);
            return (context.dataset.data[context.dataIndex] / total) > 0.08;
          },
        },
        legend: { display: false }, // legend would be too cramped at this size
        tooltip: {
          callbacks: {
            label: (item) => {
              const total = item.dataset.data.reduce((sum, v) => sum + v, 0);
              const pct = Math.round((item.parsed / total) * 100);
              return `${item.label}: ${item.parsed}g (${pct}%)`;
            },
          },
        },
      },
    },
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
        datalabels: {
          // shows grams and percentage inside each slide
          formatter: (value, context) => {
          const total = context.dataset.data.reduce((sum, val) => sum + val, 0);
          const percentage = Math.round((value / total) * 100);
          return `${value}g\n(${percentage}%)`;
        },
        color: "#fff",
        font: { size: 20, weight: "bold" },
        // hide the label if the slice is too small to fit text
        display: (context) => {
          const total = context.dataset.data.reduce((sum, val) => sum + val, 0);
          return (context.dataset.data[context.dataIndex] / total) > 0.08;
          },
        },
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

function renderPlan(data, dailyCalorieTarget) {
  mealPlan.innerHTML = "";

  Object.values(dayChartInstances).forEach(chart => chart.destroy());
  dayChartInstances = {};

  // use data.week because of how the FastAPI response is structured
  const plan = data.week;
  const allMeals = Object.values(plan).flat().filter(Boolean);

  Object.entries(plan).forEach(([day, meals]) => {
    const dayCard = document.createElement("div");
    dayCard.classList.add("dayCard");

    dayCard.innerHTML = `<h2>${day}</h2>`;

    let mealsTotal = 0;
    let cookTimeTotal = 0;

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

        // ensures meal cost is a number
        mealsTotal += Number(meal.cost);
        cookTimeTotal += Number(meal.cook_time);
      }

      dayCard.appendChild(mealDiv);
    });

    const totalsContainer = document.createElement("div");
    totalsContainer.classList.add("totalsContainer");
    totalsContainer.innerHTML = `
    <hr>
    <p><strong>Total Cost:</strong> <span>$${mealsTotal.toFixed(2)}</span></p>
    <p><strong>Total Cook Time:</strong> <span>${cookTimeTotal} mins</span></p>
    `;

    dayCard.appendChild(totalsContainer);

    // add divider section between meal info and nutrient info
    const sectionBreak = document.createElement("div");
    sectionBreak.classList.add("mealSectionBreak");
    sectionBreak.innerHTML = `
    <hr>
    <h3>Nutrient Breakdown</h3>
    `;

    dayCard.appendChild(sectionBreak);

    // render both charts at bottom of this dayCard
    renderDayCharts(dayCard, meals, day, dailyCalorieTarget);
    mealPlan.appendChild(dayCard);
  });

  renderGroceryList(data);
  renderMacroChart(allMeals);
}

function validateConstraints(calories, budget, cookTime) {
  if (calories <= 0) {
    alert("Calories must be greater than 0.");
    return false;
  }

  if (budget <= 0) {
    alert("Budget must be greater than 0.");
    return false;
  }

  if (cookTime <= 0) {
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
    if (!validateConstraints(calories, budget, cookingTime)) {
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

        // pass the daily calorie input from form into renderPlan
        const dailyCalorieTarget = Number(calories);
        renderPlan(data, dailyCalorieTarget);
    } catch (error) {
        results.textContent = "Error generating meal plan.";
        console.error("Error:", error)
    }
});