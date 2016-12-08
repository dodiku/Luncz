from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return "6";

@app.route("/csound")
def csound():
	return "8";

if __name__ == "__main__":
	app.run(debug='true')