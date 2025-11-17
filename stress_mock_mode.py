import asyncio
import random
import math

async def run_mock(signals, loop_hz=1000):
    
    loop = asyncio.get_running_loop()
    t0 = loop.time()

    signal_names = list(signals.keys())
    num_signals = len(signal_names)

    print(f"[mock-stress] Heavy-load mock active ({num_signals} signals)")

    # Timing parameters
    steady_dt = 1.0 / loop_hz          # ~1000 Hz steady
    burst_dt = 1.0 / (loop_hz * 5)     # ~5000 Hz burst
    burst_interval = 4.0               # burst every 4 seconds
    burst_duration = 0.5               # bursts last 0.5 seconds

    next_burst = t0 + burst_interval
    in_burst = False
    burst_end = None

    updates = 0
    last_report = t0
    period = 12.0

    while True:
        now = loop.time()

        # --- burst switching ---
        if not in_burst and now >= next_burst:
            in_burst = True
            burst_end = now + burst_duration
            next_burst = now + burst_interval + burst_duration
            print("[mock-stress] BURST START")

        if in_burst and now >= burst_end:
            in_burst = False
            print("[mock-stress] BURST END")

        # --- waveform value ---
        t = now - t0
        raw = 35 + 8*math.sin(2*math.pi*t/period) + random.uniform(-0.3, 0.3)

        # --- update ALL signals ---
        for sig in signal_names:
            sig.set_value(raw, loop)

        updates += num_signals

        # --- throughput print (once/sec) ---
        if now - last_report >= 1.0:
            mode = "burst" if in_burst else "steady"
            print(f"[mock-stress] {updates} updates/sec ({mode})")
            updates = 0
            last_report = now

        # --- actual sleep ---
        await asyncio.sleep(burst_dt if in_burst else steady_dt)