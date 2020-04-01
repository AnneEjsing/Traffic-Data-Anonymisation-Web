import argparse
import requests
import ast
import datetime
import time
import os
import json

dbr = "http://dbresolver:1337/"
path = "/var/lib/videodata/"

def periodically_delete(delay,days):
    queryString = dbr + "video/list"
    while True:
        #Query the database
        response = requests.get(queryString)
        if response.status_code != 200:
            print(str(response.status_code) +": "+response.content.decode('utf-8'))
        
        #Decode response
        content = response.content.decode('utf-8').replace("datetime.datetime","")
        videos = ast.literal_eval(content)

        #Delete too old videos
        now = datetime.datetime.utcnow()
        for v_id,_,_,_,date in videos:
            #Extract date
            y,mo,d,h,min,s,ms = date
            save_time = datetime.datetime(y,mo,d,h,min,s,ms)
            delete_time = save_time + datetime.timedelta(days=days)

            #Skip if it is not time to delete yet
            if delete_time > now:
                continue

            #Delete the video
            #In the file system
            if not os.path.exists(path+v_id+".mp4"):
                continue
            os.remove(path+v_id+".mp4")

            #In the database
            response = requests.delete(dbr+"video/delete",headers={'Content-type': 'application/json'},json={"video_id":v_id})
            if response.status_code != 200:
                print(str(response.status_code) +": "+response.content.decode('utf-8'))

        time.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Deletes videos and video entries.'
    )
    parser.add_argument('--delay',
                        default=300,
                        metavar='integer',
                        required=False,
                        help='The interval in seconds between removing old videos from the database')
    parser.add_argument('--days',
                        default=7,
                        metavar='integer',
                        required=False,
                        help='Number of days to store videos before deleting them.')

    args = parser.parse_args()
    delay = args.delay
    days = args.days
    periodically_delete(delay,days)