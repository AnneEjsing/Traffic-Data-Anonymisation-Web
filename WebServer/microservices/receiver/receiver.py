import argparse
import requests
import urllib
import cv2
import threading
import video_file_saver as vfs

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


def worker(functions_to_run):
    while True:
        if len(queue) <= 0:
            continue
        queueLock.acquire()
        data = queue.pop(0)
        queueLock.release()

        for func in functions_to_run:
            func(data)


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
    parser.add_argument('--output_file_path', '-o',
                        metavar='path',
                        required=False,
                        help='record video files to directory')
    parser.add_argument('--video_length', '-l',
                        metavar='integer',
                        type=int,
                        required=False,
                        help="length of videos to be saved in seconds")
    parser.add_argument('--max_video_count',
                        metavar='integer',
                        type=int,
                        required=False,
                        help="maximum amount of videos to save. Ignored if no video length is given")
    args = parser.parse_args()

    worker_functions = []
    worker_functions.append(save_to_database)
    worker_functions.append(broadcast)

    vid_saver = None
    if(args.output_file_path != None):
        vid_saver = vfs.video_file_saver(args.output_file_path, args.video_length, args.max_video_count)
        worker_functions.append(vid_saver.push_frame)

    threading.Thread(target=receive, args=(args.ip, args.port)).start()
    threading.Thread(target=worker, args=(worker_functions,)).start()
