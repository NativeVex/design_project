import pytest
from webapp.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = User("tomliuhyyd@gmail.com", "klg", "qwerty123")
    assert user.email == "tomliuhyyd@gmail.com"
    assert user.password_hashed != "qwerty123"
    assert user.__repr__() == "<User: tomliuhyyd@gmail.com>"
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == "tomliuhyyd@gmail.com"
    assert new_user.username == "klg"
    assert new_user.password_hashed != "qwerty123"


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password("MyNewPassword")
    assert new_user.password_hashed != "MyNewPassword"
    assert new_user.is_password_correct("MyNewPassword")
    assert not new_user.is_password_correct("MyNewPassword2")
    assert not new_user.is_password_correct("qwerty123")


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == "17"