from flask import Flask, render_template, request, session, redirect, url_for
import functools
from flask_login import LoginManager



app = Flask(__name__)
app.secret_key = "jose"
app.config['TEMPLATES_AUTO_RELOAD'] = True

users = {"jose": ("jose", "1234")}

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,post-check=0, pre-check=0"
    print(response)
    return response


@app.route("/")
def home():
    return render_template("home.html", name=session.get("username", None), s=session)


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        return func()

    return secure_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        next_url = request.form.get("next")
        print(username, password, next_url)

        if username in users and users[username][1] == password:
            session["username"] = username
            if next_url:
                return redirect(next_url)
            return redirect(url_for("profile_page"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username not in users:
            users[username] = (username, password)
            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    # session.pop("username")
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile_page():
    return render_template("profile.html", name=session["username"])


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
