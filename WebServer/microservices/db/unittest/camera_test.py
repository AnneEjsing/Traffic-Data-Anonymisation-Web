import sys
import os
sys.path.append(os.getcwd() + '/..')
import dbresolver
import camera
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


class CamearaGetCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()


    ## GET ONE CAMERA TESTS
    async def test_camera_get_pass(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        res = b'{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "description": "This is a description for the open cam", "label": "open cam", "ip": "0.0.0.0", "source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "last_sign_of_life": null, "owner": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12"}'
        response = await camera.camera_get(req)
        self.assertEqual(response.body, res)
    
    async def test_camera_get_fail_wrong_input(self):
        req = request({"id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await camera.camera_get(req)
        self.assertEqual(response.status, 404)

    async def test_camera_get_fail_input_is_not_uuid(self):
        req = request({"id":"b0eebc99"})
        response = await camera.camera_get(req)
        self.assertEqual(response.status, 404)

    async def test_camera_get_fail_missing_input(self):
        req = request({})
        response = await camera.camera_get(req)
        self.assertEqual(response.status, 500)

    ## GET ALL CAMERAS
    def test_camera_get_all(self):
        req = request({})
        res = b'[{"source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "description": "This is a description for the open cam", "label": "open cam", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"}, {"source": "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8", "description": "This is a very elaborate description of the camera closed to the public. Much exclusive, such rare, wow.", "label": "closed cam", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12"}, {"source": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8", "description": "This is not a live stream. However it is a good movie, so you should watch it", "label": "Best movie", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13"}]'
        response = camera.camera_list(req)
        self.assertEqual(response.body, res)

    ## GET ALL CAMERAS AVAILABLE TO A USER
    async def test_camera_get_all_for_user_pass(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        res = b'[{"source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "description": "This is a description for the open cam", "label": "open cam", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"}]'
        response = await camera.camera_userlist(req)
        self.assertEqual(response.body, res)
    
    async def test_camera_get_all_for_user_fail_input_is_not_uuid(self):
        req = request({"id":7})
        response = await camera.camera_userlist(req)
        print(response.body)
        self.assertEqual(response.status, 500)    

    async def test_camera_get_all_for_user_fail_missing_input(self):
        req = request({})
        response = await camera.camera_userlist(req)
        self.assertEqual(response.status, 500)   
    
if __name__ == '__main__':
    unittest2.main()