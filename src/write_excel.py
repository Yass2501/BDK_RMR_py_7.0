import datetime
import evc_tru as tru
from global_variables import *
import decode_raw_data
import bit_bytes_manipulation as bit
import comet_init


def write_DRU_Messages(workbook, worksheet, RMR_Messages):

    Fields_DRU_2 = [['Train name', 20],
                    ['DATE (EVC)', 20],
                    ['TIME (EVC)', 20],
                    ['SOURCE', 20],
                    ['DRU_NID_CHANNEL', 20],
                    ['DRU_M_DIAG', 20],
                    ['DRU_Q_TEXT', 20],
                    ['DRU_X_TEXT', 20]]

    titles_format = workbook.add_format({'bold': True, 'align': 'center'})
    center_format = workbook.add_format({'align': 'center'})
    coord_format = workbook.add_format({'align': 'left'})
    bg_format1 = workbook.add_format({'bg_color': '#78B0DE'})  # blue cell background color
    bg_format2 = workbook.add_format({'bg_color': '#FFFFFF'})  # white cell background color
    j = 0
    for f in Fields_DRU_2:
        worksheet.set_column(0, j, f[1])
        worksheet.write(0, j, f[0], titles_format)
        j = j + 1
    cnt = 0
    i = 1
    Nmess = len(RMR_Messages)
    for m in RMR_Messages:
        if m.OBU_DATA_TYPE == '2':
            obu_data_hex = m.OBU_DATA.encode('latin-1').hex()
            TRU_NID_MESSAGE = obu_data_hex[0:2]
            if TRU_NID_MESSAGE == '09':
                if i % 2000 == 0:
                    print('DRU writing... '+str(i)+'/'+str(Nmess))
                obu_data_bin = bit.hexToBin_loop(obu_data_hex)
                DRU_Mess = tru.DRU_Message(obu_data_bin, obu_data_hex)
                DRU_Mess.DRU_decode()
                date = DRU_Mess.dru_date_from_bin(DRU_Mess.DATE)
                time = DRU_Mess.dru_time_from_bin(DRU_Mess.TIME)

                name = decode_raw_data.OBU_NAME_FROM_OBU_ID(m.OBU_ID)

                worksheet.write(i, 0, name, center_format)
                worksheet.write(i, 1, date, center_format)
                worksheet.write(i, 2, time, center_format)
                if DRU_Mess.DRU_NID_PACKET == 1:
                    if DRU_Mess.DRU_NID_SOURCE == 1:
                        worksheet.write(i, 3, 'EVC', center_format)
                    elif DRU_Mess.DRU_NID_SOURCE == 2:
                        worksheet.write(i, 3, 'EVC CORE', center_format)
                    elif DRU_Mess.DRU_NID_SOURCE == 3:
                        worksheet.write(i, 3, 'EVC TIU', center_format)
                    elif DRU_Mess.DRU_NID_SOURCE == 4:
                        worksheet.write(i, 3, 'DMI', center_format)
                    elif DRU_Mess.DRU_NID_SOURCE == 5:
                        worksheet.write(i, 3, 'EIRENE', center_format)
                    elif DRU_Mess.DRU_NID_SOURCE == 6:
                        worksheet.write(i, 3, 'TRU', center_format)
                    elif DRU_Mess.DRU_NID_SOURCE == 7:
                        worksheet.write(i, 3, 'EVC MM', center_format)
                elif DRU_Mess.DRU_NID_PACKET == 5 and DRU_Mess.DRU_NID_SOURCE == 1:
                    worksheet.write(i, 3, 'TEXT MESSAGES', center_format)
                worksheet.write(i, 4, DRU_Mess.DRU_NID_CHANNEL, center_format)
                worksheet.write(i, 5, DRU_Mess.DRU_M_DIAG, center_format)
                worksheet.write(i, 6, DRU_Mess.DRU_Q_TEXT[:-2], center_format)
                worksheet.write(i, 7, DRU_Mess.DRU_X_TEXT[:-2])
                i = i + 1
    worksheet.autofilter(0, 0, i - 1, len(Fields_DRU_2) - 1)
    worksheet.freeze_panes(1, 0)



