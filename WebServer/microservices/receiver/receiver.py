import argparse
import requests
import urllib
import cv2
import numpy as np
import threading

queue = []
queueLock = threading.Lock()


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
