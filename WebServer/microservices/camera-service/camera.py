import argparse
import requests
from urllib3._collections import HTTPHeaderDict
from aiohttp import web
import asyncio
import json

#Create the web app
routes = web.RouteTableDef()

url = "http://dbresolver:1337/"

@routes.put('/camera/update')
async def update(request):
    return await send_request("camera/updateInfo", await request.json(), requests.put)

@routes.get('/camera/get')
async def get(request):
    return await send_request("camera/get", await request.json(),requests.get)

@routes.delete('/camera/delete')
async def delete(request):
    return await send_request("camera/delete", {"id":request.query["id"]},requests.delete)

@routes.post('/camera/create')
async def create(request):
    return await send_request("camera/create", await request.json(), requests.post)

@routes.get('/camera/userlist')
async def userlist(request):
    return await send_request("camera/userlist", await request.json(), requests.get)

@routes.get('/camera/adminlist')
async def adminlist(request):
    return await send_request("camera/adminlist", '{}', requests.get)

@routes.post('/access/create')
async def give_access(request):
    data = await request.json()
    response = requests.get(url + "user/get/email",headers={'Content-type': 'application/json'}, json=(data))
    other_data = response.json()
    if not other_data:
        return web.Response(text=response.text, status=404)
    new_data = {'camera_id': data['camera_id'], 'user_id': other_data['user_id']}
    return await send_request("access/create", new_data, requests.post)

async def send_request(path, json, query_function):
    response = query_function(url + path,headers={'Content-type': 'application/json'}, json=(json))
    return web.Response(text=response.text, status=response.status_code)

app = web.Application()

app.add_routes(routes)

web.run_app(app, host='0.0.0.0', port=1340)
