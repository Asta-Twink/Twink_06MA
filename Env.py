# ___Import Statements___
from F1_BENV.B_Env import *
import copy

# ___UI Creation___
app = Qwid.QApplication(sys.argv)
Home = uic.loadUi(fr'{ldir}\F2_MODULES\BASE_WIN\UI-HomePage.ui')
UI_Confirm_Win = uic.loadUi(fr'{ldir}\F2_MODULES\BASE_WIN\UI-Confirmation_Win.ui')
Rvt = uic.loadUi(fr'{ldir}\F2_MODULES\REGISTER\UI-Revert_Win.ui')
Mtr = uic.loadUi(fr'{ldir}\F2_MODULES\MASTER_LIST\UI-Master.ui')
Wge=uic.loadUi(fr'{ldir}\F2_MODULES\WAGE\Wage.ui')
Adv = uic.loadUi(fr'{ldir}\F2_MODULES\ADVANCE\Advance.ui')
pwd= uic.loadUi(fr'{ldir}\F2_MODULES\REGISTER\password.ui')
Rgtr = uic.loadUi(fr'{ldir}\F2_MODULES\REGISTER\UI-Register.ui')
AttnPush = uic.loadUi(fr'{ldir}\F2_MODULES\ATTENDANCE\UI-Attendance_Register.ui')
AttnView = uic.loadUi(fr'{ldir}\F2_MODULES\ATTENDANCE\UI-Attendance_View.ui')
PnchBld = uic.loadUi(fr'{ldir}\F2_MODULES\PUNCH_BUILD\UI-Punch_Build.ui')
PrsPnchTrck = uic.loadUi(fr'{ldir}\F2_MODULES\PUNCH_BUILD\UI-Personal_Punch_Track.ui')

# ___Data_Fetch_Functions___
@Exception_Handle
def DB_Creation(inp,init):
    date_split=list(inp.split("-"))
    if init == True:
        for date in DateList(int(date_split[2]),int(date_split[1])):
            try:
                DB_Cmt_WOE( f"insert into attendance_track values ('{date}','YTC','{Cur_Date_SQL}')", True)
            except Exception as e:
                break
        try:
            TBL_Data=DB_Fetch(f"SHOW TABLES LIKE '{date_split[1]}_{date_split[2]}'",False,'LOE')
            print(TBL_Data)
            if f'{date_split[1]}_{date_split[2]}' in TBL_Data:
                return
        except:
            pass


    DB_Cmt(f'CREATE TABLE IF NOT EXISTS {date_split[1]}_{date_split[2]} (empcode varchar(50), primary key ('
                  f'empcode))',False)

    try:
        for i in range (1,calendar.monthrange(int(date_split[2]),int(date_split[1]))[1]+1):
            sql="alter table %s_%s add column (`%s` varchar(30))"%(date_split[1],date_split[2],str(i).zfill((2)))
            DB_Cmt_WOE(sql,False)
    except :
        pass

    db_data=DB_Fetch("select emp_code from register where active = 'Y'",False,'LOE')
    for i in db_data:
        try:
            DB_Cmt_WOE(fr"insert into {date_split[1]}_{date_split[2]} (empcode) values ('{str(i)}')",False)
        except Exception as e:
            #print('XXs', e)
            pass

def DateList(year, month):
    first_day = datetime(year, month, 1)

    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)

    current_day = first_day
    while current_day <= last_day:
        yield current_day
        current_day += timedelta(days=1)

def TD_datelist(year, month):
    today = date.today()
    first_day = date(year, month, 1)

    # Calculate the last day of the specified month and year
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    current_day = first_day

    while current_day <= today and current_day <= last_day:
        yield current_day
        current_day += timedelta(days=1)

DB_Creation(Cur_Date_NF,True)

Active_EmpC=DB_Fetch("select emp_code from register where active= 'Y'",False,'LOE')
Active_EmpList=DB_Fetch("select employee_name from register where active = 'Y'",False,'LOE')

@Exception_Handle
def Attendance_Fetch(inp):
    form = list(inp.split("-"))
    print(form)
    try:
        sql="select register.team,register.employee_name, %s_%s.* from register inner join %s_%s on " \
            "register.emp_code = %s_%s.empcode where register.active = 'Y' order by register.emp_code" % (
                         form[0], form[1], form[0], form[1], form[0], form[1])
        db_data = DB_Fetch(sql,False,"LOL")
        print(db_data[0])
        for i in range(len(db_data)):
            db_data[i].insert(0, db_data[i][2])
            del db_data[i][3]
        db_data = [[item if item is not None else "NA" for item in inner_list]for inner_list in db_data]
    except:
        db_data=[[]]
    return db_data

