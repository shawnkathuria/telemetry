import asyncio
import json

async def send_to_clients(CONNECTIONS, message: str):
    """
    Sends a message to every connected WebSocket client.
    Safely removes disconnected clients.
    """
    if not CONNECTIONS:
        return

    to_remove = set()

    tasks = []
    for ws in CONNECTIONS:
        try:
            tasks.append(ws.send(message))
        except:
            to_remove.add(ws)

    # Await all sends
    if tasks:
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except:
            pass

    # Cleanup
    CONNECTIONS.difference_update(to_remove)


def process_msg(pkt, msg, loop, CONNECTIONS):
    """
    Decodes signals from a packet and schedules async send to WebSocket clients.
    """
    packet_signals = {}

    # Iterate through the first 2 bytes to determine which messages are updated
    for i in range(16):
        key = msg[0] if i < 8 else msg[1]

        # Determine which bit to check
        bit_index = 7 - i if i < 8 else 15 - i

        if key & (1 << bit_index):  
            m = pkt.messages[i]

            for signal in m.signals:

                if signal.len % 8 == 0:
                    # Byte-aligned
                    start = m.start_byte - 1 + int(signal.start_idx / 8)
                    data_bytes = msg[start : start + int(signal.len / 8)]
                    data = int.from_bytes(data_bytes, signal.endian, signed=signal.signed)

                else:
                    # Bit-level extraction
                    start_bit = (m.start_byte - 1) * 8 + signal.start_idx
                    start_byte = start_bit // 8
                    num_bytes = signal.len // 8 + 1
                    byte_data = msg[start_byte:start_byte + num_bytes]

                    mask = (1 << signal.len) - 1
                    full_int = int.from_bytes(byte_data, signal.endian, signed=signal.signed)

                    shift = (num_bytes * 8) - (start_bit % 8) - signal.len
                    data = (full_int >> shift) & mask

                signal.set_value(data)
                packet_signals[signal.name] = signal.value

    # Schedule async WebSocket broadcast from this thread
    asyncio.run_coroutine_threadsafe(
        send_to_clients(CONNECTIONS, json.dumps(packet_signals)),
        loop
    )


def serial_reader(ser, loop, pkts, pkt, msg, CONNECTIONS):
    while True:
        header = ser.read(1)
        if not header:
            continue

        if header == b'm':       # medium
            msg = ser.read(pkts[0].data_len + 2)
            process_msg(pkts[0], msg, loop, CONNECTIONS)

        elif header == b'f':     # fast
            msg = ser.read(pkts[1].data_len + 2)
            process_msg(pkts[1], msg, loop, CONNECTIONS)

        elif header == b's':     # slow/status
            msg = ser.read(pkts[2].data_len + 2)
            process_msg(pkts[2], msg, loop, CONNECTIONS)
