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