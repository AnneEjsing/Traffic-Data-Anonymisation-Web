from aiohttp import web
import asyncio
import subprocess as sp
import requests
import uuid
import datetime
import os
import threading
from loguru import logger
from datetime import date
import glob
import ffmpeg

routes = web.RouteTableDef()
headers = {'Content-type': 'application/json'}

@routes.post("/record/interval")
async def record_continuous(request):
    data = await request.json()    
    threading.Thread(target=work,args=(data,)).start()
    return web.Response(status=200)

def record(stream, fps, interval, filepath, i):
    # Command to record "interval" seconds from "stream"
    out, error = (
        ffmpeg
        .input(stream, r=fps,t=str(interval))
        .output(filepath+str(i)+".mp4")
        .run(capture_stdout=True, capture_stderr=True)
    )

    # Write filepath to filepath.txt
    with open(f'{filepath}.txt', "a") as file:
        file.write(f'file \'{filepath+str(i)}.mp4\'')
        file.write("\n")

def create_final_video(filepath, path, v_id):
    # Command to concatenate all temp files from filepath.txt
    out, error = (
        ffmpeg
        .input(f'{filepath}.txt', f='concat', safe=0)
        .output(f'{path}{v_id}.mp4', c='copy')
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )

    # Command to delete all temp files
    files = glob.glob(f'{filepath}*')
    for f in files:
        os.remove(f)

def work(data):
    stream = data['url']
    seconds = data['length']
    user_id = data['user_id']
    camera_id = data['camera_id']
    interval = data['recording_intervals']
    path = "/var/lib/videodata/"
    filepath = path + "temp" + str(uuid.uuid4())
    dbr = "http://dbresolver:1337/"
    fps = "25"
    
    # Splits the seconds into interval and remaining seconds
    interval_times = seconds // interval
    rest_time = seconds % interval

    #Inserts into recordings in database
    insert_response = requests.post(dbr + 'recordings/insert', headers=headers,json={
        "user_id":user_id,
        "camera_id":camera_id,
        "recording_time": seconds,
        "recording_intervals": interval})
    
    if insert_response.status_code != 200:
        logger.error(f"Cound not insert recording in database for camera_id {camera_id}, user_id: {user_id}. With error: {insert_response.text}")

    # Creates video segments of length interval.
    if interval_times:
        for i in range(interval_times):
            record(stream,fps,interval,filepath,i)
    
    # Creates video segment of length under interval
    if rest_time and rest_time > 0:
        record(stream,fps,rest_time,filepath,interval_times)

    # Queries the database with the video entry.
    response = requests.post(dbr+"video/create", headers=headers,json={"user_id":user_id,"camera_id":camera_id,"video_thumbnail":""})
    if response.status_code != 200:
        logger.error(f"Could not query database: {response.content.decode('utf-8')}. Userid: {user_id}, cameraid: {camera_id}")
    
    # Gets the ID of the video entry created
    v_id = response.json()[0]['video_id']
    
    # Concatenates the video segments and deletes the temporary files
    create_final_video(filepath,path,v_id)

    # Remove the recording in database:
    delete_response = requests.delete(dbr+"recordings/delete", headers=headers,json={"user_id":user_id,"camera_id":camera_id})
    if (delete_response.status_code != 200):
        logger.error(f"Could not delete recording for userid: {user_id}, cameraid: {camera_id}. failed with error: {delete_response.text}")


if __name__ == "__main__":
    app = web.Application()
    logger.add("error.log", retention="10 days")
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1336)
