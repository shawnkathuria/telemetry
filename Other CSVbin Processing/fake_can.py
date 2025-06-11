import sys
import pandas as pd

#To run this, use "python fake_can.py <path to csv>" 


def main(args):
    if len(args) != 1:
        print("No path provided.")
        return

    csv_file = None
    try:
        csv_file = pd.read_csv(args[0])
    except:
        print("failed to open file")     
        return
    
    f = open("fake_can.bin", "wb")
    #Number of messages
    msg_count = csv_file.shape[0]
    print(msg_count)
    t=msg_count.to_bytes()
    f.write(t)

    for i in range(msg_count):
        msg_id = int(csv_file.iat[i, 0], 16).to_bytes(4)
        f.write(msg_id)
        data_len = int(csv_file.iat[i, 1])
        dlc = int(csv_file.iat[i, 1]).to_bytes(4)
        f.write(dlc)
        zero = 0
        data = int(csv_file.iat[i, 2], 16).to_bytes(data_len)
        f.write(data)
        for j in range(data_len, 8):
            f.write(zero.to_bytes())

    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])





