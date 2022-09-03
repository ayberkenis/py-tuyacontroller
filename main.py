from core.async_ws import app_export
from core.pytc_logger import PytcLogger
import asyncio

class PyTuyaController:
    def __init__(self, port=8080):
        self.port = port
        self.web, self.app = app_export(self.port)
        self.runner = self.web.AppRunner(self.app)
        self.site = None
        self.logger = PytcLogger().setup_logger('pytc')

    async def __make_server_ready__(self):
        await self.runner.setup()
        self.site = self.web.TCPSite(self.runner)
        self.logger.info('Starting webserver...')
        await self.site.start()


    async def __start_irc__(self):
        from core.twitch_grabber import main
        self.logger.info('Establishing IRC Connection...')
        await main()


    async def __start__(self):
        await asyncio.gather(self.__make_server_ready__(), self.__start_irc__())


if __name__ == "__main__":
    ptc = PyTuyaController()
    asyncio.run(ptc.__start__())

