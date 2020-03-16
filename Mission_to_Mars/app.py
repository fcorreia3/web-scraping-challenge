# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Declare the database
db = mongo.db

# Declare the collection
collection = db.mars_db

# The database and collection, if they don't already exist, will be created at this point.
data = scrape_mars.scrape()
collection.insert_one(data)

# Route to render index.html template using data from MongoDB
@app.route("/")
def index():
    # return render_template("index.html", x=data)
    mars = collection.find_one()
    return render_template("index.html", x = mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    scraped_mars_data = scrape_mars.scrape()
    mars.update(
        {},
        scraped_mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
