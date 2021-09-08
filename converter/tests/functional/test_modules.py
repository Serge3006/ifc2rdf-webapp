import io

"""
This file constains the functional tests for the app routes

These tests use GETs and POSTs to different URL's to check for the proper behavior
of the app routes
"""


def test_get_home_page(test_client):
    """
    GIVEN a Flask app configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the IFC to RDF Converter" in response.data


def test_post_ifc_file(test_client):
    """
    GIVEN a Flask app configured for testing
    and a ".ifc" file served with the "data" keyword
    WHEN the "/" page if requested (POST)
    THEN check the response is 200
    """

    data = dict(data=(io.BytesIO(b"This is a test"), "test.ifc"))
    response = test_client.post("/", data=data, follow_redirects=True)

    assert response.status_code == 200

def test_post_non_ifc_file(test_client):
    """
    GIVEN a Flask app configured for testing
    and a ".txt" file served with the "data" keyword
    WHEN the "/" page if requested (POST)
    THEN check the response is 400
    """

    data = dict(data=(io.BytesIO(b"This is a test"), "test.txt"))
    response = test_client.post("/", data=data, follow_redirects=True)

    assert response.status_code == 400

def test_post_non_file(test_client):
    """
    GIVEN a Flask app configured for testing
    and a ".txt" file served with the "file" keyword
    WHEN the "/" page if requested (POST)
    THEN check the response is 400
    """

    data = dict(file=(io.BytesIO(b'This is a test'), "test.ifc"))
    response = test_client.post("/", data=data, follow_redirects=True)

    assert response.status_code == 400