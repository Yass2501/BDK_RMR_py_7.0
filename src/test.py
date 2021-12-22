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
import matplotlib.pyplot as plt
import random
################################################## Inputs ##################################################

if __name__ == '__main__':
    
    a = datetime.datetime.now()
    param_file_path = '../config.ini.xml'
    RMR_Messages = decode_raw_data.extract_and_decode_rawData_MM(param_file_path)
    RMR_Messages_sorted = sorted(RMR_Messages, key=lambda x: (x.date_for_sort, x.time_for_sort))
    del RMR_Messages

    M_DIAG = 421
    Train = 'DSB MQ 4128'
    Trains = ['DSB MQ 4128', 'DSB IC3 5040', 'DSB ABs 7905', 'NJ LINT41 642 672']
    d0 = datetime.date(2021,11,10)
    period = 3
    nPeriod = 5
    p =  []
    pint = []
    name = []
    for i in range(0,nPeriod):
        tmp = [d0,d0 + datetime.timedelta(days=period)]
        tmpint = [int(tmp[0].strftime('%y%m%d')), int(tmp[1].strftime('%y%m%d'))]
        p.append(tmp)
        pint.append(tmpint)
        d0 = d0 + datetime.timedelta(days=period)
        name.append('P'+str(i+1))
    Y = []
    Z = []
    plt.figure()
    for tt in Trains:
        print(tt)
        z = []
        for pp in pint:
            cnt = 0
            print(pp)
            for m in RMR_Messages_sorted:
                if (m.OBU_DATA_TYPE == '2'):
                    obu_data_hex = m.OBU_DATA.encode('latin-1').hex()
                    TRU_NID_MESSAGE = obu_data_hex[0:2]
                    if TRU_NID_MESSAGE == '09':
                        obu_data_bin = bit.hexToBin_loop(obu_data_hex)
                        DRU_Mess = evc_tru.DRU_Message(obu_data_bin, obu_data_hex)
                        DRU_Mess.DRU_decode()
                        date = DRU_Mess.dru_date_from_bin(DRU_Mess.DATE)
                        date_int = int(date[2:4]+date[5:7]+date[8:])
                        train_id = decode_raw_data.OBU_ID_FROM_OBU_NAME(tt)
                        if((pp[0] <= date_int < pp[1]) and (m.OBU_ID == train_id) and (DRU_Mess.DRU_M_DIAG == M_DIAG)):
                            cnt = cnt + 1
            #Y.append(cnt)
            z.append(cnt)
        Z.append(z)
        rgb = (random.random(), random.random(), random.random())
        plt.plot(name,z,'.-',c=rgb, label=tt)
        plt.xticks(range(len(name)), name, rotation='vertical')
        plt.legend()
    ymax = max(max(Z))
    plt.ylim(0, ymax*(1.1))
    plt.grid(True)
    b = datetime.datetime.now()
    print("Time spent: ",b-a)
    plt.show()
    
    
    

    
