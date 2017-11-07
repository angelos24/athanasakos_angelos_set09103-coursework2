from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect, session
app = Flask(__name__)

# Web root
@app.route("/")
def root():
        return render_template('index.html'), 200


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
