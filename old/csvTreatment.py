"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create october, 1, 2020
    @title: CSV functions
"""
# Libraries
import os
import csv
import pandas as pd
from datetime import datetime
from epicsConcrete import EpicsServer
from calibration import Calibration as cal
from PvProperties import PvProperties as pvp

class CsvTreatment():
    
    # Constructor Method
    def __init__(self):
        super(CsvTreatment, self).__init__()
        self.server = EpicsServer()
        self.server.start()

    # Read the csv file
    def read(self, host, port, user, password, filename):
        self.recordAction("[%s] Action: starting the file read" % self.getDateTime())
        # Use pandas to read a csv file from an FTP server
        mti = pd.read_csv("ftp://%s:%s@%s:%d/%s" %
                            (user, password, host, port, filename), 
                            error_bad_lines=False, header=None)
        self.recordAction("[%s] Action: file imported" % self.getDateTime())
        return(mti)
    
    # Get the current date and time
    def getDateTime(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Record the actions in monitor.txt
    def recordAction(self, text):
        self.monitor = open("monitor.txt", "a")
        self.monitor.write(text + "\n")
        self.monitor.close()
    
    # Separate data into a dictionary
    def newMux(self, mux):
        channel = 1 # Variable to control de number of channels
        # Initialize mux dictionary with basic informations
        muxDictionary = {
            "Id": mux[0],
            "Datetime": mux[1],
            "Volt": mux[2],
            "Temperature": mux[3]} 
        # Scroll the channels and set the info into the dictionary
        for i in range(4, len(mux)):
            if str(mux[i]) != "nan":
                if i % 2 == 0:
                    option = "Ch%d%s" % (channel, "A")
                    try:
                        muxDictionary[option] = cal.convertChannelA(mux[0], channel, mux[i])
                    except:
                        muxDictionary[option] = float("nan")
                    # Update the respective pv
                    pvName = pvp.pvName(int(mux[0]), int(channel), "A")
                    if pvName != "Dis.":
                        if str(muxDictionary[option]) not in ["Dis.", "error"]:
                            EpicsServer.driver.write(pvName, float(muxDictionary[option]))
                        else:
                            EpicsServer.driver.write(pvName, 0)
                else:
                    # Add to dictionary with convertion to Celsius degrees
                    try:
                        muxDictionary["Ch%d%s" % (channel, "B")] = cal.convertChannelB(mux[i])
                    except:
                        muxDictionary["Ch%d%s" % (channel, "B")] = str(mux[i]) + " (error)"
                    # Update the respective pv
                    pvName = pvp.pvName(mux[0], channel, "B")
                    if pvName != "Dis.":
                        if str(muxDictionary[option]) not in ["Dis.", "error"]:
                            EpicsServer.driver.write(pvName, float(muxDictionary[option]))
                        else:
                            EpicsServer.driver.write(pvName, 0)
                    channel += 1
        muxDictionary["Number of channels"] = channel - 1
        return muxDictionary
            
    # Get the last line of csv and separate data into a dictionary
    def separateLastData(self, rawData):
        setId = 0; mux = []; muxes = {}
        tableLine = rawData.tail(1).values[0]
        # Scroll the vector looking for a new mux
        for i in range(len(tableLine) - 1):
            if ":" in str(tableLine[i]): # Identify a datetime cell
                if setId != 0:
                    muxes[cal.MUXactivated[setId - 1]] = self.newMux(mux)
                mux = []; mux.append(cal.MUXactivated[setId])
                mux.append(tableLine[i])
                setId += 1
            elif tableLine[i] != "":
                mux.append(tableLine[i])
        self.updateCSV(muxes)
    
    # Generate a CSV file with the data read
    def updateCSV(self, muxes):
        with open("MTI_converted.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            header = []; data = []
            # Verify if the csv file is empty to set a header
            if os.path.getsize("MTI_converted.csv") == 0:
                for mux in muxes.keys():
                    for op in (muxes[mux]).keys():
                        header.append(op)
                        data.append(muxes[mux][op])
                writer.writerow(header)
                writer.writerow(data)
            else:
                for mux in muxes.keys():
                    for op in (muxes[mux]).keys():
                        data.append(muxes[mux][op])
                writer.writerow(data)
        csvfile.close()
        self.recordAction("[%s] CSV generate succesfully" % self.getDateTime())
