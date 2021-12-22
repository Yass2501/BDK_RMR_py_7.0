from os import listdir
import functions
import datetime
from global_variables import *
import xml.etree.ElementTree as ET

class RMR_Message(object):
    time_for_sort = 0
    date_for_sort = 0
    double_check = 0

    def __init__(self, OBU_LEN,OBU_VER,OBU_ID,OBU_ACK,OBU_GPS,OBU_DATA_TYPE, \
                OBU_CUSTOM,OBU_DATA_LEN,OBU_DATA):

        self.OBU_LEN = OBU_LEN
        self.OBU_VER = OBU_VER
        self.OBU_ID = OBU_ID
        self.OBU_ACK = OBU_ACK
        self.OBU_GPS = OBU_GPS
        self.OBU_DATA_TYPE = OBU_DATA_TYPE
        self.OBU_CUSTOM = OBU_CUSTOM
        self.OBU_DATA_LEN = OBU_DATA_LEN
        self.OBU_DATA = OBU_DATA

    def date_time_pretty(self):
        date_time = ''
        gps_field = self.decode_GPS()
        TIME = gps_field[GPS_TIME]
        DATE = gps_field[GPS_DATE]
        date_time_tmp = datetime.datetime(2000+int(DATE[4:6]),int(DATE[2:4]),int(DATE[0:2]),int(TIME[0:2]),int(TIME[2:4]),int(TIME[4:6]))
        date_time = date_time_tmp.strftime('%d-%m-%Y  %H:%M:%S')
        #print(date_time.strftime('%d-%m-%Y  %H:%M:%S'))
        return date_time

    def date_pretty(self):
        date = ''
        gps_field = self.decode_GPS()
        DATE = gps_field[GPS_DATE]
        date_tmp = datetime.date(2000+int(DATE[4:6]),int(DATE[2:4]),int(DATE[0:2]))
        date = date_tmp.strftime('%d-%m-%Y')
        return date

    def time_pretty(self):
        time = ''
        gps_field = self.decode_GPS()
        TIME = gps_field[GPS_TIME]
        time_tmp = datetime.time(int(TIME[0:2]),int(TIME[2:4]),int(TIME[4:6]))
        time = time_tmp.strftime('%H:%M:%S')
        #print(date_time.strftime('%d-%m-%Y  %H:%M:%S'))
        return time

    def decode_GPS(self):
        
        Index = functions.findIndexof(self.OBU_GPS,',', 9)
        gps_field = functions.arrayAllocate('',10)
        
        gps_field[GPS_VALIDITY] = self.OBU_GPS[0:Index[0]]
        gps_field[GPS_TIME] = self.OBU_GPS[Index[0]+1:Index[1]]
        gps_field[GPS_DATE] = self.OBU_GPS[Index[1]+1:Index[2]]
        gps_field[GPS_LATITUDE] = self.OBU_GPS[Index[2]+1:Index[3]]
        gps_field[GPS_LONGITUDE] = self.OBU_GPS[Index[3]+1:Index[4]]
        gps_field[GPS_ALTITUDE] = self.OBU_GPS[Index[4]+1:Index[5]]
        gps_field[GPS_HDOP_STATUS] = self.OBU_GPS[Index[5]+1:Index[6]]
        gps_field[GPS_SPEED] = self.OBU_GPS[Index[6]+1:Index[7]]
        gps_field[GPS_DIRECTION] = self.OBU_GPS[Index[7]+1:Index[8]]
        gps_field[GPS_SATELLITE_NB] = self.OBU_GPS[Index[8]+1:(len(self.OBU_GPS)-1)]
        
        return gps_field

    def longitude_map(self):
        gps_field = self.decode_GPS()
        long_maps = ''
        long  = gps_field[GPS_LONGITUDE]
        if(len(long)>0):
            #long_maps = float(long[:-1])
            long_maps = float(long[0]+long[1]+long[2])+float(long[3:len(long)-1])/60
        else:
            long_maps = ''
        return long_maps

    def latitude_map(self):
        gps_field = self.decode_GPS()
        lat_maps = ''
        lat  = gps_field[GPS_LATITUDE]
        if(len(lat)>0):
            #lat_maps = float(lat[:-1])
            lat_maps = float(lat[0]+lat[1])+float(lat[2:len(lat)-1])/60
        else:
            lat_maps = ''
        return lat_maps
        
        
        
        
    def print(self):

        print('=================================================')
        print('OBU Length : ',self.OBU_LEN)
        print('OBU Version : '+self.OBU_VER)
        print('OBU ID : '+self.OBU_ID)
        print('OBU Ack : '+self.OBU_ACK)
        print('OBU GPS : '+self.OBU_GPS)
        print('OBU Data type : '+self.OBU_DATA_TYPE)
        print('OBU Cust : '+self.OBU_CUSTOM)
        print('OBU data length : ',self.OBU_DATA_LEN)
        print('OBU data : ',self.OBU_DATA)
        print('=================================================')

    def name_frome_ID(self,Id_name_strings):
        i = 0
        Name = ''
        for line in Id_name_strings:
            Id = line[0:line.find('\t')]
            Name = line[line.find('\t')+1:len(line)-1]
            if(Id==self.OBU_ID):
                break
        return Name


