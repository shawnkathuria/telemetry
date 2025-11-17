import cantools
import pandas as pd
import classes

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
        p = classes.Packet(id, length)
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
        m = classes.Message(msg_id, pkt_curr_msg_count[curr_pkt_idx], pkt_curr_byte[curr_pkt_idx], data_len)
        pkt_curr_byte[curr_pkt_idx] += data_len
        for signal in msg.signals:
            name = signal.name
            endian = 'little'
            if signal.byte_order == 'big_endian':
                endian = 'big'
            s = classes.Signal(sig_count, signal.offset, signal.scale, signal.start, signal.length, signal.unit, name, signal.is_signed, endian)
            sig_count+=1
            m.add_signal(s)
            signals[name] = s
        pkts[curr_pkt_idx].add_message(m)

    print("parsed csv and database")
    return 0