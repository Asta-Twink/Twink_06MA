import copy
import PySimpleGUI as ms
import mysql.connector
from datetime import *
import os
import io
from PIL import Image
import base64
from win32api import GetSystemMetrics
import os
import calendar
import openpyxl
from PIL import Image
import pprint
import smtplib
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import traceback
import sys
from prettytable import PrettyTable
from openpyxl.styles.alignment import Alignment

mydb = mysql.connector.connect( host='localhost', user="root", passwd="MSeGa@1109",)
mycursor = mydb.cursor()
mycursor.execute('Use Twink_06ma')
mydb.commit

mycursor.execute("select value from nrdb order by description")
nrdb_data=list(sum(mycursor.fetchall(),()))
MasterPass=nrdb_data[2]
#print(MasterPass)
shi=GetSystemMetrics(1)-100
swi=GetSystemMetrics(0)

fstyle=(nrdb_data[0],int(nrdb_data[1]))
fstylehd=(nrdb_data[0],int(nrdb_data[1])+2)
del nrdb_data
file_types = [("JPEG (*.jpg)", "*.jpg"),("All files (*.*)", "*.*")]
os.chdir('C:\Twink_06MA\Icons')
with open("choose.png", "rb") as image_file:
 chse = base64.b64encode(image_file.read())
with open("browse.png", "rb") as image_file:
 browse = base64.b64encode(image_file.read())
with open("load.png", "rb") as image_file:
 load = base64.b64encode(image_file.read())
with open("logo.png", "rb") as image_file:
 logo = base64.b64encode(image_file.read())

atvar=None
avxlop=None
todate=datetime.today()
print(todate)
todatestr=todate.strftime("%Y-%m-%d")
todatenf=todate.strftime("%d-%m-%Y")
todatemy=todate.strftime("%m-%Y")
file_types = [("JPEG (*.jpg)", "*.jpg"),("All files (*.*)", "*.*")]
team_list=["PF Native","Jharkand","Assam","Odisha","NPF Native",]
def border(element, color, width=3):
    if color is None:
        color = ms.theme_background_color()
    element.Widget.configure(highlightcolor=color, highlightbackground=color,
        highlightthickness=width)

def MAILFetch():
    mycursor.execute("select * from mail_list")
    return ([list(x) for x in mycursor.fetchall()])

def CCWORKFetch():
    mycursor.execute("select * from cc_work_list")
    return ([list(x) for x in mycursor.fetchall()])

def MUWFetch():
    mycursor.execute("select * from user_details")
    return ([list(x) for x in mycursor.fetchall()])

def CCWFetch():
    mycursor.execute("select * from cleaning_crew")
    return ([list(x) for x in mycursor.fetchall()])

def EmpdataFetch(type):
    if type=="PF":
        mycursor.execute("select Emp_code, employee_name,f_sp_name,Gender,Phone_no,team "
                         "from register where active_status = 'Y' and ET ='PF' and shift_work = 'No' order by employee_name")
        S1=[list(x) for x in mycursor.fetchall()]
        mycursor.execute('select Emp_code, employee_name,f_sp_name,Gender,Phone_no,'
                         'team from register '
                         'where active_status = "Y" and ET ="PF" and shift_work = "Yes" order by employee_name')
        S2 = [list(x) for x in mycursor.fetchall()]
        #print(S1+S2)
        return S1+S2
    if type=="Non PF":
        mycursor.execute("select Emp_code, employee_name,f_sp_name,Gender,Phone_no,team "
                         "from register where active_status = 'Y' and ET ='Non PF' and shift_work = 'No' order by employee_name")
        S1=[list(x) for x in mycursor.fetchall()]
        mycursor.execute('select Emp_code, employee_name,f_sp_name,Gender,Phone_no,'
                         'team from register '
                         'where active_status = "Y" and ET ="Non PF" and shift_work = "Yes" order by employee_name')
        S2 = [list(x) for x in mycursor.fetchall()]
        #print(S1 + S2)
        return S1+S2

