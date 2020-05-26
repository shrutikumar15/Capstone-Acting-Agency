import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, setup_db
import json
import pprint
from dotenv import load_dotenv
from pathlib import Path

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        env_path = Path('setup.sh') 
        load_dotenv(dotenv_path=env_path)
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "capstone"
        self.database_path = os.getenv('DATABASE_URL')
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        def tearDown(self):
            """Executed after each test"""
            pass

    def test_get_actors(self):
        res = self.client.get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        res = self.client.get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_get_actors_casting_assistant(self):
        res = self.client.get(
            '/actors',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_without_permissions_casting_assistant(self):
        res = self.client.delete(
            '/movies/1',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 401)

    def test_get_movies_casting_director(self):
        res = self.client.get(
            '/movies',
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 200)
        

    def test_create_movie_without_permission_casting_director(self):
        res = self.client.post(
            '/movies/create',
            json={
                "title": "Harry Potter",
                "release_date": "2020-01-01"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 401)

    def test_create_actors_casting_director(self):
        res = self.client.post(
            '/actors/create',
            json={
                "name": "Timothtee Chalamet",
                "gender": "male",
                "age": 43
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR_JWT')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    

    def test_patch_actors_casting_director(self):
        res = self.client.patch(
            '/actors/1',
            json={
                "name": "Some name",
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    

    def test_patch_without_permission_casting_director(self):
        res = self.client.patch(
            '/actors/1',
            json={
                "name": "Selena Gomez"
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_ASSISTANT_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 401)

    

    def test_patch_actors_age_casting_director(self):
        res = self.client.patch(
            '/actors/2',
            json={
                "age": 8,
            },
            headers={
                "Authorization": f"Bearer {os.getenv('CASTING_DIRECTOR_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_create_actors_executive_producer(self):
        res = self.client.post(
            '/actors/create',
            json={
                "name": "Jennifer Lawrence",
                "gender": "female",
                "age": 25
            },
            headers={
                "Authorization": f"Bearer {os.getenv('EXECUTIVE_PRODUCER_JWT')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_movie_executive_producer(self):
        res = self.client.post(
            '/movies/create',
            json={
                "title": "Some movie",
                "release_date": "2020-01-01"
            },
            headers={
               "Authorization": f"Bearer {os.getenv('EXECUTIVE_PRODUCER_JWT')}"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_test_delete_actors_executive_producer(self):
        res = self.client.delete(
            '/actors/1',
            headers={
                 "Authorization": f"Bearer {os.getenv('EXECUTIVE_PRODUCER_JWT')}"
            }
        )
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
