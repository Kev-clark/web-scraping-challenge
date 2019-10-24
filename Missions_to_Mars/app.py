from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mission_to_Mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# config is a dictionary: "MONGO_URI" is specific and must contain a uri to single database
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdb"
mongo = PyMongo(app)




@app.route("/")
def index():
    marsdataset = mongo.db.marsdb.find_one()
    print(marsdataset)
    return render_template("index.html", marsdataset=marsdataset)


@app.route("/scrape")
def scraper():
    #listings is the collection name : creates shorthand instead of having to call mongo.db.listings

    marsdata = mongo.db.marsdb
    #call functions for scrap fucntion (no input is using set list)
    mars_data = Mission_to_Mars.scrape()
    marsdata.update({}, mars_data, upsert=True)
    #redirect back to homepage
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True) 
