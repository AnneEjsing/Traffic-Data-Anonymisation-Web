import cv2
import numpy as np
from time import localtime, strftime
import subprocess

class video_file_saver:

    def __init__(self, file_dest, video_length_seconds, file_creation_count_limit=None, file_prefix=None):
        self.frames_saved = 0
        self.files_saved = 0
        self.fps = 25
        self.proc = None
        self.file_dest = file_dest
        self.file_extention = 'mp4'
        self.video_length = video_length_seconds
        self.file_creation_count_limit = file_creation_count_limit

        if(file_prefix != None):
            self.file_prefix = file_prefix


    def push_frame(self, data):
        if(self.file_creation_count_limit != None and self.files_saved >= self.file_creation_count_limit):
            return

        img = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR)

        if(self.proc == None):
            self.proc = self.initiate_file_save(img)

        self.proc.stdin.write(img)
        self.frames_saved += 1

        if((self.video_length != None) and (self.frames_saved == self.fps * self.video_length)):
            self.stop_file_save()
            self.files_saved += 1


    def initiate_file_save(self, first_frame_data):
        height, width, _ = first_frame_data.shape

        dimension = '{}x{}'.format(width, height)
        output_file = self.get_file_name()

        command = ['ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-codec:v','rawvideo',
            '-s', dimension,
            '-pix_fmt', 'bgr24',
            '-r', str(self.fps),
            '-i', '-',
            '-an',
            '-codec:v', 'libx264',
            output_file ]

        return subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)


    def get_file_name(self):
        if(self.file_dest[-1] != '/'):
            self.file_dest = self.file_dest + '/'

        nowStr = strftime("%Y_%m_%d_%H_%M_%S", localtime())
        return self.file_dest + nowStr + '.' + self.file_extention


    def stop_file_save(self):
        self.proc.stdin.close()
        self.proc.stderr.close()
        self.proc.wait()
        self.proc.terminate()
        self.frames_saved = 0
        self.proc = None
