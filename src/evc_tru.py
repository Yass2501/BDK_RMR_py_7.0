import os
import decode_raw_data
import datetime
import time
import bit_bytes_manipulation
from global_variables import *

################################################## Classes ##################################################

class DRU_Message(object):

    def __init__(self,obu_data_bin,obu_data_hex):
        self.obu_data_bin = obu_data_bin
        self.obu_data_hex = obu_data_hex
        
    def DRU_decode(self):
        self.L_MESSAGE = int(self.obu_data_bin[8:24],2)
        self.DATE = self.obu_data_bin[24:40]
        self.TIME = self.obu_data_bin[40:62]
        self.DRU_NID_PACKET = int(self.obu_data_bin[64:72],2)
        self.DRU_L_PACKET   = int(self.obu_data_bin[72:88],2)
        self.DRU_NID_SOURCE = int(self.obu_data_bin[88:96],2)
        self.DRU_NID_DATA = ''
        self.DRU_L_DATA = ''
        self.DRU_Q_TEXTCLASS = ''
        self.DRU_Q_TEXTCCONFIRM = ''
        self.DRU_Q_TEXT = ''
        self.DRU_L_TEXT = ''
        self.DRU_X_TEXT = ''
        self.DRU_M_DIAG = ''
        self.DRU_NID_CHANNEL = ''
        self.DRU_N_ITER = 0
        if self.DRU_NID_PACKET == 1:
            self.DRU_M_DIAG = int(self.obu_data_bin[96:108],2)
            self.DRU_NID_CHANNEL = int(self.obu_data_bin[108:112],2)
            self.DRU_L_TEXT = int(self.obu_data_bin[112:120],2)
            if(self.DRU_L_TEXT != 0):
                dru_x_text = bytes.fromhex(self.obu_data_hex[30:])
                self.DRU_X_TEXT = dru_x_text.decode("latin-1")
            else:
                self.DRU_X_TEXT = ''
        elif self.DRU_NID_PACKET == 5:
            self.DRU_N_ITER = int(self.obu_data_bin[96:104],2)
            index = 104
            index_hex = 26
            DRU_L_DATA = []
            DRU_L_TEXT = []
            for i in range(0,self.DRU_N_ITER):
                self.DRU_NID_DATA = self.DRU_NID_DATA +str(int(self.obu_data_bin[(index):(index+8)],2)) + ' | '
                DRU_L_DATA.append(int(self.obu_data_bin[(index+8):(index+16)],2))
                self.DRU_Q_TEXTCLASS = self.DRU_Q_TEXTCLASS + str(int(self.obu_data_bin[(index+2*8):(index+3*8)],2))+ ' | '
                self.DRU_Q_TEXTCCONFIRM = self.DRU_Q_TEXTCCONFIRM + str(int(self.obu_data_bin[(index+3*8):(index+4*8)],2))+ ' | '
                self.DRU_Q_TEXT = self.DRU_Q_TEXT + str(int(self.obu_data_bin[(index+4*8):(index+5*8)],2))+ ' | '
                DRU_L_TEXT.append(int(self.obu_data_bin[(index+5*8):(index+6*8)],2))
                if(DRU_L_TEXT[i] != 0):
                    dru_x_text = bytes.fromhex(self.obu_data_hex[(index_hex+12):(index_hex+12+2*DRU_L_TEXT[i])])
                    self.DRU_X_TEXT = self.DRU_X_TEXT + str(dru_x_text.decode("latin-1")) + ' | '
                else:
                    self.DRU_X_TEXT = self.DRU_X_TEXT + ''
                index     = index + DRU_L_DATA[i]*8 + 16
                index_hex = index_hex + DRU_L_DATA[i]*2 + 4
            self.DRU_L_TEXT = DRU_L_TEXT
            self.DRU_L_DATA = DRU_L_DATA
    
    def dru_date_from_bin(self,binary_date):
        YEAR = int(binary_date[0:7], 2)
        MOUNTH = int(binary_date[7:11], 2)
        DAY = int(binary_date[11:16], 2)
        if(YEAR <= 99 and MOUNTH <= 12 and MOUNTH <= 31):
            d = datetime.date(2000+YEAR, MOUNTH, DAY)
            return d.strftime('%Y-%m-%d')
        else:
            return None

    def dru_time_from_bin(self,binary_time):
        HOUR = int(binary_time[0:5],2)
        MINUTES = int(binary_time[5:11],2)
        SECONDS = int(binary_time[11:17],2)
        TTS = int(binary_time[17:22],2)
        second_float = float(SECONDS) + float(TTS)/1000.0
        if(HOUR <= 23 and MINUTES <= 59 and SECONDS <= 59 and TTS <= 950):
            t = datetime.time(hour=HOUR, minute=MINUTES, second=SECONDS, microsecond=1000*TTS)
            return t.strftime('%H:%M:%S.%f')[:-3]
        else:
            return None


