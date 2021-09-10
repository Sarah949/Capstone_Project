import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import create_app
from models import setup_db, Actor, Movie


# casting_assistant_token = os.getenv('CASTING_ASSISTANT_JWT')
# acting_director_token = os.getenv('ACTING_DIRECTOR_JWT')
# executive_producer_token = os.getenv('EXECUTIVE_PRODUCER_JWT')
casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVFeG5vcV9NSExrZnRWU3F3QjNUUCJ9.eyJpc3MiOiJodHRwczovL3NhcmFoY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMzg2MTliNWNhZTQ2MDA2OTBhMjE2OSIsImF1ZCI6ImNhcHN0b24iLCJpYXQiOjE2MzEyNjg1OTEsImV4cCI6MTYzMTM1NDk5MSwiYXpwIjoieXFKZjZETGxMYTdpNk52c1pBOEFtckxpOWNYT0t2ZzgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.UWexoBCYFqWSW4iTnw02-GXpqw5y2z2tNHlc-IvEb1ZjJz4s6bnfCDSOPqRYnxTjB3lVyAte8HyuaHg4pvks6quM0LJo92vZbw6LFJoKng0HU_t2nXd9sYbAUYmktyAbmClo5PgdiOg8THpx91iL-3uIBWuqFzkrsqoonLTgYYZVZky3dwkML5rjPWqIQtVtNsvlsLHQSDQnNiF83kj102qWNKJe9plE7jTvxe3l3Z_BxSOsns4U7_Olrfu9iE5MwF6FuqZeh1CZkSuGg3cu61T5pTnCR84zUrDjM3VqIwxKfoXF36sqlvcvp-kANpR6zb9NVxTfLibTUndbc2g4KA'
acting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVFeG5vcV9NSExrZnRWU3F3QjNUUCJ9.eyJpc3MiOiJodHRwczovL3NhcmFoY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMzg2MjA3MDA4NDI2MDA2OWRhMDlhOCIsImF1ZCI6ImNhcHN0b24iLCJpYXQiOjE2MzEyMTU1NTMsImV4cCI6MTYzMTMwMTk1MywiYXpwIjoieXFKZjZETGxMYTdpNk52c1pBOEFtckxpOWNYT0t2ZzgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.IVGhgwJRcmznw0zaOA-dFj0b_2ylyL-1uWpfWx43a_RBlAGm7zGS9VzLUOdgG20fKSpPAYC7EmrJdV1KSowZsYlZZPP16GxN7CT3scIDX6o9HAPuEodzhYcWTTH5jXFTMP2yOztNS2oFcqM_zRTxCEfWAavQkMcEokKaeexPKBdrQ2iDbx5XE7LRX6TS23M85MdzcqZKy2luPkuRPNhJicVminBQJzMt1MX_6eoeMK5eAe6f4FQvDc3U12s_AkXewFDvNuPVDaRdjobWpLM8gIuKxulfsRPR6Ghucc0LIRxLUmhK1LK_OIqvJM-RsPf4BmyD5cd64j96V9FjK6uL_w'
executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVFeG5vcV9NSExrZnRWU3F3QjNUUCJ9.eyJpc3MiOiJodHRwczovL3NhcmFoY2Fwc3RvbmUudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMzg2MjRmOTUxODM5MDA3MDgyODdmMSIsImF1ZCI6ImNhcHN0b24iLCJpYXQiOjE2MzEyMTUzODYsImV4cCI6MTYzMTMwMTc4NiwiYXpwIjoieXFKZjZETGxMYTdpNk52c1pBOEFtckxpOWNYT0t2ZzgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.vGY_jebG-nxLL3-c84WUyOJC_IU8JK9q6b4e1aH5i26fl9bfQCBmYlFHC1BlY-ytzA2jkij9qg3v1Zq6Ttluh5mp2S1AovdDASnHLWJ7CkH5fUJP2j-3T-HwfFokB-Z5lI3BdvFAfQkO_FkYIvTYOekHqM7u3b1HLTxoPmgwPMHNrYQZ9w8zZMTSWMxn2VMA39TvI6Z9GoqMCbhYfoZXyok3Gn6hh0HDSR-oIbLa1DZ-aRg1idouWznEYcDK5GikMvzE3k-6P2-cc16QY9PxEpZKy1jbUQPa0JiXM8hGAw1PEjKkcuOQV-hG5Rr0kmkPAbG9XAl90AcYsJe2kv0QRA'


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
        # self.database_name = "actingagency"
        # self.database_path = "postgresql://{}:{}@{}/{}".format(
        #                      'postgres', '1234', 'localhost:5432',
        #                       self.database_name)
        self.database_path = os.environ['DATABASE_URL']
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
