from unittest import TestCase

from app import app
from models import db, User

# test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testing'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

# don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Testing the views for User."""

    def setUp(self):
        """Adding two sample users."""

        User.query.delete()

        user1 = User(first_name="John",
                    last_name="Smith",
                    image_url="https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png")

        user2 = User(first_name="Jane",
                    last_name="Doe")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id

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
            resp = client.get(f"/users/{self.user1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>New User:</h1>', html)
            self.assertIn('    <p>First Name: <input name="first" type="text" placeholder="Enter first name"></p>', html)

    def test_add_user(self):
        """Test if submiting new user form works."""
        with app.test_client() as client:
            new_user = {"first_name": "Brian", "last_name": "Johnson"}
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
            self.assertIn('<button id="save-changes-btn">Save</button>', html)
