import tinytuya
import webcolors
import typing
import asyncio


class LightController:
    def __init__(self):
        self.bulb_1 = tinytuya.BulbDevice('bf0704eeba8839d356e3u3', '192.168.1.48', '67177e6b80750a56')
        self.bulb_2 = tinytuya.BulbDevice('bf168f97771edaf614hac4', '192.168.1.49', 'c0c6a7bf99ec8f07')
        self.devices = [self.bulb_1, self.bulb_2]
        self.__set_version__()
        self.night_light = "000e0d0000000000000000c80000"
        self.reading_light = "010e0d0000000000000003e801f4"
        self.working_light = "020e0d0000000000000003e803e8"
        self.chill_light = "030e0d0000000000000001f401f4"
        self.green_pulse = "04464602007803e803e800000000464602007803e8000a00000000"
        self.rainbow_fast = "05464601000003e803e800000000464601007803e803e80000000046460100f003e803e800000000464601003d03e803e80000000046460100ae03e803e800000000464601011303e803e800000000"
        self.disco = "06646401000003e803e800000000646401007003e803e80000000064640100f003e803e80000000064640100c903de03e800000000646401013503e803e800000000646401009803e803e800000000646401003b03e803e800000000646401009d007701f400000000"
        self.rainbow_pulse = "07464602000003e803e800000000464602007803e803e80000000046460200f003e803e800000000464602003d03e803e80000000046460200ae03e803e800000000464602011303e803e800000000"
        self.initial_states = []
        asyncio.run(self.set_initial_states())

    def __set_version__(self):
        for device in self.devices:
            device.set_version(3.3)

    async def turn_on(self):
        for device in self.devices:
            device.turn_on()

    async def turn_off(self):
        for device in self.devices:
            device.turn_off()

    async def toggle_light_scene(self, scene:str):
        scene = getattr(self, scene)
        for device in self.devices:
            device.set_mode('scene')
            device.set_value(25, scene)

    async def change_color(self, color: typing.Union[str, hex, tuple]):
        if isinstance(color, str):
            try:
                color = webcolors.name_to_rgb(color)
            except:
                color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        elif isinstance(color, tuple):
            color = color
        for device in self.devices:
            device.set_colour(*color)

    async def change_brightness(self, brightness: float = 100):
        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")
        else:
            brightness = brightness * 10
            for device in self.devices:
                device.set_brightness(int(brightness))

    async def notification_light(self, color):
        await self.total_white()
        await asyncio.sleep(1)
        await self.change_color(color)
        await asyncio.sleep(1)
        await self.total_white()


    async def set_initial_states(self):
        for i, d in enumerate(self.devices):
            data = {i: d.status()['dps']}
            self.initial_states.append(data)
        return self.initial_states

    async def reset_to_initial(self):
        print(len(self.devices))
        print(len(self.initial_states))
        for i, d in enumerate(self.devices):
            print(self.initial_states[i])
            payload = d.generate_payload(tinytuya.CONTROL, )
            d._send_receive(payload)


    async def total_white(self):
        for device in self.devices:
            device.set_white(1000, 1000)


