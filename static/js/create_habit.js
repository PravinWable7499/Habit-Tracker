// ================= HABIT TYPE DESCRIPTION =================
const habitDesc = document.getElementById("habitDesc");
const habitTypeBtns = document.querySelectorAll(".habit-type");

const descriptions = {
    regular: "Build positive habits for your daily routine.",
    negative: "Reduce or quit habits that affect you negatively.",
    todo: "One-time tasks you want to complete."
};

habitTypeBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        habitTypeBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const type = btn.dataset.type;
        habitDesc.textContent = descriptions[type];
    });
});

// ================= CREATE YOUR OWN TOGGLE =================
const openCreateBtn = document.getElementById("openCreate");
const createForm = document.getElementById("createForm");

openCreateBtn.addEventListener("click", () => {
    createForm.classList.toggle("hidden");
});

// ================= SUGGESTED HABITS CLICK =================
const habitChips = document.querySelectorAll(".habit-chip");

habitChips.forEach(chip => {
    chip.addEventListener("click", () => {
        const habitName = chip.textContent.trim();

        // redirect to shift selection page
        window.location.href = `/select-shift?habit=${encodeURIComponent(habitName)}`;
    });
});

// ================= CUSTOM HABIT ADD =================
const saveBtn = document.querySelector(".save-btn");
const habitInput = document.querySelector(".habit-input");

saveBtn.addEventListener("click", () => {
    const habitName = habitInput.value.trim();

    if (!habitName) {
        alert("Please enter a habit name");
        return;
    }

    window.location.href = `/select-shift?habit=${encodeURIComponent(habitName)}`;
});
