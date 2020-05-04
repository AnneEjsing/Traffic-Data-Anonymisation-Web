import json
import aiounittest
import testing.postgresql
import psycopg2
import unittest2
import sys
import os
sys.path.append(os.getcwd() + '/..')
import video_settings
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


class VideoSettingsGetTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    async def test_video_settings_get(self):
        expect = b'{"recording_limit": 18000}'
        res = await video_settings.get(request({}))
        self.assertEqual(res.body, expect)


class VideoSettingsCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    async def test_video_settings_update_pass(self):
        req = request({'recording_limit': '20000'})
        expect = b'{"recording_limit": 20000}'
        res = await video_settings.update(req)
        self.assertEqual(res.body, expect)

    async def test_video_settings_update_fail_missing_input(self):
        req = request({})
        res = await video_settings.update(req)
        self.assertEqual(res.status, 500)

    async def test_video_settings_update_fail_wrong_input(self):         
        req = request({'recording_limit': 'hej'})         
        res = await video_settings.update(req)         
        self.assertEqual(res.status, 500)

if __name__ == '__main__':
    unittest2.main()