Attendance_View_XLF = False
def Attendance_datasplit(data,filter,XLF):
    #print(data)
    if filter == 'Attendance':
        try:
            for part in data:
                for i in range(3,len(part)):
                    try:
                        temp=list(part[i].split("::"))
                        part[i]=temp[0]
                    except:
                        pass
        except:
            pass
    elif filter == 'OT':
        for part in data:
            for i in range(3,len(part)):
                #print(part[i])
                try:
                    temp=list(part[i].split("::"))
                    part[i]=temp[1]
                except:
                    pass

    elif filter == 'Atn+ot':
        for part in data:
            for i in range(3,len(part)):
                try:
                    temp=list(part[i].split("::"))
                    part[i]=f'{temp[0]} :: {temp[1]}'
                except:
                    pass
    dataT1=[]
    dataT2=[]
    for step in data:
        dataT1.append(step[:3])
        dataT2.append(step[3:])
    if  XLF == True:
        return data
    return [dataT1,dataT2]

def Punch_Build_Data(empcode,inp):

    inp_next = (lambda d: (d + timedelta(days=1)).strftime("%Y-%m-%d"))(datetime.strptime(inp, "%Y-%m-%d"))
    #Check_In List
    CheckIN = DB_Fetch(f"SELECT it.punch_time FROM register r JOIN iclock_transaction it ON "
                     f"r.device_id = it.emp_Code where punch_time between '{inp} 06:00:00' "
                     f"AND '{inp} 23:50:00' and r.device_id='{Device_ID()[empcode]}' and punch_state = 0 ",False,"LOE")
#------------------------------------------------------------------------------------------------
    if len(CheckIN)==0:return["NA","NA","NA","NA","A::0"]
    CheckIN = min(CheckIN)
    try:C_I = CheckIN.strftime("%H:%M")
    except :C_I = "NA"
#------------------------------------------------------------------------------------------------
    CheckOUT = DB_Fetch(f"SELECT it.punch_time FROM register r JOIN iclock_transaction it ON "
                     f"r.device_id = it.emp_Code where punch_time between '{inp} 12:00:00' "
                     f"AND '{inp_next} 08:00:00' and r.device_id='{Device_ID()[empcode]}' and punch_state = 1 ",False,"LOE")
    try:
        CheckOUT = max(CheckOUT)
        C_O = CheckOUT.strftime("%H:%M")
    except :C_O = "NA"
# ------------------------------------------------------------------------------------------------
    OTIN = DB_Fetch(f"SELECT it.punch_time FROM register r JOIN iclock_transaction it ON "
                     f"r.device_id = it.emp_Code where punch_time between '{inp} 12:00:00' "
                     f"AND '{inp_next} 08:00:00' and r.device_id='{Device_ID()[empcode]}' and punch_state = 4 ",False,"LOE")
    try:
        OTIN = min(OTIN)
        OT_I = OTIN.strftime("%H:%M")
    except :OT_I = "NA"

# ------------------------------------------------------------------------------------------------
    OTOUT = DB_Fetch(f"SELECT it.punch_time FROM register r JOIN iclock_transaction it ON "
                     f"r.device_id = it.emp_Code where punch_time between '{inp} 12:00:00' "
                     f"AND '{inp_next} 12:00:00' and r.device_id='{Device_ID()[empcode]}' and punch_state = 5 ",False,"LOE")

    try:
        OTOUT = max(OTOUT)
        OT_O = OTOUT.strftime("%H:%M")
    except :OT_O = "NA"
# ------------------------------------------------------------------------------------------------

    NH = Convert_Punch_Attendance([C_I,C_O,OT_I,OT_O,])

    return [C_I,C_O,OT_I,OT_O,NH]

