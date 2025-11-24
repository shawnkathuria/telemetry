import asyncio
import random
import math

async def run_mock(signals, loop_hz = 10):
    period = 12.0
    dt = 1.0 / max(loop_hz,1)
    t0 = asyncio.get_running_loop().time()
    while True:
        t = asyncio.get_running_loop().time() - t0
        raw = 35 + 8*math.sin(2*math.pi*t/period) + random.uniform(-0.3, 0.3)

        for target in list(signals.keys()):
            signals[target].set_value(raw)

        await asyncio.sleep(dt)

