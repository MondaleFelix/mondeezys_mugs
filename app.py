from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.MugShop
mugs = db.mugs


app = Flask(__name__)



@app.route("/")
def mugs_index():
	# Shows all mugs
	return render_template("mugs_index.html", mugs=mugs.find())

@app.route("/mugs", methods=["POST"])
def playlists_submit():
	mug = {
		"mug_name": request.form.get("mug_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
		"color": request.form.get("color")

	}
	print(mug)
	mugs.insert_one(mug)
	return redirect(url_for("mugs_index"))


@app.route("/mugs/new")
def mugs_new():
	return render_template("mugs_new.html")


if __name__ == "__main__":
	app.run(debug=True)
