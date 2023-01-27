from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app=app)


# ~~~ Positive Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Positive Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Positive Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Coffee tests
def test_index_coffees():
    response = client.get('/coffees')
    assert response.status_code == status.HTTP_200_OK

def test_show_coffee():
    response = client.get('/coffees/1')
    assert response.status_code == status.HTTP_200_OK

def test_show_coffee_roaster():
    response = client.get('/coffees/1/roaster')
    assert response.status_code == status.HTTP_200_OK

# Roaster tests
def test_index_roasters():
    response = client.get('/roasters')
    assert response.status_code == status.HTTP_200_OK

def test_show_roaster():
    response = client.get('/roasters/1')
    assert response.status_code == status.HTTP_200_OK

def test_show_roaster_coffees():
    response = client.get('/roasters/1/coffees')
    assert response.status_code == status.HTTP_200_OK


#User tests
def test_create_user():
    response = client.post('/users', json={"username": "testuserz", "email": "testuserz@testuzerz.com", "password": "testuzerz"})
    assert response.status_code == status.HTTP_201_CREATED

# ~~~ Negative Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Negative Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Negatie Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# User tests
def test_create_user_n():
    response = client.post('/users', json={"username": "admin", "email": "admin@admin.com", "password": "admin"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

