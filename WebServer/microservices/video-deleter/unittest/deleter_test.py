import unittest2
import sys
import os
sys.path.append(os.getcwd() + '/..')
import deleter

class AuthTokenTests(unittest2.TestCase):
    def setUp(self):
        file = open('test.mp4', 'w+')
        file.close()
        deleter.path= ""

    def tearDown(self):
        if 'test.mp4' in os.listdir():
            os.remove('test.mp4')

    def test_delete_file(self):
        deleter.delete_videos([{"video_id":"test","save_time":"2019-06-05 23:56:23.3434"}],0)
        res = not 'test.mp4' in os.listdir()
        self.assertTrue(res)

    def test_dont_delete_file(self):
        deleter.delete_videos([{"video_id":"test","save_time":"2119-06-05 23:56:23.3434"}],0)
        res = 'test.mp4' in os.listdir()
        self.assertTrue(res)
    
    def test_delete_file_dont_exist(self):
        deleter.delete_videos([{"video_id":"test2","save_time":"2019-06-05 23:56:23.3434"}],0)
        res = not 'test2.mp4' in os.listdir()
        self.assertTrue(res)

if __name__ == "__main__":
    unittest2.main()