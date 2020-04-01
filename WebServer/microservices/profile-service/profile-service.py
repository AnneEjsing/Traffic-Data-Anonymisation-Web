import argparse
import requests
from urllib3._collections import HTTPHeaderDict
from aiohttp import web
import asyncio
import json

#Create the web app
routes = web.RouteTableDef()

url = "http://dbresolver:1337/user/"

@routes.post('/login')
async def login(request):
    return await send_request("login", request, requests.post)

@routes.post('/update')
async def update(request):
    return await send_request("update", request, requests.post)

@routes.get('/get')
async def get(request):
    return await send_request("get", request,requests.get)

@routes.delete('/delete')
async def delete(request):
    return await send_request("delete", request, requests.delete)

@routes.post('/signup')
async def signup(request):
    return await send_request("signup", request, requests.post)

@routes.get('/list')
async def users(request):
    return await send_request("list", request, requests.get)

async def send_request(path, request, query_function):
    response = query_function(url + path,headers={'Content-type': 'application/json'}, json=(await request.json()))
    return web.Response(text=response.text, status=response.status_code)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1338)
