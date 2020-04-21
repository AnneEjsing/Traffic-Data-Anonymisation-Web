
@routes.get('/video/settings/get')
async def video_update(request):
    query = """
    SELECT *
    FROM video_settings
    """

    result, error = executeQuery(query)
    if error: return web.Response(text=str(error), status=500)
    if (len(result) == 1):
        limit = result[0][0]
        data = json.dumps({ "recording_limit" : limit })
        return web.Response(text=data,status=200)
    else:
        return web.Response(text="An error ocurred", status=500)

@routes.post('/video/settings/update')
async def update(request):
    data = await request.json()
    f = fieldCheck(['recording_limit'], data)
    if f != None : return f

    limit = data['recording_limit']

    query = """
    UPDATE video_settings
    SET recording_limit = %s
    RETURNING *;
    """

    result, error = executeQuery(query, limit)
    if error: return web.Response(text=str(error), status=500)
    return hasOneResult(result, "An error occurred", 404)