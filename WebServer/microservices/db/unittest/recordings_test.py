import sys
import os
sys.path.append(os.getcwd() + '/..')
import dbresolver
import recordings
import unittest2
import psycopg2
import testing.postgresql
import aiounittest
import json

# mock request to resemble aiohttp request
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

class RecordingsGetTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()


        
    async def test_get_cid_wrong_input_data(self):
        req = request({"cameraid": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        expect = 500
        res = await recordings.list_camera_id(req)
        self.assertEqual(res.status,expect)
            ## GET ALL BY CAM ID TESTS
    async def test_get_cid(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        expect = b'[{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "start_time": "2020-06-22 19:10:25", "recording_time": 7000, "recording_intervals": 7}]'
        res = await recordings.list_camera_id(req)
        self.assertEqual(res.body,expect)
    async def test_get_cid_not_real_id(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380axx"})
        expect = 500
        res = await recordings.list_camera_id(req)
        self.assertEqual(res.status,expect)

    ## GET ALL BY USER ID TESTS
    async def test_get_uid(self):
        req = request({"user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = b'[{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "start_time": "2020-06-22 19:10:25", "recording_time": 7000, "recording_intervals": 7}]'
        res = await recordings.list_user_id(req)
        self.assertEqual(res.body,expect)
        
    async def test_get_uid_wrong_input_data(self):
        req = request({"userid":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = 500
        res = await recordings.list_user_id(req)
        self.assertEqual(res.status,expect)
        
    async def test_get_uid_not_real_id(self):
        req = request({"user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b"})
        expect = 500
        res = await recordings.list_user_id(req)
        self.assertEqual(res.status,expect)

    ## GET ONE BY BOTH USER AND CAMERA ID TESTS
    async def test_get_userid_cameraid_pass(self):
        req = request({'camera_id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'user_id' : 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11'})
        expect = b'{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "start_time": "2020-06-22 19:10:25", "recording_time": 7000, "recording_intervals": 7}'
        res = await recordings.get(req)
        self.assertEqual(res.body,expect)
        
    async def test_get_userid_cameraid_fail_wrong_input(self):
        req = request({'camera_id':'a0eebc99-9c0b-4aef8-bb6d-6bb9bd380a1w', 'user_id' : 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b1w'})
        res = await recordings.get(req)
        self.assertEqual(res.status,500)

    async def test_get_userid_cameraid_fail_missing_input(self):
        req = request({'user_id' : 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b1w'})
        res = await recordings.get(req)
        self.assertEqual(res.status,500)
    
class RecordingsCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    ## CREATE TESTS
    async def test_create_pass(self):
        req = request({'camera_id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'user_id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11', 'recording_time':'7000', 'recording_intervals':'7'})
        expect = {'camera_id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'user_id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11', 'recording_time': 7000, 'recording_intervals': 7}
        res = await recordings.insert(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect, res)
    
    async def test_create_fail_wrong_input(self):
        req = request({'camera_id':'a0eebc99-9c0b-4ef8-bb6d-XXXXXXXX', 'user_id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11', 'recording_time':'7000', 'recording_intervals':'7'})
        res = await recordings.insert(req)
        self.assertEquals(res.status, 500)

    async def test_create_fail_missing_input(self):
        req = request({'user_id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11', 'recording_time':'7000', 'recording_intervals':'7'})
        res = await recordings.insert(req)
        self.assertEquals(res.status, 500)

class RecordingsDeleteTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    async def test_delete(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = b'{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "start_time": "2020-06-22 19:10:25", "recording_time": 7000, "recording_intervals": 7}'
        res = await recordings.delete(req)
        self.assertEqual(res.body,expect)

    async def test_delete_wrong_input_names(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "userid":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = 500
        res = await recordings.delete(req)
        self.assertEqual(res.status,expect)

    async def test_delete_fake_cam_id(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-6bb9bd380a11", "user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = 500
        res = await recordings.delete(req)
        self.assertEqual(res.status,expect)

if __name__ == '__main__':
    unittest2.main()