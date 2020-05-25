from aiohttp import web
import asyncio
import subprocess as sp
import requests
import json

routes = web.RouteTableDef()
db_url = "http://dbresolver:1337/"

@routes.get('/get')
async def login(request):
    return await send_request("video/settings/get", {}, requests.get)

@routes.post('/update')
async def update(request):
    return await send_request("video/settings/update", await request.json(), requests.post)

@routes.get('/get/recording')
async def get_recording_info(request):
    return await send_request("recordings/get", await request.json(), requests.get)

@routes.get('/recordings/list/user_id')
async def get_recording_info(request):
    return await send_request("recordings/list/user_id", await request.json(), requests.get)

@routes.get('/video/list/user_id')
async def list_recorded_videos_user_id(request):
    return await send_request("video/list/user_id", await request.json(), requests.get)

async def send_request(path, json, query_function):
    response = query_function(db_url + path,headers={'Content-type': 'application/json'}, json=(json))
    return web.Response(text=response.text, status=response.status_code)


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=1342)
