import serial
import asyncio
import threading
import argparse
import mock_mode
import stress_mock_mode
import serial_reader
import csv_db_parser
import websocket_server
import classes

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
    parser.add_argument("--stressMock", type = bool, default = False, help = "whether to run mock mode for stress testing - False by default")
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

    if args.mock or args.stressMock:
        sig_count = 0
        mock_signals = {"temp (C)": "deg C", "volts (V)": "V", "currents (A)": "A", "wheel speeds (km/hr)": "km/hr", "throttle pos (%)": "%"}
        for sig_name, sig_unit in mock_signals.items():
            s = classes.Signal(arr_idx=sig_count, offset=0, scale=0, start=0, length=0, unit=sig_unit, name=sig_name, is_signed=0, endian=0)
            sig_count += 1
            signals[s] = 0
        if args.mock:
            asyncio.run(mock_mode.run_mock(signals))
        else:
            asyncio.run(stress_mock_mode.run_mock(signals))
    elif args.csv is None or args.db is None:
        parser.error('--csv and --db are required when --mock is False')
    else:
        asyncio.run(main(args.csv, args.db, args.port, args.baud))
