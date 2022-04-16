def test_UC3_E2E_1(test_client, login_default_user):
    """ #2px3786

    Given a logged in user, request a mealplan and validate it satisfies your expectations.
    """
    # 1. fixture for logged in user :: OK

    # 2. request mealplan 
    response = test_client.post(
        "/mealplan",
        data=dict(
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
        ),
        follow_redirects=True,
    )
    assert b"Personal Meal Plan Recommendations" in response.data
    assert response.status_code == 200

    # 3. Validate data