############################ Functions ############################

	


def extract_and_decode_rawData2(param_file_path):

    ########################## Loading parameters from XML ##########################

    myTreeMapObu = ET.parse(TrainsMapPath)
    myTreeParam  = ET.parse(param_file_path)
    myRootParam  = myTreeParam.getroot()
    myRootMapObu = myTreeMapObu.getroot()
    print(myRootMapObu.text)
    Raw_data_decoded = []
    train_names = []
    obu_ids = []
    period = []
    analysis = []
    trains_tag = myRootParam.find('Trains')
    period_tag = myRootParam.find('Period')
    date_tag = period_tag.find('DATE')
    analysis_tag = myRootParam.find('Analysis')
    for x in trains_tag.findall('OBU'):
        if x.get('obu_name') == 'all':
            obu_ids.append('all')
            train_names.append('all')
            break
        else:
            train_names.append(x.get('obu_name'))
            for y in myRootMapObu.findall('OBU'):
                name = y.get('obu_name')
                if name == x.get('obu_name'):
                    obu_ids.append(y.get('obu_id'))
    for x in trains_tag.findall('FLEET'):
        if x.get('obu_fleet') == 'all':
            obu_ids.append('all')
            train_names.append('all')
            break
        else:
            for y in myRootMapObu.findall('OBU'):
                name = y.get('obu_name')
                if x.get('obu_fleet') in name:
                    print(name, y.get('obu_id'))
                    train_names.append(name)
                    obu_ids.append(y.get('obu_id'))
    for x in analysis_tag.findall('LOG'):
        analysis.append(x.get('type'))
    print(analysis)
    period1 = date_tag.get('t0')
    period2 = date_tag.get('tend')

    period.append(datetime.date(int(period1[6:]), int(period1[3:5]), int(period1[0:2])))
    period.append(datetime.date(int(period2[6:]), int(period2[3:5]), int(period2[0:2])))

    #################################################################################

    #print(obu_ids, train_names)
    date1_int = int(period[0].strftime('%y%m%d'))
    date2_int = int(period[1].strftime('%y%m%d'))

    Raw_data_decoded = []
    i_rmr_mess = 0
    index_G1 = 0
    index_G1_end = 0

    listfiles = listdir('../inputs/Raw_Data')

    for filename in listfiles:
        #filename_date = filename[2:4] + filename[5:7] + filename[8:10]
        #print(filename_date)
        filename_date = "".join([filename[2:4] , filename[5:7], filename[8:10]])
        #print(filename_date)
        filename_date_int = int(filename_date)
        if date1_int <= filename_date_int < date2_int:
            print('File name : ' + filename)
            #f = open('../inputs/Raw_Data' + '/' + filename, 'r+', encoding='latin-1')
            f = open("".join(['../inputs/Raw_Data' , '/', filename]), 'r+', encoding='latin-1')
            lines = f.readlines()
            for i in range(0, len(lines)):
                if lines[i].find('<G1>') != -1:
                    k = i
                    data_str = lines[i]
                    while lines[k].find('</G1>') == -1:
                        k = k + 1
                        #data_str = data_str + lines[k]
                        data_str = "".join([data_str ,lines[k]])
                    index_G1 = data_str.find('<G1>')
                    index_G1_end = data_str.find('</G1>') + 5
                    Index = functions.findIndexof(data_str, ';', 8)

                    OBU_LEN = str(int((data_str[(index_G1 + 4):(Index[0])]).encode().hex(), 16))
                    OBU_VER = data_str[(Index[0] + 1):Index[1]]
                    OBU_ID = data_str[(Index[1] + 1):Index[2]]
                    OBU_ACK = data_str[(Index[2] + 1):Index[3]]
                    OBU_GPS = data_str[(Index[3] + 1):Index[4]]
                    OBU_DATA_TYPE = data_str[(Index[4] + 1):Index[5]]
                    OBU_CUSTOM = data_str[(Index[5] + 1):Index[6]]
                    OBU_DATA_LEN = data_str[(Index[6] + 1):Index[7]]
                    OBU_DATA = data_str[(Index[7] + 1):index_G1_end - 5]

                    flag = 0

                    for an in analysis:
                        if an == 'COMET_INIT' and OBU_DATA_TYPE == '14':
                            flag = 1
                            break
                        elif an == 'JRU' and OBU_DATA_TYPE == '2':
                            obu_data_hex = OBU_DATA.encode('latin-1').hex()
                            tru_nid_message = obu_data_hex[0:2]
                            if tru_nid_message == '00':
                                flag = 1
                                break
                        elif an == 'DRU' and OBU_DATA_TYPE == '2':
                            obu_data_hex = OBU_DATA.encode('latin-1').hex()
                            tru_nid_message = obu_data_hex[0:2]
                            if tru_nid_message == '09':
                                flag = 1
                                break
                        elif an == 'RMR_PERIODIC' and OBU_DATA_TYPE == '16':
                            flag = 1
                            break
                    if flag:
                        for id in obu_ids:
                            if id == OBU_ID or id == 'all':
                                obu_data_hex = OBU_DATA.encode('latin-1').hex()
                                Raw_data_decoded.append(
                                    RMR_Message(OBU_LEN, OBU_VER, OBU_ID, OBU_ACK, OBU_GPS, OBU_DATA_TYPE, OBU_CUSTOM,
                                                OBU_DATA_LEN, OBU_DATA))
                                gps_field = Raw_data_decoded[i_rmr_mess].decode_GPS()
                                Raw_data_decoded[i_rmr_mess].date_for_sort = functions.dateStringToIntConvert(
                                    gps_field[GPS_DATE])
                                obu_time = gps_field[GPS_TIME]
                                Raw_data_decoded[i_rmr_mess].time_for_sort = int(obu_time[0:6])
                                # Raw_data_decoded[i_rmr_mess].print()
                                i_rmr_mess = i_rmr_mess + 1
                                break
            f.close()

    return Raw_data_decoded

def OBU_ID_FROM_OBU_NAME(obu_name):
    obu_id = ''
    for i in range(len(OBU_NAME_ALL)):
        if(obu_name == OBU_NAME_ALL[i]):
            obu_id = OBU_ID_ALL[i]
            break
    return obu_id

def OBU_NAME_FROM_OBU_ID(obu_id):
    obu_name = ''
    for i in range(len(OBU_ID_ALL)):
        if(obu_id == OBU_ID_ALL[i]):
            obu_name = OBU_NAME_ALL[i]
            break
    return obu_name  
