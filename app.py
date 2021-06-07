"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension

app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

### 404 Custom Page ###
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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

    posts = Post.query.filter_by(user_id=user_id).all()

    return render_template("details.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    """Show user edit page."""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user-form.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update user info."""

    user = User.query.get_or_404(user_id)

    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['image']
    
    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["Post"])
def delete_user(user_id):
    """Delete user."""

    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Display new post form."""

    user = User.query.get_or_404(user_id)

    return render_template('add-post-form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Handle submission and add new post."""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def display_post(post_id):
    """Display post information."""

    post = Post.query.get(post_id)

    return render_template('post-details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def display_edit_post_form(post_id):
    """Display edit form for a given post."""

    post = Post.query.get(post_id)

    return render_template('edit-post-form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle edit post form submission."""

    post = Post.query.get_or_404(post_id)

    title = request.form['title']
    content = request.form['content']
    
    post.title=title
    post.content=content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post."""

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect('/users')