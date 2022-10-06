from Env import *
import Env

def AttendanceViewLay():

    head1=['Emp.Code','Team','Name']
    headwidth1=[15,30,30]
    head2=[]
    headwidth2=[]
    #----
    for i in range (1,32):
        head2.append(str(i).zfill(2))
        headwidth2.append(7)
    #print(todatemy)
    globals()['atnvwdata']=attendance_fetch(todatemy)
    globals()['fltrdata']=datasplit(copy.deepcopy(globals()['atnvwdata']),"Attendance")
    globals()['avfind']=0
    TL1=ms.Table(values=fltrdata[0][:((avfind+1)*25)], headings=head1,
                justification='centre', enable_events=True,
                auto_size_columns=False,
                row_height=20,
                col_widths=headwidth1,
                num_rows=26,
                font=fstyle,
                #alternating_row_color=ms.theme_button_color_background(),
                 vertical_scroll_only=False,
                 hide_vertical_scroll=True,
                key="TL1_Atview")
    TL2=ms.Table(values=fltrdata[1][:((avfind+1)*25)], headings=head2,
                justification='centre', enable_events=True,
                auto_size_columns=False,
                row_height=20,
                col_widths=headwidth2,
                size=(100,500),
                num_rows=26,
                font=fstyle,
                vertical_scroll_only=False,
                hide_vertical_scroll=True,
                #alternating_row_color=ms.theme_button_color_background(),
                key="TL2_Atview",
                 pad=(0,0))
    #print(data)
    #print(atnvwdata)
    layout=[[ms.Sizer(swi-1500),ms.Text("Attendance View",font=fstylehd,justification='center')],
            [ms.Combo(['Attendance','OT','Expenses','Atn+ot','DP_List'],default_value="Attendance",
                      enable_events=True, key='atnvwfltr',size=(15,4),font=fstyle),ms.Sizer(swi -500),
             ms.Text("Date",font=fstyle,size=(7,1)),ms.Input(todatemy,disabled= True,enable_events=True,
                                                             disabled_readonly_background_color=ms.theme_background_color(),
                                                             size=(8,2),font=fstyle,key='atvwdate'),
             ms.CalendarButton(" ",target='atvwdate',format="%m-%Y")],
            [ms.Frame("Output",layout=[[ms.Column([[ms.Column([[TL1]],size=(770,shi-200),pad=(0,0)),TL2]])],
                                        [ms.Sizer(0,20)],
                                        [ms.Button("<",key='avlswap',font=fstyle), ms.Button("Export",key='avxlexp',font=fstyle),
                                         ms.Button("Mail", key='avxlmail', font=fstyle),
                                         ms.Button("XL Fetch", key='avxlfetch', font=fstyle),
                                         ms.Button(">", key='avrswap', font=fstyle)
                                         ],
                                       ],size=(swi-70,shi-100),font=fstyle,element_justification='center')]
            ]
    return layout

def AdvanceoptLay():
    layout=[[ms.Sizer(350,0),ms.Column([[ms.Text("Advance Details",font=fstyle)],
            [ms.Input(todatemy,font=fstyle,key='advdateinp',size=(8,1),background_color=ms.theme_background_color(),enable_events=True),],
           [ms.Frame("Regsiter",[[ms.Table(values=advancefetch(todatemy),headings=["Date","Empcode","Employee Name","Amount"],
                      justification='centre',
                      auto_size_columns=False,
                      col_widths=[15,15,30,15],

                      row_height=20,
                      num_rows=20,
                      font=fstyle,
                      right_click_selects=True,
                      right_click_menu=[[], ["Remove Advance"]],
                      enable_click_events=True, key="TL_AdvView",enable_events=True
                      )]],font=fstyle)],
            [ms.Frame("Generate Advance",
                     [
                     [ms.Text("Employee Code",font=fstyle,size=(15,1)),ms.Input("",font=fstyle,size=(30,1),key="adv_empid",enable_events=True)],
                     [ms.Text("Employee Name", font=fstyle, size=(15, 1)), ms.Text("", font=fstyle, size=(30, 1),key="adv_empname")],
                     [ms.Text("Advance Amount", font=fstyle, size=(15, 1)), ms.Input("", font=fstyle, size=(30, 1),key="adv_amount",)],
                        [ms.Button("Generate",font=fstyle,key="adv_generate")],
                     ],font=fstyle,element_justification='center'),
            ],
    ],size=(swi,shi),element_justification='center'),]]
    return layout

