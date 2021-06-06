"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension

app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


### ROUTING ###
@app.route('/')
def go_to_listing():
    """Redirect to listing."""

    return redirect('/users')


@app.route('/users')
def list_users():
    """List all users."""

    users = User.query.all()
    return render_template("listing.html", users=users)


@app.route('/users/new')
def show_new_user_form():
    """Form to add new user."""

    return render_template("new-user-form.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Handle form submission to add new user."""

    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['image'] if request.form['image'] else None
    
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Display user info."""

    user = User.query.get_or_404(user_id)

    return render_template("details.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    """Show user edit page."""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user-form.html", user=user)


@app.route('users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):

    user = User.query.get_or_404(user_id)

    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['image'] if request.form['image'] else None
    
    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["Post"])
def delete_user(user_id):

    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/users')