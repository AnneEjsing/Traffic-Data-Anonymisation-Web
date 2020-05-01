
import dbresolver
import camera
import unittest2
import psycopg2
import testing.postgresql
import aiounittest
import os

class request:
    dic = {}
    def __init__(self,dict):
        self.dic = dict
    async def json(self):
        return self.dic

class CamearaGetCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        with psycopg2.connect(**cls.postgresql.dsn()) as conn:
            with conn.cursor() as cursor:
                with open("test_data.sql","r") as f:
                    cursor.execute(f.read())
            conn.commit()

        os.environ['POSTGRES_DB'] = cls.postgresql.dsn()['database']
        os.environ['POSTGRES_USER'] = cls.postgresql.dsn()['user']
        os.environ['POSTGRES_HOST'] = cls.postgresql.dsn()['host']
        os.environ["POSTGRES_PASSWORD"] = ""
        os.environ["POSTGRES_PORT"] = str(cls.postgresql.dsn()['port'])

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()


    ## GET ONE CAMERA TESTS
    async def camera_get_pass(cls):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await camera.camera_get(req)
        print(response.body)
        cls.assertEqual(response.body, b'{"id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"}')

    def asdalskd(cls):
        cls.assertEqual("you have failed this city!", "hej")



    ## GET ALL CAMERAS

    ## GET ALL CAMERAS AVAILABLE TO A USER

    
if __name__ == '__main__':
    unittest2.main()