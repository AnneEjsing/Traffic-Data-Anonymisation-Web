import unittest2
import sys
import os
sys.path.append(os.getcwd() + '/..')
import auth_token

class AuthTokenTests(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        auth_token.secretKey = "test"

    def test_is_not_expired_pass(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQ.RmEnR7ygkmXGiT6k532Zj3kEHdYfiqPzd7zlRVc3XVqM6XpdT44QwOXqvmoGYmSQ6J81VzpR4mzPBqhGud6bZg"
        res = auth_token.is_not_expired(token)
        self.assertTrue(res)
    
    #Change token
    def test_is_not_expired_fail_expired_token(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMDE5LTA1LTA0VDIzOjU0OjIzLjIzMjMifQ.ki7a9Fg3e6IcfOFFYqDOEj-tTdqhNmmzX769dqpwaXbcJEmgnEKPbLqR80_aEO_FNMINWZLV7vtPn94HByAdKw"
        res = auth_token.is_not_expired(token)
        self.assertFalse(res)

    #Change token
    def test_is_not_expired_fail_invalid_token(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQRmEnR7ygkmXGiT6k532Zj3kEHdYfiqPzd7zlRVc3XVqM6XpdT44QwOXqvmoGYmSQ6J81VzpR4mzPBqhGud6bZg"
        res = auth_token.is_not_expired(token)
        self.assertFalse(res)

    #Authenticate token
    def test_authenticate_pass(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQ.deQB3qsSJYzYAeyWlfoX9MIG1sMx1vEo9SHVQuj7_P7Sn655I-93Ng4A0WsdfGrMYY0LV3dQaJjxrXnaojVMPA"
        res = auth_token.authenticate(token)
        self.assertTrue(res)

    def test_authenticate_wrong_secret(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQ.RmEnR7ygkmXGiT6k532Zj3kEHdYfiqPzd7zlRVc3XVqM6XpdT44QwOXqvmoGYmSQ6J81VzpR4mzPBqhGud6bZg"
        res = auth_token.authenticate(token)
        self.assertFalse(res)

    ## Verify token
    def test_verify_token_admin_pass(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQ.deQB3qsSJYzYAeyWlfoX9MIG1sMx1vEo9SHVQuj7_P7Sn655I-93Ng4A0WsdfGrMYY0LV3dQaJjxrXnaojVMPA"
        rights = 'admin'
        expected = (True,200)
        res = auth_token.verify_token(token,rights)
        self.assertEqual(expected, res)

    def test_verify_token_user_pass(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoidXNlciIsImV4cCI6IjIxMjAtMDUtMDRUMjM6NTQ6MjMuMjMyMyJ9.zayLZxR_D199MU8VpvhHiLO85fKm6td3ugdbi5Y7lGTLU9KJHIthSOpo-ydaZinwbGLKznCi-BDzYIESdr-aoA"
        rights = 'user'
        expected = (True,200)
        res = auth_token.verify_token(token,rights)
        self.assertEqual(expected, res)
    
    def test_verify_token_fail_wrong_token(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiY.WRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQRmEnR7ygkmXGiT6k532Zj3kEHdYfiqPzd7zlRVc3XVqM6XpdT44QwOXqvmoGYmSQ6J81VzpR4mzPBqhGud6bZg"
        rights = ""
        expected = (False, 401)
        res = auth_token.verify_token(token, rights)
        self.assertEqual(expected, res)

    def test_verify_token_fail_user_is_not_admin(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoidXNlciIsImV4cCI6IjIxMjAtMDUtMDRUMjM6NTQ6MjMuMjMyMyJ9.zayLZxR_D199MU8VpvhHiLO85fKm6td3ugdbi5Y7lGTLU9KJHIthSOpo-ydaZinwbGLKznCi-BDzYIESdr-aoA"
        rights = "admin"
        expected = (False, 403)
        res = auth_token.verify_token(token, rights)
        self.assertEqual(expected, res)

    def test_verify_token_fail_admin_is_not_user(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoiYWRtaW4iLCJleHAiOiIyMTIwLTA1LTA0VDIzOjU0OjIzLjIzMjMifQ.deQB3qsSJYzYAeyWlfoX9MIG1sMx1vEo9SHVQuj7_P7Sn655I-93Ng4A0WsdfGrMYY0LV3dQaJjxrXnaojVMPA"
        rights = "user"
        expected = (False, 403)
        res = auth_token.verify_token(token, rights)
        self.assertEqual(expected, res)

    def test_get_user_id_pass(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoidXNlciIsImV4cCI6IjIxMjAtMDUtMDRUMjM6NTQ6MjMuMjMyMyJ9.6VTtr_0f4LAwmiGoHLl43PiXmky82GWT3KSEO3EuQ5jI3Lo1z5GmcgJW2wCiSuFhwz_R8bAGzwXmQl_reNRHNg"
        expected = "1234567890"
        res =  auth_token.get_user_id(token)
        self.assertEqual(res,expected)        

    def test_get_rights_pass(self):
        token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiamlkIjoiMTIzIiwicmlnaHRzIjoidXNlciIsImV4cCI6IjIxMjAtMDUtMDRUMjM6NTQ6MjMuMjMyMyJ9.6VTtr_0f4LAwmiGoHLl43PiXmky82GWT3KSEO3EuQ5jI3Lo1z5GmcgJW2wCiSuFhwz_R8bAGzwXmQl_reNRHNg"
        expected = "user"
        res =  auth_token.get_rights(token)
        self.assertEqual(res,expected)

    def test_encode_not_bytes(self):
        string = "hej"
        expected = 'aGVq'
        res = auth_token.encode(string)
        self.assertEqual(res,expected)

if __name__ == "__main__":
    unittest2.main()