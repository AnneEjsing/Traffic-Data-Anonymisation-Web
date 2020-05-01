
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
    dic = {"hej":"du"}
    def __init__(self,dict):
        self.dic = dict
    async def json(self):
        return self.dic

class MyTest(aiounittest.AsyncTestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql(port=7654)
        with psycopg2.connect(**self.postgresql.dsn()) as conn:
            with conn.cursor() as cursor:
                with open("test_data.sql","r") as f:
                    cursor.execute(f.read())
            conn.commit()
            
        os.environ['POSTGRES_DB'] = self.postgresql.dsn()['database']
        os.environ['POSTGRES_USER'] = self.postgresql.dsn()['user']
        os.environ['POSTGRES_HOST'] = self.postgresql.dsn()['host']
        os.environ["POSTGRES_PASSWORD"] = ""
        os.environ["POSTGRES_PORT"] = str(self.postgresql.dsn()['port'])

    
    def tearDown(self):
        self.postgresql.stop()

    @asyncio.coroutine
    async def test_get(self):
        dbresolver.connection_func = lambda: psycopg2.connect(**self.postgresql.dsn())
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})

        response = await access_right.right_get(req)

        self.assertEqual(response.body, b'[{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}]')

    @asyncio.coroutine
    async def test_get_wrong_uid(self):
        dbresolver.connection_func = lambda: psycopg2.connect(**self.postgresql.dsn())
        req = request({"camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        
        response = await access_right.right_get(req)

        self.assertEqual(response.body, b'[]')
    

if __name__ == '__main__':
    unittest2.main()