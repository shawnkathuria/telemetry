import cantools
import pandas as pd

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
        self.value = self.offset + self.scale*data

def parse_csv_and_db(csvpath, dbpath, pkts, signals):
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