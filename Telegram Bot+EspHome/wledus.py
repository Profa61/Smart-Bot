import asyncio
from wled import WLED

IP = "192.168.0.90"


async def main(stat=True, lig=30):
    async with WLED(IP) as led:
        device = await led.update()
        print(device.info.version)

        await led.master(on=stat, brightness=lig)

if __name__ == "__main__":
    asyncio.run(main())
