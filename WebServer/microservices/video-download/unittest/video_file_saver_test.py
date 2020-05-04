import unittest2
import sys
import os
sys.path.append(os.getcwd() + '/..')
import video_file_saver

class AuthTokenTests(unittest2.TestCase):
    @classmethod
    def tearDown(cls):
        [os.remove(f) for f in os.listdir() if f.endswith('.mp4') or f.endswith('.txt')]
        
    def test_record(self):
        stream = 'https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8'
        fps = "25"
        interval = 5
        filepath = "test"
        i = 0
        video_file_saver.record(stream,fps,interval,filepath,i)
        res = f'{filepath}{i}.mp4' in os.listdir() and f'{filepath}.txt' in os.listdir() 
        self.assertTrue(res)

    def test_create_final_video(self):
        stream = 'https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8'
        fps = "25"
        interval = 5
        filepath = "test"
        i = 0
        v_id = 0
        path = 'output'
        video_file_saver.record(stream,fps,interval,filepath,i)
        video_file_saver.record(stream,fps,interval,filepath,i+1)

        video_file_saver.create_final_video(filepath,path,v_id)

        res = not f'{filepath}{i}.mp4' in os.listdir() and not f'{filepath}{i+1}.mp4' in os.listdir() and not f'{filepath}.txt' in os.listdir() and f'{path}{i}.mp4' in os.listdir()
        self.assertTrue(res)


if __name__ == "__main__":
    unittest2.main()