def Convert_Punch_Attendance(data):


    if datetime.strptime(data[0], "%H:%M").time() <=  time(11,00,0) :

        try:
            NH =  (datetime.strptime(data[1], "%H:%M") - datetime.strptime(data[0], "%H:%M")).total_seconds() / 3600

            try:
                OT = round((datetime.strptime(data[3], "%H:%M") - datetime.strptime(data[2], "%H:%M")).total_seconds() / 3600,2)
            except:
                OT = 0

            if NH < 7.5:
                NH = "1A::" + str(NH)
            else:
                NH = "1::" + str(OT)
        except Exception as e:
            print(e)
            NH = "1-IN"

    if time(14, 50, 0) <= datetime.strptime(data[0], "%H:%M").time()<= time(15, 50, 0):

        try:
            NH =  (datetime.strptime(data[1], "%H:%M") - datetime.strptime(data[0], "%H:%M")).total_seconds() / 3600
            try:
                OT = round((datetime.strptime(data[3], "%H:%M") - datetime.strptime(data[2], "%H:%M")).total_seconds() / 3600,2)
            except:
                OT = 0
            if NH < 7.5:
                NH = "2A::" + str(NH)
            else:
                NH = "2::" + str(OT)
        except:
            NH = "2-IN"

    if time(22, 00, 0) <= datetime.strptime(data[0], "%H:%M").time() <= time(23, 50, 0):
        try:
            h1, m1 = map(int, data[0].split(":"))
            h2, m2 = map(int, data[1].split(":"))

            # Convert to total minutes
            minutes_in = h1 * 60 + m1
            minutes_out = (h2 * 60 ) + m2 + (24 * 60)

            NH =  minutes_out - minutes_in /60
            try:
                OT = round((datetime.strptime(data[3], "%H:%M") - datetime.strptime(data[2], "%H:%M")).total_seconds() / 3600,2)
            except:
                OT = 0
            if NH < 7.5:
                NH = "3A::" + str(NH)
            else:
                NH = "3::" + str(OT)
        except:
            NH = "3-IN"

    return NH

def Punch_Build_Fetch(res,date):
    try:
        data=DB_Fetch(fr"select gen_attn from punch_build where emp_code = '{res}' and gen_date='{date}'",
                      False,"LOE")
        return data[0]
    except Exception as e:print(e);return 'A::0.0'

def EmpCode_Fetch(inp):
    try:
        return DB_Fetch(f"select emp_code from register where employee_name= '{inp}'",False,"LOE")[0]
    except:
        pass

@Exception_Handle
def read_image(file_path):
        with open(file_path, 'rb') as file:
            return file.read()

Dept=DB_Fetch("select distinct description from Dep_list;",False,"LOE")
Team = DB_Fetch("select distinct team from register;",False,"LOE")
Blod_grp=['A+','A-','B+','B-','O+','O-','AB+','AB-']


def AttendaceFetch_Day(inp):
    date_split=inp.split("-")
    return DB_Fetch(fr"select empcode,`{date_split[2]}` from {date_split[1]}_{date_split[0]}",False,"DIC")

def Emp_code_Gen(type):
    if type :
        db_data = DB_Fetch( "SELECT MAX(CAST(SUBSTRING(emp_code, 4) AS UNSIGNED)) +1 AS max_value FROM register "
                                "WHERE emp_code LIKE 'SIL%';", False, "LOE")[0]
        return str("SIL" + str(db_data).zfill(3))
    else:
        db_data = DB_Fetch( "SELECT MAX(CAST(SUBSTRING(emp_code, 5) AS UNSIGNED)) +1 AS max_value FROM register "
                                "WHERE emp_code LIKE 'TEMP%';", False, "LOE")[0]
        return str("TEMP" + str(db_data).zfill(3))

def resize_image(image_data, new_width, new_height):
    image = Image.open(BytesIO(image_data))
    resized_image = image.resize((new_width, new_height))
    buffered = BytesIO()
    resized_image.save(buffered, format="JPEG")  # You can change the format if needed (JPEG, PNG, etc.)
    return buffered.getvalue()

def Fetch_Employee_ID(inp):
    return DB_Fetch(f"select UID from register where employee_name ='{inp}'",False,"LOE")[0]

@Exception_Handle
def Fetch_Employee_Info(inp):
    return DB_Fetch(f"select * from register where UID = '{Fetch_Employee_ID(inp)}'",False,"LOE")

@Exception_Handle
def Incentive_List():
    return DB_Fetch("select total_days, Incentive from incentive_list", True, "DIC")

Incentive = DB_Fetch("select total_days, Incentive from incentive_list", True, "DIC")

print(Incentive)

# Worker_List = DB_Fetch("Select emp_code from register where Worker = 'Y'",False,"LOE")

Device_ID = lambda : DB_Fetch("select emp_code,device_id from register",False,"DIC")

print(DB_Fetch("select emp_code,device_id from register",False,"DIC"))
print(Device_ID()['SIL003'])
print(Punch_Build_Data('SIL003','2025-03-29'))