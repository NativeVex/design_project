from dataclasses import dataclass


def utility_webbrowser(html: str):
    import tempfile
    import webbrowser

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        url = "file://" + f.name
        f.write(html)
    webbrowser.open(url)


# def test_old_UC3_E2E_1(test_client, login_default_user):
#     """#2px3786

#     Given a logged in user, request a mealplan and validate it satisfies your expectations.
#     """
#     # 1. fixture for logged in user :: login_default_user

#     # 2. request mealplan
#     response = test_client.post(
#         "/mealplan",
#         data=dict(
#             Calories="129.7",
#             Carbs="57.6",
#             Proteins="68.5",
#             fiber="75.9",
#             caloriesbreakfastamount=".7",
#             calorieslunchamount=".2",
#             carbsbreakfastamount=".3",
#             carbslunchamount=".6",
#             proteinsbreakfastamount=".5",
#             proteinslunchamount=".1",
#         ),
#         follow_redirects=True,
#     )
#     assert b"Personal Meal Plan Recommendations" in response.data
#     assert response.status_code == 200

#     from bs4 import BeautifulSoup

#     soup = BeautifulSoup(response.data, 'html.parser')
#     # calories = soup.find(text="calories") # dunno why this doesn't work

#     import numpy as np
#     import pandas as pd

#     data = [x.strip() for x in soup.text.split("\n") if x != ""]
#     df = pd.DataFrame(data, dtype="string")[0].str.split(":", expand=True)

#     splits = df[df[0] == "Name"].index

#     # TODO
#     # 3. Validate data


def test_UC3_E2E_1(test_client, login_default_user):
    """#2px3786

    Given a logged in user, request a mealplan and validate it satisfies your expectations.
     Uses 'scaling_factor' variable to determine tolerance bounds for received mealplans
    """
    scaling_factor = 0.2

    # Send user constraints
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

    import pandas as pd
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find_all("table")
    tbl_items = [
        x for x in [x for x in table[0].children if x != "\n"][0] if x != "\n"
    ][1:]
    partitioned = [tbl_items[4 * i: 4 * (i + 1)] for i in range(3)]
    dfs = []
    # replaces last index of partitioned with series
    for A in partitioned:
        whitespace_fix = [
            x.strip().split(":") for x in A[-1].text.split("\n") if x.strip() != ""
        ]
        df = (pd.DataFrame(whitespace_fix).set_index(0))[1]
        dfs.append([*A[:-1], df])

    # HERE VALIDATE CODE
    @dataclass
    class Meal:
        name: str
        ingredients: str
        directions: str
        stats: pd.Series

    Expected_Breakfast = Meal(
        "Expected_Breakfast",
        "",
        "",
        pd.Series(
            [
                float(data["Calories"]) *
                float(data["caloriesbreakfastamount"]),
                float(data["Carbs"]) * float(data["carbsbreakfastamount"]),
                float(data["Proteins"]) *
                float(data["proteinsbreakfastamount"]),
            ],
            index=["Calories", "Carbs", "Proteins"],
        ),
    )
    Expected_Lunch = Meal(
        "Expected_Lunch",
        "",
        "",
        pd.Series(
            [
                float(data["Calories"]) * float(data["calorieslunchamount"]),
                float(data["Carbs"]) * float(data["carbslunchamount"]),
                float(data["Proteins"]) * float(data["proteinslunchamount"]),
            ],
            index=["Calories", "Carbs", "Proteins"],
        ),
    )

    derived_calories_dinner: float = 1 - (
        float(data["calorieslunchamount"]) +
        float(data["caloriesbreakfastamount"])
    )
    derived_carbs_dinner: float = 1 - (
        float(data["carbslunchamount"]) + float(data["carbsbreakfastamount"])
    )
    derived_proteins_dinner: float = 1 - (
        float(data["proteinslunchamount"]) +
        float(data["proteinsbreakfastamount"])
    )
    assert derived_proteins_dinner <= 1 and derived_proteins_dinner >= 0
    assert derived_carbs_dinner <= 1 and derived_carbs_dinner >= 0
    assert derived_proteins_dinner <= 1 and derived_proteins_dinner >= 0
    Expected_Dinner = Meal(
        "Expected_Dinner",
        "",
        "",
        pd.Series(
            [
                float(data["Calories"]) * derived_calories_dinner,
                float(data["Carbs"]) * derived_carbs_dinner,
                float(data["Proteins"]) * derived_proteins_dinner,
            ],
            index=["Calories", "Carbs", "Proteins"],
        ),
    )

    # Breakfast
    Breakfast = Meal(
        dfs[0][0], dfs[0][1], dfs[0][2], dfs[0][3][[
            "Calories", "Carbs", "Protein"]]
    )
    # Lunch
    Lunch = Meal(
        dfs[1][0], dfs[1][1], dfs[1][2], dfs[1][3][[
            "Calories", "Carbs", "Protein"]]
    )
    # Dinner
    Dinner = Meal(
        dfs[2][0], dfs[2][1], dfs[2][2], dfs[2][3][[
            "Calories", "Carbs", "Protein"]]
    )

    def _generic_meal_check(Meal, Expected_Meal, scaling_factor):
        # calories
        assert float(Meal.stats.Calories) < (
            Expected_Meal.stats.Calories * (1 + scaling_factor)
        )
        assert float(Meal.stats.Calories) > (
            Expected_Meal.stats.Calories * (1 - scaling_factor)
        )
        # carbs
        assert float(Meal.stats.Carbs) < (
            Expected_Meal.stats.Carbs * (1 + scaling_factor)
        )
        assert float(Meal.stats.Carbs) > (
            Expected_Meal.stats.Carbs * (1 - scaling_factor)
        )
        # proteins
        assert float(Meal.stats.Proteins) < (
            Expected_Meal.stats.Proteins * (1 + scaling_factor)
        )
        assert float(Meal.stats.Carbs) > (
            Expected_Meal.stats.Carbs * (1 - scaling_factor)
        )

    _generic_meal_check(Breakfast, Expected_Breakfast, scaling_factor)
    _generic_meal_check(Lunch, Expected_Lunch, scaling_factor)
    _generic_meal_check(Dinner, Expected_Dinner, scaling_factor)
