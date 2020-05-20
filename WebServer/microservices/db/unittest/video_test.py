import json
import aiounittest
import testing.postgresql
import psycopg2
import unittest2
import sys
import os
sys.path.append(os.getcwd() + '/..')
import video
import dbresolver
# mock request to resemble aiohttp request


class request:
    dic = {}

    def __init__(self, dict):
        self.dic = dict

    async def json(self):
        return self.dic


def initailise_database(postgresql):
    with psycopg2.connect(**postgresql.dsn()) as conn:
        with conn.cursor() as cursor:
            with open("test_data.sql", "r") as f:
                cursor.execute(f.read())
        conn.commit()
    os.environ['POSTGRES_DB'] = postgresql.dsn()['database']
    os.environ['POSTGRES_USER'] = postgresql.dsn()['user']
    os.environ['POSTGRES_HOST'] = postgresql.dsn()['host']
    os.environ["POSTGRES_PASSWORD"] = ""
    os.environ["POSTGRES_PORT"] = str(postgresql.dsn()['port'])


class VideoGetTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    ## UPDATE
    async def test_update_video(self):
        req = request({"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11","video_thumbnail":"new thumb","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = {"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11","video_thumbnail":"new thumb","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}
        res = await video.video_update(req)
        res = json.loads(res.body.decode("utf-8"))
        self.assertDictContainsSubset(expect,res)

    async def test_update_video_wrong_input(self):
        req = request({"vide_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11","video_thumbnail":"new thumb","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = 500
        res = await video.video_update(req)
        self.assertEqual(expect,res.status)

    async def test_update_video_invalid_params(self):
        req = request({"video_id":"3","video_thumbnail":"new thumb","camera_id":"a0ef8-bb6d-6bb9bd380a11","user_id":"a0eebcbb6d-6bb9bd380b11"})
        expect = 500
        res = await video.video_update(req)
        self.assertEqual(expect,res.status)

    async def test_update_video_no_user_id_match(self):
        req = request({"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb0bd380c11","video_thumbnail":"new thumb","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = 404
        res = await video.video_update(req)
        self.assertEqual(expect,res.status)

    ## GET
    async def test_get_video(self):
        req = request({"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11"})
        expect = {"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11","video_thumbnail":"new vid","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}
        res = await video.video_get(req)
        res = json.loads(res.body.decode("utf-8"))
        self.assertDictContainsSubset(expect,res)

    async def test_get_video_wrong_params(self):
        req = request({"video_id":"a0eebcbb6d-6bb9bd380c11"})
        expect = 500
        res = await video.video_get(req)
        self.assertEqual(expect,res.status)
        
    async def test_get_video_wrong_input_names(self):
        req = request({"video_i":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11"})
        expect = 500
        res = await video.video_get(req)
        self.assertEqual(expect,res.status)
        
    async def test_get_video_wrong_vid(self):
        req = request({"video_id":"a0eebc09-9c0b-4ef8-bb6d-6bb9bd380c11"})
        expect = 404
        res = await video.video_get(req)
        self.assertEqual(expect,res.status)

    async def test_video_list_user(self):
        req = request({"user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = [{'label': 'open cam', 'video_id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11', 'save_time': '2020-06-22 19:10:25', 'camera_id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'}]
        res = await video.video_list_user_id(req)
        res = json.loads(res.body.decode("utf-8"))
        self.assertEqual(res,expect)

    async def test_video_list_user_wrong_input(self):
        req = request({"use_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = 500
        res = await video.video_list_user_id(req)
        self.assertEqual(res.status,expect)

    async def test_video_list_user_wrong_uuid(self):
        req = request({"user_id":"a0eebc99-9c0b-4ef8-b6d-6bb9bd380b11"})
        expect = 500
        res = await video.video_list_user_id(req)
        self.assertEqual(res.status,expect)    

    

class VideoCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    ## Create video
    async def test_create_video_pass(self):
        req = request({"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c12","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11","save_time":"2020-06-22 19:10:25"})
        expect = {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12"}
        res = await video.video_create(req)
        res = json.loads(res.body.decode("utf-8"))
        self.assertDictContainsSubset(expect,res)

    async def test_create_video_fail_params(self):
        req = request({"video_id":"a0eebc99-4ef8-bb6d-6bb9bd380c12","camera_id":"a0eebc99-9c0b-4ef8-6bb9bd380a12","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11","save_time":"2020-06-22 19:10:25"})
        res = await video.video_create(req)
        self.assertEqual(res.status,500)

    async def test_create_video_fail_missing_input(self):
        req = request({})
        res = await video.video_create(req)
        self.assertEqual(res.status,500)

class VideoDeleteTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()
    
    async def test_delete_video(self):
        req = request({"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11"})
        expect = {"video_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11","video_thumbnail":"new vid","camera_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11","user_id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}
        res = await video.video_delete(req)
        res = json.loads(res.body.decode("utf-8"))
        self.assertDictContainsSubset(expect,res)
        
    async def test_delete_video_wrong_params(self):
        req = request({"video_id":"a0eebc99-9c0b-4efd-6bb9bd380c11"})
        expect = 500
        res = await video.video_delete(req)
        self.assertEqual(expect,res.status)
        
    async def test_delete_video_wrong_input_names(self):
        req = request({"video_i":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11"})
        expect = 500
        res = await video.video_delete(req)
        self.assertEqual(expect,res.status)
        
    async def test_delete_video_wrong_vid(self):
        req = request({"video_id":"a0eebc09-9c0b-4ef8-bb6d-6bb9bd380c11"})
        expect = 404
        res = await video.video_delete(req)
        self.assertEqual(expect,res.status)

if __name__ == '__main__':
    unittest2.main()
