import os
from flask import Flask, redirect, render_template, request
from cs50 import SQL
from functions import lookup, rain


db = SQL("sqlite:///grass.db")

app = Flask(__name__)


# Landing page to get initial user input to determine watering needs of their yard
@app.route("/", methods=["GET", "POST"])
def index():

    # Post method gets user input for API call to determine recent rain and current watering needs
    if request.method == "POST":
        zipcode = request.form.get("zip")
        grass = request.form.get("grass_type")

        # Verifies valid user input
        if (len(zipcode) != 5):
            return render_template("apology.html")

        if grass == None:
            return render_template("apology.html")

        # Returns list of grass species for selection by user
        grass_name = db.execute("SELECT DISTINCT grass_type FROM grass;")

        # API calls to return rain amount for users given zipcode
        # lookup and rain functions pulled from functions.py 
        location = lookup(zipcode)

        rain_sum = rain(location)

        if location != None and rain_sum != None:

            # SQL query to return user information based on their grass type selection
            grass_stats = db.execute("SELECT * FROM grass WHERE grass_type=?;", grass)
            grass_type = grass_stats[0]['grass_type']
            temp = grass_stats[0]['temp']
            mow_height = grass_stats[0]['mow_height']
            optimal_water = grass_stats[0]['optimal_water']
            rain_needed = optimal_water - rain_sum
            if rain_needed >= 0:
                current_need = ['Sufficient']
            elif rain_needed < 0:
                current_need = ['Insufficient']


            return render_template("responce.html", current_need=current_need, rain_needed=rain_needed, rain_sum=rain_sum, grass_type=grass_type, temp=temp, mow_height=mow_height, optimal_water=optimal_water)

        else:
            return render_template("index.html", grass_name=grass_name)

    else:

        # Queries SQL database for grass types for user selectioin
        grass_name = db.execute("SELECT DISTINCT grass_type FROM grass;")

        return render_template("index.html", grass_name=grass_name)


# Hidden data entry page for admin to enter grass species and optimal growing conditions.
@app.route("/entry", methods=["GET", "POST"])
def entry():

    # Gets input and inserts into SQL database
    if request.method == "POST":

        # User variables harvested from entry.html page
        grass = request.form.get("grass")
        temp = request.form.get("temp")
        mow_height = request.form.get("height")
        water = request.form.get("water")

        # Inserts user data into SQL database for later recall
        db.execute("INSERT INTO grass (grass_type, temp, mow_height, optimal_water) VALUES (?, ?, ?, ?);", grass, temp, mow_height, water)

        return render_template("entered.html")

    else:

        return render_template("entry.html")
