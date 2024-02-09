# ___StandAlone INIT___
import traceback
from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Wage_FN(Wge):
    def attendance_Wfetch(inp, chk):
        form = list(inp.split("-"))
        if chk == 0:
            try:
                db_data = DB_Fetch(dbc,
                                   "select register.employee_name,register.f_sp_name,register.team,register.office_staff, %s_%s.* "
                                   "from register inner join %s_%s on register.emp_code = %s_%s.empcode where register.active_status = 'Y' order by register.emp_code" % (
                                       form[0], form[1], form[0], form[1], form[0], form[1]), False, "LOL")
                # db_data = [list(x) for x in mycursor.fetchall()]

                for i in range(len(db_data)):
                    db_data[i].insert(0, db_data[i][4])
                    del db_data[i][5]
                # print(db_data)
            except:
                db_data = [[]]
        else:
            try:
                db_data = DB_Fetch(dbc,
                                   "select register.employee_name,register.f_sp_name,register.team,register.office_staff, %s_%s.* "
                                   "from register inner join %s_%s on register.emp_code = %s_%s.empcode where register.active_status = 'Y' "
                                   "and team = 'Odisha' order by register.emp_code" % (
                                       form[0], form[1], form[0], form[1], form[0], form[1]), False, "LOL")
                # db_data = [list(x) for x in mycursor.fetchall()]
                # print(db_data)
                for i in range(len(db_data)):
                    db_data[i].insert(0, db_data[i][4])
                    del db_data[i][5]
                    del db_data[i][-15:]
                # print(db_data)
            except:
                db_data = [[]]
        return db_data
    def wage_fetch():
        db_data = DB_Fetch(dbc,
                           "Select emp_code,shift_1_salary,shift_2_salary,shift_3_salary from register where shift_work='Yes'",
                           False, "LOL")
        # db_data=[list(x) for x in mycursor.fetchall()]
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
        # print(dict_data)
        return dict_data
    def shiftcheck(inp):
        chk = DB_Fetch(dbc, "select shift_work from register where emp_code='%s'" % inp, False, "LOL")[0][0]
        # chk=mycursor.fetchall()[0][0]
        return True if chk == "Yes" else False
    data = attendance_Wfetch(Cur_Date_MY, 0)
    print("daa", data)
    data = attendance_Wfetch(Cur_Date_MY, 0)
    wagedata = wage_fetch()
    globals()['wage_proc_data'] = []
    for step in data:
        try:
            # print(step)
            temp = []
            for i in range(4):  # EMP Details addition
                temp.append(step[i])
            # print(step,"Step")
            # print(temp)
            chk = shiftcheck(step[0])
            # print(chk, "Chk")
            if chk == True:  # if Emp is Shift resource
                # print(step)
                wagetemp = wagedata.get(step[0])
                temp.append("0.0")
                S1, S2, S3, OT1, OT2, OT3 = 0, 0, 0, 0, 0, 0

                for i in range(5, len(step)):  # Custom Shift Calc
                    # print("Step",step)
                    try:
                        i = step[i].split("::")
                        # print(i,"i")
                    except:
                        continue
                    if i[0] == '1':
                        S1 += 1
                        OT1 += int(i[1])  # OT Addition
                    if i[0] == '2':
                        S2 += 1
                        OT2 += int(i[1])  # OT Addition
                    if i[0] == '3':
                        S3 += 1
                        OT3 += int(i[1])  # OT Addition
                    if i[0] == "A":
                        pass
                    try:
                        if i[0][1] == "A":
                            if i[0][0] == '1':
                                OT1 += int(i[1])
                            if i[0][0] == '2':
                                OT2 += int(i[1])
                            if i[0][0] == '3':
                                OT3 += int(i[1])
                    except:
                        print("hello")
                    OT = OT1 + OT2 + OT3

                    # OT+=int(float(i[1]))
                # temp.append(OT)
                temp.append(S1)
                temp.append(S2)
                temp.append(S3)
                temp.append(str(wagetemp[0]) + "," + str(wagetemp[1]) + "," + str(wagetemp[2]))
                wage = round((S1 * wagetemp[0]) + (S2 * wagetemp[1]) + (S3 * wagetemp[2]), 2)  # Wage Calc
                temp.append(wage)
                # OT Calc
                ot_wage = round((OT / 8 * wagetemp[0]), 2)
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
                    if len(i) != 4:
                        continue
                    if i[0] == 'P':
                        DP += 1
                        OT += int(i[1])  # OT Addition
                    if i[0] == "A":
                        OT += int(i[1])

                temp.append(DP)
                temp.append("0.0")
                temp.append("0.0")
                temp.append("0.0")
                temp.append(wagetemp)
                wage = round(DP * wagetemp, 2)
                temp.append(wage)
                # print(OT,wagetemp)
                ot_wage = round((OT / 8 * wagetemp), 2)
            temp.append(OT)
            temp.append(ot_wage)
            # temp.append(incentive)
            # print(incentive)
            gross_wage = wage + ot_wage
            temp.append(gross_wage)
            PFS1 = 0.0 if "TEMP" in step[0] else round(gross_wage * 12 / 100, 0)  # PF Calculation
            PF = 1800.0 if PFS1 > 1800.0 else PFS1
            temp.append(PF)
            ESIS1 = 0.0 if "TEMP" in step[0] else round(gross_wage * 0.75 / 100, 0)  # ESI Calculation
            ESI = 0.0 if gross_wage > 21000.0 else ESIS1
            temp.append(ESI)
            # ADV = wageadvfetch(step[0], values['wcdateinp'])
            # temp.append(ADV)
            netwage = gross_wage - PF - ESI
            temp.append(netwage)
            wage_proc_data.append(temp)
        except Exception as e:
            traceback.print_exc()
    print("Wage", wage_proc_data)
    Push_Table_Values(Wge.IQTB_WageReport, wage_proc_data, False)

# ___StandAlone Running___
if SAR == True:
    Wage_FN(Wge)
    Wge.show()
    sys.exit(app.exec_())
