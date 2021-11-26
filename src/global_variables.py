# GPS field names
GPS_VALIDITY     = 0
GPS_TIME         = 1
GPS_DATE         = 2
GPS_LATITUDE     = 3
GPS_LONGITUDE    = 4
GPS_ALTITUDE     = 5
GPS_HDOP_STATUS  = 6
GPS_SPEED        = 7
GPS_DIRECTION    = 8
GPS_SATELLITE_NB = 9

# Maintenance Manager states
OK = 0
WARNING = 1
DEFECT = 2
BLOCKING_DEFECT = 3

# Train <--> IDs mapping
OBU_ID_ALL = []
OBU_NAME_ALL = []
with open("../inputs/ID_TRAINS_MAPPING.xml") as Fleet_map:
    Fleet = Fleet_map.readlines()
    for row in Fleet :
        if "OBU" in row :
            tmp = row.split('"')
            OBU_NAME_ALL.append(tmp[3])
            OBU_ID_ALL.append(tmp[1])
    Fleet_map.close()

# EVC TEXT MESSAGES
TXT_MESS_ALL = []
TXT_CODE_ALL = []
with open("../inputs/EVC_TXT_MESSAGES_CODES.xml") as Txt_list:
    Text_mess = Txt_list.readlines()
    for row in Text_mess :
        if "TXT_MESS" in row :
            tmp = row.split('"')
            TXT_MESS_ALL.append(tmp[3])
            TXT_CODE_ALL.append(int(tmp[1]))
            #print(tmp)
    Txt_list.close()
#print(TXT_MESS_ALL)
import xlrd
filename_path = '../inputs/MM_ID_Map.xls'
wb = xlrd.open_workbook(filename_path)
sheet = wb.sheet_by_index(0)
N = 61
ID_LLRU_Map = []
for i in range (1,N):
    ID = int(sheet.cell_value(i,0))
    LLRU = str(sheet.cell_value(i,1))
    ID_LLRU_Map.append([ID,LLRU])
    #print(ID_LLRU_Map[i-1])

#print(ID_LLRU_Map)

TrainsMapPath = '../inputs/ID_TRAINS_MAPPING.xml'

