from core.controller import LightController
from core.async_ws import app_export
import asyncio


controller = LightController()


web, app = app_export()
asyncio.run(web.run_app(app, port=8080))
