from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)


@app.route("/")
def	get():
	return render_template('index.jinja', data={
		"Coalitions": [
			{
				"Name" : "L'Armada",
			},
			{
				"Name" : "Torrent",
			},
			{
				"Name" : "La Legion",
			},

		] 
	})

app.run(host="0.0.0.0", port=80)