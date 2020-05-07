import sys
import os
sys.path.append(os.getcwd() + '/..')
import dbresolver
import access_right
import unittest2
import psycopg2
import testing.postgresql
import aiounittest

class request:
    dic = {}
    def __init__(self,dict):
        self.dic = dict
    async def json(self):
        return self.dic

def initailise_database(postgresql):
    with psycopg2.connect(**postgresql.dsn()) as conn:
        with conn.cursor() as cursor:
            with open("test_data.sql","r") as f:
                cursor.execute(f.read())
        conn.commit()

    os.environ['POSTGRES_DB'] = postgresql.dsn()['database']
    os.environ['POSTGRES_USER'] = postgresql.dsn()['user']
    os.environ['POSTGRES_HOST'] = postgresql.dsn()['host']
    os.environ["POSTGRES_PASSWORD"] = ""
    os.environ["POSTGRES_PORT"] = str(postgresql.dsn()['port'])


class AccessRightGetCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    ## GET TESTS
    async def test_get_pass(self):
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_get(req)
        self.assertEqual(response.body, b'[{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}]')

    async def test_get_fail_wrong_user_uuid(self):
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_get(req)
        self.assertEqual(response.body, b'[]')
    
    async def test_get_fail_wrong_camera_uuid(self):
        req = request({"camera_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_get(req)
        self.assertEqual(response.body, b'[]')

    async def test_get_fail_missing_input(self):
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await access_right.right_get(req)
        self.assertEqual(response.status, 500)

    ## POST TESTS
    async def test_create_pass(self):
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_create(req)
        self.assertEqual(response.body, b'[{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}]')
        
    async def test_create_fail_wrong_user_uuid(self):
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "user_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_create(req)
        self.assertEqual(response.status, 409)

    async def test_create_fail_wrong_camera_uuid(self):
        req = request({"camera_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_create(req)
        self.assertEqual(response.status, 409)       

    async def test_create_fail_missing_input(self):
        req = request({"camera_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12"})
        response = await access_right.right_create(req)
        self.assertEqual(response.status, 500)   

class AccessRightDeleteTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    ## DELETE TESTS
    async def test_delete_pass(self):
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_delete(req)
        self.assertEqual(response.body, b'{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}')

    async def test_delete_fail_wrong_input(self):
        req = request({"camera_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_delete(req)
        self.assertEqual(response.status, 404)
        
    async def test_delete_fail_input_param(self):
        req = request({"camera_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await access_right.right_delete(req)
        self.assertEqual(response.status, 500)
    
if __name__ == '__main__':
    unittest2.main()