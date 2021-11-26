import decode_raw_data   
import datetime
import time
import xlsxwriter
import evc_tru
import comet_init
import rmr_periodic
import bit_bytes_manipulation as bit
import write_excel
import xml.etree.ElementTree as ET
################################################## Inputs ##################################################

if __name__ == '__main__':
    param_file_path = '../config.ini.xml'
    RMR_Messages = decode_raw_data.extract_and_decode_rawData2(param_file_path)
    RMR_Messages_sorted = sorted(RMR_Messages, key=lambda x: (x.date_for_sort, x.time_for_sort))
    del RMR_Messages

    for m in RMR_Messages_sorted:
        if (m.OBU_DATA_TYPE == '16'):
            obu_data_hex = m.OBU_DATA.encode('latin-1').hex()
            obu_data_bin = bit.hexToBin_loop(obu_data_hex)
            RMR_PERIODIC_Mess = rmr_periodic.RMR_PERIODIC_Message(obu_data_bin,obu_data_hex)
            RMR_PERIODIC_Mess.RMR_PERIODIC_decode()
            print(RMR_PERIODIC_Mess.V_TRAIN,'------',m.date_time_pretty())

    
