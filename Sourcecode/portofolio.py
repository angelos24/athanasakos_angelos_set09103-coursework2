import os
from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/blog.db' % os.getcwd()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Custom 401
@app.errorhandler(401)
def http_error_handler(error):
        return render_template('401.html', error=error), error.code

# Custom 404
@app.errorhandler(404)
def http_error_handler(error):
    return render_template('404.html', error=error), error.code

@app.route("/")
def root():
        return render_template('index.html'), 200

@app.route("/work")
def work_index():
        return render_template('work_index.html'), 200

@app.route("/work/websites/")
def work_websites_index():
    with open("websites.json","r") as f:
        websites_all = json.load(f)
        return render_template('work_websites_all.html', websites_all=websites_all), 200

@app.route("/work/websites/<int:page>/")
def work_websites_index_showcase(page):
    with open("websites.json","r") as f:
        websites = json.load(f)
        f.close
        return render_template('work_websites.html', page=page, websites=websites), 200

@app.route("/world")
def world_index():
        return render_template('world_index.html'), 200



if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
