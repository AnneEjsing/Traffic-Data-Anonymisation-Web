from aiohttp import web
import asyncio
import requests

routes = web.RouteTableDef()

@routes.post("/model/upload")
async def remote_change_ml(request):
    # request.post is nessecary as data is not json, but a file.
    data = await request.post()
    ip = data['ip']
    model = data['file']

    # File extension .pb is for SSD models, and extension .m5 is for retinanet models.
    extension = model.filename.split('.')[1]
    if extension != "pb" and extension != "h5":
        return web.Response(status=500)

    # Redirect to correct url with correct port and path
    url = f"http://{ip}:5000/model/upload"

    # Sends file to specified url
    files = {'file': (model.filename, model.file, model.content_type, model.headers)}
    response = requests.post(url, files=files)

    # Returns status code recevied from nano
    return web.Response(status=response.status_code)

if __name__ == "__main__":  
    app = web.Application(client_max_size=0)
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1340)