def DB_Creation(inp):
    date_split=list(inp.split("-"))
    mycursor.execute('CREATE TABLE IF NOT EXISTS %s_%s (empcode varchar(50), primary key (empcode))'%(date_split[1],date_split[2]))
    #print(inp)
    mydb.commit()
    try:
        for i in range (1,calendar.monthrange(int(date_split[2]),int(date_split[1]))[1]+1):
            sql="alter table %s_%s add column (`%s` varchar(30))"%(date_split[1],date_split[2],str(i).zfill((2)))
            mycursor.execute(sql)
    except:
        pass
    mycursor.execute("select emp_code from register where active_status = 'Y'" )
    db_data=list(sum(mycursor.fetchall(),()))

    for i in db_data:
        try:
            mycursor.execute("insert into %s_%s (empcode) values ('%s')"%(date_split[1],date_split[2],str(i)))
            mydb.commit()
        except:
            pass
    try:
        mycursor.execute("insert into %s_%s (empcode) values ('counter')" % (date_split[1], date_split[2]))
        mydb.commit()
    except:
        pass

#DB_Creation("01-10-2022")

def datasplit(data,filter):
    #print(data)
    if filter == 'Attendance':
        try:
            for part in data:
                part.pop(3)
                for i in range(3,len(part)):
                    try:
                        temp=list(part[i].split(","))
                        part[i]=temp[0]
                    except:
                        pass
        except:
            pass
    elif filter == 'OT':
        for part in data:
            part.pop(3)
            for i in range(3,len(part)):
                #print(part[i])
                try:
                    temp=list(part[i].split(","))
                    part[i]=temp[1]
                except:
                    pass
    elif filter == 'Expenses':
        for part in data:
            part.pop(3)
            for i in range(3,len(part)):
                try:
                    temp=list(part[i].split(","))
                    part[i]=temp[2]
                except:
                    pass
    elif filter == 'Atn+ot':
        for part in data:
            part.pop(3)
            for i in range(3,len(part)):
                try:
                    temp=list(part[i].split(","))
                    part[i]=str(temp[0])+";",str(temp[1])
                except:
                    pass
    elif filter == 'DP_List':
        mycursor.execute("select UID,Description from dep_list")
        db_data = mycursor.fetchall()
        dplist = {int(x[0]): (x[1]) for x in db_data}
        #print(dplist)
        for part in data:
            part.pop(3)
            for i in range(3,len(part)):
                try:
                    temp=list(part[i].split(","))
                    part[i]=temp[3]
                except:
                    pass
    if  avxlop == True:
        globals()['avxlop'] = False
        return data
    dataT1=[]
    dataT2=[]
    for step in data:
        dataT1.append(step[:3])
        dataT2.append(step[3:])
    return [dataT1,dataT2]

def attendance_Wfetch(inp,chk):

    form = list(inp.split("-"))
    if chk == 0:
        try:
            mycursor.execute("select register.employee_name,register.f_sp_name,register.team,register.office_staff, %s_%s.* "
                             "from register inner join %s_%s on register.emp_code = %s_%s.empcode where register.active_status = 'Y' order by register.emp_code" % (
                             form[0], form[1], form[0], form[1], form[0], form[1]))
            db_data = [list(x) for x in mycursor.fetchall()]

            for i in range(len(db_data)):
                db_data[i].insert(0, db_data[i][4])
                del db_data[i][5]
            #print(db_data)
        except:
            db_data=[[]]
    else:
        try:
            mycursor.execute("select register.employee_name,register.f_sp_name,register.team,register.office_staff, %s_%s.* "
                             "from register inner join %s_%s on register.emp_code = %s_%s.empcode where register.active_status = 'Y' "
                             "and team = 'Odisha' order by register.emp_code" % (
                             form[0], form[1], form[0], form[1], form[0], form[1]))
            db_data = [list(x) for x in mycursor.fetchall()]
            #print(db_data)
            for i in range(len(db_data)):
                db_data[i].insert(0, db_data[i][4])
                del db_data[i][5]
                del db_data[i][-15:]
            #print(db_data)
        except:
            db_data=[[]]

    return db_data

