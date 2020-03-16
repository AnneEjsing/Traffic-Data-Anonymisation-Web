import argparse
import requests
import urllib
import cv2
import numpy as np
import threading
from time import localtime, strftime
import subprocess

queue = []
queueLock = threading.Lock()

framesSaved = 0
videoLengthSeconds = 600
height = None
width = None
fps = 24
proc = None

def receive(ip, port):
    queryString = 'http://' + ip + ':' + str(port)
    stream = urllib.request.urlopen(queryString)
    total_bytes = b''

    #https://github.com/hyansuper/picam-video-streaming/blob/master/receive.py
    while True:
        total_bytes += stream.read(1024)  #load a chunk
        b = total_bytes.find(b'\xff\xd9')  # search for JPEG end
        if not b == -1:
            a = total_bytes.find(b'\xff\xd8')  # JPEG start
            jpg = total_bytes[a:b + 2]  # actual image
            total_bytes = total_bytes[b + 2:]  # other informations

            queueLock.acquire()
            queue.append(jpg)
            queueLock.release()



def initiate_file_save(img):
    height, width, _ = img.shape

    dimension = '{}x{}'.format(width, height)
    nowStr = strftime("%Y_%m_%d_%H_%M_%S", localtime())
    output_file = './' + nowStr + ".mp4"

    print(dimension)

    command = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-codec:v','rawvideo',
        '-s', dimension,
        '-pix_fmt', 'bgr24',
        '-r', str(fps),
        '-i', '-',
        '-an',
        '-codec:v', 'libx264',
        output_file ]

    return subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

def save_frame_to_file(data):
    global framesSaved, proc

    img = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR) 
    
    if(proc == None):
        proc = initiate_file_save(img)
    
    proc.stdin.write(img)
    framesSaved += 1

    print(framesSaved)

    if(framesSaved == fps * videoLengthSeconds):
        proc.stdin.close()
        proc.stderr.close()
        proc.wait()
        framesSaved = 0
        proc = None

def save_to_database(data):
    return


def broadcast(data):
    return


def worker():
    while True:
        if len(queue) <= 0:
            continue
        queueLock.acquire()
        data = queue.pop(0)
        queueLock.release()

        save_frame_to_file(data)
        save_to_database(data)
        broadcast(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Receives a stream and sends it along, while saving it to the database.'
    )
    parser.add_argument('--ip',
                        metavar='string',
                        required=True,
                        help='ip address to the camera')
    parser.add_argument('--port',
                        metavar='integer',
                        required=True,
                        help='port to access the camera through')
    args = parser.parse_args()

    threading.Thread(target=receive, args=(args.ip, args.port)).start()
    threading.Thread(target=worker).start()
