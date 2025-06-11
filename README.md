# LiveTelemetry
This is the code for Columbia Formula Racing Club's Live Telemetry Visualisation.
## To Run the Visual
1. Plug the radio into your computer and identify the serial port number
	1. You can use the XCTU software to find the port number
	2. An orange light on the radio dev board should be blinking
2. Start the dashboard. The radio must be plugged in first else the dashboard will run.
	1. In your terminal, use the command, where ‘EV25_Telemetry.dbc’ is replaced with the path to the CAN dbc, and ‘CANSETTINGS.csv’ is the path to the .csv file with packet details:  
	python dashboard.py CANSETTINGS.csv .\EV25_Telemetry.dbc
	3. If the port doesn’t equal ‘COMS6’ , pass your port number as an argument like so, where ‘COM4’ is the serial port.  
 	dashboard.py CANSETTINGS.csv .\EV25_Telemetry.dbc COM4
2. Start the visualisation 
	1. In the desired visualisation folder use the following to start the visual:
		tsx main.ts
		(to force a restart use npx tsx main.ts instead)
	2. This will report the port number. Connect to this from a browser:  
	Eg. http://localhost:5000/   
	(replace 5000 with the desired port number)
	3. The primary visual is in ‘LT Dash 2.0’ folder, use this unless debugging. A simple visual for debugging is in the ‘LT Dash 1.0’ folder

## Dashboard.py
Dashboard.py contains the script to process data from the radio and transmit it to the visualisation. It takes the CAN dbc and a csv file as inputs so it can read the signals from our custom packets.

## LT Dash 2.0
LT Dash 2.0 contains the newer visual which is the current primary used by CUFR. It features 6 predetermined graphs and a table of other signal values.

## LT Dash 1.0
LT Dash 1.0 creates a new graph for every signal recieved and displays them in the order recieved. This is useful for debugging purposes.

## Create_bin.py 
This script creates a binary file encoding instructions for the STM MCU to process the CAN message and transmit them in the desired packets. It takes the csv file as input.
