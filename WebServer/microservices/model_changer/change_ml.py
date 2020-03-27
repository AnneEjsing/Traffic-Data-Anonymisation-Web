from aiohttp import web
import asyncio
import aiohttp_cors
import subprocess as sp
import requests

routes = web.RouteTableDef()
url = 'http://192.168.1.107:XX/XX'


@routes.post("/ml")
async def remote_change_ml(data):
    model = data['file']

    # .filename contains the name of the file in string format.
    filename = model.filename

    # .file contains the actual file data that needs to be stored somewhere.
    model_file = data['file'].file

    r = requests.post(url, files={'model.h5': model_file})

    content = model_file.read()


    return web.Response(status=200)

app = web.Application()
web.run_app(app, host='0.0.0.0', port=5000)
