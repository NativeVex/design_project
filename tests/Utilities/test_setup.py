import pytest

from webapp.app import db
from webapp.models import User


def test_new_db_exists(test_client, register_sample_account):
    cnt = db.session.query(User).count()
    assert cnt == 1
