from webapp import data_src
from webapp.data_src import DataStructures
from webapp.models import User, db


def save_health_req(email: str, health_req):
    user = db.session.query(User).filter_by(email=email).first()

    if user:
        user.add_health_req(health_req)

    db.session.add(user)
    db.session.commit()
    return health_req


def get_curr_health_req(email: str):
    user = db.session.query(User).filter_by(email=email).first()

    if user:
        curr_health_req = user.get_curr_health_req()
        return curr_health_req
    return


def get_old_health_req(email: str):
    user = db.session.query(User).filter_by(email=email).first()

    if user:
        old_health_req = user.get_old_health_req()
        return old_health_req
    return
