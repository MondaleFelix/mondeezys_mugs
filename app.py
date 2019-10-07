from flask import Flask, render_template

app = Flask(__name__)

mugs = [
	{ "product_name" : "Mondale's Mug", 'price' : 2}
]

@app.route("/")
def mugs_index():
	# Shows all mugs
	return render_template("mugs_index.html", mugs=mugs)



if __name__ == "__main__":
	app.run(debug=True)
