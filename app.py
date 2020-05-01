from flask import Flask, render_template, redirect
from scrape_mars import scrape_info
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set route
@app.route('/')
def index():
    marsdata = mongo.db.marsdata.find_one()

    # Return the template with the teams list passed in
    return render_template('index.html', marsdata=marsdata)

@app.route('/scrape')
def scrape():
    marsdata = mongo.db.marsdata
    scrape_dict = scrape_info()
    # Store the entire dictionary in Mongo
    marsdata.update({}, scrape_dict, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