class JRU_Message2(object):

    def __init__(self, obu_data_bin, obu_data_hex):
        self.obu_data_bin = obu_data_bin
        self.obu_data_hex = obu_data_hex

    def JRU_decode(self):
        self.L_MESSAGE = int(self.obu_data_bin[8:24], 2)
        self.DATE = self.obu_data_bin[24:40]
        self.TIME = self.obu_data_bin[40:62]
        self.DRU_NID_PACKET = int(self.obu_data_bin[64:72], 2)
        self.DRU_L_PACKET = int(self.obu_data_bin[72:88], 2)
        self.DRU_NID_SOURCE = int(self.obu_data_bin[88:96], 2)
        self.DRU_NID_DATA = ''
        self.DRU_L_DATA = ''
        self.DRU_Q_TEXTCLASS = ''
        self.DRU_Q_TEXTCCONFIRM = ''
        self.DRU_Q_TEXT = ''
        self.DRU_L_TEXT = ''
        self.DRU_X_TEXT = ''
        self.DRU_M_DIAG = ''
        self.DRU_NID_CHANNEL = ''
        self.DRU_N_ITER = 0
        if self.DRU_NID_PACKET == 1:
            self.DRU_M_DIAG = int(self.obu_data_bin[96:108], 2)
            self.DRU_NID_CHANNEL = int(self.obu_data_bin[108:112], 2)
            self.DRU_L_TEXT = int(self.obu_data_bin[112:120], 2)
            if (self.DRU_L_TEXT != 0):
                dru_x_text = bytes.fromhex(self.obu_data_hex[30:])
                self.DRU_X_TEXT = dru_x_text.decode("latin-1")
            else:
                self.DRU_X_TEXT = ''
        elif self.DRU_NID_PACKET == 5:
            self.DRU_N_ITER = int(self.obu_data_bin[96:104], 2)
            index = 104
            index_hex = 26
            DRU_L_DATA = []
            DRU_L_TEXT = []
            for i in range(0, self.DRU_N_ITER):
                self.DRU_NID_DATA = self.DRU_NID_DATA + str(int(self.obu_data_bin[(index):(index + 8)], 2)) + ' | '
                DRU_L_DATA.append(int(self.obu_data_bin[(index + 8):(index + 16)], 2))
                self.DRU_Q_TEXTCLASS = self.DRU_Q_TEXTCLASS + str(
                    int(self.obu_data_bin[(index + 2 * 8):(index + 3 * 8)], 2)) + ' | '
                self.DRU_Q_TEXTCCONFIRM = self.DRU_Q_TEXTCCONFIRM + str(
                    int(self.obu_data_bin[(index + 3 * 8):(index + 4 * 8)], 2)) + ' | '
                self.DRU_Q_TEXT = self.DRU_Q_TEXT + str(
                    int(self.obu_data_bin[(index + 4 * 8):(index + 5 * 8)], 2)) + ' | '
                DRU_L_TEXT.append(int(self.obu_data_bin[(index + 5 * 8):(index + 6 * 8)], 2))
                if (DRU_L_TEXT[i] != 0):
                    dru_x_text = bytes.fromhex(self.obu_data_hex[(index_hex + 12):(index_hex + 12 + 2 * DRU_L_TEXT[i])])
                    self.DRU_X_TEXT = self.DRU_X_TEXT + str(dru_x_text.decode("latin-1")) + ' | '
                else:
                    self.DRU_X_TEXT = self.DRU_X_TEXT + ''
                index = index + DRU_L_DATA[i] * 8 + 16
                index_hex = index_hex + DRU_L_DATA[i] * 2 + 4
            self.DRU_L_TEXT = DRU_L_TEXT
            self.DRU_L_DATA = DRU_L_DATA

    def jru_date_from_bin(binary_date):
        YEAR = int(binary_date[0:7], 2)
        MOUNTH = int(binary_date[7:11], 2)
        DAY = int(binary_date[11:16], 2)
        if (YEAR <= 99 and MOUNTH <= 12 and MOUNTH <= 31):
            d = datetime.date(2000 + YEAR, MOUNTH, DAY)
            return d.strftime('%Y-%m-%d')
        else:
            return None

    def jru_time_from_bin(binary_date):
        HOUR = int(binary_date[0:5], 2)
        MINUTES = int(binary_date[5:11], 2)
        SECONDS = int(binary_date[11:17], 2)
        TTS = int(binary_date[17:22], 2)
        second_float = float(SECONDS) + float(TTS) / 1000.0
        if (HOUR <= 23 and MINUTES <= 59 and SECONDS <= 59 and TTS <= 950):
            t = datetime.time(hour=HOUR, minute=MINUTES, second=SECONDS, microsecond=1000 * TTS)
            return t.strftime('%H:%M:%S.%f')[:-3]
        else:
            return None


        


