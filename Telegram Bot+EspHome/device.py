import asyncio
import esphome2 as esp
import wledus as wled


class Light:
    key = None
    state = None
    brightness = None

    def __init__(self, key, state, brightness):
        self.key = key
        self.state = state
        self.brightness = brightness
        asyncio.run(esp.serv(key=key, state=state, brightness=brightness))

    def get_state(self):
        print(self.key, self.state, self.brightness)


class Wled:
    on = None
    brightness = None

    def __init__(self, on, brightness):
        self.on = on
        self.brightness = brightness
        asyncio.run(wled.main(on=on, brightness=brightness))
