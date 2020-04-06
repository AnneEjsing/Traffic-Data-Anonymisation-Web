import json
import requests
from aiohttp import web, BasicAuth, ClientSession
import asyncio
import aiohttp_cors

# Used for token creation and Verification
from authToken import create_token, verify_credentials, verify_token, get_user_id, authenticate

routes = web.RouteTableDef()

profileService = "http://profileservice:1338"
videoDownloadService = "http://videodownloader:1336"


###### Standard Get, Post, Delete, Out Requests
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

###### Userservice endpoints
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
        return await getQueryAsync(string, { "id" : userId })
    else:
        return web.Response(status=status_code)

@routes.get('/get/admin')
async def getAdmin(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised, status_code = verify_token(token, "admin")
    if(isAuthorised):
        userId = get_user_id(token)
        string = profileService + "/get"
        return await getQueryAsync(string, { "id" : userId })
    else:
        return web.Response(status=status_code)


@routes.get('/user/list')
async def listUsers(request):
    listString = profileService + "/list"
    return await getQueryAsync(listString, json.dumps({}))


###### Authenticate endpoint
@routes.get("/auth/authenticate")
async def authenticator(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    return web.Response(text=json.dumps((authenticate(token))))


###### Video downloader endpoints
@routes.post("/record/interval")
async def record_continuous(request):
    token = request.headers['Authorization'].split('Bearer ')[1]
    isAuthorised = authenticate(token)
    if (isAuthorised):
        return postQueryAsync("/record/interval", request.json())
    else:
        return web.Response(text="User must be logged in to downloade a video", status=401)


app = web.Application()

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
