import aioesphomeapi
import asyncio
sensor = None


async def serv(deb=None):


    cli = aioesphomeapi.APIClient("192.168.0.50", 6053, "MyPass")
    await cli.connect(login=True)

    def change_callback(state):


        if type(state) == aioesphomeapi.SensorState:
            global sensor
            sensor = ('%.1f' % state.state)
            print(sensor)

    state = await cli.subscribe_states(change_callback)
    try:

        state = await cli.list_entities_services()

        retu = await cli.light_command(key=4244719125, state=deb, brightness=0.5,)


    except:RuntimeWarning

asyncio.run(serv())
