#---Initiation
from Env import *
import Attendance_Push
import Attendance_View
import Register
import Wage_Calc
import Master_User
import Cleaning_Crew
import CC_Attendence_View
#---Custom DB Declaration

sys.stdout = open('C:\Twink_06MA\Logs\%s.txt'%todate.strftime("%Y-%m-%d-%H-%M") , 'w')
mycursor.execute('Use Twink_06ma')
mydb.commit()
ms.theme('Topanga')
#--- Base Menu Declaration
MenuDef = [
           ['Navigate',   ['Home','Register','Master User']],
           ['Attendance', ['Create','View','CC_Attendence','CC_View','Advance']],
           ['Reports',    ['Wages_Monthly Calc',"Wages_Category Split"]],
]
#--- Base Layout Declaration
BaseLayout=[
            [ms.Sizer(swi/2-200,0),ms.Image(source=logo)],
            [ms.Sizer(swi/2-200,0) ,ms.Text("SUNIL INDUSTRIES LIMITED",font=("Courier New",18),justification='center'),],
            [],
            [ms.Sizer(0,150)],
            [ms.Sizer(600,500),ms.Frame(layout=[
                [ms.Text('Date',font=fstyle,size=(20,1)),ms.Input(todatenf,font=fstyle,size=(10,1),key="SW_date",enable_events=True)],
                [ms.Text('No. of Employees',font=fstyle,size=(20,1)),ms.Text(empcount,font=fstyle,size=(10,1))],
                [ms.Text('Attendance Status',font=fstyle,size=(20,1)),ms.Text(atstat,font=fstyle,size=(15,1))],
                [ms.Sizer(150,0),ms.Button("Mail",disabled= False if atstat == "created" else True,font=fstyle,key='mailreport')]
            ],size=(400,140),font=fstyle,title="Infographics")]
            ]

layout=[[ms.Menu    (MenuDef, key='MENU',font=fstyle)],
        [
        ms.Column  (BaseLayout,key="base",visible=True,size=(swi,shi),element_justification='center'),
        ms.Column  (Register.RegsiterLay(),key='register',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (Master_User.Master_User_GUI(),key='mumneu',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (Attendance_Push.AttendancePushLay(),key='atnpush',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (Attendance_View.AttendanceViewLay(),key='atnview',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (Wage_Calc.WageCalcLay(),key='wagecalc',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (Cleaning_Crew.crew_att_gui(),key='cc_att',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (CC_Attendence_View.CC_View_GUI(),key='c_view',visible=False,size=(swi,shi)),
        ms.Column  (Wage_Calc.WageCalcLay(),key='wagecalc',visible=False,size=(swi,shi),element_justification='center'),
        ms.Column  (Attendance_View.AdvanceoptLay(), key='advopt', visible=False, size=(swi, shi),element_justification='center'),
        ms.Column  (Wage_Calc.CategorySplitWage(), key='cwsvw', visible=False, size=(swi, shi),element_justification='center')

        ]]

MenuList=["base","register",'atnpush','atnview','wagecalc','mumneu','c_view','cc_att','advopt','cwsvw']

Menu = ms.Window("Twink_Attendance",layout,location=(0,0),size=(swi,shi),element_justification='center',return_keyboard_events=True)

while True:
    try:
        event, values = Menu.read()
        print(event)
        if event == ms.WIN_CLOSED:
            Menu.close()
            break
        if event == "Home" or  event[:6] == 'Escape':
            try:
                mycursor.execute(
                    "select `%s` from %s_%s where empcode = 'counter'" % (tempdate[0], tempdate[1], tempdate[2]))
                atstat = "created" if mycursor.fetchall()[0][0] == "v" else "To be Created"
            except:
                atstat = "To be Created"
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['base'].update(visible=True)

        if event == 'Register' or  event[:2] == 'F1' :
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['register'].update(visible=True)

        if event == 'Create' or event[:2] == 'F2':
            Menu['SW_date'].block_focus(block=True)
            Menu['atpdate'].block_focus(block=True)
            Menu['atpers'].block_focus(block=True)

            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['atnpush'].update(visible=True)

        if event == 'View' or event[:2] == 'F3':
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['atnview'].update(visible=True)

        if event == 'Master User' or event[:2] == 'F9' :
            chk = ms.popup_get_text("Enter password to enter Master User ", password_char='*', size=(20, 1), font=fstyle,
                                     keep_on_top=True)
            if chk == MasterPass:
                for i in MenuList:
                    Menu[i].update(visible=False)
                Menu['mumneu'].update(visible=True)
            else:
                ms.popup_auto_close("Please try again",font=fstyle, no_titlebar=True, auto_close_duration=2)

        if event == 'CC_Attendence':
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['cc_att'].update(visible=True)

        if event == 'CC_View':
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['c_view'].update(visible=True)

        if event == 'Wages_Monthly Calc' or event[:2] == 'F4':
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['wagecalc'].update(visible=True)

        if event == 'Advance':
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['advopt'].update(visible=True)

        Register.RegisterFn(Menu,event,values)
        Attendance_Push.AttendancePushFn(Menu,event,values)
        Attendance_View.AttendaceViewFn(Menu,event,values)
        Wage_Calc.WageCalcFn(Menu,event,values)
        Master_User.Master_User(Menu,event,values)
        Cleaning_Crew.cc_att_(event, values, Menu)
        CC_Attendence_View.c_view_db(event, values, Menu)

        if event == 'mailreport':
            chk=ms.popup_ok("Please confrim to send mail",font=fstyle,no_titlebar=True)
            if chk == "OK":
                mailreport(values['SW_date'])

        if event == 'SW_date':
            tempMdate = values['SW_date'].split("-")
            try:
                print("x")
                mycursor.execute(
                    "select `%s` from %s_%s where empcode = 'counter'" % (tempMdate[0], tempMdate[1], tempMdate[2]))
                atstat = "created" if mycursor.fetchall()[0][0] == "v" else "To be Created"
            except:
                atstat = "To be Created"
            if atstat == "created":
                Menu['mailreport'].update(disabled=False)
            else:
                Menu['mailreport'].update(disabled=True)

        if event == 'Wages_Category Split':
            for i in MenuList:
                Menu[i].update(visible=False)
            Menu['cwsvw'].update(visible=True)


    except Exception as e:
        tb = traceback.format_exc()
        ms.popup_animated(None)
        ms.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

sys.stdout.close()

#v6.3