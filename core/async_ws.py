from aiohttp import web
import aiohttp_cors
from core.controller import LightController

lc = LightController()

async def hello(request):
    await lc.notification_light('green')
    return web.json_response({'data': 'success'})

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
"*": aiohttp_cors.ResourceOptions(
    allow_credentials=True,
    expose_headers="*",
    allow_headers="*"
)
})
app.add_routes([web.post('/api/v1/whatsapp_notification/', hello)])

for route in list(app.router.routes()):
    cors.add(route)

def app_export(port=8080):

    return web, app