""" This file appears to assume that there already exists a user with email "anything@gmail.com in the db.

I'm going to need to look into why this works, if the db gets dropped inbetween
runs... It's likely that the sqlite3 file is pre-filled with this value, which
is bad practice because we can't re-create that file on demand using pytest
afaik.

042322 FIXED --Artur

"""

import pytest


def test_login_success(test_client, register_sample_account):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check the response is valid when users enter their username and password
    """
    response = test_client.post(
        "/",
        data=dict(email="anything@gmail.com", password="some"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Enter your Diet/Nutrition Preferences" in response.data


# @pytest.mark.xfail(reason="testing that unregistered account login will fail")
# @pytest.mark.skip(reason="Appears that users table doesn't exist... Need to investigate")
def test_login_failed(test_client, register_sample_account):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (POST)
    THEN check that the response is valid

    This test requires the database table users to exist. The
    register_sample_account fixture ensures that this happens.
    """
    response = test_client.post(
        "/", data=dict(email="any@gmail.com", password="notsome"), follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data
