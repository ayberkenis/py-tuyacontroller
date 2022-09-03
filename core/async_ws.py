from aiohttp import web
import aiohttp_cors
from core.controller import LightController
from core.pytc_logger import PytcLogger
logger = PytcLogger().setup_logger('aiohttp.server')
lc = LightController()
routes = web.RouteTableDef()


async def bulb_control_handler(request):
    logger.info(f"BULB Endpoint Received: {await request.text()}")
    rd = await request.json()
    _function_ = lc.__getattribute__(rd['action'])
    await _function_(rd['color'])
    return web.json_response(data="OK")


async def api_control(request):
    return web.json_response(data="SERVER OK")


async def index(request):
    return web.json_response(data="This page only exists for making you sure webserver is running and accessible. All API pages are available. Docs can be found at: https://github.com/ayberkenis/py-tuyacontroller")


app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
"*": aiohttp_cors.ResourceOptions(
    allow_credentials=True,
    expose_headers="*",
    allow_headers="*",
    allow_methods="*",
)
})

app.add_routes([
    web.post('/api/v1/bulb/', bulb_control_handler),
    web.post('/api/v1/server_status/', api_control),
    web.get('/', index)
])

for route in list(app.router.routes()):
    cors.add(route)

def app_export(port=8080):
    return web, app