# __StandAlone INIT__
from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Attendance_Push_FN(AttnPush):
    #_________ Defintion_List _________
    @Exception_Handle
    def Atten_Tbl_Refresh():
        Table_Data_Temp = DB_Fetch( 'select emp_code,team,employee_name,designation from register where '
                                        'active = "Y" order by team,employee_name', False, 'LOL')
        for step in Table_Data_Temp:
            step.append(QCheckBox())
            QS = QSpinBox();
            QS.setRange(1, 3);
            step.append(QS)
            QS = QSpinBox();
            QS.setRange(0, 8);
            step.append(QS)
        Push_Table_Values(AttnPush.OQTB_Register, Table_Data_Temp, False)

    @Exception_Handle
    def Update_Attendance():
        pushdate=AttnPush.IQDE_Date.date().toString("dd-MM-yyyy").split("-")
        data = Fetch_Table_Values(AttnPush.OQTB_Register)
        for step in data:
            #------Attendance Logic
            temp= "P" if step[4] == True else "A"
            if temp == "P":
                temp = str(step[5])
            if temp == 'A' and step[6]>0:
                temp=f'{step[5]}A'
            temp+='::'
            temp+=str(step[6])
            #-------
            sql=fr'''update {pushdate[1]}_{pushdate[2]} set `{pushdate[0]}` = '{temp}' where empcode = '{step[0]}' '''
            DB_Cmt(sql,False)
        AttnView.OQTB_EmpDetails.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        View_Table_Data = Attendance_datasplit(Attendance_Fetch(AttnView.IQDE_Date.date().toString('MM-yyyy')),
                                               AttnView.IQCB_Attendance.currentText(),False)
        Push_Table_Values(AttnView.OQTB_EmpDetails, View_Table_Data[0], False)
        Push_Table_Values(AttnView.OQTB_EmpAttendance, View_Table_Data[1], False)
        UI_Confirmation(UI_Confirm_Win, "Atttendance Generated Successfully")

    @Exception_Handle
    def Fetch_Attendance():
        if AttnPush.IQC_AttendanceFetch.isChecked():
            Table_Data_Temp = DB_Fetch( 'select emp_code,team,employee_name,designation from register where '
                        'active = "Y" order by team,employee_name',
                        False, 'LOL')
            AttnData = AttendaceFetch_Day(AttnPush.IQDE_Date.date().toString('yyyy-MM-dd'))

            for step in Table_Data_Temp:
                try:
                    Data=AttnData[step[0]].split("::")
                except:
                    Data = ['A','0.0']

                print(Data)
                CB = QCheckBox(); CB.setChecked(True if 'A' not in Data[0] else False)
                step.append(CB)

                QS = QSpinBox();QS.setRange(1, 3);QS.setValue(int(float(Data[0][0]))
                                    if Data[0][0]!='A'and Data[0]!='NA' and Data[0]!='P' else 1)
                step.append(QS)

                QS = QSpinBox();QS.setRange(0, 8);QS.setValue(int(float(Data[1]))
                                    if Data[1]!= "NA" else 0)
                step.append(QS)

            Push_Table_Values(AttnPush.OQTB_Register, Table_Data_Temp, False)

    #_________ Functionality_List _________
    AttnPush.IQDE_Date.setDate(QtCore.QDate.currentDate())
    Adjust_Table_Width(AttnPush.OQTB_Register, [10,12,25,15,5,8,8])

    Table_Data_Temp = DB_Fetch('select emp_code,team,employee_name,designation from register where '
        'active = "Y" order by team DESC,employee_name',False,'LOL')
    for step in Table_Data_Temp:
        step.append(QCheckBox())
        QS = QSpinBox();QS.setRange(1,3);step.append(QS)
        QS = QSpinBox();QS.setRange(0,8);step.append(QS)
    Push_Table_Values(AttnPush.OQTB_Register,Table_Data_Temp,False)
    AttnPush.pushButton.clicked.connect(lambda: Update_Attendance())
    AttnPush.IQDE_Date.dateChanged.connect(lambda : Fetch_Attendance())
    AttnPush.IQC_Refresh.clicked.connect(lambda: Atten_Tbl_Refresh())

