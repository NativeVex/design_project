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
    """
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

    from bs4 import BeautifulSoup
    import pandas as pd

    soup = BeautifulSoup(response.data, 'html.parser')
    table = soup.find_all('table')
    tbl_items = [x for x in [x for x in table[0].children if x != '\n'][0] if x != '\n'][1:]
    partitioned = [tbl_items[4*i:4*(i+1)] for i in range(3)]
    dfs = []
    # replaces last index of partitioned with series
    for A in partitioned:
        whitespace_fix = [x.strip().split(':') for x in A[-1].text.split('\n') if x.strip() != '']
        df = (pd.DataFrame(whitespace_fix).set_index(0))[1]
        dfs.append([*A[:-1], df])

    # HERE VALIDATE CODE