def write_COMET_INIT_Messages(workbook, worksheet, RMR_Messages):
    fields_comet_init_names = []
    for k in range(0, 16):
        fields_comet_init_names.append(comet_init.comet_init_field_from_comet_init_id(k))
    Fields_COMET_INIT = ['Train name', 'DATE (GPS)', 'TIME (GPS)'] + [fields_comet_init_names[i] for i in
                                                                      range(len(fields_comet_init_names))]

    Fields_COMET_INIT_2 = [['Train name', 20],
                           ['DATE (GPS)', 20],
                           ['TIME (GPS)', 20],
                           ['COMET_TRAIN_OP_TIME', 20],
                           ['COMET_DMI1_OP_TIME', 20],
                           ['COMET_DMI2_OP_TIME', 20],
                           ['COMET_DMI3_OP_TIME', 20],
                           ['COMET_DMI4_OP_TIME', 20],
                           ['COMET_TRAIN_MVNT_TIME', 20],
                           ['COMET_KM_GPS', 20],
                           ['COMET_KM_ODO', 20],
                           ['COMET_EVC_TEST_DATE', 20],
                           ['COMET_EVC_TEST_STATUS', 20],
                           ['COMET_EVC_PRJ_VERSION_INCOHERENT', 30],
                           ['COMET_EVC_CUR_PRJ_VERSION', 20],
                           ['COMET_EVC_CUR_GATC_BASELINE', 20],
                           ['COMET_EVC_CUR_CONFIG_VERSION', 30],
                           ['FIFO', 30]]

    titles_format = workbook.add_format({'bold': True, 'align': 'center'})
    center_format = workbook.add_format({'align': 'center'})
    coord_format = workbook.add_format({'align': 'left'})

    j = 0
    for f in Fields_COMET_INIT_2:
        worksheet.write(0, j, f[0], titles_format)
        worksheet.set_column(0, j, f[1])
        j = j + 1
    cnt = 0
    i = 1
    Nmess = len(RMR_Messages)
    for m in RMR_Messages:
        if m.OBU_DATA_TYPE == '14':
            if (i % 2000 == 0):
                print('COMET INIT writing... '+str(i) + '/' + str(Nmess))
            COMET_INIT_Mess = comet_init.extract_comet_init_message(m)
            name = decode_raw_data.OBU_NAME_FROM_OBU_ID(m.OBU_ID)
            time = m.time_pretty()
            date = m.date_pretty()
            worksheet.write(i, 0, name, center_format)
            worksheet.write(i, 1, date, center_format)
            worksheet.write(i, 2, time, center_format)
            worksheet.write(i, 3, COMET_INIT_Mess.COMET_TRAIN_OP_TIME, center_format)
            worksheet.write(i, 4, COMET_INIT_Mess.COMET_DMI1_OP_TIME, center_format)
            worksheet.write(i, 5, COMET_INIT_Mess.COMET_DMI2_OP_TIME, center_format)
            worksheet.write(i, 6, COMET_INIT_Mess.COMET_DMI3_OP_TIME, center_format)
            worksheet.write(i, 7, COMET_INIT_Mess.COMET_DMI4_OP_TIME, center_format)
            worksheet.write(i, 8, COMET_INIT_Mess.COMET_TRAIN_MVNT_TIME, center_format)
            worksheet.write(i, 9, COMET_INIT_Mess.COMET_KM_GPS, center_format)
            worksheet.write(i, 10, COMET_INIT_Mess.COMET_KM_ODO, center_format)
            worksheet.write(i, 11, COMET_INIT_Mess.COMET_EVC_TEST_DATE, center_format)
            worksheet.write(i, 12, COMET_INIT_Mess.COMET_EVC_TEST_STATUS, center_format)
            worksheet.write(i, 13, COMET_INIT_Mess.COMET_EVC_PRJ_VERSION_INCOHERENT, center_format)
            worksheet.write(i, 14, COMET_INIT_Mess.COMET_EVC_CUR_PRJ_VERSION, center_format)
            worksheet.write(i, 15, COMET_INIT_Mess.COMET_EVC_CUR_GATC_BASELINE, center_format)
            worksheet.write(i, 16, COMET_INIT_Mess.COMET_EVC_CUR_CONFIG_VERSION, center_format)
            worksheet.write(i, 17, COMET_INIT_Mess.COMET_FIFO_CLEARED, center_format)
            i = i + 1
    worksheet.autofilter(0, 0, i-1, len(Fields_COMET_INIT_2)-1)
    worksheet.freeze_panes(1, 0)

