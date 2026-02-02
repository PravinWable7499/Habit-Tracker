from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

habits = []   # temporary storage


app = Flask(__name__)
app.secret_key = "super_secret_key_123"  # change in production


# ================== LOGIN ==================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Please enter both email and password", 400

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, password_hash FROM users WHERE email = ?", email)
            user = cursor.fetchone()
        finally:
            conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))

        return " Invalid email or password"

    return render_template("login.html")


# ================== REGISTER ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            return "All fields are required", 400

        hashed_password = generate_password_hash(password)

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE email = ?", email)
            if cursor.fetchone():
                return " Email already registered"

            cursor.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ================== DASHBOARD ==================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check onboarding
        cursor.execute("""
            SELECT wakeup_time, end_day_time, target, first_habit
            FROM user_onboarding
            WHERE user_id = ?
        """, (session["user_id"],))
        onboarding = cursor.fetchone()

        # Get user name
        cursor.execute("SELECT full_name FROM users WHERE user_id = ?", (session["user_id"],))
        user = cursor.fetchone()
    finally:
        conn.close()

    if not onboarding:
        return redirect(url_for("onboarding"))

    data = {
        "full_name": user[0],
        "wakeup_time": onboarding[0],
        "end_day_time": onboarding[1],
        "target": onboarding[2],
        "first_habit": onboarding[3]
    }

    return render_template("dashboard.html", data=data)


# ================== ONBOARDING ==================
@app.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        wakeup = request.form.get("wakeup_time")
        end_day = request.form.get("end_day_time")
        target = request.form.get("target")
        habit = request.form.get("first_habit")

        if not wakeup or not end_day or not target or not habit:
            return "All fields are required", 400

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Prevent duplicate onboarding
            cursor.execute("SELECT user_id FROM user_onboarding WHERE user_id = ?", (session["user_id"],))
            if cursor.fetchone():
                return redirect(url_for("dashboard"))


            cursor.execute("""
                INSERT INTO user_onboarding (user_id, wakeup_time, end_day_time, target, first_habit)
                VALUES (?, ?, ?, ?, ?)
            """, (session["user_id"], wakeup, end_day, target, habit))
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for("dashboard"))

    return render_template("onboarding.html")


# ================== SAVE HABIT PLAN ==================
@app.route("/save_habit_plan", methods=["POST"])
def save_habit_plan():
    if "user_id" not in session:
        return redirect(url_for("login"))

    habit_name = request.form.get("habit_name")
    habit_time = request.form.get("habit_time")

    if not habit_name or not habit_time:
        return "Please provide habit name and time", 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO HabitPlans (user_id, HabitName, HabitTime) VALUES (?, ?, ?)",
            (session["user_id"], habit_name, habit_time)
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("dashboard"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/create-habit")
def create_habit():
    return render_template("create_habit.html")



# ================== LOGOUT ==================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
