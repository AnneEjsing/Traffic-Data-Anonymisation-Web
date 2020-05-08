import json
import requests
from aiohttp import web, BasicAuth, ClientSession
import asyncio
import aiohttp_cors
from os import listdir

# Used for token creation and Verification
from auth_token import create_token, verify_credentials, verify_token, get_user_id, authenticate, get_rights

routes = web.RouteTableDef()

video_download_service = "http://videodownloader:1336"
profile_service = "http://profileservice:1338"
video_service = "http://videoservice:1342"
model_changer_service = "http://modelchanger:1341"
camera_service = "http://cameraservice:1340"
split_at_bearer = 'Bearer '
# Standard Get, Post, Delete, Out Requests


async def get_query_async(query_string, json):
    async with ClientSession() as session:
        async with session.get(query_string, json=json) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)


async def delete_query_async(query_string):
    async with ClientSession() as session:
        async with session.delete(query_string) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)


async def post_query_async(query_string, data):
    async with ClientSession(headers={'Content-type': 'application/json'}) as session:
        async with session.post(query_string, json=data) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)


async def put_query_async(query_string, data):
    async with ClientSession(headers={'Content-type': 'application/json'}) as session:
        async with session.put(query_string, json=data) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)

# Userservice endpoints
@routes.get('/login')
async def login(request):
    auth = request.headers['Authorization']
    decoded = BasicAuth.decode(auth)
    is_success, user_id, rights = verify_credentials(
        decoded.login, decoded.password)
    if (is_success):
        return web.Response(text=create_token(user_id, rights))
    else:
        return web.Response(status=401)


@routes.post('/signup')
async def user_signup(request):
    signup_string = profile_service + "/signup"
    data = await request.json()
    return await post_query_async(signup_string, data)


@routes.get('/get/user')
async def get_user(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    role = get_rights(token)
    is_authorised, status_code = verify_token(token, role)
    if(is_authorised):
        user_id = get_user_id(token)
        string = profile_service + "/get"
        return await get_query_async(string, {"id": user_id})
    else:
        return web.Response(status=status_code)


@routes.get('/user/list')
async def list_users(request):
    list_string = profile_service + "/list"
    return await get_query_async(list_string, json.dumps({}))

# Camera endpoints
@routes.get('/camera/list')
async def list_camera(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    user_id = get_user_id(token)
    rights = get_rights(token)
    is_authorised, status_code = verify_token(token, rights)
    if is_authorised:
        list_string = ""
        if rights == "admin":
            list_string = camera_service + "/camera/adminlist"
        else: 
            list_string = camera_service + "/camera/userlist"
        return await get_query_async(list_string,{"id": user_id}) 
    else:
        return web.Response(status=status_code)

@routes.get('/camera/get')
async def get_camera(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if is_authorised:
        endpoint = camera_service + "/camera/get"
        data = {'id': request.query['id']}
        return await get_query_async(endpoint, data)
    else:
        return web.Response(text="User must be logged in to edit a camera", status=401)

@routes.post('/camera/create')
async def create_camera(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if is_authorised and get_rights(token) == 'admin':
        endpoint = camera_service + "/camera/create"
        data = await request.json()
        data["owner"] = get_user_id(token)
        return await post_query_async(endpoint, data)
    else:
        return web.Response(text="User must be logged in with administrative privileges to create a camera", status=401)

@routes.put('/camera/update')
async def update_camera(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if is_authorised and get_rights(token) == 'admin':
        endpoint = camera_service + "/camera/update"
        data = await request.json()
        return await put_query_async(endpoint, data)
    else:
        return web.Response(text="User must be logged in with administrative privileges to update a camera", status=401)

@routes.delete('/camera/delete')
async def delete_camera(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if is_authorised and get_rights(token) == 'admin':
        endpoint = camera_service + "/camera/delete?id=" + request.query['id']
        return await delete_query_async(endpoint)
    else:
        return web.Response(text="User must be logged in with administrative privileges to delete a camera", status=401)

@routes.post('/access/create')
async def create_access(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if is_authorised and get_rights(token) == 'admin':
        endpoint = camera_service + "/access/create"
        data = await request.json()
        return await post_query_async(endpoint, data)
    else:
        return web.Response(text="User must be logged in with administrative privileges to allow another user to access a camera", status=401)


@routes.post('/stream/start')
async def start_stream_on_device(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if is_authorised and get_rights(token) == 'admin':
        data = await request.json()
        endpoint = data['device'] + ':5000'
        endpoint = endpoint + '/start'
        
        return await post_query_async(endpoint, data)
    else:
        return web.Response(text="User must be logged in with administrative privileges to start streams on devices")


# Authenticate endpoint
@routes.get("/auth/authenticate")
async def authenticator(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    return web.Response(text=json.dumps((authenticate(token))))


# Video downloader endpoints
@routes.post("/record/interval")
async def record_continuous(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if (is_authorised):
        endpoint = video_download_service + "/record/interval"
        data = await request.json()
        return await post_query_async(endpoint, data)
    else:
        return web.Response(text="User must be logged in to downloade a video", status=401)

###### Video endpoints
@routes.get('/settings/get')
async def get_settings(request):
    return await get_query_async(video_service + "/get", { })

@routes.post('/settings/update')
async def update_settings(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised, status_code = verify_token(token, "admin")
    if(is_authorised):
        string = video_service + "/update"
        return await post_query_async(string, (await request.json()))
    else:
        return web.Response(status=status_code)

@routes.post('/get/recording')
async def get_recording_info(request):
    return await get_query_async(video_service + "/get/recording", (await request.json()))

@routes.post('/recordings/list/user_id')
async def get_recording_info(request):
    return await get_query_async(video_service + "/recordings/list/user_id", (await request.json()))


@routes.get('/video/list/user_id')
async def list_video_recordings_user_id(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    user_id = get_user_id(token)
    rights = get_rights(token)
    is_authorised, status_code = verify_token(token, rights)
    if is_authorised:
        return await get_query_async(video_service + "/video/list/user_id",{"user_id": user_id}) 
    else:
        return web.Response(status=status_code)

@routes.get('/video/download/{video_id}')
async def download_video(request):
    video_id = request.match_info['video_id']
    file_path = "/var/lib/videodata/" + video_id + ".mp4"
    return web.FileResponse(file_path)


# Model changer
@routes.post("/model/upload")
async def upload_model(request):
    token = request.headers['Authorization'].split(split_at_bearer)[1]
    is_authorised = authenticate(token)
    if (is_authorised):
        endpoint = model_changer_service + "/model/upload"
        data = await request.post()
        
        # Data cannot just be forwarded. File need to be sent using the format below.
        model = data['file']
        files = {'file': (model.filename, model.file, model.content_type, model.headers)}
        data={'camera_id':data['camera_id']}
        response = requests.post(endpoint,data=data, files=files)
        return web.Response(status=response.status_code)
    else:
        return web.Response(text="User must be logged in to upload a model", status=401)

if __name__ == "__main__":
    # Client_max_size disables size limits on sent files
    app = web.Application(client_max_size=0)

    # Configure default CORS settings.
    resources = [
        '*',
    ]

    cors = aiohttp_cors.setup(app, defaults={
        resource: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_methods='*',
            allow_headers='*',
        ) for resource in resources
    })
    app.add_routes(routes)

    for route in app.router.routes():
        cors.add(route)

    web.run_app(app, host='0.0.0.0', port=443)
