import asyncio
import random

# Set your ranges here (min, max)
RANGES = {
    "SEN_WSS_FL": (0.0, 120.0),
    "SEN_WSS_FR": (0.0, 120.0),
    "SEN_WSS_RL": (0.0, 120.0),
    "SEN_WSS_RR": (0.0, 120.0),

    # raw ADC counts (so your JS BPT conversion makes sense)
    "LV_BPT_Front": (0.0, 4095.0),
    "LV_BPT_Rear": (0.0, 4095.0),

    "SEN_Damper_Pos_FL": (0.0, 100.0),
    "SEN_Damper_Pos_FR": (0.0, 100.0),
    "SEN_Damper_Pos_RL": (0.0, 100.0),
    "SEN_Damper_Pos_RR": (0.0, 100.0),

    "INV_Motor_Speed": (0.0, 20000.0),

    "SEN_G_FORCE_X": (-3.0, 3.0),
    "SEN_G_FORCE_Y": (-3.0, 3.0),
    "SEN_G_FORCE_Z": (-3.0, 3.0),

    "INV_Commanded_Torque": (-250.0, 250.0),
    "INV_Torque_Feedback": (-250.0, 250.0),
    "VCU_INV_Torque_Command": (-250.0, 250.0),
}

async def run_mock(signals, loop_hz=10):
    dt = 1.0 / max(loop_hz, 1)

    while True:
        for name, sig in signals.items():
            lo, hi = RANGES.get(name, (0.0, 1.0))
            value = random.uniform(lo, hi)
            sig.set_value(value)
        
        # if name == "SEN_WSS_FL":
        # print("trying to set:", value)
        # print("sig.__dict__:", sig.__dict__)

        await asyncio.sleep(dt)



# async def run_mock(signals, loop_hz=10):
#     period = 12.0
#     dt = 1.0 / max(loop_hz, 1)
#     loop = asyncio.get_running_loop()
#     t0 = loop.time()

#     while True:
#         t = loop.time() - t0
#         # raw = 35 + 8*math.sin(2*math.pi*t/period) + random.uniform(-0.3, 0.3)

#         for name, sig in signals.items():
#             if name == "BeaconCount":
#                 sig.set_value(int(t) % 100)          # 0..99 counter
#             elif name == "LV_FILTERED_V":
#                 sig.set_value(250 + 10*math.sin(t))  # looks like a voltage
#             elif name == "LV_Vehicle_State":
#                 sig.set_value(int(t) % 6)            # state 0..5
#             else:
#                 sig.set_value(raw)

#         await asyncio.sleep(dt)