import asyncio
import random
import math

async def run_mock(signals, loop_hz = 10):
    period = 12.0
    dt = 1.0 / max(loop_hz,1)
    t0 = asyncio.get_running_loop().time()
    target = "INV_Module_C_Temp" if "INV_Module_C_Temp" in signals else next(iter(signals.keys()))
    print(f"[mock] driving signal: {target}")
    while True:
        t = asyncio.get_running_loop().time() - t0
        raw = 35 + 8*math.sin(2*math.pi*t/period) + random.uniform(-.03, 0.3)
        signals[target].set_value(raw,asyncio.get_running_loop())
        await asyncio.sleep(dt)