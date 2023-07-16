from flask import Flask, render_template, request, redirect, session,flash
import secrets
import requests

app = Flask(__name__)
app.secret_key = "surya@123"

# Route for the login page
@app.route("/")
def login():
    return render_template("index.html")

# Route for handling login form submission
@app.route("/login", methods=["POST","GET"])
def authenticate():
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if username and password match in the text file
    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if username == stored_username and password == stored_password:
                # Generate a unique API key for the authenticated user
                api_key = secrets.token_hex(16)
                session["api_key"] = api_key
                return redirect("/dashboard")
            else:
                return "Invalid username or password"

# Route for the dashboard page
@app.route("/dashboard")
def dashboard():
    # Check if the user is authenticated by verifying the API key
    if "api_key" in session:
        # Make the API request
        api_key = "ea063b77f790582f88d2b4a4c2533251"
        url = "https://api.themoviedb.org/3/movie/popular"
        params = {
            "api_key": api_key
        }
        response = requests.get(url, params=params)
        data = response.json()


        # Extract the movie results
        movies = data.get('results', [])

        return render_template("dashboard.html", movies=movies)
    else:
        flash('error',"You are not Authorized please login and try again....")
        return render_template("index.html"), 401

# Route for the registration page
@app.route("/register")
def register():
    return render_template("register.html")

# Route for logging out
@app.route("/logout")
def logout():
    # Clear the session to log out the user
    session.clear()
    return redirect("/")


# Route for handling registration form submission
@app.route("/register", methods=["POST"])
def save_user():
    username = request.form.get("username")
    password = request.form.get("password")

    # Save the username, password, and API key in a text file
    with open("users.txt", "a") as file:
        file.write(f"{username}:{password}\n")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
