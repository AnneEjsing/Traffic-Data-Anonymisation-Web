from aiohttp import web
import asyncio
import requests

routes = web.RouteTableDef()
dbresolver = 'http://dbresolver:1337/'

@routes.post("/model/upload")
async def remote_change_ml(request):
    # request.post is nessecary as data is not json, but a file.
    data = await request.post()
    camera_id = data['camera_id']
    model = data['file']
    model_type = data['type']
    response = requests.get(dbresolver+'camera/get', headers={'Content-type': 'application/json'}, json={'id': camera_id})
    ip = response.json()['ip']

    # File extension .pb is for SSD models, and extension .m5 is for retinanet models.
    extension = model.filename.split('.')[1]
    if extension != "pb" and extension != "h5":
        return web.Response(status=500)

    # Redirect to correct url with correct port and path
    url = f"http://{ip}:5000/model/upload"

    # Sends file to specified url
    files = {'file': (model.filename, model.file, model.content_type, model.headers)}
    response = requests.post(url, files=files, data={ 'type': model_type})

    if (response.status_code == 200):
        # The model has been updated on the nano. Now update in database
        if (model_type == 'face'):
            model_face = model.filename
            requests.put(dbresolver + "camera/update_models/face", headers={'Content-type': 'application/json'}, json={'id': camera_id,'model_face': model_face})
        elif (model_type == 'license_plate'):
            model_licens = model.filename
            requests.put(dbresolver + "camera/update_models/licens", headers={'Content-type': 'application/json'}, json={'id': camera_id,'model_licens': model_licens})

    # Returns status code recevied from nano
    return web.Response(status=response.status_code)

if __name__ == "__main__":  
    app = web.Application(client_max_size=0)
    app.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=1341)
