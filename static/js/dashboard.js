const today = new Date();

/* TODAY TEXT */
const options = { month: "short", day: "numeric" };
document.getElementById("today-date").textContent =
    today.toLocaleDateString("en-US", options);

/* MONTH CALENDAR */
const calendarRow = document.getElementById("calendarRow");

const year = today.getFullYear();
const month = today.getMonth();

/* Get total days in month */
const totalDays = new Date(year, month + 1, 0).getDate();

/* Day names */
const dayNames = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

for (let day = 1; day <= totalDays; day++) {
    const dateObj = new Date(year, month, day);
    const dayName = dayNames[dateObj.getDay()];

    const dayCard = document.createElement("div");
    dayCard.classList.add("day-card");

    if (dateObj.toDateString() === today.toDateString()) {
        dayCard.classList.add("today");
    }

    dayCard.innerHTML = `
        <div class="day-name">${dayName}</div>
        <div class="day-date">${day}</div>
    `;

    calendarRow.appendChild(dayCard);
}

/* Auto scroll to today */
const todayEl = document.querySelector(".day-card.today");
if (todayEl) {
    todayEl.scrollIntoView({
        behavior: "smooth",
        inline: "center"
    });
}


const shiftButtons = document.querySelectorAll(".shift-btn");

shiftButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        // remove active from all
        shiftButtons.forEach(b => b.classList.remove("active"));

        // add active to clicked
        btn.classList.add("active");

        const selectedShift = btn.dataset.shift;
        console.log("Selected shift:", selectedShift);

        // 🔥 later we will filter habits here
        // filterHabits(selectedShift);
    });
});

