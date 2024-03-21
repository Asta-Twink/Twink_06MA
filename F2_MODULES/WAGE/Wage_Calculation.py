# ___StandAlone INIT___
import traceback
from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Wage_FN(Wge):
    # _________ Definition List _________
    @Exception_Handle
    def attendance_Wfetch(inp):
        form = list(inp.split("-"))
        try:
            db_data = DB_Fetch(
                "select register.employee_name,register.f_sp_name,register.team,register.office_staff, %s_%s.* "
                "from register inner join %s_%s on register.emp_code = %s_%s.empcode where register.active = 'Y' order by register.emp_code" % (
                    form[0], form[1], form[0], form[1], form[0], form[1]), False, "LOL")

            for i in range(len(db_data)):
                db_data[i].insert(0, db_data[i][4])
                del db_data[i][5]

        except:
            db_data = [[]]

        return db_data

    @Exception_Handle
    def LatePunch_Report(ec, start, end):
        print("----")
        print(ec, start, end)
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        sql = f"SELECT CI FROM punch_build WHERE emp_code = '{ec}' AND gen_date BETWEEN '{start}'  AND '{end}'"
        data = DB_Fetch(sql,False,"LOE")

        timespan = int(round((len(data) / 7), 0) * 2)

        for i in range(len(data)):
            try:
                data[i] = datetime.strptime(data[i], "%H.%M")
            except:
                data[i] = datetime.strptime("00.00", "%H.%M")
        # print(data)
        Alwd_Punch = []
        Crtl_Punch = []

        for dt in data:
            if time(7, 0, 0) <= dt.time() < time(11, 0, 0):
                if time(9, 0, 0) <= dt.time() < time(9, 15, 0):
                    Alwd_Punch.append(dt)
                if time(9, 15, 0) <= dt.time():
                    Crtl_Punch.append(dt)
            if time(17, 0, 0) <= dt.time() < time(19, 0, 0):
                if time(18, 0, 0) <= dt.time() < time(18, 15, 0):
                    Alwd_Punch.append(dt)
                if time(18, 15, 0) <= dt.time():
                    Crtl_Punch.append(dt)

        # print(len(Alwd_Punch),":",timespan)
        # print(Crtl_Punch)
        lp = f"AWD:{len(Alwd_Punch)}<>CTC:{len(Crtl_Punch)}"
        lph = 0
        if len(Alwd_Punch) > timespan:
            lphtemp = (len(Alwd_Punch) - timespan) * 2
            lph += lphtemp
        lph += len(Crtl_Punch)
        lp = f"AWD:{len(Alwd_Punch)} CTC:{len(Crtl_Punch)} <> {lph}"
        return lp, lph

    @Exception_Handle
    def wage_fetch():
        db_data = DB_Fetch(
            "Select emp_code,shift_1_salary,shift_2_salary,shift_3_salary from register where shift_work='Yes'",
            False, "LOL")
        output = []
        for step in db_data:
            temp = []
            temp.append(step[0])
            temp1 = []
            for i in range(1, 4):
                temp1.append(float(step[i]))
            temp.append(temp1)
            output.append(temp)
        dict_data = {x[0]: x[1] for x in output}
        db_data = DB_Fetch(
            "Select emp_code,shift_1_salary from register where shift_work='No'",
            False, "DIC")
        dict_data.update(db_data)

        return dict_data

    @Exception_Handle
    def mysql_date(inp):
        try:
            dateform = datetime.strptime(inp, '%d/%m/%Y')
        except:
            dateform = datetime.strptime(inp, '%d-%m-%Y')

        return dateform.strftime('%Y-%m-%d')

    @Exception_Handle
    def wageadvfetch(inp, po):
        # dateform=datefo.split("-")
        print('inp', inp)
        db_data = DB_Fetch(fr"select amount from advance_details where empcode='{inp}'",False,"LOL")
        # mycursor.execute("select amount from advance_details where empcode='%s'" % (inp))
        # db_data = list(sum(mycursor.fetchall(), ()))
        print(db_data,"sum")
        return sum(db_data)

    @Exception_Handle
    def Generate_Advance():
        global Advance_Data
        Wge.IQPB_Generate.setEnabled(True)
        Advance_Data = {key: float(value) for key,x,y, value in Fetch_Table_Values(Wge.IQTB_AdvanceDetail)}
        Wge.toolBox.setCurrentIndex(1)
        Wge.IQPB_Finalize.setEnabled(True)
        Wge.IQPB_Generate.setEnabled(True)
        Wge.IQPB_Export.setEnabled(True)
        Wge.IQPB_Mail.setEnabled(True)

    def shiftcheck(inp):
        chk = DB_Fetch("select shift_work from register where emp_code='%s'" % inp, False, "LOL")[0][0]
        # chk=mycursor.fetchall()[0][0]
        return True if chk == "Yes" else False

    @Exception_Handle
    def Wageee():
        global Advance_Data
        adv_data = []
        Max_Days=calendar.monthrange(int(Wge.IQDE_Date.date().toString('yyyy')), int(Wge.IQDE_Date.date().\
        toString('MM')))[1]
        data = attendance_Wfetch(Wge.IQDE_Date.date().toString('MM-yyyy'))
        wagedata = wage_fetch()
        globals()['wage_proc_data'] = []
        for step in data:
            temp = []
            for i in range(4):  # EMP Details addition
                temp.append(step[i])
            chk = shiftcheck(step[0])
            if chk == True:  # if Emp is Shift resource
                wagetemp = wagedata.get(step[0])
                S1, S2, S3, OT1, OT2, OT3 = 0, 0, 0, 0.0, 0.0, 0.0
                for i in range(5, len(step)):  # Custom Shift Calc
                    try:
                        i = step[i].split("::")
                    except:
                        continue
                    if i[0] == '1' or i[0] == 'P':
                        S1 += 1
                        if i[1] != 'NA' :OT1 += float(i[1])  # OT Addition
                    if i[0] == '2':
                        S2 += 1
                        if i[1] != 'NA' : OT2 += float(i[1])  # OT Addition
                    if i[0] == '3':
                        S3 += 1
                        if i[1] != 'NA' : OT3 += float(i[1])  # OT Addition
                    if i[0] == "A":
                        pass
                    try:
                        if i[0][1] == "A":
                            if i[0][0] == '1':
                                OT1 += float(i[1])
                            if i[0][0] == '2':
                                OT2 += float(i[1])
                            if i[0][0] == '3':
                                OT3 += float(i[1])
                    except:
                        pass

                OT = OT1 + OT2 + OT3
                DP=S1+S2+S3
                temp.append(DP)
                temp.append(S1)
                temp.append(S2)
                temp.append(S3)
                temp.append(str(wagetemp[0]) + "; " + str(wagetemp[1]) + "; " + str(wagetemp[2]))
                wage = round((S1 * wagetemp[0]) + (S2 * wagetemp[1]) + (S3 * wagetemp[2]), 2)  # Wage Calc
                temp.append(wage)
                # OT Calc
                ot_wage = round((OT1 / 8 * wagetemp[0]) +(OT2 / 8 * wagetemp[1]) + (OT3 / 8 * wagetemp[2]),2)
                Inc_Days = Max_Days-DP
                try:
                    Inc_Amount = float(Incentive[str(Inc_Days)])*DP if step[0] in Worker_List else 0
                except :
                    Inc_Amount = 0
            else:
                wagetemp = wagedata.get(step[0])
                if wagetemp == None:
                    wagetemp = 10
                DP, OT = 0, 0
                for i in range(5, len(step)):  # DP Calc
                    try:
                        i = list(step[i].split("::"))
                    except:
                        break
                    if i[0] == '1' or i[0] == 'P':
                        DP += 1
                        if i[1] != 'NA' :OT += float(i[1])   # OT Addition
                    if i[0] == "A":
                        if i[1] != 'NA' :OT += float(i[1])
                temp.append(DP)
                temp.append("0.0")
                temp.append("0.0")
                temp.append("0.0")
                temp.append(wagetemp)
                Inc_Days = Max_Days-DP

                try:
                    Inc_Amount = float(Incentive[str(Inc_Days)])*DP if step[0] in Worker_List else 0
                except:
                    Inc_Amount = 0
                wage = round(DP * wagetemp, 2)
                temp.append(wage)
                ot_wage = round((OT / 8 * wagetemp), 2)
            # ----------------------
            temp.append(OT)
            temp.append(ot_wage)
            temp.append(Inc_Amount)
            gross_wage = round(wage + ot_wage + Inc_Amount, 2)
            temp.append(gross_wage)
            PFS1 = 0.0 if "TEMP" in step[0] else round(gross_wage * 12 / 100, 0)  # PF Calculation
            PF = 1800.0 if PFS1 > 1800.0 else PFS1
            temp.append(PF)
            ESIS1 = 0.0 if "TEMP" in step[0] else round(gross_wage * 0.75 / 100, 0)  # ESI Calculation
            ESI = 0.0 if gross_wage > 21000.0 else ESIS1
            temp.append(ESI)
            try:
                ADV=Advance_Data[step[0]]
            except:
                ADV=0.0
            temp.append(ADV)
            netwage = round(gross_wage - PF - ESI - ADV, 2)
            temp.append(netwage)
            temp.insert(4,netwage)
            wage_proc_data.append(temp)
        Push_Table_Values(Wge.IQTB_WageReport,globals()['wage_proc_data'],False)
        Wge.IQPB_Export.setEnabled(True)
        Wge.IQPB_Mail.setEnabled(True)

    @Exception_Handle
    def Push_Data():
        if UI_Confirmation(UI_Confirm_Win, f"Please Confrim to Finalize Attendance "):
            global Advance_Data
            Advance_Data =[[key, value] for key, value in Advance_Data.items()]

            for data in Advance_Data:
                if data[1]>0:
                    sql = fr'insert into advance_details (empcode,amount,exdate)' \
                          fr'values("{data[0]}","{-data[1]}","{Cur_Date_SQL}")'
                    DB_Cmt(sql,False)

            sql = fr"select empcode, register.employee_name, SUM(amount) AS total_amount, '0.0' from advance_details inner join " \
                  "register on advance_details.empcode = register.emp_code GROUP BY empcode order by empcode"
            Push_Table_Values(Wge.IQTB_AdvanceDetail, DB_Fetch(sql, False, "LOL"), False)
            for row in range(Wge.IQTB_AdvanceDetail.rowCount()):
                item = Wge.IQTB_AdvanceDetail.item(row, 3)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)

            data =Fetch_Table_Values(Wge.IQTB_WageReport)

            data = [sublist[:4] + sublist[4+1:] for sublist in data if len(sublist) > 4]

            for step in data:
                dict = {
                    'g_date': Cur_Date_SQL,
                    'mm_yyyy': Wge.IQDE_Date.date().toString('MM-yyyy'),
                    'EmpCode': step[0],
                    'Name': step[1],
                    'F_S_Name': step[2],
                    'Team': step[3],
                    'Days_Present': step[4],
                    'S1': step[5],
                    'S2': step[6],
                    'S3': step[7],
                    'PD_Wage': step[8],
                    'Wage': step[9],
                    'OT': step[10],
                    'OT_Wages': step[11],
                    'incentive':step[12],
                    'Gross_Wages': step[13],
                    'PF': step[14],
                    'ESI': step[15],
                    'Adv': step[16],
                    'Net_Wages': float(step[17])
                }
                DB_Push_Dict(dict,'wage_db_push',False)
            UI_Confirmation(UI_Confirm_Win, f"Finalized Attendance and Pushed to Database Successfully")

    @Exception_Handle
    def Export_Wage_Report():
        xl = openpyxl.load_workbook(fr"{ldir}\EXTERNAL\Wage_Export.xlsx")
        xl.active = xl['Wage_Calc']
        xlc = xl.active
        rowc = 2
        colc = 1
        pfemp = []
        nonpfemp = []
        wage_proc_data = Fetch_Table_Values(Wge.IQTB_WageReport)
        for step in wage_proc_data:
            colc = 1
            for i in step:
                xlc.cell(row=rowc, column=colc).value = i
                colc += 1
            rowc += 1
            if "TEMP" in step[0]:
                nonpfemp.append(step)
            else:
                pfemp.append(step)
        nonpfempwage = []
        for step in nonpfemp:
            sql="select emp_code,employee_name,designation,bank_account_no,bank_name,"\
                             "ifsc_code,branch from register where emp_code ='%s'" % step[0]
            db_data = DB_Fetch(sql,False,"LOE")
            db_data.append(step[17])
            nonpfempwage.append(db_data)
        pfempwage = []
        for step in pfemp:
            sql="select emp_code,employee_name,designation,bank_account_no,bank_name,"\
                             "ifsc_code,branch from register where emp_code ='%s'" % step[0]
            db_data = DB_Fetch(sql,False,"LOE")
            db_data.append(step[17])
            pfempwage.append(db_data)


        xl.active = xl['PF']
        xlc = xl.active
        rowc = 2
        colc = 1
        for step in pfempwage:
            colc = 1
            for i in step:
                xlc.cell(row=rowc, column=colc).value = i
                colc += 1
            rowc += 1

        xl.active = xl['NonPF']
        xlc = xl.active
        rowc = 2
        colc = 1
        for step in nonpfempwage:
            colc = 1
            for i in step:
                xlc.cell(row=rowc, column=colc).value = i
                colc += 1
            rowc += 1

        xl.save(fr"{ldir}\EXTERNAL\Wage_Export_OP.xlsx")
        subprocess.run(['start', 'excel', fr"{ldir}\EXTERNAL\Wage_Export_OP.xlsx"], shell=True, check=True)

    def Fetch_Wage_Data():
        date=Wge.IQDE_Date.date().toString("MM-yyyy")
        data=DB_Fetch(fr'select * from wage_db_push where mm_yyyy = "{date}"',
                      True,"LOL")
        for i in range (len(data)):
            data[i]=data[i][2:]
            data[i].insert(4,data[i][-1])
        Push_Table_Values(Wge.IQTB_WageReport,data,False)
        Wge.toolBox.setCurrentIndex(1)
        Wge.IQPB_Finalize.setEnabled(True)
        Wge.IQPB_Generate.setEnabled(True)
        Wge.IQPB_Export.setEnabled(True)
        Wge.IQPB_Mail.setEnabled(True)

    def Check_Attendance():
        Wage_Stat_CM = DB_Fetch("select distinct mm_yyyy from wage_db_push", False, "LOE")
        if Wge.IQDE_Date.date().toString('MM-yyyy') in Wage_Stat_CM:
            Wage_Stat_CM = True
        else:
            Wage_Stat_CM = False
        Wge.IQPB_Fetch.setEnabled(Wage_Stat_CM)

    def Reset_View():
        Push_Table_Values(Wge.IQTB_WageReport,[[]],False)
        Wge.toolBox.setCurrentIndex(0)
        Wge.IQPB_Finalize.setEnabled(False)
        Wge.IQPB_Export.setEnabled(False)
        Wge.IQPB_Mail.setEnabled(False)

    # _________ Functionality_List _________
    Wge.toolBox.setCurrentIndex(0)
    Adjust_Table_Width(Wge.IQTB_AdvanceDetail,[10,25,15,15])
    Adjust_Table_Width(Wge.IQTB_WageReport, [10,30,25,15,10,5,5,5,5,22,10,5,10,12,10,10,10,15])
    Wge.IQTB_WageReport.setAlternatingRowColors(True)
    Wge.IQTB_WageReport.setStyleSheet("alternate-background-color: lightblue;")

    sql=fr"select empcode, register.employee_name, SUM(amount) AS total_amount,SUM(amount) AS total_amount  from advance_details inner join "\
    "register on advance_details.empcode = register.emp_code GROUP BY empcode order by empcode"
    Push_Table_Values(Wge.IQTB_AdvanceDetail,DB_Fetch(sql,False,"LOL"),False)

    for row in range(Wge.IQTB_AdvanceDetail.rowCount()):
        item = Wge.IQTB_AdvanceDetail.item(row, 3)
        if item:
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    Wge.IQPB_Generate.clicked.connect(lambda: Generate_Advance())
    Wge.IQPB_Generate.clicked.connect(lambda : Wageee())
    Wge.IQDE_Date.setDate(QDate.currentDate())
    Wge.IQDE_Date.dateChanged.connect(Check_Attendance)
    Check_Attendance()

    Wge.IQPB_Finalize.clicked.connect(lambda:Push_Data())
    Wge.IQPB_Export.clicked.connect(lambda:Export_Wage_Report())
    Wge.IQPB_Fetch.clicked.connect(lambda:Fetch_Wage_Data())
    Wge.IQDE_Date.dateChanged.connect(lambda : Reset_View())

# ___StandAlone Running___
if SAR == True:
    Wage_FN(Wge)
    Wge.show()
    sys.exit(app.exec_())
