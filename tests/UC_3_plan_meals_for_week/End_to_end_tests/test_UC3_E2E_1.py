

def UC3_E2E_1(test_client):
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200

