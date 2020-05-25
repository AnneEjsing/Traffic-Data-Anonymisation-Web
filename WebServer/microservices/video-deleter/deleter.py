import argparse
import requests
import ast
import datetime
import time
import os
import json
from loguru import logger
import glob

dbr = "http://dbresolver:1337/"
path = "/var/lib/videodata/"
delay = 300

#Delete too old videos
def delete_videos(videos,days):
    now = datetime.datetime.utcnow()

    files = set(glob.glob(f'{path}*.mp4'))
    files_from_database = set()

    for video in videos:
        #Extract date
        v_id = video['video_id']
        save_time = datetime.datetime.strptime(video['save_time'],'%Y-%m-%d %H:%M:%S.%f')
        delete_time = save_time + datetime.timedelta(days=days)

        file_path = path + v_id + '.mp4'
        files_from_database.add(file_path)

        #Skip if it is not time to delete yet
        if delete_time > now:
            continue

        #Delete the video
        #In the file system
        if not os.path.exists(file_path):
            logger.error(f"Could not delete file from path: {path+v_id}.mp4, as the path does not exist")
            continue
        os.remove(file_path)

        #In the database
        try:
            response = requests.delete(dbr+"video/delete",headers={'Content-type': 'application/json'},json={"video_id":v_id})
            if response.status_code != 200:
                logger.error(f"Could not delete from database: {response.status_code} {response.content.decode('utf-8')}. video: {v_id}")
        except Exception as e:
            logger.error(e)
    
    #Removing videos that are not listed in the database
    videoes_not_in_db = files - files_from_database
    for vid_path in videoes_not_in_db:
        os.remove(vid_path)



def periodically_delete():
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
        
        delete_videos(videos,days)

        time.sleep(delay)


if __name__ == "__main__":
    logger.add("error.log", retention="10 days")
    periodically_delete()
