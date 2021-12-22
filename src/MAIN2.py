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
################################################## Inputs ##################################################

if __name__ == '__main__':
    param_file_path = '../config.ini.xml'
    a = datetime.datetime.now()
    RMR_Messages = decode_raw_data.extract_and_decode_rawData2(param_file_path)
    #cProfile.run("RMR_Messages = decode_raw_data.extract_and_decode_rawData2(param_file_path)")
    b = datetime.datetime.now()
    RMR_Messages_sorted = sorted(RMR_Messages, key=lambda x: (x.date_for_sort, x.time_for_sort))
    print("Time spent: ",b-a)
    
    del RMR_Messages
    print("Time spent: ",b-a)
    print('number of RMR_Messages_sorted: '+str(len(RMR_Messages_sorted)))

    current_time = datetime.datetime.now()
    current_time_string = current_time.strftime("%y%m%d %H%M%S")
    output_report_path = '../outputs/reports/LOGS_RMR_' + current_time_string[0:6] + '_' + current_time_string[
                                                                                           7:] + '.xlsx'
    workbook = xlsxwriter.Workbook(output_report_path)

    myTreeParam = ET.parse(param_file_path)
    myRootParam = myTreeParam.getroot()
    analysis_tag = myRootParam.find('Analysis')
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
