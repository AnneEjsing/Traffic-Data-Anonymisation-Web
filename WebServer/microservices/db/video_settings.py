
@routes.get('/video/settings/get')
async def video_update(request):
    query = """
    SELECT *
    FROM video_settings
    """

    result, error = execute_query(query)
    if error: return web.Response(text=str(error), status=500)
    return hasOneResult(result, "An error occurred", 500)

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

    result, error = execute_query(query, limit)
    if error: return web.Response(text=str(error), status=500)
    return hasOneResult(result, "An error occurred", 404)