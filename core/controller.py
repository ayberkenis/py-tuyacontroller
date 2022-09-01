import tinytuya
import webcolors
import typing
import time


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
        self.initial_payloads = []

    def __set_version__(self):
        for device in self.devices:
            device.set_version(3.3)

    def turn_on(self):
        for device in self.devices:
            device.turn_on()

    def turn_off(self):
        for device in self.devices:
            device.turn_off()

    def toggle_light_scene(self, scene:str):
        scene = getattr(self, scene)
        for device in self.devices:
            device.set_mode('scene')
            device.set_value(25, scene)

    def change_color(self, color: typing.Union[str, hex, tuple]):
        if isinstance(color, str):
            try:
                color = webcolors.name_to_rgb(color)
            except:
                color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        elif isinstance(color, tuple):
            color = color
        for device in self.devices:
            device.set_colour(*color)

    def change_brightness(self, brightness: float = 100):
        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")
        else:
            brightness = brightness * 10
            for device in self.devices:
                device.set_brightness(int(brightness))

    def notification_light(self, color):
        self.get_current_status()
        self.change_color(color)
        self.get_current_status()
        self.change_color(color)
        self.get_current_status()


    def get_current_status(self):
        payloads = self.__send_receive__()
        for p in payloads:
            for d in self.devices:
                d._send_receive(p)


    def total_white(self):
        for device in self.devices:
            device.set_white(1000, 1000)

    def __send_receive__(self):
        payloads = []
        for i, d in enumerate(self.devices):
            d.set_socketPersistent(True)
            payload = d.generate_payload(tinytuya.DP_QUERY)
            d.send(payload)
            data = d.receive()
            payload = d.generate_payload(tinytuya.HEART_BEAT)
            d.send(payload)
            payloads.append(payload)
        return payloads

