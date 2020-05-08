from aiohttp import web
import json
import dbresolver

routes = web.RouteTableDef()

@routes.post('/video/update')
async def video_update(request):
    data = await request.json()
    f = dbresolver.field_check(['video_id', 'user_id', 'camera_id', 'video_thumbnail'], data)
    if f != None: return f

    video_id = data['video_id']
    user_id = data['user_id']
    camera_id = data['camera_id']
    video_thumbnail = data['video_thumbnail']
    query = """
    UPDATE recorded_videos 
    SET user_id = %s, camera_id = %s, video_thumbnail = %s
    WHERE video_id = %s
    RETURNING *;
    """

    result, error = dbresolver.execute_query(query, user_id, camera_id, video_thumbnail, video_id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "There is no video with that id.", 404)

@routes.get('/video/get')
async def video_get(request):
    data = await request.json()
    f = dbresolver.field_check(['video_id'], data)
    if f != None: return f
    
    video_id = data['video_id']
    query = """
    SELECT *
    FROM recorded_videos
    WHERE video_id = %s;
    """

    result, error = dbresolver.execute_query(query, video_id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "There is no video with that id.", 404)


@routes.delete('/video/delete')
async def video_delete(request):
    data = await request.json()
    f = dbresolver.field_check(['video_id'], data)
    if f != None: return f

    video_id = data['video_id']
    query = """
    DELETE FROM recorded_videos
    WHERE video_id = %s
    RETURNING *;
    """
    result, error = dbresolver.execute_query(query, video_id)
    if error: return web.Response(text=str(error),status=500)
    
    return dbresolver.has_one_result(result, "There is no video with this id.", 404)

@routes.post('/video/create')
async def video_create(request):
    data = await request.json()
    f = dbresolver.field_check(['user_id', 'camera_id'], data)
    if f != None: return f
    
    user_id = data['user_id']
    camera_id = data['camera_id']

    query = """
    INSERT INTO recorded_videos (user_id, camera_id, save_time)
    VALUES (
        %s, %s, NOW()
    )
    RETURNING *;
    """
    result, error = dbresolver.execute_query(query, user_id, camera_id)
    if error: return web.Response(text=str(error),status=500)
    return dbresolver.has_one_result(result, "Something went wrong", 500)

@routes.get('/video/list/user_id')
async def video_list_user_id(request):
    data = await request.json()
    f = dbresolver.field_check(['user_id'], data)
    if f != None: return f
    
    user_id = data['user_id']

    query = """
    SELECT cameras.label, recorded_videos.video_id, recorded_videos.save_time, recorded_videos.camera_id
    FROM recorded_videos, cameras
    WHERE recorded_videos.user_id = %s
    AND (recorded_videos.camera_id = cameras.camera_id OR recorded_videos.camera_id IS NULL);
    """
    
    result, error = dbresolver.execute_query(query, user_id)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str),status=200)

@routes.get('/video/list')
def video_list(request):
    query = "SELECT * FROM recorded_videos;"
    result, error = dbresolver.execute_query(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str),status=200)
