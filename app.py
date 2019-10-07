from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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
	mug_id = mugs.insert_one(mug).inserted_id
	return redirect(url_for("mugs_show", mug_id = mug_id))


@app.route("/mugs/<mug_id>")
def mugs_show(mug_id):
	mug = mugs.find_one({'_id' : ObjectId(mug_id)})
	return render_template("mugs_show.html", mug = mug)

@app.route("/mugs/new")
def mugs_new():
	return render_template("mugs_new.html")


if __name__ == "__main__":
	app.run(debug=True)
