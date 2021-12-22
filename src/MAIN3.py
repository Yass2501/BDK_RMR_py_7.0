import decode_raw_data   
import datetime
import time
import xlsxwriter
import evc_tru
import comet_init
import bit_bytes_manipulation as bit
import write_excel
import xml.etree.ElementTree as ET
import cProfile
import matplotlib.pyplot as plt
################################################## Inputs ##################################################

if __name__ == '__main__':
    param_file_path = '../config.ini.xml'
    a = datetime.datetime.now()
    #RMR_Messages = decode_raw_data.extract_and_decode_rawData2(param_file_path)
    cProfile.run("RMR_Messages = decode_raw_data.extract_and_decode_rawData2(param_file_path)")
    b = datetime.datetime.now()
    RMR_Messages_sorted = sorted(RMR_Messages, key=lambda x: (x.date_for_sort, x.time_for_sort))
    print("Time spent: ",b-a)
    
    del RMR_Messages
    print("Time spent: ",b-a)
    print('number of RMR_Messages_sorted: '+str(len(RMR_Messages_sorted)))

    

    myTreeParam  = ET.parse(param_file_path)
    myTreeTXT_MESS = ET.parse('../inputs/EVC_TXT_MESSAGES_CODES.xml')
    myTreeMM_ID_MAP = ET.parse('../inputs/MM_ID_MAP.xml')
    myRootParam  = myTreeParam.getroot()
    myRootTXT_MESS = myTreeTXT_MESS.getroot()
    myRootMM_ID_MAP = myTreeMM_ID_MAP.getroot()

    trains_tag = myRootParam.find('Trains')
    period_tag = myRootParam.find('Period')
    MM_tag = myRootParam.find('Maintenance_Manager')
    text_tag = myRootParam.find('Text_Message')
    date_tag = period_tag.find('DATE')
    analysis_tag = myRootParam.find('Analysis')
    mm_tag = MM_tag.find('MM')

    ACTIVATE_logs = (analysis_tag.find('ACTIVATE')).get('value')
    ACTIVATE_mm = (MM_tag.find('ACTIVATE')).get('value')
    ACTIVATE_txt = (text_tag.find('ACTIVATE')).get('value')

    if(ACTIVATE_logs == 'True'):
        print('kk*--------------------')
        current_time = datetime.datetime.now()
        current_time_string = current_time.strftime("%y%m%d %H%M%S")
        output_report_path = '../outputs/reports/LOGS_RMR_' + current_time_string[0:6] + '_' + current_time_string[
                                                                                           7:] + '.xlsx'
        workbook = xlsxwriter.Workbook(output_report_path)
        for x in analysis_tag.findall('LOG'):
            if x.get('type') == 'JRU':
                worksheet_jru = workbook.add_worksheet('JRU Messages')
                write_excel.write_JRU_Messages(workbook, worksheet_jru, RMR_Messages_sorted)
            elif x.get('type') == 'DRU':
                worksheet_dru = workbook.add_worksheet('DRU Messages')
                write_excel.write_DRU_Messages(workbook, worksheet_dru, RMR_Messages_sorted)
            elif x.get('type') == 'COMET_INIT':
                worksheet_comet_init = workbook.add_worksheet('COMET_INIT Messages')
                write_excel.write_COMET_INIT_Messages(workbook, worksheet_comet_init, RMR_Messages_sorted)
        workbook.close()
    if(ACTIVATE_mm == 'True'):
        LLRU = mm_tag.get('LLRU')
        STATE = mm_tag.get('state')
        LLRU_ID = None
        LLRU_STATE = None
        period = []
        Trains = []
        if(STATE == 'OK'):
            LLRU_STATE = 0
        elif(STATE == 'WARNING'):
            LLRU_STATE = 1
        elif(STATE == 'DEFECT'):
            LLRU_STATE = 2
        elif(STATE == 'BLOCKING'):
            LLRU_STATE = 3
        
        for map in myRootMM_ID_MAP.findall('LLRU'):
            if(LLRU == map.get('name')):
                LLRU_ID = int(map.get('id'))
                break
        for x in trains_tag.findall('OBU'):
            if x.get('obu_name') == 'all':
                Trains.append('all')
                break
            else:
                Trains.append(x.get('obu_name'))
        M_DIAG = LLRU_ID+(160 * LLRU_STATE)

        print(LLRU_ID, LLRU_STATE, M_DIAG)
        period1 = date_tag.get('t0')
        period2 = date_tag.get('tend')
        
        period.append(datetime.date(int(period1[6:]), int(period1[3:5]), int(period1[0:2])))
        period.append(datetime.date(int(period2[6:]), int(period2[3:5]), int(period2[0:2])))
        
        print(Trains)
        print(period)
        print(LLRU,STATE,M_DIAG)
        name = []
        pp = [int(period[0].strftime('%y%m%d')), int(period[1].strftime('%y%m%d'))]
        print(pp)
        Z = []
        plt.figure()
        for tt in Trains:
            print(tt)
            cnt = 0
            for m in RMR_Messages_sorted:
                if (m.OBU_DATA_TYPE == '2'):
                    obu_data_hex = m.OBU_DATA.encode('latin-1').hex()
                    TRU_NID_MESSAGE = obu_data_hex[0:2]
                    if TRU_NID_MESSAGE == '09':
                        obu_data_bin = bit.hexToBin_loop(obu_data_hex)
                        DRU_Mess = evc_tru.DRU_Message(obu_data_bin, obu_data_hex)
                        DRU_Mess.DRU_decode()
                        if((DRU_Mess.DRU_NID_PACKET == 1) and (DRU_Mess.DRU_NID_SOURCE == 7)):
                            date = DRU_Mess.dru_date_from_bin(DRU_Mess.DATE)
                            date_int = int(date[2:4]+date[5:7]+date[8:])
                            train_id = decode_raw_data.OBU_ID_FROM_OBU_NAME(tt)
                            if((pp[0] <= date_int < pp[1]) and (m.OBU_ID == train_id) and (DRU_Mess.DRU_M_DIAG == M_DIAG)):
                                cnt = cnt + 1
            #Y.append(cnt)
            Z.append(cnt)
        b = datetime.datetime.now()
        print("Time spent: ",b-a)
        print(Z)
        plt.bar(Trains,Z)
        plt.ylabel('Occurences')
        plt.title(LLRU+' '+STATE+'\n'+'Period: '+period[0].strftime('%d-%m-%y')+' -- '+period[1].strftime('%d-%m-%y'))
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.24)
        plt.savefig('../outputs/plots/'+LLRU+'_'+STATE+'_plots.jpg')
        plt.show()
        


















        
