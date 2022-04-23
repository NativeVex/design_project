from webapp.app import db
from webapp.models import User

def test_UC3_E2E_2(test_client, register_sample_account, login_default_user):
    """#2px3bng

    Given a logged in user, create a request for a mealplan and validate that
    it is stored in the db after creation. 
    """

    data = dict(
        Calories="129.7",
        Carbs="57.6",
        Proteins="68.5",
        fiber="75.9",
        caloriesbreakfastamount=".7",
        calorieslunchamount=".2",
        carbsbreakfastamount=".3",
        carbslunchamount=".6",
        proteinsbreakfastamount=".5",
        proteinslunchamount=".1",
    )

    response = test_client.post(
        "/mealplan",
        data=data,
        follow_redirects=True,
    )
    assert b"Personal Meal Plan Recommendations" in response.data
    assert response.status_code == 200

    user = db.session.query(User).filter(User.email == "anything@gmail.com").first()
    A = user.get_mealplan()
    assert A is not None