@Exception_Handle
def Attendance_View_Fn(AttnView):
    @Exception_Handle
    def Custom_Attendance_View():
        AttnView.OQTB_EmpDetails.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        View_Table_Data = Attendance_datasplit(Attendance_Fetch(AttnView.IQDE_Date.date().toString('MM-yyyy')),
                                               AttnView.IQCB_Attendance.currentText(),False)
        Push_Table_Values(AttnView.OQTB_EmpDetails, View_Table_Data[0], False)
        Push_Table_Values(AttnView.OQTB_EmpAttendance, View_Table_Data[1], False)
        Adjust_Table_Width(AttnView.OQTB_EmpDetails, [10,12,30])
        Adjust_Table_Width(AttnView.OQTB_EmpAttendance, [8] * 30)


    @Exception_Handle
    def Export_Attendance_ExcelFetch():
        if UI_Confirmation(UI_Confirm_Win, f"Please Confrim to Data to Export"):
            xl = openpyxl.load_workbook(filename=fr'{ldir}\Temp\Excel_Fetch.xlsx')
            for step in ['Attendance', 'OT']:
                xl.active = xl[step]
                xlc = xl.active
                data = Attendance_Fetch(AttnView.IQDE_Date.date().toString('MM-yyyy'))
                atndata = Attendance_datasplit(copy.deepcopy(data), step,True)
                print(atndata)
                crow = 2
                ccol = 1
                for part in atndata:
                    # print(part)
                    for i in range(len(part)):
                        xlc.cell(row=crow, column=ccol).value = part[i]
                        ccol += 1
                    crow += 1
                    ccol = 1
            xl.save(filename=fr'{ldir}\Temp\Excel_Fetch_OP.xlsx')
            os.system(fr'{ldir}\Temp\Excel_Fetch_OP.xlsx')

    @Exception_Handle
    def ExcelFetch_Attendance():
        if UI_Confirmation(UI_Confirm_Win, f"Please Confrim to Fetch the Attendance from Excel Fetch Export"):
            xl = openpyxl.load_workbook(filename=fr'{ldir}\Temp\Excel_Fetch_OP.xlsx')
            xlc1 = xl['Attendance']
            xlc2 = xl['OT']
            Data = []
            pushdate = list(AttnView.IQDE_Date.date().toString('MM-yyyy').split("-"))
            for i in range(int(xlc1.max_row) - 1):
                temp = []
                cursor = xlc1.cell(row=i + 2, column=1)
                temp.append(cursor.value)
                for j in range(calendar.monthrange(int(pushdate[1]), int(pushdate[0]))[1]):
                    c1 = xlc1.cell(row=i + 2, column=j + 4)
                    if c1.value == None:
                        c1.value = "A"
                    c2 = xlc2.cell(row=i + 2, column=j + 4)
                    if c2.value == None:
                        c2.value = "0.0"
                    temp.append(str(c1.value) + "::" + str(c2.value))
                Data.append(temp)
                # print(len(Data[0]))
            for step in Data:
                for i in range(len(step) - 1):
                    try:
                        sql = "update %s_%s set `%s` = '%s' where empcode = '%s'" % \
                              (pushdate[0], pushdate[1], str(i + 1).zfill(2), step[i + 1], step[0])
                        # print(sql)
                        DB_Cmt(sql,False)
                    except Exception as e:
                        ms.popup(e, font=fstyle)
                        break

            Custom_Attendance_View()
            UI_Confirmation(UI_Confirm_Win, f"Excel Fetch Export is Done")

    @Exception_Handle
    def Export_Attendance_FormExport():
        if UI_Confirmation(UI_Confirm_Win, f"Please Confrim to Export Attendance data in FormExport"):
            xl = openpyxl.load_workbook(filename=fr'{ldir}\Temp\Attendance_Form.xlsx')
            xlc = xl.active
            data = Attendance_Fetch(AttnView.IQDE_Date.date().toString('MM-yyyy'))
            atndata = Attendance_datasplit(copy.deepcopy(Attendance_Fetch(AttnView.IQDE_Date.date().toString('MM-yyyy'))), "Attendance",True)
            for step in atndata:
                S1Data = DB_Fetch(f"select uan_no,esic_no,f_sp_name,designation,shift_work from register where "
                                     f"emp_code='{step[0]}'",False,"LOE")
                print(S1Data)
                step.pop(1)
                step.insert(1, S1Data[0])
                step.insert(2, S1Data[1])
                step.insert(4, S1Data[2])
                step.insert(5, S1Data[3])
                step.insert(6, "SFT" if S1Data[4] == "Yes" else "Gen")
            crow = 8
            ccol = 2
            for part in atndata:
                for i in range(len(part)):
                    xlc.cell(row=crow, column=ccol).value = part[i]
                    ccol += 1
                crow += 1
                ccol = 2
            pushdate = list(AttnView.IQDE_Date.date().toString('MM-yyyy').split("-"))
            tot_days = int(calendar.monthrange(int(pushdate[1]), int(pushdate[0]))[1])
            hide_list = ['AM', 'AL', 'AK']
            for i in range(31 - tot_days):
                xlc.column_dimensions[hide_list[i]].hidden = True
            crow = 7
            ccol = 9
            for i in range(tot_days):
                xlc.cell(row=crow, column=ccol).value = datetime.strptime(str(i + 1) + "-" + AttnView.IQDE_Date.date().toString('MM-yyyy'),
                                                                          "%d-%m-%Y").strftime("%A")
                ccol += 1
            for i in range(len(atndata) + 1, 201):
                xlc.row_dimensions[i + 7].hidden = True

            xlc.cell(row=4, column=3).value = "01-" + AttnView.IQDE_Date.date().toString('MM-yyyy')\
                                              + " TO " + str(tot_days) + "-" + AttnView.IQDE_Date.date().toString('MM-yyyy')
            xl.save(filename=fr'{ldir}\Temp\Attendance_Form_OP.xlsx')
            os.system(fr'{ldir}\Temp\Attendance_Form_OP.xlsx')

    AttnView.IQDE_Date.setDate(QtCore.QDate.currentDate())
    View_Table_Data = Attendance_datasplit(Attendance_Fetch(Cur_Date_MY),"Atn+ot",False)
    Adjust_Table_Width(AttnView.OQTB_EmpDetails, [10, 12, 30])
    Adjust_Table_Width(AttnView.OQTB_EmpAttendance, [8]*30)
    Push_Table_Values(AttnView.OQTB_EmpDetails,View_Table_Data[0],False)
    Push_Table_Values(AttnView.OQTB_EmpAttendance,View_Table_Data[1],False)

    AttnView.OQTB_EmpDetails.setSortingEnabled(False)
    AttnView.OQTB_EmpDetails.verticalScrollBar().valueChanged.connect(
        AttnView.OQTB_EmpAttendance.verticalScrollBar().setValue)

    AttnView.OQTB_EmpAttendance.setSortingEnabled(False)
    AttnView.OQTB_EmpAttendance.verticalScrollBar().valueChanged.connect(
        AttnView.OQTB_EmpDetails.verticalScrollBar().setValue)

    AttnView.IQCB_Attendance.currentIndexChanged.connect(lambda : Custom_Attendance_View())
    AttnView.IQDE_Date.dateChanged.connect(lambda : Custom_Attendance_View())

    #AttnView.IQPB_Export.clicked.connect(lambda : Export_Attendance_ExcelFetch())
    #AttnView.IQPB_XLFetch.clicked.connect(lambda: ExcelFetch_Attendance())
    AttnView.IQPB_FormExp.clicked.connect(lambda : Export_Attendance_FormExport() )

# __StandAlone Running__
if SAR == True:
    Attendance_Push_FN(AttnPush)
    AttnPush.show()
    Attendance_View_Fn(AttnView)
    AttnView.show()
    sys.exit(app.exec_())