'''
TestMenu=ms.Window("", AdvanceoptLay(),location=(0,0),element_justification='center')
while True:
    event,values = TestMenu.read()
'''
def AttendaceViewFn(Menu,event,values):
    if event == 'atnvwfltr':
        globals()['fltrdata'] = datasplit(copy.deepcopy(globals()['atnvwdata']), values['atnvwfltr'])
        globals()['avfind'] = 0
        Menu['TL1_Atview'].update(values=fltrdata[0][:((avfind+1)*25)])
        Menu['TL2_Atview'].update(values=fltrdata[1][:((avfind+1)*25)])
    if event == 'atvwdate':
        globals()['atnvwdata'] = attendance_fetch(values['atvwdate'])
        globals()['fltrdata'] = datasplit(copy.deepcopy(globals()['atnvwdata']), values['atnvwfltr'])
        globals()['avfind'] = 0
        Menu['TL1_Atview'].update(values=fltrdata[0][:((avfind+1)*25)])
        Menu['TL2_Atview'].update(values=fltrdata[1][:((avfind+1)*25)])
    if event == 'avxlexp':
        xl=openpyxl.load_workbook(filename=r'C:\Twink_06MA\Master_Files\Atn_Exp.xlsx')
        for step in ['Attendance','OT','Expenses',"DP_List"]:
            xl.active=xl[step]
            xlc=xl.active
            Env.avxlop = True
            data = attendance_fetch(values['atvwdate'])
            atndata=datasplit(copy.deepcopy(data),step)
            crow=2
            ccol=1
            for part in atndata:
                #print(part)
                for i in range(len(part)):
                    xlc.cell(row=crow,column=ccol).value=part[i]
                    ccol+=1
                crow+=1
                ccol = 1
        xl.save(filename=r'C:\Twink_06MA\Master_Files\Atn_ExpT1.xlsx')
        os.system(r'C:\Twink_06MA\Master_Files\Atn_ExpT1.xlsx')
    if event == 'adv_empid':
        Menu['adv_empname'].update(empnamefetch(values['adv_empid']))
    if event == 'adv_generate':
        chk=ms.popup_ok("Please confirm to generate advance amount",font=fstyle)
        if chk == "OK":
            mycursor.execute("insert into advance_details (empcode,"
                             "amount,exdate) values('%s','%s','%s')"%(values['adv_empid'],values['adv_amount'],todatestr))
            mydb.commit()
            Menu['TL_AdvView'].update(values=(advancefetch(todatemy)))
            Menu['adv_empid'].update("")
            Menu['adv_empname'].update("")
            Menu['adv_amount'].update("")
        else:
            pass
    if event == 'TL_AdvView':
        data = Menu['TL_AdvView'].get()
        globals()['advcrow'] = [data[row] for row in values[event]]
        #print(advcrow)
    if event == 'Remove Advance':
        chk = ms.popup_ok("Please Confirm to Delete", font=fstyle)
        if chk == "OK":
            mpass=ms.popup_get_text("Enter Master Password to proceed", font=fstyle)
            if mpass == MasterPass:
                mycursor.execute("delete from advance_details where "
                        "empcode='%s' and exdate = '%s'" %(advcrow[0][1],(datetime.strptime(advcrow[0][0], "%d-%m-%Y").strftime("%Y-%m-%d"))))
                mydb.commit()
                Menu['TL_AdvView'].update(values=advancefetch(todatenf))
            else:
                ms.popup_ok("Wrong Pasword", font=fstyle)
    if event == 'advdateinp':
        try:
            Menu['TL_AdvView'].update(values=(advancefetch(values['advdateinp'])))
        except:
            pass
    if event == 'avxlmail':
        data=attendance_fetch(values['atvwdate'])
        xl=openpyxl.load_workbook(filename=r'C:\Twink_06MA\Master_Files\Atn_Exp.xlsx')
        for step in ['Attendance','OT','Expenses']:
            xl.active=xl[step]
            xlc=xl.active
            atndata=datasplit(copy.deepcopy(data),step)
            crow=2
            ccol=1
            for part in atndata:
                for i in range(len(part)):
                    xlc.cell(row=crow,column=ccol).value=part[i]
                    ccol+=1
                crow+=1
                ccol = 1

        xl.save(filename=r'C:\Twink_06MA\Master_Files\Atn_ExpT1.xlsx')
        maillist = popup_select(mailid_fetch(False,""))
        for i in maillist:
            mail_content = "PFA"
            sender_address = 'asta.sunilindustries@gmail.com'
            sender_pass = 'uxzgkfvkdzuxwpad'
            # Setup the MIME
            receiver_address = mailid_fetch(True,i)
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = "Attendance_Output"
            message.attach(MIMEText(mail_content, 'plain'))
            attach_file_name = r'C:\Twink_06MA\Master_Files\Atn_ExpT1.xlsx'
            attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            payload.add_header('Content-Disposition ', 'attachment',
                               filename='Attendance_Output.xlsx')
            message.attach(payload)
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            #print('Mail Sent')
        ms.popup_auto_close("Mail Successfully Sent", font=fstyle, no_titlebar=True)
    if event == 'avxlfetch':
        pwchk = ms.popup_get_text("Enter password to proceed further ", password_char='*', size=(20, 1), font=fstyle,
                                keep_on_top=True)
        if pwchk == MasterPass:
            chk = ms.popup_ok("Please Confirm to Fetch", font=fstyle)
            if chk == "OK":
                xl = openpyxl.load_workbook(filename=r"C:\Twink_06MA\Master_Files\Atn_ExpT1.xlsx")
                xlc1 = xl['Attendance']
                xlc2 = xl['OT']
                xlc3 = xl['Expenses']
                xlc4 = xl['DP_List']
                Data = []
                pushdate = list(values['atvwdate'].split("-"))
                for i in range(int(xlc1.max_row)-1):
                    temp = []
                    cursor = xlc1.cell(row=i + 2, column=1)
                    temp.append(cursor.value)
                    for j in range(calendar.monthrange(int(pushdate[1]),int(pushdate[0]))[1]):
                        c1 = xlc1.cell(row=i + 2, column=j + 4)
                        if c1.value == None:
                            temp.append("A")
                        c2 = xlc2.cell(row=i + 2, column=j + 4)
                        if c2.value == None:
                            temp.append("0")
                        c3 = xlc3.cell(row=i + 2, column=j + 4)
                        if c3.value == None:
                            temp.append("0.0")
                        c4 = xlc4.cell(row=i + 2, column=j + 4)
                        if c4.value == None:
                            temp.append("28")
                        temp.append(str(c1.value) + "," + str(c2.value) + "," + str(c3.value) + "," + str(c4.value))
                    Data.append(temp)
                OPXL = openpyxl.Workbook()
                XLC = OPXL.active
                pushdate = list(values['atvwdate'].split("-"))
                rowc = 1
                colc = 1
                for step in Data:
                    colc = 1
                    for i in step:
                        XLC.cell(row=rowc, column=colc).value = i
                        colc += 1
                    rowc += 1
                print(step)
                for step in Data:
                    for i in range(len(step)-1):
                        try:
                            sql = "update %s_%s set `%s` = '%s' where empcode = '%s'" % \
                                  (pushdate[0], pushdate[1],str(i+1).zfill(2) , step[i+1], step[0])
                            #print(sql)
                            mycursor.execute(sql)
                        except Exception as e:
                            ms.popup(e,font=fstyle)
                            break
                mydb.commit()
                OPXL.save(r'C:\Twink_06MA\Logs\ATXLFETCH\%s_%s.xlsx'%(todate.strftime("%d-%m-%Y-%H-%M"),values['atvwdate']))
                globals()['fltrdata'] = datasplit(copy.deepcopy(globals()['atnvwdata']), values['atnvwfltr'])
                globals()['avfind'] = 0
                Menu['TL1_Atview'].update(values=fltrdata[0][:((avfind + 1) * 25)])
                Menu['TL2_Atview'].update(values=fltrdata[1][:((avfind + 1) * 25)])
                ms.popup_auto_close("Updated Successfully",font=fstyle)
    if event == 'avrswap':
        globals()['avfind'] += 1
        Menu['TL2_Atview'].update(values=fltrdata[1][globals()['avfind']*25:((globals()['avfind']+1)*25)])
        Menu['TL1_Atview'].update(values=fltrdata[0][globals()['avfind']*25:((globals()['avfind']+1)*25)])
    if event == 'avlswap':
        globals()['avfind'] -= 1
        Menu['TL2_Atview'].update(values=fltrdata[1][globals()['avfind']*25:((globals()['avfind']+1)*25)])
        Menu['TL1_Atview'].update(values=fltrdata[0][globals()['avfind']*25:((globals()['avfind']+1)*25)])
#v6.1