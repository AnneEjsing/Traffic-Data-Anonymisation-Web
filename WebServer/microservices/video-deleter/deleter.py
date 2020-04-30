import argparse
import requests
import ast
import datetime
import time
import os
import json
from loguru import logger

dbr = "http://dbresolver:1337/"
path = "/var/lib/videodata/"

def periodically_delete(delay):
    query_string = dbr + "video/list"
    while True:
        #Query the database
        response = requests.get(query_string)
        if response.status_code != 200:
            logger.error(f"Could not query database: {response.status_code} {response.content.decode('utf-8')}. Query: {query_string}")

        settings_response = requests.get(dbr + 'video/settings/get')
        if (response.status_code != 200):
            logger.error("Could not retrive the settings from the database")
        days = settings_response.json()['keep_days']

        #Decode response
        videos = response.json()

        #Delete too old videos
        now = datetime.datetime.utcnow()
        for video in videos:
            #Extract date
            v_id = video['video_id']
            save_time = datetime.datetime.strptime(video['save_time'],'%Y-%m-%d %H:%M:%S.%f')
            delete_time = save_time + datetime.timedelta(days=days)

            #Skip if it is not time to delete yet
            if delete_time > now:
                continue

            #Delete the video
            #In the file system
            if not os.path.exists(path+v_id+".mp4"):
                logger.error(f"Could not delete file from path: {path+v_id}.mp4, as the path does not exist")
                continue
            os.remove(path+v_id+".mp4")

            #In the database
            response = requests.delete(dbr+"video/delete",headers={'Content-type': 'application/json'},json={"video_id":v_id})

            if response.status_code != 200:
                logger.error(f"Could not delete from database: {response.status_code} {response.content.decode('utf-8')}. video: {v_id}")

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
    
    args = parser.parse_args()
    delay = args.delay
    
    logger.add("error.log", retention="10 days")
    periodically_delete(delay)
