#   import pytest
#   from flaskr.models import User
#   from flaskr import create_app


#   @pytest.fixture(scope='module')
#   def new_user():
#       user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
#       return user

#   def test_new_user_with_fixture(new_user):
#       """
#       GIVEN a User model
#       WHEN a new User is created
#       THEN check the email, hashed_password, authenticated, and role fields are defined correctly
#       """
#       assert new_user.email == 'patkennedy79@gmail.com'
#       assert new_user.username == 'patkennedy'
#       assert new_user.hashed_password != 'FlaskIsAwesome'
#       assert new_user.role == 'user'


#   @pytest.fixture(scope='module')
#   def test_client():
#       flask_app = create_app('flask_test.cfg')

#       # Create a test client using the Flask application configured for testing
#       with flask_app.test_client() as testing_client:
#           # Establish an application context
#           with flask_app.app_context():
#               yield testing_client  # this is where the testing happens!


#   def test_home_page_with_fixture(test_client):
#       """
#       GIVEN a Flask application configured for testing
#       WHEN the '/' page is requested (GET)
#       THEN check that the response is valid
#       """
#       response = test_client.get('/')
#       assert response.status_code == 200
#       assert b"Login to your Health/Diet Planner Account" in response.data



#   def test_points_page_with_fixture(test_client):
#       """
#       GIVEN a Flask application configured for testing
#       WHEN the '/points/' page is requested (GET)
#       THEN check that the response is valid
#       """
#       response = test_client.get('/points/')
#       assert response.status_code == 200
#       assert b"Points History Calendar" in response.data


#   def test_points_page_post_with_fixture(test_client):
#       """
#       GIVEN a Flask application
#       WHEN the '/points/' page is posted to (POST)
#       THEN check that a '405' status code is returned
#       """
#       response = test_client.post('/points/')
#       assert response.status_code == 405
#       assert b"Points History Calendar" not in response.data


#   def test_signup_page_with_fixture(test_client):
#       """
#       GIVEN a Flask application configured for testing
#       WHEN the '/signup/' page is requested
#       THEN check that the response is valid
#       """
#       response = test_client.get('/signup/')
#       assert response.status_code == 200
#       assert b"Sign Up for a New Health/Diet Planner Account" in response.data


#   def test_diet_page_with_fixture(test_client):
#       """
#       GIVEN a Flask application configured for testing
#       WHEN the '/signup/' page is requested
#       THEN check that the response is valid
#       """
#       response = test_client.get('/diet/')
#       assert response.status_code == 200
#       assert b"Enter your Diet/Nutrition Preferences" in response.data
