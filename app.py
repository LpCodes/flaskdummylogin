from flask import Flask, render_template, request, session, redirect, url_for
import functools

# Create a Flask application instance
app = Flask(__name__)

# Set a secret key for the Flask application
app.secret_key = "jose"

# Enable auto-reloading of templates
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Define a dictionary of users (for demonstration purposes)
users = {"jose": ("jose", "1234")}


# Define a function to be called after each request is processed
@app.after_request
def after_request(response):
    # Set response headers to disable caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,post-check=0, pre-check=0"
    print(response)
    return response


# Define a route for the home page
@app.route("/")
def home():
    # Render the home page template with the current username (if available) and session data
    return render_template("home.html", name=session.get("username", None), s=session)


# Define a function that can be used as a decorator to require login for certain routes
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        # If the user is not logged in, redirect them to the login page
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        # Otherwise, allow them to access the requested route
        return func()

    return secure_function


# Define a route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get the username and password from the submitted form data
        username = request.form.get("username")
        password = request.form.get("password")
        next_url = request.form.get("next")
        print(username, password, next_url)

        # If the username and password are valid, store the username in the session and redirect to the profile page
        if username in users and users[username][1] == password:
            session["username"] = username
            if next_url:
                return redirect(next_url)
            return redirect(url_for("profile_page"))

    # If the request method is GET or the login was unsuccessful, render the login page template
    return render_template("login.html")


# Define a route for the registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get the username and password from the submitted form data
        username = request.form.get("username")
        password = request.form.get("password")

        # If the username is not already in the users dictionary, add it with the provided password and redirect to the home page
        if username not in users:
            users[username] = (username, password)
            return redirect(url_for("home"))

    # If the request method is GET or the registration was unsuccessful, render the registration page template
    return render_template("register.html")


# Define a route for the logout function
@app.route("/logout")
def logout():
    # Clear the user's session data and redirect to the home page
    session.clear()
    return redirect(url_for("home"))


# Define a route for the profile page that requires login
@app.route("/profile")
@login_required
def profile_page():
    # Render the profile page template with the current username
    return render_template("profile.html", name=session["username"])


# If the script is executed as the main program, run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
