import sys
import os
sys.path.append(os.getcwd() + '/..')
import dbresolver
import camera
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

class CamearaGetTests(aiounittest.AsyncTestCase):
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
        res = b'{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "description": "This is a description for the open cam", "label": "open cam", "ip": "0.0.0.0", "source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "last_sign_of_life": null, "owner": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12", "model_licens": "Default", "model_face": "Default"}'
        response = await camera.camera_get(req)
        self.assertEqual(response.body, res)
    
    async def test_camera_get_fail_wrong_input(self):
        req = request({"id":"b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await camera.camera_get(req)
        self.assertEqual(response.status, 404)

    async def test_camera_get_fail_input_is_not_uuid(self):
        req = request({"id":"b0eebc99"})
        response = await camera.camera_get(req)
        self.assertEqual(response.status, 500)

    async def test_camera_get_fail_missing_input(self):
        req = request({})
        response = await camera.camera_get(req)
        self.assertEqual(response.status, 500)

    ## GET ALL CAMERAS
    def test_camera_get_all(self):
        req = request({})
        res = b'[{"source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "description": "This is a description for the open cam", "label": "open cam", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "model_licens": "Default", "model_face": "Default"}, {"source": "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8", "description": "This is a very elaborate description of the camera closed to the public. Much exclusive, such rare, wow.", "label": "closed cam", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "model_licens": "Default", "model_face": "Default"}, {"source": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8", "description": "This is not a live stream. However it is a good movie, so you should watch it", "label": "Best movie", "camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13", "model_licens": "Default", "model_face": "Default"}]'
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
        self.assertEqual(response.status, 500)    

    async def test_camera_get_all_for_user_fail_missing_input(self):
        req = request({})
        response = await camera.camera_userlist(req)
        self.assertEqual(response.status, 500)

class CamearaCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()
    ## CREATE CAMERA   
    async def test_camera_create_camera_pass(self):
        req = request({'owner':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12', 'description':'XXX', 'ip':'XXX', 'label':'XXX', 'source':'XXX'})
        response = await camera.camera_create(req)
        self.assertEqual(response.status, 200)

    async def test_camera_create_camera_fail_missing_input(self):
        req = request({'description':'XXX', 'ip':'XXX', 'label':'XXX', 'source':'XXX'})
        response = await camera.camera_create(req)
        self.assertEqual(response.status, 500)

    async def test_camera_create_camera_fail_non_existing_owner(self):
        req = request({'owner':'00000000-9c0b-4ef8-bb6d-6bb9bd380b12','description':'XXX', 'ip':'XXX', 'label':'XXX', 'source':'XXX'})
        response = await camera.camera_create(req)
        self.assertEqual(response.status, 500)

class CamearaUpdateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    ## UPDATE INFO
    async def test_camera_update_info_pass(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "description": "test", "label": "test", "ip": "0.0.0.0", "source": "https://test.m3u8", "last_sign_of_life": "null", "owner": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12"})
        res = b'{"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", "description": "test", "label": "test", "ip": "0.0.0.0", "source": "https://test.m3u8", "last_sign_of_life": null, "owner": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12", "model_licens": "Default", "model_face": "Default"}'
        response = await camera.camera_update(req)
        self.assertEqual(response.body, res)

    async def test_camera_update_info_fail_wrong_id(self):
        req = request({"camera_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "description": "This is a description for the open cam", "label": "open cam", "ip": "0.0.0.0", "source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "last_sign_of_life": "null", "owner": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12"})
        response = await camera.camera_update(req)
        self.assertEqual(response.status, 500)

    async def test_camera_update_info_fail_missing_input(self):
        req = request({"description": "This is a description for the open cam", "label": "open cam", "ip": "0.0.0.0", "source": "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "last_sign_of_life": "null", "owner": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12"})
        response = await camera.camera_update(req)
        self.assertEqual(response.status, 500)

    ## Update face model
    async def test_camera_update_face_pass(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "model_face":"new face"})
        expect = "new face"
        response = await camera.camera_update_model_face(req)
        res = json.loads(response.body.decode('utf-8'))
        self.assertEqual(res["model_face"], expect)

    async def test_camera_update_face_wrong_id(self):
        req = request({"id":"a0eebc99-9cb-4ef8-bb6d-6bb9cd380a12", "model_face":"new face"})
        expect = 500
        response = await camera.camera_update_model_face(req)
        self.assertEqual(response.status, expect)

    async def test_camera_update_face_missing_input(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9cd380a12", "model_fce":"new face"})
        expect = 500
        response = await camera.camera_update_model_face(req)
        self.assertEqual(response.status, expect)

    ## Update license plate model
    async def test_camera_update_license_pass(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12", "model_licens":"new license"})
        expect = "new license"
        response = await camera.camera_update_model_license_plate(req)
        res = json.loads(response.body.decode('utf-8'))
        self.assertEqual(res["model_licens"], expect)

    async def test_camera_update_license_wrong_id(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bbbc380a12", "model_licens":"new license"})
        expect = 500
        response = await camera.camera_update_model_license_plate(req)
        self.assertEqual(response.status, expect)

    async def test_camera_update_license_missing_input(self):
        req = request({"id":"a0eebc99-9c0b-4ef8-bb6d-6bb9cd380a12", "model_lices":"new license"})
        expect = 500
        response = await camera.camera_update_model_license_plate(req)
        self.assertEqual(response.status, expect)

    ## UPDATE LAST SIGN OF LIFE
    async def test_camera_update_lsol_pass(self):
        req = request({"id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await camera.camera_updatelsol(req)
        self.assertEqual(response.status, 200)

    async def test_camera_update_lsol_fail_wrong_id(self):
        req = request({"id": 9})
        response = await camera.camera_updatelsol(req)
        self.assertEqual(response.status, 500)

    async def test_camera_update_lsol_fail_missing_input(self):
        req = request({})
        response = await camera.camera_updatelsol(req)
        self.assertEqual(response.status, 500)

class CamearaDeleteTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    async def test_camera_delete_pass(self):
        req = request({"id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"})
        response = await camera.camera_delete(req)
        self.assertEqual(response.status, 200)

    async def test_camera_delete_fail_uuid_not_found(self):
        req = request({"id": "00000000-9c0b-4ef8-b6d-6bb9bd380a11"})
        response = await camera.camera_delete(req)
        self.assertEqual(response.status, 500)

    async def test_camera_delete_fail_missing_input(self):
        req = request({})
        response = await camera.camera_delete(req)
        self.assertEqual(response.status, 500)

if __name__ == '__main__':
    unittest2.main()