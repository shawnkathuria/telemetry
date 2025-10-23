import serial
import asyncio
import threading
import argparse
import mock_mode
import serial_reader
import csv_db_parser
import websocket_server

async def main(csv, db, port, baud):
    error_code = csv_db_parser.parse_csv_and_db(csv, db, pkts, signals)
    if error_code != 0:
        return
    
    server = await websocket_server.serve(CONNECTIONS) # TODO does this change work?
    #to read pkts, read first byte, determine which pkt, read the rest
    #update value of all relevant signals
    ser = serial.Serial()
    ser.baudrate = baud
    ser.port = port
    ser.timeout=0.5
    ser.open()
    #read from the radio
    print("serial open")
    threading.Thread(target=serial_reader.serial_reader, args=(ser,asyncio.get_running_loop(), pkts, pkt, msg, CONNECTIONS), daemon=True).start()
    await asyncio.Future()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", type = bool, default = False, help = "whether to use real data - False by default")
    parser.add_argument("--csv", type = str, default = None, help = "path to csv (required if --mock is False)")
    parser.add_argument("--db", type = str, default = None, help = "path to database (required if --mock is False)")
    parser.add_argument("--port", type = str, default = "COM6", help = "serial port - COM6 by default")
    parser.add_argument("--baud", type = int, default = 115200, help = "baudrate - 115200 by default")
    args = parser.parse_args()

    CONNECTIONS = set()
    pkts = []
    signals = dict()
    server = None
    pkt = None
    msg = None

    if args.mock:
        for i in ["temp (C)", "volts (V)", "currents (A)", "wheel speeds (km/hr)", "throttle pos (%)"]:
            name = signal.name
            endian = 'little'
            if signal.byte_order == 'big_endian':
                endian = 'big'
            s = Signal(sig_count, signal.offset, signal.scale, signal.start, signal.length, signal.unit, name, signal.is_signed, endian)
            signals[s] = 0
        asyncio.run(mock_mode.run_mock(signals))
    elif args.csv is None or args.db is None:
        parser.error('--csv and --db are required when --mock is False')
    else:
        asyncio.run(main(args.csv, args.db, args.port, args.baud))