def attendance_fetch(inp):
    form = list(inp.split("-"))
    #print(form)
    try:
        mycursor.execute("select register.team,register.employee_name,register.office_staff, %s_%s.* "
                         "from register inner join %s_%s on register.emp_code = %s_%s.empcode where register.active_status = 'Y' order by register.emp_code" % (
                         form[0], form[1], form[0], form[1], form[0], form[1]))

        db_data = [list(x) for x in mycursor.fetchall()]
        #print(db_data)
        for i in range(len(db_data)):
            db_data[i].insert(0, db_data[i][3])
            del db_data[i][4]
            #del db_data[i][3]
        #print(db_data)
    except:
        db_data=[[]]
    return db_data

def wage_fetch():

    mycursor.execute("Select emp_code,base_salary from register where shift_work='No' ")
    db_data=[list(x) for x in mycursor.fetchall()]
    #print(db_data)
    dict_data={x[0]:float(x[1]) for x in db_data}
    #print(dict_data)
    mycursor.execute("Select emp_code,shift_1_salary,shift_2_salary,shift_3_salary from register where shift_work='Yes'")
    db_data=[list(x) for x in mycursor.fetchall()]
    output=[]
    for step in db_data:
        temp=[]
        temp.append(step[0])
        temp1=[]
        for i in range (1,4):
            temp1.append(float(step[i]))
        temp.append(temp1)
        output.append(temp)
    dict_data_SY= {x[0]:x[1] for x in output}
    dict_data.update(dict_data_SY)
    #print(dict_data)
    return dict_data

wage_fetch()

def user_pass(name):
    sql = "select user_password from user_details where `user_name`='%s'" % name
    #print(sql)
    mycursor.execute(sql)

    return [list(x) for x in mycursor.fetchall()]

def user_name():
    sql="select user_name from user_details"
    mycursor.execute(sql)
    return list(sum(mycursor.fetchall(),()))

def remove_data(Menu,event,values):
    if event == "user_data"or 'wrk_data' or 'mail_data':
        data = Menu[event].get()
        inx = [data[row] for row in values[event]]
    return inx

def Emp_code_Gen(type):
        if type=="PF":
            mycursor.execute("SELECT emp_code FROM register WHERE emp_code LIKE 'SIL0%'")
            db_data=mycursor.fetchall()
            #print(mycursor.fetchall())
            return  str("SIL" + str((int("0" if (db_data)==None else (len(db_data))) + 1)).zfill(3))
        if type=="Non PF":
            mycursor.execute("SELECT emp_code FROM register WHERE emp_code LIKE 'SILTEMP%'")
            db_data=mycursor.fetchall()
            return "SILTEMP" + str((int("0" if (db_data)==None else str(len(db_data))) + 1)).zfill(3)

def DepListFetch():
    mycursor.execute("select * from dep_list")
    return ([list(x) for x in mycursor.fetchall()])

mycursor.execute("select description from dep_list")
dep_list=list(sum(mycursor.fetchall(),()))

mycursor.execute("select count(*) from register where active_status = 'Y'")
empcount=mycursor.fetchall()[0][0]
tempdate=todatenf.split("-")
try:
    mycursor.execute("select `%s` from %s_%s where empcode = 'counter'" % (tempdate[0], tempdate[1], tempdate[2]))
    atstat= "created" if mycursor.fetchall()[0][0] == "v" else "To be Created"
except:
    atstat = "To be Created"
