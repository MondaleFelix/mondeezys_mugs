from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.MugShop
mugs = db.mugs


app = Flask(__name__)



@app.route("/")
def mugs_index():
	# Shows all mugs
	return render_template("mugs_index.html", mugs=mugs.find())



if __name__ == "__main__":
	app.run(debug=True)
