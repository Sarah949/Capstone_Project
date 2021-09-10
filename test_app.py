import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import create_app
from models import setup_db, Actor, Movie
from dotenv import load_dotenv

load_dotenv()

casting_assistant_token = os.getenv('CASTING_ASSISTANT_JWT')
acting_director_token = os.getenv('ACTING_DIRECTOR_JWT')
executive_producer_token = os.getenv('EXECUTIVE_PRODUCER_JWT')


def get_header(role):
    if role == 'casting_assistant':
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(casting_assistant_token)
        }
    elif role == 'acting_director':
        return {
            "Content-Type": "application/json",
            'Authorization': 'Bearer {}'.format(acting_director_token)
        }
    elif role == 'executive_producer':
        return {
            "Content-Type": "application/json",
            'Authorization': 'Bearer {}'.format(executive_producer_token)
        }


class CapstonTestCase(unittest.TestCase):
    """This class represents the capston test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "actingagency"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
                             'postgres', '1234', 'localhost:5432',
                              self.database_name)
        # self.database_path = os.getenv('DATABASE_URL')
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "age": 44,
            "gender": "Male",
            "name": "Édgar Ramírez"
        }

        self.new_movie = {
            "release_date": "2021-06-17",
            "title": "Luca"
        }

        self.new_movie_no_title = {
            "release_date": "2021-06-17",
        }
        self.update_movie = {
            "release_date": "2021-06-17",
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    GET /movies
    """

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers=get_header("casting_assistant"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_failed(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    """
    GET /actors
    """
    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers=get_header("acting_director"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_failed(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    POST /movies
    """
    def test_create_movies(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=get_header("executive_producer"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_post_movies_failed(self):
        res = self.client().post('/movies', json=self.new_movie_no_title,
                                 headers=get_header("executive_producer"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    """
    POST /movies
    """
    def test_create_actors(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=get_header("acting_director"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_post_actors_failed(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=get_header("casting_assistant"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    """
    DELETE /movies/<id>
    """

    def test_delete_movies(self):
        res = self.client().delete('/movies/1',
                                   headers=get_header("executive_producer"))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_failed(self):
        res = self.client().delete('/movies/20',
                                   headers=get_header("executive_producer"))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """
    DELETE /actors/<id>
    """
    def test_delete_actors(self):
        res = self.client().delete('/actors/1',
                                   headers=get_header("executive_producer"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_failed(self):
        res = self.client().delete('/actors/20',
                                   headers=get_header("executive_producer"))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """
    PATCH /movies/<id>
    """

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers=get_header('executive_producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_update_movies_failed(self):
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers=get_header('casting_assistant'))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    PATCH /actors/<id>
    """
    def test_update_actors(self):
        res = self.client().patch('/actors/1', json={'age': 40},
                                  headers=get_header('executive_producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_actors_failed(self):
        res = self.client().patch('/actors/3', json={'age': 40},
                                  headers=get_header('casting_assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
