# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/home")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Portfolio</title>" in html
        # TODO Add more tests relating to the home page
        assert '<div class="base__header">' in html
        assert '<div class="base__container">' in html
        assert '<div class="base__card">' in html


    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # TODO Add more tests relating to the /api/timeline_post GET and POST apis
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "name" in json

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert len(json["timeline_posts"]) == 1

        # TODO Add more tests relating to the timeline page
    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<button type="submit">' in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        print(html)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "Johne Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html