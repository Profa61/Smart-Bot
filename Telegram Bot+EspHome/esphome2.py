import aioesphomeapi
import asyncio

sensor = None

IP = "192.168.0.50"
PORT = 6053
API = "RX/okru7tmJQIrzb3I9D7uTW65a1/2Nw9BHFhQBi46U="


async def serv(key=None, state=None, brightness=None):
    cli = aioesphomeapi.APIClient(IP, PORT, API)
    await cli.connect(login=True)

    def sens(state):
        if type(state) == aioesphomeapi.SensorState:
            global sensor
            sensor = ('%.1f' % state.state)
            print(sensor)

    await cli.subscribe_states(sens)
    try:

        await cli.list_entities_services()

        await cli.light_command(key=key, state=state, brightness=brightness,)

    except: RuntimeWarning

asyncio.run(serv())

