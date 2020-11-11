"""
    @author Leonardo Rossi Leão / Rodrigo de Oliveira Neto
    @create november, 09, 2020
    @title: EPICS
"""

import threading
from pcaspy import SimpleServer, Driver




def aux(mux, inicio, fim):
    saida = "";
    for i in range(inicio, fim+1):
        saida += '{"mux": %d, "channel": %d, "position": 0, "level": "A"}, ' % (mux, i)
    return saida

class LocalServer():
    
    floor = {"01B": [{"mux": 14, "channel": 1, "position": 5, "level": "A"}, {"mux": 14, "channel": 2, "position": 5, "level": "B"}, {"mux": 14, "channel": 3, "position": 5, "level": "C"}, {"mux": 14, "channel": 4, "position": 7, "level": "A"}, {"mux": 14, "channel": 5, "position": 7, "level": "C"}, {"mux": 14, "channel": 6, "position": 9, "level": "A"}, {"mux": 14, "channel": 7, "position": 9, "level": "C"}, ],
             "02B": [{"mux": 14, "channel": 8, "position": 5, "level": "A"}, {"mux": 14, "channel": 9, "position": 5, "level": "B"}, {"mux": 14, "channel": 10, "position": 5, "level": "C"}, {"mux": 14, "channel": 11, "position": 7, "level": "A"}, {"mux": 14, "channel": 12, "position": 7, "level": "C"}, {"mux": 14, "channel": 13, "position": 9, "level": "A"}, {"mux": 14, "channel": 14, "position": 9, "level": "C"}],
             "03B": [{"mux": 17, "channel": 1, "position": 5, "level": "A"}, {"mux": 17, "channel": 2, "position": 5, "level": "B"}, {"mux": 17, "channel": 3, "position": 5, "level": "C"}],
             "04A": [{"mux": 23, "channel": 1, "position": 1, "level": "A"}, {"mux": 23, "channel": 2, "position": 1, "level": "C"}, {"mux": 23, "channel": 3, "position": 2, "level": "A-Y"}, {"mux": 23, "channel": 4, "position": 2, "level": "C-Y"}, {"mux": 23, "channel": 5, "position": 3, "level": "A"}, {"mux": 23, "channel": 6, "position": 3, "level": "B"}, {"mux": 23, "channel": 7, "position": 3, "level": "C"}, {"mux": 23, "channel": 8, "position": 4, "level": "A-Y"}, {"mux": 24, "channel": 1, "position": 4, "level": "C-Y"}, {"mux": 24, "channel": 2, "position": 5, "level": "A"}, {"mux": 24, "channel": 3, "position": 5, "level": "C"}, {"mux": 24, "channel": 4, "position": 6, "level": "A-X"}, {"mux": 24, "channel": 5, "position": 6, "level": "C-X"}, {"mux": 24, "channel": 6, "position": 7, "level": "A"}, {"mux": 24, "channel": 7, "position": 7, "level": "C"}, {"mux": 24, "channel": 8, "position": 8, "level": "A"}, {"mux": 24, "channel": 9, "position": 8, "level": "C"}, {"mux": 24, "channel": 10, "position": 9, "level": "A"}, {"mux": 24, "channel": 11, "position": 9, "level": "C"}, {"mux": 24, "channel": 12, "position": 10, "level": "A-X"}, {"mux": 24, "channel": 13, "position": 10, "level": "C-X"}, {"mux": 24, "channel": 14, "position": 11, "level": "A"}, {"mux": 24, "channel": 15, "position": 11, "level": "C"}, {"mux": 24, "channel": 16, "position": 12, "level": "A"}, {"mux": 28, "channel": 1, "position": 12, "level": "C"}, {"mux": 28, "channel": 2, "position": 13, "level": "A-X"}, {"mux": 28, "channel": 3, "position": 13, "level": "A-Y"}, {"mux": 28, "channel": 4, "position": 13, "level": "B"}, {"mux": 28, "channel": 5, "position": 13, "level": "C-X"}, {"mux": 28, "channel": 6, "position": 13, "level": "C-Y"}, {"mux": 28, "channel": 7, "position": 14, "level": "A"}, {"mux": 28, "channel": 8, "position": 14, "level": "C"}, {"mux": 28, "channel": 9, "position": 15, "level": "A"}, {"mux": 28, "channel": 10, "position": 15, "level": "B"}, {"mux": 28, "channel": 11, "position": 15, "level": "C"}, {"mux": 28, "channel": 12, "position": 16, "level": "A-X"}, {"mux": 28, "channel": 13, "position": 16, "level": "C-X"}, {"mux": 28, "channel": 14, "position": 17, "level": "A"}, {"mux": 28, "channel": 15, "position": 17, "level": "C"}, {"mux": 28, "channel": 16, "position": 18, "level": "A"}, {"mux": 29, "channel": 1, "position": 18, "level": "C"}, {"mux": 29, "channel": 2, "position": 19, "level": "A"}, {"mux": 29, "channel": 3, "position": 19, "level": "C"}, {"mux": 29, "channel": 4, "position": 20, "level": "A-X"}, {"mux": 29, "channel": 5, "position": 20, "level": "C-X"}, {"mux": 29, "channel": 6, "position": 21, "level": "A"}, {"mux": 29, "channel": 7, "position": 21, "level": "C"}, {"mux": 29, "channel": 8, "position": 22, "level": "A-Y"}, {"mux": 29, "channel": 9, "position": 22, "level": "C-Y"}, {"mux": 29, "channel": 10, "position": 23, "level": "A"}, {"mux": 29, "channel": 11, "position": 23, "level": "B"}, {"mux": 29, "channel": 12, "position": 23, "level": "C"}, {"mux": 29, "channel": 13, "position": 24, "level": "A-Y"}, {"mux": 29, "channel": 14, "position": 24, "level": "C-Y"}, {"mux": 29, "channel": 15, "position": 25, "level": "A"}, {"mux": 29, "channel": 16, "position": 25, "level": "C"}],
             "04B": [{"mux": 17, "channel": 4, "position": 5, "level": "A"}, {"mux": 17, "channel": 5, "position": 5, "level": "C"}, {"mux": 17, "channel": 6, "position": 7, "level": "A"}, {"mux": 17, "channel": 7, "position": 7, "level": "B"}, {"mux": 17, "channel": 8, "position": 7, "level": "C"}, {"mux": 17, "channel": 9, "position": 7, "level": "A_H"}, {"mux": 17, "channel": 10, "position": 7, "level": "A_V"}, {"mux": 17, "channel": 11, "position": 7, "level": "C_H"}, {"mux": 17, "channel": 12, "position": 7, "level": "C_V"}, {"mux": 15, "channel": 1, "position": 4, "level": "A"}, {"mux": 15, "channel": 2, "position": 4, "level": "B"}, {"mux": 15, "channel": 3, "position": 4, "level": "C"}, {"mux": 15, "channel": 4, "position": 4, "level": "A_H"}, {"mux": 15, "channel": 5, "position": 4, "level": "A_V"}, {"mux": 15, "channel": 6, "position": 4, "level": "C_H"}, {"mux": 15, "channel": 7, "position": 4, "level": "C_V"}, {"mux": 15, "channel": 8, "position": 3, "level": "A"}, {"mux": 15, "channel": 9, "position": 3, "level": "B"}, {"mux": 15, "channel": 10, "position": 3, "level": "C"}, {"mux": 15, "channel": 11, "position": 3, "level": "A_H"}, {"mux": 15, "channel": 12, "position": 3, "level": "A_V"}, {"mux": 15, "channel": 13, "position": 3, "level": "C_H"}, {"mux": 15, "channel": 14, "position": 3, "level": "C_V"}, {"mux": 15, "channel": 15, "position": 6, "level": "A"}, {"mux": 15, "channel": 16, "position": 6, "level": "B"}, {"mux": 16, "channel": 1, "position": 6, "level": "C"}, {"mux": 16, "channel": 2, "position": 6, "level": "A_H"}, {"mux": 16, "channel": 3, "position": 6, "level": "A_V"}, {"mux": 16, "channel": 4, "position": 6, "level": "C_H"}, {"mux": 16, "channel": 5, "position": 6, "level": "C_V"}, {"mux": 16, "channel": 6, "position": 1, "level": "A_H"}, {"mux": 16, "channel": 7, "position": 1, "level": "A_V"}, {"mux": 16, "channel": 8, "position": 1, "level": "C_H"}, {"mux": 16, "channel": 9, "position": 1, "level": "C_V"}, {"mux": 16, "channel": 10, "position": 9, "level": "A_H"}, {"mux": 16, "channel": 11, "position": 9, "level": "A_V"}, {"mux": 16, "channel": 12, "position": 9, "level": "C_H"}, {"mux": 16, "channel": 13, "position": 9, "level": "C_V"}],
             "05B": [{"mux": 1, "channel": 7, "position": 5, "level": "A"}, {"mux": 2, "channel": 1, "position": 5, "level": "B"}, {"mux": 2, "channel": 2, "position": 5, "level": "C"}, {"mux": 2, "channel": 3, "position": 7, "level": "A"}, {"mux": 2, "channel": 4, "position": 7, "level": "C"}, {"mux": 2, "channel": 5, "position": 9, "level": "A"}, {"mux": 2, "channel": 6, "position": 9, "level": "C"}, ],
             "06B": [{"mux": 1, "channel": 8, "position": 5, "level": "A"}, {"mux": 1, "channel": 1, "position": 5, "level": "B"}, {"mux": 1, "channel": 2, "position": 5, "level": "C"}, {"mux": 1, "channel": 3, "position": 7, "level": "A"}, {"mux": 1, "channel": 4, "position": 7, "level": "C"}, {"mux": 1, "channel": 5, "position": 9, "level": "A"}, {"mux": 1, "channel": 6, "position": 9, "level": "C"}, ],
             "07B": [{"mux": 2, "channel": 7, "position": 5, "level": "A"}, {"mux": 2, "channel": 8, "position": 5, "level": "B"}, {"mux": 2, "channel": 9, "position": 5, "level": "C"}, {"mux": 2, "channel": 10, "position": 7, "level": "A"}, {"mux": 2, "channel": 11, "position": 7, "level": "C"}, {"mux": 2, "channel": 12, "position": 9, "level": "A"}, {"mux": 2, "channel": 13, "position": 9, "level": "C"}],
             "08B": [{"mux": 3, "channel": 1, "position": 5, "level": "A"}, {"mux": 3, "channel": 2, "position": 5, "level": "B"}, {"mux": 3, "channel": 3, "position": 5, "level": "C"}],
             "09B_LINAC": [{"mux": 3, "channel": 4, "position": 5, "level": "A"}, {"mux": 3, "channel": 5, "position": 5, "level": "C"}, {"mux": 3, "channel": 6, "position": 7, "level": "A"}, {"mux": 3, "channel": 7, "position": 7, "level": "B"}, {"mux": 3, "channel": 8, "position": 7, "level": "C"}, {"mux": 3, "channel": 9, "position": 7, "level": "A_H"}, {"mux": 3, "channel": 10, "position": 7, "level": "A_V"}, {"mux": 3, "channel": 11, "position": 7, "level": "C_H"}, {"mux": 3, "channel": 12, "position": 7, "level": "C_V"}, {"mux": 3, "channel": 13, "position": 4, "level": "A"}, {"mux": 3, "channel": 14, "position": 4, "level": "B"}, {"mux": 3, "channel": 15, "position": 4, "level": "C"}, {"mux": 3, "channel": 16, "position": 4, "level": "A_H"}, {"mux": 4, "channel": 1, "position": 4, "level": "A_V"}, {"mux": 4, "channel": 2, "position": 4, "level": "C_H"}, {"mux": 4, "channel": 3, "position": 4, "level": "C_V"}, {"mux": 4, "channel": 4, "position": 3, "level": "A"}, {"mux": 4, "channel": 5, "position": 3, "level": "B"}, {"mux": 4, "channel": 6, "position": 3, "level": "C"}, {"mux": 4, "channel": 7, "position": 3, "level": "A_H"}, {"mux": 4, "channel": 8, "position": 3, "level": "A_V"}, {"mux": 4, "channel": 9, "position": 3, "level": "C_H"}, {"mux": 4, "channel": 10, "position": 3, "level": "C_V"}, {"mux": 4, "channel": 11, "position": 6, "level": "A"}, {"mux": 4, "channel": 12, "position": 6, "level": "B"}, {"mux": 4, "channel": 13, "position": 6, "level": "C"}, {"mux": 4, "channel": 14, "position": 6, "level": "A_H"}, {"mux": 4, "channel": 15, "position": 6, "level": "A_V"}, {"mux": 4, "channel": 16, "position": 6, "level": "C_H"}, {"mux": 5, "channel": 1, "position": 6, "level": "C_V"}, {"mux": 5, "channel": 2, "position": 1, "level": "A_H"}, {"mux": 5, "channel": 3, "position": 1, "level": "A_V"}, {"mux": 5, "channel": 4, "position": 1, "level": "C_H"}, {"mux": 5, "channel": 5, "position": 1, "level": "C_V"}, {"mux": 5, "channel": 6, "position": 9, "level": "A_H"}, {"mux": 5, "channel": 7, "position": 9, "level": "A_V"}, {"mux": 5, "channel": 8, "position": 9, "level": "C_H"}, {"mux": 5, "channel": 9, "position": 9, "level": "C_V"}],
             "10B_LINAC": [{"mux": 5, "channel": 10, "position": 5, "level": "A"}, {"mux": 5, "channel": 11, "position": 5, "level": "B"}, {"mux": 5, "channel": 12, "position": 5, "level": "C"}, {"mux": 5, "channel": 13, "position": 7, "level": "A"}, {"mux": 5, "channel": 14, "position": 7, "level": "C"}, {"mux": 5, "channel": 15, "position": 9, "level": "A"}, {"mux": 5, "channel": 16, "position": 9, "level": "C"}],
             "11B": [{"mux": 6, "channel": 1, "position": 5, "level": "A"}, {"mux": 6, "channel": 2, "position": 5, "level": "B"}, {"mux": 6, "channel": 3, "position": 5, "level": "C"}, {"mux": 6, "channel": 4, "position": 7, "level": "A"}, {"mux": 6, "channel": 5, "position": 7, "level": "C"}, {"mux": 6, "channel": 6, "position": 9, "level": "A"}, {"mux": 6, "channel": 7, "position": 9, "level": "C"}],
             "12B": [{"mux": 6, "channel": 8, "position": 5, "level": "A"}, {"mux": 6, "channel": 9, "position": 5, "level": "B"}, {"mux": 6, "channel": 10, "position": 5, "level": "C"}, {"mux": 6, "channel": 11, "position": 7, "level": "A"}, {"mux": 6, "channel": 12, "position": 7, "level": "C"}, {"mux": 6, "channel": 13, "position": 9, "level": "A"}, {"mux": 6, "channel": 14, "position": 9, "level": "C"}],
             "13B": [{"mux": 7, "channel": 1, "position": 5, "level": "A"}, {"mux": 7, "channel": 2, "position": 5, "level": "B"}, {"mux": 7, "channel": 3, "position": 5, "level": "C"}],
             "14B": [{"mux": 7, "channel": 4, "position": 5, "level": "A"}, {"mux": 7, "channel": 5, "position": 5, "level": "C"}, {"mux": 7, "channel": 6, "position": 7, "level": "A"}, {"mux": 7, "channel": 7, "position": 7, "level": "B"}, {"mux": 7, "channel": 8, "position": 7, "level": "C"}, {"mux": 7, "channel": 9, "position": 7, "level": "A_H"}, {"mux": 7, "channel": 10, "position": 7, "level": "A_V"}, {"mux": 7, "channel": 11, "position": 7, "level": "C_H"}, {"mux": 7, "channel": 12, "position": 7, "level": "C_V"}, {"mux": 7, "channel": 13, "position": 4, "level": "A"}, {"mux": 7, "channel": 14, "position": 4, "level": "B"}, {"mux": 7, "channel": 15, "position": 4, "level": "C"}, {"mux": 7, "channel": 16, "position": 4, "level": "A_H"}, {"mux": 8, "channel": 1, "position": 4, "level": "A_V"}, {"mux": 8, "channel": 2, "position": 4, "level": "C_H"}, {"mux": 8, "channel": 3, "position": 4, "level": "C_V"}, {"mux": 8, "channel": 4, "position": 3, "level": "A"}, {"mux": 8, "channel": 5, "position": 3, "level": "B"}, {"mux": 8, "channel": 6, "position": 3, "level": "C"}, {"mux": 8, "channel": 7, "position": 3, "level": "A_H"}, {"mux": 8, "channel": 8, "position": 3, "level": "A_V"}, {"mux": 8, "channel": 9, "position": 3, "level": "C_H"}, {"mux": 8, "channel": 10, "position": 3, "level": "C_V"}, {"mux": 8, "channel": 11, "position": 6, "level": "A"}, {"mux": 8, "channel": 12, "position": 6, "level": "B"}, {"mux": 8, "channel": 13, "position": 6, "level": "C"}, {"mux": 8, "channel": 14, "position": 6, "level": "A_H"}, {"mux": 8, "channel": 15, "position": 6, "level": "A_V"}, {"mux": 8, "channel": 16, "position": 6, "level": "C_H"}, {"mux": 9, "channel": 1, "position": 6, "level": "C_V"}, {"mux": 9, "channel": 2, "position": 1, "level": "A_H"}, {"mux": 9, "channel": 3, "position": 1, "level": "A_V"}, {"mux": 9, "channel": 4, "position": 1, "level": "C_H"}, {"mux": 9, "channel": 5, "position": 1, "level": "C_V"}, {"mux": 9, "channel": 6, "position": 9, "level": "A_H"}, {"mux": 9, "channel": 7, "position": 9, "level": "A_V"}, {"mux": 9, "channel": 8, "position": 9, "level": "C_H"}, {"mux": 9, "channel": 9, "position": 9, "level": "C_V"}],
             "15B": [{"mux": 9, "channel": 10, "position": 5, "level": "A"}, {"mux": 9, "channel": 11, "position": 5, "level": "B"}, {"mux": 9, "channel": 12, "position": 5, "level": "C"}, {"mux": 9, "channel": 13, "position": 7, "level": "A"}, {"mux": 9, "channel": 14, "position": 7, "level": "C"}, {"mux": 9, "channel": 15, "position": 9, "level": "A"}, {"mux": 9, "channel": 16, "position": 9, "level": "C"}],
             "16B": [{"mux": 10, "channel": 1, "position": 5, "level": "A"}, {"mux": 10, "channel": 2, "position": 5, "level": "B"}, {"mux": 10, "channel": 3, "position": 5, "level": "C"}, {"mux": 10, "channel": 4, "position": 7, "level": "A"}, {"mux": 10, "channel": 5, "position": 7, "level": "C"}, {"mux": 10, "channel": 6, "position": 9, "level": "A"}, {"mux": 10, "channel": 7, "position": 9, "level": "C"}],
             "17B": [{"mux": 10, "channel": 8, "position": 5, "level": "A"}, {"mux": 10, "channel": 9, "position": 5, "level": "B"}, {"mux": 10, "channel": 10, "position": 5, "level": "C"}, {"mux": 10, "channel": 11, "position": 7, "level": "A"}, {"mux": 10, "channel": 12, "position": 7, "level": "C"}, {"mux": 10, "channel": 13, "position": 9, "level": "A"}, {"mux": 10, "channel": 14, "position": 9, "level": "C"}],
             "18B": [{"mux": 11, "channel": 1, "position": 5, "level": "A"}, {"mux": 11, "channel": 2, "position": 5, "level": "B"}, {"mux": 11, "channel": 3, "position": 5, "level": "C"}],
             "19B": [{"mux": 11, "channel": 4, "position": 5, "level": "A"}, {"mux": 11, "channel": 5, "position": 5, "level": "C"}, {"mux": 11, "channel": 6, "position": 7, "level": "A"}, {"mux": 11, "channel": 7, "position": 7, "level": "B"}, {"mux": 11, "channel": 8, "position": 7, "level": "C"}, {"mux": 11, "channel": 9, "position": 7, "level": "A_H"}, {"mux": 11, "channel": 10, "position": 7, "level": "A_V"}, {"mux": 11, "channel": 11, "position": 7, "level": "C_H"}, {"mux": 11, "channel": 12, "position": 7, "level": "C_V"}, {"mux": 11, "channel": 13, "position": 4, "level": "A"}, {"mux": 11, "channel": 14, "position": 4, "level": "B"}, {"mux": 11, "channel": 15, "position": 4, "level": "C"}, {"mux": 11, "channel": 16, "position": 4, "level": "A_H"}, {"mux": 12, "channel": 1, "position": 4, "level": "A_V"}, {"mux": 12, "channel": 2, "position": 4, "level": "C_H"}, {"mux": 12, "channel": 3, "position": 4, "level": "C_V"}, {"mux": 12, "channel": 4, "position": 3, "level": "A"}, {"mux": 12, "channel": 5, "position": 3, "level": "B"}, {"mux": 12, "channel": 6, "position": 3, "level": "C"}, {"mux": 12, "channel": 7, "position": 3, "level": "A_H"}, {"mux": 12, "channel": 8, "position": 3, "level": "A_V"}, {"mux": 12, "channel": 9, "position": 3, "level": "C_H"}, {"mux": 12, "channel": 10, "position": 3, "level": "C_V"}, {"mux": 12, "channel": 11, "position": 6, "level": "A"}, {"mux": 12, "channel": 12, "position": 6, "level": "B"}, {"mux": 12, "channel": 13, "position": 6, "level": "C"}, {"mux": 12, "channel": 14, "position": 6, "level": "A_H"}, {"mux": 12, "channel": 15, "position": 6, "level": "A_V"}, {"mux": 12, "channel": 16, "position": 6, "level": "C_H"}, {"mux": 13, "channel": 1, "position": 6, "level": "C_V"}, {"mux": 13, "channel": 2, "position": 1, "level": "A_H"}, {"mux": 13, "channel": 3, "position": 1, "level": "A_V"}, {"mux": 13, "channel": 4, "position": 1, "level": "C_H"}, {"mux": 13, "channel": 5, "position": 1, "level": "C_V"}, {"mux": 13, "channel": 6, "position": 9, "level": "A_H"}, {"mux": 13, "channel": 7, "position": 9, "level": "A_V"}, {"mux": 13, "channel": 8, "position": 9, "level": "C_H"}, {"mux": 13, "channel": 9, "position": 9, "level": "C_V"}],
             "20B": [{"mux": 13, "channel": 10, "position": 5, "level": "A"}, {"mux": 13, "channel": 11, "position": 5, "level": "B"}, {"mux": 13, "channel": 12, "position": 5, "level": "C"}, {"mux": 13, "channel": 13, "position": 7, "level": "A"}, {"mux": 13, "channel": 14, "position": 7, "level": "C"}, {"mux": 13, "channel": 15, "position": 9, "level": "A"}, {"mux": 13, "channel": 16, "position": 9, "level": "C"}]        
            }
    
    locker = {"Eixo58": [{"mux": 27, "channel": 1, "position": 0, "level": "A"}, {"mux": 27, "channel": 2, "position": 0, "level": "A"}, {"mux": 27, "channel": 3, "position": 0, "level": "A"}, {"mux": 27, "channel": 4, "position": 0, "level": "A"}, {"mux": 27, "channel": 5, "position": 0, "level": "A"}, {"mux": 27, "channel": 6, "position": 0, "level": "A"}, {"mux": 27, "channel": 7, "position": 0, "level": "A"}, {"mux": 27, "channel": 8, "position": 0, "level": "A"}, {"mux": 27, "channel": 9, "position": 0, "level": "A"}, {"mux": 27, "channel": 10, "position": 0, "level": "A"}, {"mux": 27, "channel": 11, "position": 0, "level": "A"}, {"mux": 27, "channel": 12, "position": 0, "level": "A"}]}
    
    def __init__(self):
        super(LocalServer, self).__init__()
        self.prefix = "CONCRETE"
        self.pvdb = ""
    
    def run(self):
        server = SimpleServer()
        server.createPV(self.prefix, self.pvdb)
        while True:
            server.process(0.1)
        
class MyDriver(Driver):
    
    def __init__(self):
        super(MyDriver, self).__init__()
        
    def updateData(self):
        self.setParam("PV", "value")
        self.updatePvs()