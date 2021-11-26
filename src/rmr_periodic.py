import os
import decode_raw_data
import datetime
import time
import bit_bytes_manipulation
from global_variables import *

################################################## Classes ##################################################

class RMR_PERIODIC_Message(object):

    def __init__(self,obu_data_bin,obu_data_hex):
        self.obu_data_bin = obu_data_bin
        self.obu_data_hex = obu_data_hex
        
    def RMR_PERIODIC_decode(self):
        self.RMR_PERIODIC_VERSION = self.obu_data_bin[0:8]
        self.Q_SCALE = int(self.obu_data_bin[8:10],2)
        self.NID_LRBG = int(self.obu_data_bin[10:34],2)
        self.D_LRBG = int(self.obu_data_bin[34:49],2)
        self.Q_DIRLRBG = int(self.obu_data_bin[49:51],2)
        self.Q_DLRBG = int(self.obu_data_bin[51:53],2)
        self.L_DOUBTOVER = int(self.obu_data_bin[53:68],2)
        self.L_DOUBTUNDER = int(self.obu_data_bin[68:83],2)
        self.V_TRAIN = int(self.obu_data_bin[83:93],2)





        

################################################## Functions ##################################################





