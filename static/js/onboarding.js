let currentStep = 0;
const steps = document.querySelectorAll(".step");
const progressBars = document.querySelectorAll(".progress div");

function nextStep() {
    if (currentStep < steps.length - 1) {
        steps[currentStep].classList.remove("active");
        progressBars[currentStep].classList.remove("active");

        currentStep++;

        steps[currentStep].classList.add("active");
        progressBars[currentStep].classList.add("active");
    }
}

function selectOption(btn, value) {
    document.querySelectorAll(".options button").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    document.getElementById("target").value = value;
}

function selectHabit(btn, value) {
    document.querySelectorAll(".options button").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    document.getElementById("first_habit").value = value;
}

function customHabit(value) {
    document.getElementById("first_habit").value = value;
}

function showGeneratingStep() {
    nextStep();
    startProgress();
}

function startProgress() {
    let percent = 0;
    const text = document.querySelector(".progress-text");
    const circle = document.querySelector(".fg");
    const circumference = 339.292;

    const timer = setInterval(() => {
        percent++;
        text.innerText = percent + "%";
        circle.style.strokeDashoffset =
            circumference - (percent / 100) * circumference;

        if (percent >= 100) {
            clearInterval(timer);
            setTimeout(nextStep, 400);
        }
    }, 25);
}
