from aiohttp import web
import asyncio
import subprocess as sp
import requests
import json

routes = web.RouteTableDef()
url = "http://dbresolver:1337/video/settings/"

@routes.get('/get')
async def login(request):
    return await send_request("get", await request.json(), requests.get)

@routes.post('/update')
async def update(request):
    return await send_request("update", await request.json(), requests.post)

async def send_request(path, json, query_function):
    response = query_function(url + path,headers={'Content-type': 'application/json'}, json=(json))
    return web.Response(text=response.text, status=response.status_code)


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=1339)