def write_JRU_Messages(workbook, worksheet, RMR_Messages):
    Fields_JRU = ['Train name', 'DATE (EVC)', 'TIME (EVC)', 'NID_MESSAGE', \
                  'Q_SCALE', 'NID_C', 'NID_BG', 'D_LRBG', 'Q_DIRLRBG', 'Q_DLRBG', 'L_DOUBTOVER', 'L_DOUBTUNDER',
                  'V_TRAIN', \
                  'NID_ENGINE', 'SYSTEM_VERSION', 'LEVEL', 'MODE', 'PACKET']

    Fields_JRU_2 = [['Train name', 20],
                    ['DATE (EVC)', 20],
                    ['TIME (EVC)', 20],
                    ['NID_MESSAGE', 20],
                    ['Q_SCALE', 10],
                    ['NID_C', 10],
                    ['NID_BG', 10],
                    ['D_LRBG', 20],
                    ['Q_DIRLRBG', 20],
                    ['Q_DLRBG', 20],
                    ['L_DOUBTOVER', 15],
                    ['L_DOUBTUNDER', 20],
                    ['V_TRAIN', 20],
                    ['NID_ENGINE', 15],
                    ['SYSTEM_VERSION', 15],
                    ['LEVEL', 20],
                    ['MODE', 15],
                    ['PACKET', 20]]

    titles_format = workbook.add_format({'bold': True, 'align': 'center'})
    center_format = workbook.add_format({'align': 'center'})
    coord_format = workbook.add_format({'align': 'left'})

    #column_width = [20, 20, 20, ]
    j = 0
    for f in Fields_JRU_2:
        worksheet.set_column(0, j, f[1])
        worksheet.write(0, j, f[0], titles_format)
        j = j + 1
    cnt = 0
    i = 1
    Nmess = len(RMR_Messages)
    for m in RMR_Messages:
        if m.OBU_DATA_TYPE == '2':
            obu_data_hex = m.OBU_DATA.encode('latin-1').hex()
            TRU_NID_MESSAGE = obu_data_hex[0:2]
            if TRU_NID_MESSAGE == '00':
                if (i % 2000 == 0):
                    print('JRU writing... '+str(i) + '/' + str(Nmess))
                obu_data_bin = bit.hexToBin_loop(obu_data_hex)
                TRU_NID_MESSAGE = int(obu_data_bin[0:8], 2)
                name = decode_raw_data.OBU_NAME_FROM_OBU_ID(m.OBU_ID)
                NID_MESSAGE = int(obu_data_bin[8:16], 2)
                # L_MESSAGE = int(obu_data_bin[16:27],2)
                DATE = obu_data_bin[27:43]
                TIME = obu_data_bin[43:65]
                Q_SCALE = int(obu_data_bin[65:67], 2)
                NID_LRBG = obu_data_bin[67:91]
                D_LRBG = int(obu_data_bin[91:106], 2)
                Q_DIRLRBG = int(obu_data_bin[106:108], 2)
                Q_DLRBG = int(obu_data_bin[108:110], 2)
                L_DOUBTOVER = int(obu_data_bin[110:125], 2)
                L_DOUBTUNDER = int(obu_data_bin[125:140], 2)
                V_TRAIN = int(obu_data_bin[140:150], 2)
                DRIVER_ID = obu_data_bin[150:278]
                NID_ENGINE = int(obu_data_bin[278:302], 2)
                SYSTEM_VERSION = int(obu_data_bin[302:309], 2)
                LEVEL = int(obu_data_bin[309:312], 2)
                if obu_data_bin[312:316] == '':
                    MODE = ''
                else:
                    MODE = int(obu_data_bin[312:316], 2)
                PACKET_VARIABLES = obu_data_bin[316:]

                if (V_TRAIN == 1023):
                    v_train = 'Standstill'
                else:
                    v_train = V_TRAIN

                if (MODE == 0):
                    mode = 'Full Supervision'
                elif (MODE == 1):
                    mode = 'On Sight'
                elif (MODE == 2):
                    mode = 'Staff Responsible'
                elif (MODE == 3):
                    mode = 'Shunting'
                elif (MODE == 4):
                    mode = 'Unfitted'
                elif (MODE == 5):
                    mode = 'Sleeping'
                elif (MODE == 6):
                    mode = 'Standby'
                elif (MODE == 7):
                    mode = 'Trip'
                elif (MODE == 8):
                    mode = 'Post Trip'
                elif (MODE == 9):
                    mode = 'System Failure'
                elif (MODE == 10):
                    mode = 'Isolation'
                elif (MODE == 11):
                    mode = 'Non Leading'
                elif (MODE == 12):
                    mode = 'Limited Supervision'
                elif (MODE == 13):
                    mode = 'National System'
                elif (MODE == 14):
                    mode = 'Reversing'
                elif (MODE == 15):
                    mode = 'Passive Shunting'
                else:
                    mode = 'None'

                if (LEVEL == 0):
                    level = 0
                elif (LEVEL == 1):
                    level = 'NTC'
                elif (LEVEL == 2):
                    level = 1
                elif (LEVEL == 3):
                    level = 2
                else:
                    level = 'None'
                if (name == ''):
                    worksheet.write(i, 0, m.OBU_ID)
                else:
                    worksheet.write(i, 0, name, center_format)
                worksheet.write(i, 1, tru.jru_date_from_bin(DATE), center_format)
                worksheet.write(i, 2, tru.jru_time_from_bin(TIME), center_format)
                worksheet.write(i, 3, NID_MESSAGE, center_format)
                # worksheet.write(i,4,L_MESSAGE)
                worksheet.write(i, 4, Q_SCALE, center_format)
                worksheet.write(i, 5, int(NID_LRBG[0:10], 2), center_format)
                worksheet.write(i, 6, int(NID_LRBG[10:24], 2), center_format)
                worksheet.write(i, 7, D_LRBG, center_format)
                worksheet.write(i, 8, Q_DIRLRBG, center_format)
                worksheet.write(i, 9, Q_DLRBG, center_format)
                worksheet.write(i, 10, L_DOUBTOVER, center_format)
                worksheet.write(i, 11, L_DOUBTUNDER, center_format)
                worksheet.write(i, 12, v_train, center_format)
                # worksheet.write(i,13,DRIVER_ID)
                worksheet.write(i, 13, NID_ENGINE, center_format)
                worksheet.write(i, 14, SYSTEM_VERSION, center_format)
                worksheet.write(i, 15, level, center_format)
                worksheet.write(i, 16, mode, center_format)
                worksheet.write(i, 17, PACKET_VARIABLES)
                i = i + 1
    worksheet.autofilter(0, 0, i - 1, len(Fields_JRU_2) - 1)
    worksheet.freeze_panes(1, 0)