#atstat="created"
def mailreport(inp):
    mycursor.execute("select UID,Description from dep_list")
    db_data = mycursor.fetchall()
    dplist = {int(x[0]): (x[1]) for x in db_data}
    dateform = inp.split("-")
    mycursor.execute(
        "select empcode,`%s` from %s_%s where empcode !='counter'" % (dateform[0], dateform[1], dateform[2]))
    db_data = [list(x) for x in mycursor.fetchall()]

    db_data_Fn = []
    wage_data = wage_fetch()

    for i in db_data:
        if i[1] != None:
            temp = list(i[1].split(","))

            if temp[0] in ['1', '2', '3', 'P']:
                try:
                    i[1] = dplist.get(int(temp[3]))
                except:
                    i[1] = "Wander"
                wage = wage_data.get(i[0])
                i[0] = wage
                if type(i[0]) == list:
                    i[0] = wage[int(temp[0]) - 1]
                else:
                    i[0]
            db_data_Fn.append(i)

        else:
            pass
    mycursor.execute("select Description from dep_list order by Description")
    dep_data = list(sum(mycursor.fetchall(), ()))
    output = []
    for i in dep_data:
        count = 0
        wage = 0
        for j in db_data_Fn:
            if j[1] == i:
                count += 1
                wage += round(j[0],2)
        output.append([i, count, wage])

    #print(output)
    ctot,wtot=0,0.0
    tabular_table = PrettyTable()
    tabular_table.field_names =  ["<   Department   >","<  Count  > ","Net Wage"]
    for i in output:
        tabular_table.add_row(i)
        ctot+=i[1]
        wtot+=i[2]
    tabular_table.add_row(["-------------", "----", "-------"])
    tabular_table.add_row(["Total",ctot,round(wtot,0)])
    ms.popup_ok(tabular_table,title="Employee Split",font=("Courier New",10),)
    maillist = popup_select(mailid_fetch(False, ""))
    sys.stdout.close()
    DS1 = todate.strftime("%Y-%m-%d-%H-%M")
    sys.stdout = open('C:\Twink_06MA\Logs\Atn_Mail_OP_%s.txt' % DS1, 'w')
    print(tabular_table)
    sys.stdout.close()
    os.system('C:\Twink_06MA\Logs\Atn_Mail_OP_%s.txt' % DS1)
    sys.stdout = open('C:\Twink_06MA\Logs\%s.txt' % todate.strftime("%Y-%m-%d-%H-%M"), 'w')

    if maillist == None:
        return
    for i in maillist:
        sender_address = 'asta.sunilindustries@gmail.com'
        sender_pass = 'uxzgkfvkdzuxwpad'
        # Setup the MIME
        receiver_address = mailid_fetch(True, i)
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = "Daily Attendance Mail - %s"%inp
        message.attach(MIMEText(tabular_table.get_html_string(), 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
    ms.popup_auto_close("Mail Successfully Sent",font=fstyle,no_titlebar=True)

def advancefetch(inp):
    dateform=inp.split("-")
    mycursor.execute("select DATE_FORMAT(exdate,'%s'), empcode, register.employee_name, amount from advance_details inner join register"
                     " on advance_details.empcode = register.emp_code "
                     "where month(exdate) = '%s' and year(exdate) = '%s'"%(r'%d-%m-%Y',dateform[0],dateform[1]))
    return [list(x) for x in mycursor.fetchall()]

def empnamefetch(inp):
    try:
        mycursor.execute("select employee_name from register where emp_code = '%s'"%inp)
        return mycursor.fetchall()[0][0]
    except:
        pass

def wageadvfetch(inp,datefo):
    dateform=datefo.split("-")
    mycursor.execute("select amount from advance_details where empcode='%s' and "
                     "month(exdate) = '%s' and year(exdate) = '%s'"%(inp,dateform[0],dateform[1]))
    db_data=list(sum(mycursor.fetchall(),()))
    #print(db_data)
    return sum(db_data)

def shiftcheck(inp):
    mycursor.execute("select shift_work from register where emp_code='%s'"%inp)
    chk=mycursor.fetchall()[0][0]
    return True if chk=="Yes" else False

def popup_select(the_list):
    layout = [[ms.Listbox(the_list,key='_LIST_',size=(45,5),select_mode=ms.LISTBOX_SELECT_MODE_MULTIPLE,bind_return_key=True),ms.OK()]]
    window = ms.Window('Select the mail id to send',layout=layout)
    event, values = window.read()
    window.close()
    del window

    return values['_LIST_']

def mailid_fetch(x,inp):
    if x == False:
        mycursor.execute("select name_ from mail_list")
        return list(sum(mycursor.fetchall(),()))
    else:
        mycursor.execute("select mail_id from mail_list where name_='%s'"%inp)
        return mycursor.fetchall()[0][0]

def deplistfetch():
    mycursor.execute("select description from dep_list")
    return list(sum(mycursor.fetchall(),()))
def Emp_Revert_Fetch():
    mycursor.execute("select emp_code, employee_name,Phone_no,date_of_birth,date_of_exit,reason from register where active_status = 'N' order by employee_name")
    return [list(x) for x in mycursor.fetchall()]
atpatmt = 'N'
#v6.1
