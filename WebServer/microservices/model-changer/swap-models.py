from aiohttp import web
import asyncio
import requests

routes = web.RouteTableDef()

@routes.post("/model/upload")
async def remote_change_ml(request):
    # request.post is nessecary as data is not json, but a file.
    data = await request.post()
    url = data['url']
    input_file = data['file']

    # File extension .pb is for SSD models, and extension .m5 is for retinanet models.
    filename = input_file.filename.split('.')
    if filename[1] != "pb" or filename[1] != "m5":
        return web.Response(status=500)

    # Sends file to specified url
    action = {"file": input_file.file}
    r = requests.post(url, files=action)

    # Returns status code recevied from nano
    return web.Response(status=r.status_code)

if __name__ == "__main__":  
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1339)