class JRU_Message(object):

    def __init__(self, NID_MESSAGE, L_MESSAGE, DATE, TIME, Q_SCALE, NID_LRBG,\
                 D_LRBG, Q_DIRLRBG, Q_DLRBG, L_DOUBTOVER,\
                 L_DOUBTUNDER, V_TRAIN, DRIVER_ID, NID_ENGINE,\
                 SYSTEM_VERSION, LEVEL, MODE, PACKET_VARIABLES):
        
        self.NID_MESSAGE = NID_MESSAGE
        self.L_MESSAGE = L_MESSAGE
        self.DATE = DATE
        self.TIME = TIME
        self.Q_SCALE = Q_SCALE
        self.NID_LRBG = NID_LRBG
        self.D_LRBG = D_LRBG
        self.Q_DIRLRBG = Q_DIRLRBG
        self.Q_DLRBG = Q_DLRBG
        self.L_DOUBTOVER = L_DOUBTOVER
        self.L_DOUBTUNDER = L_DOUBTUNDER
        self.V_TRAIN = V_TRAIN
        self.DRIVER_ID = DRIVER_ID
        self.NID_ENGINE = NID_ENGINE
        self.SYSTEM_VERSION = SYSTEM_VERSION
        self.LEVEL = LEVEL
        self.MODE = MODE
        self.PACKET_VARIABLES = PACKET_VARIABLES
        

################################################## Functions ##################################################




def jru_date_from_bin(binary_date):
    YEAR = int(binary_date[0:7],2)
    MOUNTH = int(binary_date[7:11],2)
    DAY = int(binary_date[11:16],2)
    if(YEAR <= 99 and MOUNTH <= 12 and MOUNTH <= 31):
        d = datetime.date(2000+YEAR, MOUNTH, DAY)
        return d.strftime('%Y-%m-%d')
    else:
        return None

def jru_time_from_bin(binary_date):
    HOUR = int(binary_date[0:5],2)
    MINUTES = int(binary_date[5:11],2)
    SECONDS = int(binary_date[11:17],2)
    TTS = int(binary_date[17:22],2)
    second_float = float(SECONDS) + float(TTS)/1000.0
    if(HOUR <= 23 and MINUTES <= 59 and SECONDS <= 59 and TTS <= 950):
        t = datetime.time(hour=HOUR, minute=MINUTES, second=SECONDS, microsecond=1000*TTS)
        return t.strftime('%H:%M:%S.%f')[:-3]
    else:
        return None






