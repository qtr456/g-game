from flask import Flask, request, render_template, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
highscores = []

@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("register"))

    message = ""
    if "secret" not in session:
        session["secret"] = random.randint(1, 100)
        session["attempts"] = 0

    if request.method == "POST":
        guess = int(request.form["guess"])
        session["attempts"] += 1

        if guess < session["secret"]:
            message = "Больше!"
        elif guess > session["secret"]:
            message = "Меньше!"
        else:
            message = f"🎉 Угадал! Попыток: {session['attempts']}"
            highscores.append({
                "name": session["username"],
                "attempts": session["attempts"],
                "time": datetime.now().strftime("%H:%M:%S")
            })
            highscores.sort(key=lambda x: x["attempts"])
            session.pop("secret")
            session.pop("attempts")

    return render_template("index.html", message=message, attempts=session.get("attempts", 0),
                           highscores=highscores, username=session["username"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/reset")
def reset():
    session.pop("secret", None)
    session.pop("attempts", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
