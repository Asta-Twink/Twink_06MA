# __StandAlone INIT__
import os

from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

def Punch_Build_FN(PnchBld,PrsPnchTrck):
    print("Start")

    #_________ Defintion_List _________

    def Punch_Build_Push(res_list,date,reset,update): # create Punch data from Iclock Transaction
        for step in res_list:
            try:
                data=Punch_Build_Data(step, date)

                if reset:
                    DB_Cmt(fr"DELETE FROM `punch_build` WHERE (`emp_code` = '{step}') and "\
                                     fr"(`gen_date` = '{date}');",False)

                try:
                    DB_Cmt_WOE(fr'''INSERT INTO `punch_build` VALUES ('{step}', '{date}', 
                    '{data[0] if data [0] != "NA" else "NA"}',
                     '{data[1] if data [1] != "NA" else "NA"}',
                      '{data[2] if data [2] != "NA" else "NA"}',
                       '{data[3] if data [3] != "NA" else "NA"}',
                       '{data[4]}');''',False)
                except:
                    traceback.print_exec()
                    pass
                # if update:
                #    DB_Cmt(f"update attendance_track set status = 'MCU', lu_date = '{Cur_Date_SQL}' where s_date = '"
                #           f"{date}' ",False)

            except Exception as e:
                print(e)
                pass

    def Attendance_Build_Push(res,date): # create Attendance data from punchdata
        pushdate = date.split("-")
        sql = fr'''update {pushdate[1]}_{pushdate[0]} set `{pushdate[2]}` = '{Punch_Build_Fetch(res, date)}' where empcode = '{res}' '''
        DB_Cmt(sql,False)

    def Mass_Attendance_Build_Push(emplist,inp): # create Attendance data from punchdata
        pushdate=inp.split("-")
        for step in emplist:
            sql = fr'''update {pushdate[1]}_{pushdate[0]} set `{pushdate[2]}` = '{Punch_Build_Fetch(step, inp)}' where empcode = '{step}' '''
            DB_Cmt( sql, False)

    def PB_Daliy_Trigger():
        mm=int(Cur_Date_MY.split("-")[0])
        yy=int(Cur_Date_MY.split("-")[1])

        db_list = DB_Fetch(f'select s_date from attendance_track where status != "YTC" and month(s_date) = {mm} '
                               f'and year(s_date) = {yy} ',False,"LOE")
        netlist = list(TD_datelist(yy, mm))[:-1]

        sub_list = list(set(netlist).difference(set(db_list)))
        #print(netlist,sub_list)

        for date in sub_list:#Monthly Data Trigger
            print(date)
            Punch_Build_Push(Active_EmpC, date.strftime("%Y-%m-%d"),reset=False,update=True)
            Mass_Attendance_Build_Push(Active_EmpC,date.strftime("%Y-%m-%d"))

    #PB_Daliy_Trigger()
    # PunchBuild_Layout
    def PTrack_Functions(Menu,event,values):
        if event == 'ptrkdateinp':
            Menu['TL_PTrkView'].update(values=P_Track_Data(mysql_date(values['ptrkdateinp'])))
            Menu['PTrk_Status'].update(PTrk_Status(mysql_date(values['ptrkdateinp'])))

        if event == 'Ptrk_Mail':
            data=Menu['TL_PTrkView'].get()
            #print(data)
            df = pd.DataFrame(data, columns=['Emp Code','Employee Name','Check In Time', 'Lunch Out Time','Lunch In Time',
                                             'Check Out Time', 'DS Check Out'])
            email_body = df.to_html(index=False, justify="center")
            chk = ms.popup_ok("Please confrim to send mail", font=fstyle, no_titlebar=True)
            if chk == "OK":
                ms.popup_auto_close("Mail ID not Configured",font=fstyle)
                return
                maillist = popup_select(mailid_fetch(False, ""))
                if maillist == None:
                    pass
                for i in maillist:
                    sender_address = 'attendance.seasonmotors@gmail.com'
                    sender_pass = 'nftzunafqtemqbsv'
                    # Setup the MIME
                    receiver_address = mailid_fetch(True, i)
                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    message['Subject'] = "Punch Data - %s" % values['ptrkdateinp']
                    message.attach(MIMEText(email_body, "html"))

                    # Create SMTP session for sending the mail
                    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
                    session.starttls()  # enable security
                    session.login(sender_address, sender_pass)
                    text = message.as_string()
                    session.sendmail(sender_address, receiver_address, text)
                    session.quit()
                ms.popup_auto_close("Mail Successfully Sent", font=fstyle, no_titlebar=True)

        if event == 'Ptrk_Exp':
            data=Menu['TL_PTrkView'].get()
            for i in range (len(data)):
                data[i][1] = data[i][1][3:]
            df = pd.DataFrame(data, columns=['Emp Code','Employee Name','Check In Time', 'Lunch Out Time','Lunch In Time',
                                             'Check Out Time', 'DS Check Out'])
            df.to_csv(r'C:\Twink_08SD\Master_Files\PTRACKTemp.csv')
            subprocess.run(['start', 'excel', r'C:\Twink_08SD\Master_Files\PTRACKTemp.csv'], shell=True, check=True)

        if event == "PTrk_Update_CB":
            if values['PTrk_Update_CB'] == True:
                Menu['PTrk_Update'].update(visible = True)
                Menu['PTrk_Update_Note'].update(visible=True)
                if PTrk_Status(mysql_date(values['ptrkdateinp'])) == "Manual Update" or \
                        PTrk_Status(mysql_date(values['ptrkdateinp'])) == "Custom Update":
                    Menu['PTrk_Regen'].update(visible=True)
            else:
                Menu['PTrk_Update'].update(visible = False);
                Menu['PTrk_Update_Note'].update(visible=False)
                Menu['PTrk_Regen'].update(visible=False)

        if isinstance(event, tuple):
            if event[0] == 'TL_PTrkView':
                if values['PTrk_Update_CB'] == True:
                    try:
                        cell = event[2]
                        if int(cell[1]) > 1:
                            new_value = edit_cell_list(Menu.mouse_location())
                            try:
                                val_chk = False
                                val_chk_temp=new_value.split(".")
                                if len(val_chk_temp) == 2:
                                    if int(val_chk_temp[0])<=23:
                                        if int(val_chk_temp[1])<=59:
                                            val_chk = True
                            except:
                                val_chk = False
                                ms.popup_auto_close("Please Enter Valid Time",font=fstyle)
                            if val_chk == True:
                                templist = Menu['TL_PTrkView'].get()
                                templist[cell[0]][cell[1]] = new_value
                                Menu['TL_PTrkView'].update(values=templist)
                            else:
                                ms.popup_auto_close("Please Enter Valid Time",font=fstyle)
                    except Exception as e:
                        print(e)
                        pass

        if event == 'PTrk_Update':
            tempdata=Menu['TL_PTrkView'].get()
            chk = ms.popup_get_text("Enter password to proceed Further ", password_char='*', size=(20, 1), font=fstyle,
                                    keep_on_top=True)
            if chk == MasterPass:
                for step in tempdata:
                #print(step)
                    try:
                        inpdate=mysql_date(values['ptrkdateinp'])
                        mycursor.execute(fr"DELETE FROM `punch_build` WHERE (`emp_code` = '{step[0]}') and " \
                                             fr"(`gen_date` = '{inpdate}');")
                        sql=fr'''INSERT INTO `punch_build` VALUES ('{step[0]}', '{inpdate}','{step[2] if step[2] != "NA" else "NA"}','{step[3] if step[3] != "NA" else "NA"}','{step[4] if step[4] != "NA" else "NA"}','{step[5] if step[5] != "NA" else "NA"}','{step[6] if step[6] != "NA" else "NA"}')'''
                        #print(sql)
                        mycursor.execute(sql)
                        mydb.commit()
                        mycursor.execute(f"update attendance_track set status = 'MNU', lu_date = '{todatestr}' where "
                                         f"s_date = '{inpdate}'")

                        mycursor.execute(sql)
                        mydb.commit()

                    except Exception as e:
                        pass
                Mass_Attendance_Build_Push(res_list,inpdate)
                Menu['PTrk_Status'].update(PTrk_Status(mysql_date(values['ptrkdateinp'])))
                ms.popup_auto_close("Punch Track Updated Successfully", font=fstyle)

        if event == 'PTrk_Regen':
            inpdate = mysql_date(values['ptrkdateinp'])
            Punch_Build_Push(res_list, mysql_date(values['ptrkdateinp']), reset=True, update=True)
            Menu['TL_PTrkView'].update(values=P_Track_Data(mysql_date(values['ptrkdateinp'])))
            Menu['PTrk_Status'].update(PTrk_Status(mysql_date(values['ptrkdateinp'])))
            Mass_Attendance_Build_Push(res_list, inpdate)
            ms.popup_auto_close("Time stamps and Attendance data Regenerated for the given Date", font=fstyle)

        if event == 'ptrkpers_empname' or event == 'ptrkpersdateinp':
            Menu['TL_PTrkpersView'].update(values=P_Track_PersData(empidfetch
                                            (values['ptrkpers_empname']).split("__")[1],values['ptrkpersdateinp']))

        if event == 'Ptrkpers_Mail':
            data=Menu['TL_PTrkpersView'].get()
            df = pd.DataFrame(data, columns=['Emp Code','Date','Check In Time', 'Lunch Out Time','Lunch In Time',
                                             'Check Out Time', 'DS Check Out'])
            email_body = df.to_html(index=False, justify="center")
            chk = ms.popup_ok("Please confrim to send mail", font=fstyle, no_titlebar=True)
            if chk == "OK":
                ms.popup_auto_close("Mail ID not Configured",font=fstyle)
                return
                maillist = popup_select(mailid_fetch(False, ""))
                if maillist == None:
                    pass
                for i in maillist:
                    sender_address = 'attendance.seasonmotors@gmail.com'
                    sender_pass = 'nftzunafqtemqbsv'
                    # Setup the MIME
                    receiver_address = mailid_fetch(True, i)
                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    message['Subject'] = "Punch Data - %s" % values['ptrkdateinp']
                    message.attach(MIMEText(email_body, "html"))

                    # Create SMTP session for sending the mail
                    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
                    session.starttls()  # enable security
                    session.login(sender_address, sender_pass)
                    text = message.as_string()
                    session.sendmail(sender_address, receiver_address, text)
                    session.quit()
                ms.popup_auto_close("Mail Successfully Sent", font=fstyle, no_titlebar=True)

        if event == 'Ptrkpers_Exp':
            data=Menu['TL_PTrkpersView'].get()
            df = pd.DataFrame(data, columns=['Emp Code','Date','Check In Time', 'Lunch Out Time','Lunch In Time',
                                             'Check Out Time', 'DS Check Out'])
            df.to_csv(r'C:\Twink_08SD\Master_Files\PTRACKPERSTemp.csv')
            subprocess.run(['start', 'excel', r'C:\Twink_08SD\Master_Files\PTRACKPERSTemp.csv'], shell=True, check=True)

    @Exception_Handle
    def Editable_Table():
        if PnchBld.IQC_Update.isChecked():
            PnchBld.IQPB_Update.setEnabled(True)
            PnchBld.IQPB_Regen.setEnabled(True)
            for row in range(PnchBld.OQTB_PunchTrack.rowCount()):
                for j in range (2,6):
                    item = PnchBld.OQTB_PunchTrack.item(row, j)
                    if item:
                        item.setFlags(item.flags() | Qt.ItemIsEditable)

        else:
            PnchBld.IQPB_Update.setEnabled(False)
            Push_Table_Values(PnchBld.OQTB_PunchTrack,Fetch_Table_Values(PnchBld.OQTB_PunchTrack),False)

    @Exception_Handle
    def Update_Punch_Build():
        tempdata = Fetch_Table_Values(PnchBld.OQTB_PunchTrack)
        for step in tempdata:
            try:
                inpdate = PnchBld.IQDE_Date.date().toString(sqlformat)
                DB_Exe(fr"DELETE FROM `punch_build` WHERE (`emp_code` = '{step[0]}') and " \
                                 fr"(`gen_date` = '{inpdate}');",False)

                Convert_Punch_Attendance(step[2:6])
                sql = fr'''INSERT INTO `punch_build` VALUES ('{step[0]}', '{inpdate}','{step[2]}','{step[3]}'
                ,'{step[4]}','{step[5]}','{Convert_Punch_Attendance(step[2:6])}')'''
                # print(sql)
                DB_Exe(sql,False)

                DB_Cmt(f"update attendance_track set status = 'MNU', lu_date = '{Cur_Date_SQL}' where "
                                 f"s_date = '{inpdate}'",False)

            except Exception as e:
                print(e)
                pass

        sql = f"select punch_build.emp_code, register.employee_name, punch_build.CI, punch_build.CO, punch_build.OTI, " \
              f"punch_build.OTO, punch_build.gen_attn from punch_build left join register on  punch_build.emp_code = " \
              f"register.emp_code where punch_build.gen_date = '{inpdate}' order by punch_build.gen_attn"
        Push_Table_Values(PnchBld.OQTB_PunchTrack, DB_Fetch( sql, False, "LOL"), False)
        Mass_Attendance_Build_Push(Active_EmpC, inpdate)
        UI_Confirmation(UI_Confirm_Win, "Punch time stamps Updated Successfully")

    @Exception_Handle
    def Regen_Punch_Build():

        inpdate = PnchBld.IQDE_Date.date().toString(sqlformat)
        Punch_Build_Push(Active_EmpC,PnchBld.IQDE_Date.date().toString(sqlformat) , True, True)
        sql = f"select punch_build.emp_code, register.employee_name, punch_build.CI, " \
                      f"punch_build.CO,punch_build.OTI, punch_build.OTO, punch_build.gen_attn from punch_build left join register on  punch_build.emp_code = " \
                      f"register.emp_code where punch_build.gen_date = '{inpdate}' order by punch_build.gen_attn"
        Push_Table_Values(PnchBld.OQTB_PunchTrack, DB_Fetch( sql, False, "LOL"), False)
        UI_Confirmation(UI_Confirm_Win, "Punch time stamps regenerated Successfully")

    @Exception_Handle
    def Export_Punch_Track():

        data = Fetch_Table_Values(PnchBld.OQTB_PunchTrack)

        inv = openpyxl.load_workbook(filename=fr"{os.getcwd()}\_internal\F3_AUX\TEMP\Attendance Report.xlsx")
        sheet = inv.active
        for j in range(len(data)):
            sheet.cell(row=4 + j, column=2).value = data[j][0]
            sheet.cell(row=4 + j, column=3).value = data[j][1]
            sheet.cell(row=4 + j, column=4).value = data[j][2] if data[j][2] != "NA" else "00:00"
            sheet.cell(row=4 + j, column=5).value = data[j][3] if data[j][3] != "NA" else "00:00"
            sheet.cell(row=4 + j, column=6).value = data[j][4] if data[j][4] != "NA" else "00:00"
            sheet.cell(row=4 + j, column=7).value = data[j][5] if data[j][5] != "NA" else "00:00"
            sheet.cell(row=4 + j, column=8).value = data[j][6]

            if "IN" in data[j][6]:
                sheet.cell(row=4 + j, column=9).value = data[j][6].split("-")[0]
            elif "A::" in data[j][6] and not ("1A::" in data[j][6] or "2A::" in data[j][6] or "3A::" in data[j][6]):
                sheet.cell(row=4 + j, column=9).value = data[j][6].split("::")[0]
            elif "1A::" in data[j][6] or "2A::" in data[j][6] or "3A::" in data[j][6]:
                sheet.cell(row=4 + j, column=9).value = "A"
            else:
                sheet.cell(row=4 + j, column=9).value = data[j][6].split("::")[0]

            if "A::" in data[j][6] and not ("1A::" in data[j][6] or "2A::" in data[j][6] or "3A::" in data[j][6]):
                sheet.cell(row=4 + j, column=10).value = float(0)
            elif "1A::" in data[j][6] or "2A::" in data[j][6] or "3A::" in data[j][6]:
                sheet.cell(row=4 + j, column=10).value = float(data[j][6].split("::")[1])
            elif "IN" in data[j][6]:
                sheet.cell(row=4 + j, column=10).value = float(0)
            else:
                sheet.cell(row=4 + j, column=10).value = float(data[j][6].split("::")[1])

        inv.save(fr"{os.getcwd()}\_internal\F3_AUX\TEMP\Attendance Report1.xlsx")
        inv.close()
        subprocess.run(['start', '', fr"{os.getcwd()}\_internal\F3_AUX\TEMP\Attendance Report1.xlsx"], shell=True,
                       check=True)
        UI_Confirmation(UI_Confirm_Win, "Punch Track Exported Successfully")
    @Exception_Handle
    def Export_Perosnal_Punch_Track():

        df = pd.DataFrame(Fetch_Table_Values(PrsPnchTrck.OQTB_PersonalPunchTrack),
                          columns=['Emp Code', 'Date', 'Check In Time', 'Check Out Time', 'OT In Time',
                                   'OT Out Time', 'Attendance'])
        df['Name'] = PrsPnchTrck.IQCB_EmpName.currentText()
        df[['Emp Code','Name', 'Date', 'Check In Time', 'Check Out Time', 'OT In Time',
                                   'OT Out Time', 'Attendance']].to_csv(fr'{ldir}\F3_AUX\PTRACKTemp.csv')
        os.system(fr'{ldir}\F3_AUX\PTRACKTemp.csv')


    # _________ Functionality_List _________

    PnchBld.IQDE_Date.setDate(QtCore.QDate.currentDate())

    sql = f"select punch_build.emp_code, register.employee_name, punch_build.CI, punch_build.CO, punch_build.OTI, " \
          f"punch_build.OTO, punch_build.gen_attn from punch_build left join register on  punch_build.emp_code = " \
          f"register.emp_code where punch_build.gen_date = '{Cur_Date_SQL}' order by punch_build.gen_attn"
    # print(DB_Fetch(sql,False,"LOL"))
    Adjust_Table_Width(PnchBld.OQTB_PunchTrack, [10, 35, 12, 12, 12,12,12])
    Push_Table_Values(PnchBld.OQTB_PunchTrack,DB_Fetch(sql,False,"LOL"),False)

    PnchBld.IQDE_Date.dateChanged.connect(lambda :
    Push_Table_Values(PnchBld.OQTB_PunchTrack,DB_Fetch(
        f"select punch_build.emp_code, register.employee_name, punch_build.CI, " \
        f"punch_build.CO,punch_build.OTI, punch_build.OTO, punch_build.gen_attn from punch_build left join register on  punch_build.emp_code = " \
        f"register.emp_code where punch_build.gen_date = '{PnchBld.IQDE_Date.date().toString(sqlformat)}' order by punch_build.gen_attn",
    False,"LOL"),False))

    PnchBld.IQC_Update.stateChanged.connect(lambda : Editable_Table())
    PnchBld.IQPB_Update.clicked.connect(lambda: Update_Punch_Build())
    PnchBld.IQPB_Regen.clicked.connect(lambda: Regen_Punch_Build())
    PnchBld.IQPB_Export.clicked.connect(lambda : Export_Punch_Track())

        #_________Personal Punch Track _________

    PrsPnchTrck.IQDE_Date.setDate(QtCore.QDate.currentDate())
    PrsPnchTrck.IQCB_EmpName.addItems(Active_EmpList)

    # Push_Table_Values(PrsPnchTrck.OQTB_PersonalPunchTrack,DB_Fetch(
    #                     f'select emp_code, DATE_FORMAT(gen_date, "%d-%m-%Y"),CI,CO,OTI,OTO,gen_attn from punch_build where '
    #                     f'emp_code = "{EmpCode_Fetch(PrsPnchTrck.IQCB_EmpName.currentText())}" and '
    #                     f'month(gen_date)= "{PrsPnchTrck.IQDE_Date.date().toString(sqlformat).split("-")[1]}" and year('
    #                     f'gen_date) = "{PrsPnchTrck.IQDE_Date.date().toString(sqlformat).split("-")[0]}"',
    #                      False, "LOL"),False)

    PrsPnchTrck.IQDE_Date.dateChanged.connect(lambda:
            Push_Table_Values(PrsPnchTrck.OQTB_PersonalPunchTrack, DB_Fetch(
                        f'select emp_code, DATE_FORMAT(gen_date, "%d-%m-%Y"),CI,CO,OTI,OTO,gen_attn from punch_build where '
                        f'emp_code = "{EmpCode_Fetch(PrsPnchTrck.IQCB_EmpName.currentText())}" and '
                        f'month(gen_date)= "{PrsPnchTrck.IQDE_Date.date().toString(sqlformat).split("-")[1]}" and year('
                        f'gen_date) = "{PrsPnchTrck.IQDE_Date.date().toString(sqlformat).split("-")[0]}"',
                         False, "LOL"), False))

    PrsPnchTrck.IQCB_EmpName.currentIndexChanged.connect( lambda :
            Push_Table_Values(PrsPnchTrck.OQTB_PersonalPunchTrack,DB_Fetch(
                        f'select emp_code, DATE_FORMAT(gen_date, "%d-%m-%Y"),CI,CO,OTI,OTO,gen_attn from punch_build where '
                        f'emp_code = "{EmpCode_Fetch(PrsPnchTrck.IQCB_EmpName.currentText())}" and '
                        f'month(gen_date)= "{PrsPnchTrck.IQDE_Date.date().toString(sqlformat).split("-")[1]}" and year('
                        f'gen_date) = "{PrsPnchTrck.IQDE_Date.date().toString(sqlformat).split("-")[0]}"',
                         False, "LOL"), False))

    PrsPnchTrck.IQPB_Export.clicked.connect(lambda: Export_Perosnal_Punch_Track())

#__StandAlone Running__
if SAR == True:
    Punch_Build_FN(PnchBld,PrsPnchTrck)
    PnchBld.show()
    PrsPnchTrck.show()
    sys.exit(app.exec_())