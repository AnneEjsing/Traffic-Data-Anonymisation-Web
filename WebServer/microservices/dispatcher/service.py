import json
import requests
from aiohttp import web, BasicAuth, ClientSession
import asyncio
import aiohttp_cors

# Used for token creation and Verification
from authToken import create_token, verify_credentials, verify_token, get_user_id, authenticate

routes = web.RouteTableDef()

videoDownloadService = "http://videodownloader:1336"
profileService = "http://profileservice:1338"
videoSettingsService = "http://videoservice:1339"
modelChangerService = "http://modelchanger:1339"

# Standard Get, Post, Delete, Out Requests


async def getQueryAsync(queryString, json):
    async with ClientSession() as session:
        async with session.get(queryString, json=json) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)


async def deleteQueryAsync(queryString):
    async with ClientSession() as session:
        async with session.delete(queryString) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)


async def postQueryAsync(queryString, data):
    async with ClientSession(headers={'Content-type': 'application/json'}) as session:
        async with session.post(queryString, json=data) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)


async def putQueryAsync(queryString, data):
    async with ClientSession(headers={'Content-type': 'application/json'}) as session:
        async with session.put(queryString, json=data) as response:
            if(response.status == 200):
                return web.Response(text=await response.text())
            return web.Response(status=response.status)

# Userservice endpoints
@routes.get('/login')
async def login(request):
    auth = request.headers['Authorization']
    decoded = BasicAuth.decode(auth)
    isSuccess, userId, rights = verify_credentials(
        decoded.login, decoded.password)
    if (isSuccess):
        return web.Response(text=create_token(userId, rights))
    else:
        return web.Response(status=401)


@routes.post('/signup')
async def userSignup(request):
    signupString = profileService + "/signup"
    data = await request.json()
    return await postQueryAsync(signupString, data)


@routes.get('/get/user')
async def getUser(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised, status_code = verify_token(token, "user")
    if(isAuthorised):
        userId = get_user_id(token)
        string = profileService + "/get"
        return await getQueryAsync(string, {"id": userId})
    else:
        return web.Response(status=status_code)


@routes.get('/get/admin')
async def getAdmin(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised, status_code = verify_token(token, "admin")
    if(isAuthorised):
        userId = get_user_id(token)
        string = profileService + "/get"
        return await getQueryAsync(string, {"id": userId})
    else:
        return web.Response(status=status_code)


@routes.get('/user/list')
async def listUsers(request):
    listString = profileService + "/list"
    return await getQueryAsync(listString, json.dumps({}))


# Authenticate endpoint
@routes.get("/auth/authenticate")
async def authenticator(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    return web.Response(text=json.dumps((authenticate(token))))


# Video downloader endpoints
@routes.post("/record/interval")
async def record_continuous(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised = authenticate(token)
    if (isAuthorised):
        endpoint = videoDownloadService + "/record/interval"
        data = await request.json()
        return await postQueryAsync(endpoint, data)
    else:
        return web.Response(text="User must be logged in to downloade a video", status=401)

###### Video settings endpoints
@routes.get('/settings/get')
async def get_settings(request):
    return await getQueryAsync(videoSettingsService + "/get", { })

@routes.post('/settings/update')
async def update_settings(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised, status_code = verify_token(token, "admin")
    if(isAuthorised):
        string = videoSettingsService + "/update"
        return await postQueryAsync(string, (await request.json()))
    else:
        return web.Response(status=status_code)

# Model changer
@routes.post("/model/upload")
async def upload_model(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised = authenticate(token)
    if (isAuthorised):
        endpoint = modelChangerService + "/model/upload"
        data = await request.post()
        
        # Data cannot just be forwarded. File need to be sent using the format below.
        model = data['file']
        files = {'file': (model.filename, model.file, model.content_type, model.headers)}
        data={'ip':data['ip']}
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
