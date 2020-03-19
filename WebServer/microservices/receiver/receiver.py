import argparse
import requests
import urllib
import cv2
import threading
import video_file_saver as vfs
from flask import Response, Flask

queueSize = 100
queueIndex = 0
queue = {}
queueLock = threading.Lock()
app = Flask(__name__)

def receive(ip, port, functions_to_run):
    # Tells python to access the global queueIndex variable
    # https://www.pythoncircle.com/post/680/solving-python-error-unboundlocalerror-local-variable-x-referenced-before-assignment/
    global queueIndex
    queryString = 'http://' + ip + ':' + str(port)
    stream = urllib.request.urlopen(queryString)
    total_bytes = b''

    # https://github.com/hyansuper/picam-video-streaming/blob/master/receive.py
    while True:
        total_bytes += stream.read(1024)  # load a chunk
        b = total_bytes.find(b'\xff\xd9')  # search for JPEG end
        if not b == -1:
            # Decode a jpg from the buffer
            a = total_bytes.find(b'\xff\xd8')  # JPEG start
            jpg = total_bytes[a:b + 2]  # actual image
            total_bytes = total_bytes[b + 2:]  # other informations

            # Save the jpeg to the image buffer
            queue[queueIndex] = jpg
            queueIndex = (queueIndex + 1) % queueSize
            for func in functions_to_run:
              func(jpg)

def save_to_database():
  return
              

def broadcast():
    localIndex = queueIndex
    while True:
        if localIndex == queueIndex:
            continue

        data = queue[localIndex]
        localIndex = (localIndex + 1) % queueSize
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')


@app.route('/')
def video_feed():
    return Response(broadcast(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Receives a stream and sends it along, while saving it to the database.'
    )
    parser.add_argument('--inputip',
                        default="0.0.0.0",
                        metavar='string',
                        required=False,
                        help='ip address to the camera')
    parser.add_argument('--inputport',
                        default=5000,
                        metavar='integer',
                        required=False,
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
    parser.add_argument('--port',
                        default=4000,
                        metavar='integer',
                        required=False,
                        help='port to supply stream over')
    parser.add_argument('--saveToDatabase',
                        default=False,
                        metavar='boolean',
                        required=False,
                        help='determines whether the stream should be saved to the database')
    args = parser.parse_args()
    database_save = args.saveToDatabase

    worker_functions = []
    worker_functions.append(save_to_database)

    vid_saver = None
    if(args.output_file_path != None):
        vid_saver = vfs.video_file_saver(args.output_file_path, args.video_length, args.max_video_count)
        worker_functions.append(vid_saver.push_frame)

    threading.Thread(target=receive, args=(
        args.inputip, args.inputport, worker_functions)).start()
    app.run(host='0.0.0.0', port=args.port, debug=True)
