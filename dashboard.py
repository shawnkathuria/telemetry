import cantools
import pandas as pd
import sys
import serial
import json
import asyncio
import websockets
import asyncio
import random
import threading
import argparse


CONNECTIONS = set()

async def echo_handler(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)
    
async def send_to_clients(message: str):
        if CONNECTIONS:
            await asyncio.gather(*(ws.send(message) for ws in CONNECTIONS))

server = None

# Note: each Packet has Messages, and each Message has Signals
class Packet:
    def __init__(self, id, data_len):
        self.id = id
        self.data_len = data_len
        self.num_messages = 0
        self.messages = []
    
    def is_packet(self, id):
        return id.equals(self.id)
    
    def add_message(self, message):
        self.num_messages += 1
        self.messages.append(message)

class Message:
    def __init__(self, id, idx, start_byte, len):
        self.id = id
        self.idx = idx
        self.start_byte = start_byte
        self.len = len
        self.num_signals = 0
        self.signals = []
    
    def is_packet(self, id):
        return id.equals(self.id)
    
    def add_signal(self, signal):
        self.num_signals += 1
        self.signals.append(signal)

class Signal:
    def __init__(self, arr_idx, offset, scale, start_idx, len, unit, name, signed, endian):
        self.dict_idx = arr_idx
        self.offset = offset
        self.scale = scale
        self.start_idx = start_idx #start index in the packet in bytes
        self.value = -1
        self.len = len
        self.unit = unit
        self.name = name
        self.signed = signed
        self.endian = endian
 
    def get_value(self):
        return self.value
    
    def set_value(self, data):
        #print("set")
        #value = int.from_bytes(data, "big")
        self.value = self.offset + self.scale*data
        #data_final = {"name":self.name,"value":self.value}
        #asyncio.run_coroutine_threadsafe(send_to_clients(json.dumps(data_final)), loop)

    
pkts = []
signals = dict()

def parse_csv_and_db(csvpath, dbpath):
    csv_file = None
    db = None
    try:
        csv_file = pd.read_csv(csvpath)
    except:
        print("failed to open csv file")     
        return -1
    
    try:
        db = cantools.database.load_file(dbpath)
    except:
        print("failed to open db file")     
        return -1
    
    msg_count = int(csv_file.iat[0, 0])

    #Create the 3 packets
    for i in range(3):
        id = csv_file.iat[i+1, 0]
        length = int(csv_file.iat[i+1, 1])
        speed = int(csv_file.iat[i+1, 2]/10)
        num_messages = int(csv_file.iat[i+1, 3])
        p = Packet(id, length)
        pkts.append(p)

    pkt_curr_byte = [3,3,3]
    pkt_curr_msg_count = [0,0,0]
    curr_pkt_idx = None
    sig_count = 0
    for i in range(msg_count):
        msg_id = int(csv_file.iat[i+4, 0], 16)
        pkt = csv_file.iat[i+4, 4]
        data_len = int(int(csv_file.iat[i+4, 1])/8)
        
        if pkt == "m":
            curr_pkt_idx = 0
        elif pkt == "f":
            curr_pkt_idx = 1
        elif pkt == "s":
            curr_pkt_idx = 2

        msg = db.get_message_by_frame_id(msg_id)
        m = Message(msg_id, pkt_curr_msg_count[curr_pkt_idx], pkt_curr_byte[curr_pkt_idx], data_len)
        pkt_curr_byte[curr_pkt_idx] += data_len
        for signal in msg.signals:
            name = signal.name
            endian = 'little'
            if signal.byte_order == 'big_endian':
                endian = 'big'
            s = Signal(sig_count, signal.offset, signal.scale, signal.start, signal.length, signal.unit, name, signal.is_signed, endian)
            sig_count+=1
            m.add_signal(s)
            signals[name] = s
        pkts[curr_pkt_idx].add_message(m)

    print("parsed csv and database")
    return 0

def process_msg(pkt, msg, loop):
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

    asyncio.run_coroutine_threadsafe(send_to_clients(json.dumps(packet_signals)), loop)


pkt = None
msg = None
def serial_reader(ser, loop):
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
    

async def main(csv, db, port, baud, mock):
    if mock:
        # make randomized data for pkts[]
        pass
    else:
        error_code = parse_csv_and_db(csv, db)
        if error_code != 0:
            return
    
    server = await websockets.serve(echo_handler, "localhost", 4040)
    #to read pkts, read first byte, determine which pkt, read the rest
    #update value of all relevant signals
    ser = serial.Serial()
    ser.baudrate = baud
    ser.port = port
    ser.timeout=0.5
    ser.open()
    #read from the radio
    print("serial open")
    threading.Thread(target=serial_reader, args=(ser,asyncio.get_running_loop()), daemon=True).start()
    await asyncio.Future()

async def mock():
    pass

parser = argparse.ArgumentParser()
parser.add_argument("--csv", type = str, required=True, help = "path to csv")
parser.add_argument("--db", type = str, required=True, help = "path to database")
parser.add_argument("--port", type = str, default = "COM6", help = "serial port - COM6 by default")
parser.add_argument("--mock", type = bool, default = False, help = "default is False (uses real data)")
parser.add_argument("--baud", type = int, default = 115200, help = "baudrate - 115200 by default")

args = parser.parse_args()

asyncio.run(main(args.csv, args.db, args.port, args.baud, args.mock))
