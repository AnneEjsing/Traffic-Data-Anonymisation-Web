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

routes = web.RouteTableDef()

@routes.post("/record/interval")
async def record_continuous(request):
    data = await request.json()    
    threading.Thread(target=work,args=(data,)).start()
    return web.Response(status=200)

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
    #['user_id', 'camera_id', 'start_time', 'recording_time', 'recording_intervals']
    insert_response = requests.post(dbr + 'recordings/insert', headers={'Content-type': 'application/json'},json={
        "user_id":user_id,
        "camera_id":camera_id,
        "recording_time": seconds,
        "recording_intervals": interval})
    
    if insert_response.status_code != 200:
        logger.error(f"Cound not insert recording in database for camera_id {camera_id}, user_id: {user_id}. With error: {insert_response.text}")

    # Creates video segments of length interval.
    if interval_times:
        for i in range(interval_times):
            sp.call("ffmpeg -i " + stream + " -r " + fps + " -t " + str(interval) +" " + filepath+str(i)+".mp4;", shell=True)
            sp.call("echo file \'" + filepath+str(i) + ".mp4\' >>  " + filepath + ".txt", shell=True)
    
    # Creates video segment of length under interval
    if rest_time and rest_time > 0:
        sp.call("ffmpeg -i "+ stream + " -r " + fps + " -t " + str(rest_time) + " " + filepath+str(interval_times)+".mp4;", shell=True)
        sp.call("echo file \'" + filepath + str(interval_times) + ".mp4\' >>  " + filepath + ".txt", shell=True)

    # Queries the database with the video entry.
    response = requests.post(dbr+"video/create", headers={'Content-type': 'application/json'},json={"user_id":user_id,"camera_id":camera_id,"video_thumbnail":""})

    if response.status_code != 200:
        logger.error(f"Could not query database: {response.content.decode('utf-8')}. Userid: {user_id}, cameraid: {camera_id}")
    
    # Gets the ID of the video entry created
    v_id = response.json()[0]['video_id']
    
    # Concatenates the video segments and deletes the temporary files
    sp.call("ffmpeg -y -f concat -safe 0 -i '"+ filepath +".txt' -c copy '" + path + v_id + ".mp4'" ,shell=True)
    sp.call("rm "+ filepath + "*", shell=True)

    # Remove the recording in database:
    delete_response = requests.delete(dbr+"recordings/delete", headers={'Content-type': 'application/json'},json={"user_id":user_id,"camera_id":camera_id})
    if (delete_response.status_code != 200):
        logger.error(f"Could not delete recording for userid: {user_id}, cameraid: {camera_id}. failed with error: {delete_response.text}")


if __name__ == "__main__":
    app = web.Application()
    logger.add("error.log", retention="10 days")
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1336)
