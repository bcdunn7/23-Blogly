from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testing'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

# don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class ApplicationTestCase(TestCase):
    """Testing the views for the application."""

    def setUp(self):
        """Adding two sample users, three sample posts, two sample tage, and 1 posttag."""

        db.drop_all()
        db.create_all()

        user1 = User(first_name="John",
                    last_name="Smith",
                    image_url="https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png")

        user2 = User(first_name="Jane",
                    last_name="Doe")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        post1 = Post(title="Sample Title1",
                    content="Content1",
                    user_id=user1.id)

        post2 = Post(title="Sample Title2",
                    content="Content2",
                    user_id=user1.id)

        post3 = Post(title="Sample Title3",
                    content="Content3",
                    user_id=user2.id)

        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()

        tag1 = Tag(name="funny")
        tag2 = Tag(name="great")

        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()

        # posttag1 = PostTag(post_id=1,tag_id=1)

        # db.session.add(posttag1)
        # db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id
        self.post1_id = post1.id
        self.tag1_id = tag1.id

    def teatDown(self):
        """Clean db of failed transactions."""

        db.session.rollback()

    def test_listing_all_users(self):
        """Test if homepage displays list of users."""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John', html)
            self.assertIn('Jane', html)

    def test_show_add_user_form(self):
        """Test if form routing shows form."""
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>New User:</h1>', html)
            self.assertIn('<p>First Name: <input name="first" type="text" placeholder="Enter first name"></p>', html)

    def test_add_user(self):
        """Test if submiting new user form works."""
        with app.test_client() as client:
            new_user = {"first": "Brian", "last": "Johnson", "image": "https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png"}
            resp = client.post("/users/new", data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Brian", html)

    def test_show_user_edit_page(self):
        """Test if user edit form is show."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user2_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('save-changes-btn', html)

    def test_show_add_post_form(self):
        """Test if route shows new post form."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user1_id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add Post for', html)

    def test_listing_posts_for_user(self):
        """Test if posts are shown on a user page."""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user1_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sample Title1", html)
            self.assertIn("Sample Title2", html)

    def test_show_post_edit_form(self):
        """Test if post edit form is correctly displayed."""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post1_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)

    def test_add_new_post(self):
        """Test if add new post form works."""
        with app.test_client() as client:
            new_post = {"title": "Sample Title99", "content": "content here"}
            resp = client.post(f"/users/{self.user1_id}/posts/new", data=new_post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sample Title99", html)