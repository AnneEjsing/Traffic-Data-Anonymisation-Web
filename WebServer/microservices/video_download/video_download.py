from aiohttp import web
import asyncio
import aiohttp_cors
import subprocess as sp

routes = web.RouteTableDef()

@routes.post("/record/interval")
async def record_interval(data):
    data = await data.json()
    stream = data['url']
    seconds = data['length']
    try:
        sp.call("ffmpeg -y -i " + stream + " -r 25 -t " +
                seconds + " output.mp4;", shell=True)
        return web.Response(status=200)
    except:
        return web.Response(status=404)

@routes.post("/record/continuous")
async def record_continuous(data):
    data = await data.json()
    stream = data['url']
    name = "test"
    i = 0

    sp.call("mkdir test", shell=True)
    for i in range(2):
        sp.call("ffmpeg -i "+ stream +" -r 25 -t 30 "+'test/'+name+str(i)+".mp4;", shell=True)
        sp.call("echo file \'"+name+str(i)+".mp4\' >>  test/input.txt", shell=True)

    sp.call("ffmpeg -y -f concat -safe 0 -i 'test/input.txt' -c copy 'test/output.mp4'" ,shell=True)
    sp.call("rm test/test* test/input.txt", shell=True)

app = web.Application()
web.run_app(app, host='0.0.0.0', port=5001)