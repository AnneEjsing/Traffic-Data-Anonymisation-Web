from aiohttp import web
import json
import dbresolver

routes = web.RouteTableDef()

@routes.get('/video/settings/get')
async def get(request):
    query = """
    SELECT *
    FROM video_settings
    """

    result, error = dbresolver.execute_query(query)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "An error occurred", 500)

@routes.post('/video/settings/update')
async def update(request):
    data = await request.json()
    f = dbresolver.field_check(['recording_limit', 'keep_days'], data)
    if f != None : return f

    limit = data['recording_limit']
    keep_days = data['keep_days']

    query = """
    UPDATE video_settings
    SET recording_limit = %s, keep_days = %s
    RETURNING *;
    """

    result, error = dbresolver.execute_query(query, limit, keep_days)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "An error occurred", 404)