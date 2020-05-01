import sys
import os
sys.path.append(os.getcwd() + '/..')
import dbresolver
import unittest2
import psycopg2

class TestDbresolverMethods(unittest2.TestCase):
    def test_field_check_matching(self):
        input = ['hej', 'med', 'dig'] 
        data = {'hej':"data", 'med':"data", 'dig':"data"}
        res = dbresolver.field_check(input,data)
        self.assertEqual(res,None)
        
    def test_field_check_less_input(self):
        input = ['hej'] 
        data = {'hej':"data", 'med':"data", 'dig':"data"}
        res = dbresolver.field_check(input,data)
        self.assertEqual(res,None)

    def test_field_check_incorrect_data_not_containing_input(self):
        input = ['hej', 'med', 'dig'] 
        data = {'hej':"data", 'med':"data"}
        res = dbresolver.field_check(input,data)
        self.assertEqual(res.status, 500)

    def test_field_check_incorrect_data_wrong_case_in_input(self):
        input = ['Hej', 'med', 'dig'] 
        data = {'hej':"data", 'med':"data", 'dig':"data"}
        res = dbresolver.field_check(input,data)
        self.assertEqual(res.status, 500)

    def test_field_check_incorrect_data_wrong_case_in_data(self):
        input = ['Hej', 'med', 'dig'] 
        data = {'hej':"data", 'mEd':"data", 'dig':"data"}
        res = dbresolver.field_check(input,data)
        self.assertEqual(res.status, 500)

    def test_has_one_result_pass_array(self):
        input = ['hej']
        res = dbresolver.has_one_result(input, "error", 500)
        self.assertEqual(res.status, 200)
        
    def test_has_one_result_throws_keyerror_dictionary(self):
        input = {'hej':"med"}
        errorcode = 500
        self.assertRaises(KeyError, dbresolver.has_one_result, input, "error", errorcode)

    def test_has_one_result_error_code(self):
        input = ["hej", "med"]
        error = 403
        res = dbresolver.has_one_result(input,"hej",error)
        self.assertEqual(res.status, 403)
    
    def test_execute_query(self):
        query = "SELECT * FROM cameras"
        self.assertRaises(psycopg2.OperationalError,dbresolver.execute_query,query)
    
if __name__ == '__main__':
    unittest2.main()