from aiohttp import web
import asyncio
import subprocess as sp
import requests
import uuid
import datetime
import ast
import os
import threading
from loguru import logger

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
    path = "/var/lib/videodata/"
    filepath = path + "temp" + str(uuid.uuid4())
    dbr = "http://dbresolver:1337/"
    fps = "25"
    one_hour = "3600"
    
    
    # Splits the seconds into hours and remaining seconds
    time = str(datetime.timedelta(seconds=int(seconds))).split(':')
    hours = int(time[0])
    rest_time = int(time[1])*60 + int(time[2])

    # Creates video segments of length one hour. This creates intermediate results in case something goes wrong.
    if hours:
        for i in range(hours):
            sp.call("ffmpeg -i " + stream + " -r " + fps + " -t " + one_hour +" " + filepath+str(i)+".mp4;", shell=True)
            sp.call("echo file \'" + filepath+str(i) + ".mp4\' >>  " + filepath + ".txt", shell=True)
    
    # Creates video segment of length under one hour
    if rest_time:
        sp.call("ffmpeg -i "+ stream + " -r " + fps + " -t " + str(rest_time) + " " + filepath+str(hours)+".mp4;", shell=True)
        sp.call("echo file \'" + filepath + str(hours) + ".mp4\' >>  " + filepath + ".txt", shell=True)

    # Queries the database with the video entry.
    response = requests.post(dbr+"video/create", headers={'Content-type': 'application/json'},json={"user_id":user_id,"camera_id":camera_id,"video_thumbnail":""})

    if response.status_code != 200:
        logger.error(f"Could not query database: {response.content.decode('utf-8')}. Userid: {user_id}, cameraid: {camera_id}")
    
    # Gets the ID of the video entry created
    content = response.content.decode('utf-8').replace("datetime.datetime","")
    v_id,_,_,_,_ = ast.literal_eval(content)[0]
    
    # Concatenates the video segments and deletes the temporary files
    sp.call("ffmpeg -y -f concat -safe 0 -i '"+ filepath +".txt' -c copy '" + path + v_id + ".mp4'" ,shell=True)
    sp.call("rm "+ filepath + "*", shell=True)


if __name__ == "__main__":
    app = web.Application()
    logger.add("error.log", retention="10 days")
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1336)
