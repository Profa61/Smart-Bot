import asyncio
from wled import WLED

IP = "192.168.0.90"


async def main(on=None, brightness=None):
    async with WLED(IP) as led:
        await led.update()


        await led.master(on=on, brightness=brightness)

if __name__ == "__main__":
    asyncio.run(main())
