from unittest import TestCase
from .models import UserDetail
from app import create_app

app = create_app()

class TestUserModel(TestCase):

  # def test_create_user(self):
  #   """Tests successful user creation with valid data."""
  #   username = "test_user"
  #   email = "test@example11.com"
  #   password = "password123"
  #   isAdmin ="Y"
  #   mobileno="98878"

  #   with app.app_context():
  #     user = UserDetail.insert_user(username,mobileno, email, password,isAdmin)

  #   self.assertIsNotNone(user)  # Check if user object is created
  #   self.assertEqual(user.username, username)
  #   self.assertEqual(user.email, email)
  #   # Password is hashed, so we can't directly compare it
  #   self.assertTrue(user.password_hash is not None)  # Check password is hashed

  def test_create_user_duplicate_email(self):
    """Tests creating a user with an existing email raises an error."""
    username = "test_user"
    email = "test@example2342.com"
    password = "password123"
    isAdmin ="Y"
    mobileno="98878"

    with app.app_context():
      # Create a user first
      UserDetail.insert_user(username, mobileno, email, password,isAdmin)

    with self.assertRaises(Exception):  # Replace with specific error type if known
      with app.app_context():
        UserDetail.insert_user(username,mobileno, email, "new_password",isAdmin)  # Try creating with same email

  # def test_create_user_empty_fields(self):
  #   """Tests creating a user with empty fields raises an error."""
  #   empty_username = ""
  #   empty_email = ""
  #   password = "password123"
  #   isAdmin ="Y"
  #   mobileno="98878"

  #   with app.app_context():
  #     with self.assertRaises("Please enter correct email id/password combination"):
  #       UserDetail.insert_user(empty_username,mobileno, "desai@v.com", password,isAdmin)  # Empty username

  #     with self.assertRaises("Please enter correct email id/password combination"):
  #       UserDetail.insert_user("hj",mobileno, "d@b.com", "",isAdmin)  # Empty password
