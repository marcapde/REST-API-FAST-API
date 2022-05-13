import json
from urllib import response
from fastapi import FastAPI
from fastapi.testclient import TestClient


from app import app

client = TestClient(app)
#will use these list to sabes g_id and i_id returned by the api
galleries = []
images = []


def test_root():
    response = client.get("/")
    assert response.status_code==200
    assert response.json() == {"WELCOME":"go to /galleries for more data"}

###########################################
#lets try to get everything with no data in
###########################################
def test_get_galleries():
    response = client.get("/galleries")
    assert response.status_code==200
    assert response.json() == []

def test_get_galleries_id():
    response = client.get('/galleries/33')
    assert response.status_code==404
    assert response.json() == {'detail': "Gallery not found"}

def test_get_galleries_images():
    response = client.get('/galleries/33/images')
    assert response.status_code==404
    assert response.json() == {'detail': "Gallery not found"}

def test_get_galleries_images_id():
    response = client.get('/galleries/33/images/12')
    assert response.status_code==404
    assert response.json() == {'detail': "Gallery not found"}

def test_get_galleries_images_id():
    response = client.get('/galleries/33/images/12/file')
    assert response.status_code==404
    assert response.json() == {'detail': "Gallery not found"}
