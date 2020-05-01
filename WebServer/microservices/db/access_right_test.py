
import dbresolver
import access_right
import unittest2
import psycopg2
import testing.postgresql
import requests
import aiounittest
from aiohttp.test_utils import make_mocked_request
from multidict import MultiDict
import asyncio
import os

class request:
    dic = {}
    def __init__(self,dict):
        self.dic = dict
    async def json(self):
        return self.dic

class AccessRightGetTests(aiounittest.AsyncTestCase):
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

    @asyncio.coroutine
    async def test_get_pass(cls):
        dbresolver.connection_func = lambda: psycopg2.connect(**cls.postgresql.dsn())
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_get(req)
        cls.assertEqual(response.body, b'[{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}]')

    @asyncio.coroutine
    async def test_get_fail_wrong_user_uuid(cls):
        dbresolver.connection_func = lambda: psycopg2.connect(**cls.postgresql.dsn())
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_get(req)
        cls.assertEqual(response.body, b'[]')
    
    @asyncio.coroutine
    async def test_get_fail_wrong_camera_uuid(cls):
        dbresolver.connection_func = lambda: psycopg2.connect(**cls.postgresql.dsn())
        req = request({"camera_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        response = await access_right.right_get(req)
        cls.assertEqual(response.body, b'[]')

    @asyncio.coroutine
    async def test_get_fail_missing_input(cls):
        dbresolver.connection_func = lambda: psycopg2.connect(**cls.postgresql.dsn())
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await access_right.right_get(req)
        cls.assertEqual(response.status, 500)
    
if __name__ == '__main__':
    unittest2.main()