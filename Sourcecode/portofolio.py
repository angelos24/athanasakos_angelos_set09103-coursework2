import os
from datetime import datetime
from flask  import Flask, url_for, abort, request, render_template, json, flash, redirect, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhhhhh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/blog_new.db' % os.getcwd()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB structure
class Pages(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.BLOB)
    description = db.Column(db.String(500))
    datetime =  db.Column(db.DateTime, default=datetime.now())

    def __init__(self, title, content, description, datetime):
        self.title = title
        self.content = content
        self.description = description
        self.datetime = datetime

    def __repr__(self):
         return '<Pages : id=%r, title=%s, content=%s, description=%s, datetime=%s>' \
     % (self.id, self.title, self.content, self.description, self.datetime)

# New post root
@app.route('/new-post/', methods=['POST','GET'])
def save_post():
    if not session.get('logged_in'):
        return abort(401)
    if request.method == "POST":
        page = Pages(title = request.form['title'],
        content = request.form['content'],
        description = request.form['description'],
        datetime = datetime.now().replace(second=0, microsecond=0))
        db.session.add(page)
        db.session.commit()
        return redirect('world'), 303

# Delete post
@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    db.session.query(Pages).filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('world'), 303

# Edit post
@app.route('/edit-post/<int:post_id>')
def edit_post(post_id):
    if not session.get('logged_in'):
        return abort(401)
    post = db.session.query(Pages).filter_by(id=post_id).first()
    return render_template('edit_post.html', id=post.id, title=post.title, content=post.content, description=post.description)

# Update post
@app.route('/update-post/', methods=['POST','GET'])
def update_post():
     if request.method == "POST":
         post_id = request.form['id']
         title = request.form['title']
         content = request.form['content']
         description = request.form['description']
         db.session.query(Pages).filter_by(id=post_id).update({'title': title, 'content': content, 'description': description})
         db.session.commit()
         return redirect('/world/'+post_id), 303

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'angelos' or request.form['password'] != 'admin':
            flash('<div class="alert alert-danger" role="alert"> Invalid Credentials. Please try again.</div>')
        else:
            session['logged_in'] = True
            flash('<div class="alert alert-success" role="alert"> <strong>Well done!</strong> You have successfully logged in!</div>')
    return redirect('world'), 303

# Logout page
@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('<div class="alert alert-success" role="alert"> <strong>Well done!</strong> You have successfully logged out!</div>')
    return redirect(url_for('root')), 303

# root
@app.route("/")
def root():
        return render_template('index.html'), 200

# index page of work page
@app.route("/work")
def work_index():
        return render_template('work_index.html'), 200

# About me page
@app.route("/work/aboutme")
def aboutme():
        return render_template('aboutme.html'), 200

# All projects page
@app.route("/work/projects/")
def work_projects_index():
    with open("websites.json","r") as f:
        projects_all = json.load(f)
        f.close
        return render_template('work_projects_all.html', projects_all=projects_all), 200

# Specific project pages
@app.route("/work/projects/<int:page>/")
def work_projects_index_showcase(page):
    with open("websites.json","r") as f:
        projects = json.load(f)
        f.close
        return render_template('work_projects.html', page=page, projects=projects), 200

# All websites page
@app.route("/work/websites/")
def work_websites_index():
    with open("websites.json","r") as f:
        websites_all = json.load(f)
        f.close
        return render_template('work_websites_all.html', websites_all=websites_all), 200

# Specific website pages
@app.route("/work/websites/<int:page>/")
def work_websites_index_showcase(page):
    with open("websites.json","r") as f:
        websites = json.load(f)
        f.close
        return render_template('work_websites.html', page=page, websites=websites), 200

# index of My World page
@app.route("/world")
def world_index():
    pages = db.session.query(Pages).all()
    return render_template('world_index.html', pages=pages), 200

# Convertes to specific post
@app.route('/world/<int:post_id>')
def view_page(post_id):
    post = db.session.query(Pages).filter_by(id=post_id).first()
    return render_template('world_posts.html',
                            id=post.id, title=post.title, content=post.content, description=post.description), 200
# New post page
@app.route('/world/new_post')
def new_post():
    return render_template('world_newpage.html'), 200

# Custom 404
@app.errorhandler(404)
def http_error_handler(error):
    return render_template('404.html', error=error), error.code

# Download CV root
@app.route('/cv/')
def cv():
    return send_from_directory(directory='static', filename='angel_athan.pdf', as_attachment=True)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
