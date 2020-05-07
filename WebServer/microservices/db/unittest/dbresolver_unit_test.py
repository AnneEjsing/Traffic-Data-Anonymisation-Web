import sys
import os
sys.path.append(os.getcwd() + '/..')
import testing.postgresql
import psycopg2
import unittest2
import dbresolver
import json


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


class TestDbresolverMethods(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(port=7654)
        initailise_database(cls.postgresql)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    def test_field_check_matching(self):
        input = ['hej', 'med', 'dig']
        data = {'hej': "data", 'med': "data", 'dig': "data"}
        res = dbresolver.field_check(input, data)
        self.assertEqual(res, None)

    def test_field_check_less_input(self):
        input = ['hej']
        data = {'hej': "data", 'med': "data", 'dig': "data"}
        res = dbresolver.field_check(input, data)
        self.assertEqual(res, None)

    def test_field_check_incorrect_data_not_containing_input(self):
        input = ['hej', 'med', 'dig']
        data = {'hej': "data", 'med': "data"}
        res = dbresolver.field_check(input, data)
        self.assertEqual(res.status, 500)

    def test_field_check_incorrect_data_wrong_case_in_input(self):
        input = ['Hej', 'med', 'dig']
        data = {'hej': "data", 'med': "data", 'dig': "data"}
        res = dbresolver.field_check(input, data)
        self.assertEqual(res.status, 500)

    def test_field_check_incorrect_data_wrong_case_in_data(self):
        input = ['Hej', 'med', 'dig']
        data = {'hej': "data", 'mEd': "data", 'dig': "data"}
        res = dbresolver.field_check(input, data)
        self.assertEqual(res.status, 500)

    def test_has_one_result_pass_array(self):
        input = ['hej']
        res = dbresolver.has_one_result(input, "error", 500)
        self.assertEqual(res.status, 200)

    def test_has_one_result_throws_keyerror_dictionary(self):
        input = {'hej': "med"}
        errorcode = 500
        self.assertRaises(KeyError, dbresolver.has_one_result,
                          input, "error", errorcode)

    def test_has_one_result_error_code(self):
        input = ["hej", "med"]
        error = 403
        res = dbresolver.has_one_result(input, "hej", error)
        self.assertEqual(res.status, 403)

    def test_execute_query_pass(self):
        id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
        query = """
        SELECT camera_id, description
        FROM cameras
        WHERE camera_id = %s;
        """
        expect = {'camera_id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'description': 'This is a description for the open cam'}
        result,error = dbresolver.execute_query(query,id)
        result = dict(result[0])

        self.assertDictEqual(expect,result)
        self.assertFalse(error)

    def test_execute_query_invalid_text_representation(self):
        id = 'not_a_uuid'
        query = """
        SELECT *
        FROM cameras
        WHERE camera_id = %s;
        """
        expect = "invalid input syntax"
        result,error = dbresolver.execute_query(query,id)

        self.assertIn(expect,error)
        self.assertFalse(result)

    def test_execute_query_unique_violation(self):
        camera_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'  
        user_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b11'
        query = """
        INSERT INTO access_rights (camera_id,user_id)
        VALUES (
            %s, %s
        )
        RETURNING *;
        """
        expect = "duplicate key value violates unique constraint"
        result,error = dbresolver.execute_query(query,camera_id,user_id)

        self.assertIn(expect,error)
        self.assertFalse(result)

    def test_execute_query_invalid_datatime_format(self):
        camera_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'  
        user_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12'
        recording_time = 10
        recording_intervals = 10
        start_time = "not an actual date"
        
        query = """
        INSERT INTO recordings (user_id, camera_id, start_time, recording_time, recording_intervals)
        VALUES (
            %s, %s,  %s, %s, %s
        )
        RETURNING *;
        """
        expect = "The data time format is invalid"
        result,error = dbresolver.execute_query(query,user_id,camera_id,start_time,recording_time,recording_intervals)

        self.assertIn(expect,error)
        self.assertFalse(result)

    def test_execute_query_foreign_key_violation(self):
        camera_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11'  
        user_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12'
        recording_time = 10
        recording_intervals = 10
        
        query = """
        INSERT INTO recordings (user_id, camera_id, start_time, recording_time, recording_intervals)
        VALUES (
            %s, %s,  NOW(), %s, %s
        )
        RETURNING *;
        """
        expect = "violates foreign key constraint"
        result,error = dbresolver.execute_query(query,user_id,camera_id,recording_time,recording_intervals)

        self.assertIn(expect,error)
        self.assertFalse(result)

    def test_execute_query_undefined_function(self):
        camera_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380c11'  
        user_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380b12'
        recording_time = 10
        recording_intervals = 10
        
        query = """
        INSERT INTO recordings (user_id, camera_id, start_time, recording_time, recording_intervals)
        VALUES (
            %s, %s,  DEFINETLT_NOT_NOW(), %s, %s
        )
        RETURNING *;
        """
        expect = "No function matches the given name and argument types"
        result,error = dbresolver.execute_query(query,user_id,camera_id,recording_time,recording_intervals)

        self.assertIn(expect,error)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest2.main()
