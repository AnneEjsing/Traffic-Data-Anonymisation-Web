import sys
import os
sys.path.append(os.getcwd() + '/..')
import dbresolver
import user
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

class UserGetUpdateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()
    
    ## GET USER BY ID
    async def test_user_get_by_id_pass(self):
        req = request({'id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11'})
        expect = {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "email": "notadmin@notadmin.no", "role": "user"}
        res = await user.user_get_id(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect, res)

    async def test_user_get_by_id_fail_wrong_input(self):
        req = request({'id':'a0eebc99-9c0b-4ef8-XXXX-6bb9bd380b11'})
        res = await user.user_get_id(req)
        self.assertEqual(res.status,500)

    async def test_user_get_by_id_fail_missing_input(self):
        req = request({})
        res = await user.user_get_id(req)
        self.assertEqual(res.status,500)

    ## GET USER BY EMAIL
    async def test_user_get_by_email_pass(self):
        req = request({"email": "notadmin@notadmin.no"})
        expect = {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "email": "notadmin@notadmin.no", "role": "user"}
        res = await user.user_get_email(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect, res)

    async def test_user_get_by_email_fail_wrong_input(self):
        req = request({"email": "notadmin@notadmin.dk"})
        res = await user.user_get_email(req)
        self.assertEqual(res.status,404)

    async def test_user_get_by_email_fail_missing_input(self):
        req = request({})
        res = await user.user_get_email(req)
        self.assertEqual(res.status,500)

    ## Login
    async def test_user_login(self):
        req = request({"email":"notadmin@notadmin.no","password":"passpass"})
        expect = {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "email": "notadmin@notadmin.no", "role": "user"}
        res = await user.user_login(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect,res)

    async def test_user_login_wrong_input_name(self):
        req = request({"emil":"notadmin@notadmin.no","password":"passpass"})
        expect = 500
        res = await user.user_login(req)
        self.assertEqual(expect,res.status)

    async def test_user_login_wrong_email(self):
        req = request({"email":"notadmin@notadmi.no","password":"passpass"})
        expect = 401
        res = await user.user_login(req)
        self.assertEqual(expect,res.status)

    async def test_user_login_wrong_password(self):
        req = request({"email":"notadmin@notadmin.no","password":"notpasspass"})
        expect = 401
        res = await user.user_login(req)
        self.assertEqual(expect,res.status)

    ## GET ALL
    def test_user_get_all_pass(self):
        expect = [{"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "email": "notadmin@notadmin.no", "role": "user"}, {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12", "email": "admin@admin.no", "role": "admin"}]
        res = user.user_list(request({}))
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect[0],res[0])
        self.assertDictContainsSubset(expect[1],res[1])

    ## User update
    async def test_user_update(self):
        req = request({"email":"notadmin@notadmin.no","password":"passpass","rights":"admin","id":"a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"})
        expect = {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11", "email": "notadmin@notadmin.no", "role": "admin"}
        res = await user.user_update(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect,res)

    async def test_user_update_wrong_input_name(self):
        req = request({"emil":"notadmin@notadmin.no","password":"passpass"})
        expect = 500
        res = await user.user_update(req)
        self.assertEqual(expect,res.status)

    async def test_user_update_incorrect_id(self):
        req = request({"email":"notadmin@notadmin.no","password":"passpass","rights":"admin","id":"a0eebc99-9c0b-4ef8-bbd-6bb9bd380b11"})
        expect = 500
        res = await user.user_update(req)
        self.assertEqual(expect,res.status)

    async def test_user_update_nonexisting_id(self):
        req = request({"email":"notadmin@notadmin.no","password":"passpass","rights":"admin","id":"a0eebc99-9c0b-4ef8-bb7d-6bb9bd380b11"})
        expect = 404
        res = await user.user_update(req)
        self.assertEqual(expect,res.status)


class UserCreateTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    async def test_user_signup(self):
        req = request({"email":"notadmin@notadmin.yes","password":"passpass","rights":"admin"})
        expect = {"email": "notadmin@notadmin.yes", "role": "admin"}
        res = await user.user_signup(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect,res)

    async def test_user_signup_wrong_input_names(self):
        req = request({"emaail":"notadmin@notadmin.yes","password":"passpass","rights":"admin"})
        expect = 500
        res = await user.user_signup(req)
        self.assertEqual(expect,res.status)

    async def test_user_signup_same_email(self):
        req = request({"email":"notadmin@notadmin.no","password":"passpass","rights":"admin"})
        expect = 500
        res = await user.user_signup(req)
        self.assertEqual(expect,res.status)

   
class UserDeleteTests(aiounittest.AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    async def test_user_delete_pass(self):
        req = request({'id':'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11'})
        expect = {"user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11"}
        res = await user.user_delete(req)
        res = json.loads(res.body.decode('utf-8'))
        self.assertDictContainsSubset(expect, res)

    async def test_user_delete_fail_wrong_input(self):
        req = request({'id':'a0eebc99-9c0b-4ef8-XXXX-6bb9bd380b11'})
        res = await user.user_delete(req)
        self.assertEqual(res.status,500)

    async def test_user_delete_fail_missing_input(self):
        req = request({})
        res = await user.user_delete(req)
        self.assertEqual(res.status,500)

if __name__ == '__main__':
    unittest2.main()
