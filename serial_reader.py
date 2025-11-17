import asyncio
import json

async def send_to_clients(CONNECTIONS, message: str):
    if CONNECTIONS:
        await asyncio.gather(*(ws.send(message) for ws in CONNECTIONS))

def process_msg(pkt, msg, loop, CONNECTIONS):
    #iterate through the first 2 bytes to iterate through messages and update values of the signals
    #test by printing one of the message testing sending
    
    packet_signals = {}
    key = msg[0]
    for i in range(16):
        # start of every packet: first byte = identifier, next two bytes = set of keys (message updated or not)
        # bitmask iterates through individual bits to not spend multiple bytes making indicators
        key = msg[0] if i < 8 else msg[1]
        if (i < 8 and (key & (1<<(7-i)) != 0)) or (i >= 8 and (key & (1<<(15-i)) != 0)):
            m = pkt.messages[i]
            for signal in m.signals:
                data = 0
                if(signal.len % 8 == 0):
                    start = m.start_byte-1+int(signal.start_idx/8)
                    data = msg[start:start + int(signal.len/8)]
                    data = int.from_bytes(data, signal.endian, signed=signal.signed)
                    if(signal.name == "SEN_TT_RR_8"):
                        print(signal.name, data, msg[start:start + int(signal.len/8)], msg)
                else:
                    start_bit = (m.start_byte-1)*8+signal.start_idx
                    start_byte = int(start_bit/8)
                    num_bytes = int(signal.len/8)+1
                    byte_data = msg[start_byte:start_byte+num_bytes]
                    mask = 0
                    for i in range(signal.len):
                        mask += pow(2,i)
                    int_data = int.from_bytes(byte_data, byteorder=signal.endian, signed=signal.signed)
                    data = int_data >> (num_bytes*8-start_bit%8-signal.len)
                    data = data&mask
                signal.set_value(data)
                packet_signals[signal.name] = signal.value

    asyncio.run_coroutine_threadsafe(send_to_clients(CONNECTIONS, json.dumps(packet_signals)), loop)

def serial_reader(ser, loop, pkts, pkt, msg, CONNECTIONS):
    while True:
        pkt = ser.read(1)
        #print(pkt)
        if(pkt == b'm'):
            msg = ser.read(pkts[0].data_len + 2)
            #print("med")
            print(msg)
            process_msg(pkts[0], msg, loop)
            #print(signals['INV_Module_C_Temp'].value)
        elif(pkt == b'f'):
            msg = ser.read(pkts[1].data_len + 2)
            #print("fast")
            process_msg(pkts[1], msg, loop)
        elif(pkt == b's'):
            msg = ser.read(pkts[2].data_len + 2)   
            print("stat")
            process_msg(pkts[2], msg, loop)
            #print(signals['LV_Vehicle_State'].value)