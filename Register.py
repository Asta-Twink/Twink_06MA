import base64
import os

from Env import *


def RegsiterLay():
    layout = [[ms.Text("Employee Register", font=fstylehd)],
              [ms.Sizer(swi - 400, 0),
               ms.Button("Export", font=fstyle, key='empexp'),
               ms.Button("Mail", font=fstyle, key='empmail'),
               ms.Button("Add", font=fstyle, key='empadd')],
              [ms.Frame("Employee Data",
                        [[ms.Table(values=EmpdataFetch("PF"),
                                   headings=["Employee Code", "Name", "Father/Spouse Name", "Gender", "Phone No.",
                                             "Team"],
                                   justification='centre', enable_events=True, auto_size_columns=False, row_height=30,
                                   col_widths=[15, 40, 40, 10, 20, 15],
                                   right_click_selects=True,
                                   right_click_menu=[[], ["Update Employee", "Remove"]],
                                   enable_click_events=True, size=(swi - 70, shi - 120), key="emp_data", font=fstyle)]],
                        font=fstyle, size=(swi - 50, shi - 180), element_justification='center')],
              [ms.Button("Cleaning Crew", font=fstyle, key='ccwin'),ms.Sizer(swi-300,0),ms.Checkbox("Non PF",key="etcnge",enable_events=True,default=False,)]]

    return layout

def RegisterFn(Menu, event, values):

    def Cleaning_Crew_GUI():
        layout = [[ms.Text("Cleaning Crew Register", font=fstylehd)],
                  [ms.Sizer(swi - 900, 0),
                   ms.Button("Add", font=fstyle, key='ccwadd')],

                  [ms.Frame("Cleaning Crew Data",
                            [[ms.Table(values=CCWFetch(),
                                       headings=["UID", "Name", "Phone No","Pan No","Bank Account No"],
                                       justification='centre', enable_events=True, auto_size_columns=False,
                                       row_height=30,
                                       col_widths=[10, 20, 20,20,20],
                                       right_click_selects=True,
                                       right_click_menu=[[], ["Remove"]],
                                       enable_click_events=True, size=(swi - 100, shi - 300), key="ccw_data",
                                       font=fstyle)]],
                            font=fstyle, size=(swi - 585, shi - 300), element_justification='center')],
                  [ms.Frame("Adding Crew",[[ms.Text("Name",size=(20,1)),ms.Sizer(45,0),ms.Text("Phone No",size=(20,1)),ms.Sizer(40,0),
                                            ms.Text("Pan No",size=(20,1)),ms.Sizer(40,0),ms.Text("Bank Account No",size=(20,1))],
                                           [ms.Input("", size=(20, 1), do_not_clear=False, key='c_name', font=fstyle),ms.Sizer(5,0),
                                            ms.Input("", size=(20, 1), do_not_clear=False, key='c_ph.no', font=fstyle),
                                            ms.Input("", size=(20, 1), do_not_clear=False,key='c_pan.no', font=fstyle),
                                            ms.Input("", size=(20, 1), do_not_clear=False,key='c_bkac.no', font=fstyle),
                                            ms.Button("Add",font=fstyle,key="add_crow")]],visible=False,key="add_frame")]]
        return layout

    def Employee_Add_GUI():
        Employee_Details = [
            [ms.Text("Employee Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e1', font=fstyle)],
            [ms.Text("Emp Code:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(Emp_code_Gen("PF"), size=(30, 1),disabled=True, enable_events=True,do_not_clear=True, key='e2', font=fstyle)],
            [ms.Text("Designation/Dept.:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Combo(deplistfetch(),enable_events=True, size=(29, 1), key='e3', font=fstyle)],
            [ms.Text("ESIC NO:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e4', font=fstyle)],
            [ms.Text("UAN NO:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e5', font=fstyle)],
            [ms.Text("Pan No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e6', font=fstyle)],
            [ms.Text("Aadhar No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e7', font=fstyle)],
            [ms.Text("Address:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Multiline("", size=(28, 3), enable_events=True,do_not_clear=True, key='e8', font=fstyle)],
            [ms.Text("Married Status:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("Yes", "ms", size=(5, 1), enable_events=True, key='m_yes', font=fstyle),
             ms.Radio("No", "ms", size=(5, 1), enable_events=True, key='m_no', font=fstyle)],
            [ms.Text("Father/Spouse Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e9', font=fstyle)],
            [ms.Text("Gender:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("M","gender", size=(5, 1), key='m', font=fstyle),
             ms.Radio("F","gender", size=(5, 1), key='f', font=fstyle),
             ms.Radio("O","gender", size=(5, 1), key='o', font=fstyle)],
            [ms.Text("Shift Work:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("Yes","sw", size=(5, 1),enable_events=True, key='yes', font=fstyle),
             ms.Radio("No","sw", size=(5, 1),enable_events=True, key='no', font=fstyle)],
            [ms.Text("Base salary:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("0.00", size=(30, 1),disabled=True, enable_events=True,do_not_clear=True, key='e10', font=fstyle,disabled_readonly_background_color=ms.theme_background_color())],
            [ms.Text("Shift  salary:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("0.00", size=(9, 1),tooltip="shift 1 salary",disabled=True,disabled_readonly_background_color=ms.theme_background_color(), enable_events=True,do_not_clear=True, key='e11', font=fstyle),
             ms.Input("0.00", size=(9, 1),tooltip="shift 2 salary",disabled=True,disabled_readonly_background_color=ms.theme_background_color(), enable_events=True,do_not_clear=True, key='e12', font=fstyle),
             ms.Input("0.00", size=(9, 1),tooltip="shift 3 salary",disabled=True, disabled_readonly_background_color=ms.theme_background_color(),enable_events=True,do_not_clear=True, key='e13', font=fstyle)],
            [ms.Text("Phone No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e14', font=fstyle)],
            [ms.Text("Blood Group:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Combo(("O+","O-","A+"),enable_events=True, size=(30, 1), key='e15', font=fstyle)],
            [ms.Text("Bank Account Number:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e16', font=fstyle)],
            [ms.Text("Bank Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e17', font=fstyle)],
            [ms.Text("IFSC Code:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e18', font=fstyle)],
            [ms.Text("Branch:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e19', font=fstyle)],
            [ms.Text("Date of Birth :", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(26, 1), enable_events=True,do_not_clear=True, key='e20', font=fstyle),ms.Sizer(4, 0),
             ms.CalendarButton('Choose',image_data=chse, format='%Y-%m-%d', target='e20', font=fstyle, size=(6, 1), key='date1'), ],
            [ms.Text("Date of Joining :", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(26, 1), enable_events=True,do_not_clear=True, key='e21', font=fstyle),ms.Sizer(4, 0),
             ms.CalendarButton('Choose',image_data=chse, format='%Y-%m-%d', font=fstyle, target='e21', size=(6, 1), key='date1'), ],
            [ms.Text("photo:", justification='left', size=(20, 1), font=fstyle),
             ms.Input("", size=(19, 1), enable_events=True,do_not_clear=True, key='e22', font=fstyle),
             ms.FileBrowse(file_types=file_types,size=(6,1),enable_events=True, target="e22",key="b1", font=fstyle),
             ms.Button("Load",image_data=load, font=fstyle,size=(5,1), key="load pimg"), ms.Sizer(2, 0),
             ],
            [ms.Text("Specimen Signature:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(19, 1), enable_events=True,do_not_clear=True, key='e23', font=fstyle),
             ms.FileBrowse(file_types=file_types,size=(6,1),enable_events=True, target="e23",key="b2", font=fstyle),
             ms.Button("Load",image_data=load,size=(5,1), font=fstyle, key="load simg"), ms.Sizer(2, 0),
             ],
            [ms.Text("Nominee Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e24', font=fstyle)],
            [ms.Text("Nominee Phone No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(30, 1), enable_events=True,do_not_clear=True, key='e25', font=fstyle)],
            [ms.Text("Nominee photo:", justification='left', size=(20, 1), font=fstyle),
             ms.Input("", size=(19, 1), enable_events=True,do_not_clear=True, key='e26', font=fstyle),
             ms.FileBrowse(file_types=file_types,size=(6,1),enable_events=True, target="e26",key="b3", font=fstyle),
             ms.Button("Load",image_data=load,size=(5,1), font=fstyle, key="load nimg"), ms.Sizer(2, 0),
             ],
            [ms.Text("ET :", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("PF","etype", size=(5, 1),enable_events=True, key='pf', font=fstyle),
             ms.Radio("Non PF","etype", size=(6, 1),enable_events=True, key='non pf', font=fstyle),ms.Sizer(10,0),
             ms.Checkbox("Office Staff",key="o_staff",font=fstyle)],
        ]
        Employee_Image = [[ms.Image(key="-IMAGE-")]]
        Signature_Image = [[ms.Image(key="-IMAGE2-")]]
        Nominee_Image = [[ms.Image(key="-IMAGE3-")]]
        Employee_Add_GUI = [[
            ms.Column([[ms.Frame("Employee Details", Employee_Details, font=fstyle)]]),
            ms.Column([
                [ms.Frame("Employee Photo", Employee_Image,size=(170,200), font=fstyle)],
                [ms.Frame("Signature", Signature_Image,size=(170,100), font=fstyle)],
                [ms.Frame(" Nominee Photo", Nominee_Image,size=(170,200), font=fstyle)]])],
            [ms.Button("Add", key="add employee", font=fstyle)],[ms.Text(" "),ms.Sizer(3,0)],[ms.Text(" ")],[ms.Text(" ")],[ms.Text(" ")],[ms.Text(" ")],[ms.Text(" ")]]

        return Employee_Add_GUI

    def Add_Employee(event, values):
        if event == "add employee":
            for i in range(1,22):
                chk=True
                if values['e' + str(i)] == "":
                    chk = False
                    break
            for i in [24,25]:
                chk=True
                if values['e' + str(i)] == "":
                    chk = False
                    break
            if chk == True:
                try:
                    shutil.copy(values['e22'],r'C:\Twink_06MA\Image_Data\%s_img.jpg'%values['e2'])
                    shutil.copy(values['e23'], r'C:\Twink_06MA\Image_Data\%s_simg.jpg' % values['e2'])
                    shutil.copy(values['e26'], r'C:\Twink_06MA\Image_Data\%s_nimg.jpg' % values['e2'])
                except:
                    pass

                dict = {'employee_name': values['e1'], 'emp_code': values['e2'],'designation':values['e3'],'esic_no':values['e4'],'uan_no':values['e5'],'pan_no': values['e6'],
                        'aadhar_no': values['e7'],'address': values['e8'],'marriage_status':"Yes" if values["m_yes"]==True else "No", 'f_sp_name': values['e9'],
                        'gender':"M" if values['m']==True else "F" if values['f']==True else "O" ,
                        'shift_work':"Yes" if values["yes"]==True else "No",'base_salary': values['e10'],
                        'shift_1_salary': values['e11'],'shift_2_salary': values['e12'],'shift_3_salary': values['e13'],
                        'phone_no': values['e14'],'blood_group': values['e15'],'bank_account_no': values['e16'], 'bank_name': values['e17'],
                        'ifsc_code': values['e18'],'branch': values['e19'],'date_of_birth': values['e20'],
                        'date_of_join': values['e21'],
                        'nominee_name': values['e24'],'nominee_phone_no': values['e25'],
                        'ET':"PF" if values['pf']==True else "Non PF",'office_staff':'yes'if values["o_staff"]==True else 'no'}

                placeholders = ', '.join(['%s'] * len(dict))
                columns = ', '.join(dict.keys())
                sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('register',
                                                               columns, placeholders)
                mycursor.execute(sql, list(dict.values()))
                mydb.commit()

                ms.PopupTimed("Successfully Added",
                              title='Employee Added',
                              button_type=0,
                              auto_close=True,
                              auto_close_duration=1)
                eMenu.close()
                DB_Creation(todatenf)
            else:
                ms.popup("Enter valid info..!")

    def Employee_update_GUI(epc):
        mycursor.execute("select * from register where emp_code='%s'" % epc)
        ep_dat= list(mycursor.fetchall())

        ep_data=ep_dat[0]
        #print("ep_data",ep_data)
        if ep_data[9]=="Yes":
            m_val=[True,False]
        else:
            m_val=[False,True]
        if ep_data[11]=="M":
            g_val=[True,False,False]
        elif ep_data[11]=="F":
            g_val=[False,True,False]
        else :
            g_val=[False,False,True]
        if ep_data[12]=="Yes":
            s_val=[True,False]
        else:
            s_val=[False,True]
        if ep_data[31]=="PF":
            et_val=[True,False]
        elif ep_data[31]=="Non PF":
            et_val=[False,True]
        if ep_data[33]=="yes":
            o_f=True
        elif ep_data[33] == "no":
            o_f=False
        Employee_Details = [
            [ms.Text("Employee Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[1], size=(30, 1), enable_events=True,do_not_clear=True, key='u1', font=fstyle)],
            [ms.Text("Emp Code:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[2], size=(30, 1),disabled=True, enable_events=True,do_not_clear=True, key='u2', font=fstyle)],
            [ms.Text("Designation:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Combo(("Worker","Supervisor","Manager"),default_value= ep_data[3],enable_events=True, size=(29, 1), key='u3', font=fstyle)],
            [ms.Text("ESIC NO:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[4], size=(30, 1), enable_events=True,do_not_clear=True, key='u4', font=fstyle)],
            [ms.Text("UAN NO:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[5], size=(30, 1), enable_events=True,do_not_clear=True, key='u5', font=fstyle)],
            [ms.Text("Pan No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[6], size=(30, 1), enable_events=True,do_not_clear=True, key='u6', font=fstyle)],
            [ms.Text("Aadhar No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[7], size=(30, 1), enable_events=True,do_not_clear=True, key='u7', font=fstyle)],
            [ms.Text("Address:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Multiline(ep_data[8], size=(28, 3), enable_events=True,do_not_clear=True, key='u8', font=fstyle)],
            [ms.Text("Married Status:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("Yes", "ms", size=(5, 1),default=m_val[0], enable_events=True, key='m_yes', font=fstyle),
             ms.Radio("No", "ms", size=(5, 1),default=m_val[1], enable_events=True, key='m_no', font=fstyle)],
            [ms.Text("Father/Spouse Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[10], size=(30, 1), enable_events=True,do_not_clear=True, key='u9', font=fstyle)],
            [ms.Text("Gender:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("M","gender",default=g_val[0], size=(5, 1), key='m', font=fstyle),
             ms.Radio("F","gender",default=g_val[1], size=(5, 1), key='f', font=fstyle),
             ms.Radio("O","gender",default=g_val[2], size=(5, 1), key='o', font=fstyle)],
            [ms.Text("Shift Work:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("Yes","sw",default=s_val[0], size=(5, 1),enable_events=True, key='yes', font=fstyle),
             ms.Radio("No","sw",default=s_val[1], size=(5, 1),enable_events=True, key='no', font=fstyle)],
            [ms.Text("Base salary:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[13], size=(30, 1),disabled=False, enable_events=True,do_not_clear=True, key='u10', font=fstyle)],
            [ms.Text("Shift  salary:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[14], size=(9, 1),tooltip="shift 1 salary",disabled=False, enable_events=True,do_not_clear=True, key='u11', font=fstyle),
             ms.Input(ep_data[15], size=(9, 1),tooltip="shift 2 salary",disabled=False, enable_events=True,do_not_clear=True, key='u12', font=fstyle),
             ms.Input(ep_data[16], size=(9, 1),tooltip="shift 3 salary",disabled=False, enable_events=True,do_not_clear=True, key='u13', font=fstyle)],
            [ms.Text("Phone No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[17], size=(30, 1), enable_events=True,do_not_clear=True, key='u14', font=fstyle)],
            [ms.Text("Blood Group:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Combo(("O+","O-","A+"),default_value= ep_data[18],enable_events=True, size=(30, 1), key='u15', font=fstyle)],
            [ms.Text("Bank Account Number:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[19], size=(30, 1), enable_events=True,do_not_clear=True, key='u16', font=fstyle)],
            [ms.Text("Bank Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[20], size=(30, 1), enable_events=True,do_not_clear=True, key='u17', font=fstyle)],
            [ms.Text("IFSC Code:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[21], size=(30, 1), enable_events=True,do_not_clear=True, key='u18', font=fstyle)],
            [ms.Text("Branch:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[22], size=(30, 1), enable_events=True,do_not_clear=True, key='u19', font=fstyle)],
            [ms.Text("Date of Birth :", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[23], size=(26, 1), enable_events=True,do_not_clear=True, key='u20', font=fstyle),ms.Sizer(4, 0),
             ms.CalendarButton('Choose',image_data=chse, format='%d-%m-%y', target='e20', font=fstyle, size=(6, 1), key='date1'), ],
            [ms.Text("Date of Joining :", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[24], size=(26, 1), enable_events=True,do_not_clear=True, key='u21', font=fstyle),ms.Sizer(4, 0),
             ms.CalendarButton('Choose',image_data=chse, format='%d-%m-%y', font=fstyle, target='u21', size=(6, 1), key='date1'), ],
            [ms.Text("photo:", justification='left', size=(20, 1), font=fstyle),
             ms.Input("", size=(19, 1), enable_events=True,do_not_clear=True, key='u22', font=fstyle),
             ms.FileBrowse(file_types=file_types,size=(6,1),enable_events=True, target="u22",key="b1", font=fstyle),
             ms.Button("Load",image_data=load, font=fstyle,size=(5,1), key="load pimg"), ms.Sizer(2, 0),
             ],
            [ms.Text("Specimen Signature:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input("", size=(19, 1), enable_events=True,do_not_clear=True, key='u23', font=fstyle),
             ms.FileBrowse(file_types=file_types,size=(6,1),enable_events=True, target="u23",key="b2", font=fstyle),
             ms.Button("Load",image_data=load,size=(5,1), font=fstyle, key="load simg"), ms.Sizer(2, 0),
             ],
            [ms.Text("Nominee Name:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[28], size=(30, 1), enable_events=True,do_not_clear=True, key='u24', font=fstyle)],
            [ms.Text("Nominee Phone No:", justification='left', size=(20, 1), font=fstyle, ),
             ms.Input(ep_data[29], size=(30, 1), enable_events=True,do_not_clear=True, key='u25', font=fstyle)],
            [ms.Text("Nominee photo:", justification='left', size=(20, 1), font=fstyle),
             ms.Input(r"", size=(19, 1), enable_events=True,do_not_clear=True, key='u26', font=fstyle),
             ms.FileBrowse(file_types=file_types,size=(6,1),enable_events=True, target="u26",key="b3", font=fstyle),
             ms.Button("Load",image_data=load,size=(5,1), font=fstyle, key="load nimg"), ms.Sizer(2, 0),
             ],
            [ms.Text("ET :", justification='left', size=(20, 1), font=fstyle, ),
             ms.Radio("PF","etype",default=et_val[0], size=(5, 1),enable_events=True, key='pf', font=fstyle),
             ms.Radio("Non PF","etype",default=et_val[1], size=(6, 1),enable_events=True, key='non pf', font=fstyle),
             ms.Checkbox("Office Staff",default=o_f, key="o_staffu", font=fstyle)
             ],
        ]
        try:
            filename = r"C:\Twink_06MA\Image_Data\%s_img.jpg"%epc
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((300, 300))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                Photo=bio.getvalue()
            else:
                Photo=None
            filename = r"C:\Twink_06MA\Image_Data\%s_simg.jpg"%epc
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((300, 300))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                Signature=bio.getvalue()
            else:
                Signature=None
            filename = r"C:\Twink_06MA\Image_Data\%s_nimg.jpg"%epc
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((300, 300))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                Nominee=bio.getvalue()
            else:
                Nominee=None
        except:
            Photo,Signature,Nominee=None,None,None
        #print(Photo,Signature,Nominee)
        #---
        Employee_Image = [[ms.Image(data=Photo, key="-IMAGE-",subsample=3)]]
        Signature_Image = [[ms.Image(data=Signature,key="-IMAGE2-",size=(170, 100),subsample=10)]]
        Nominee_Image = [[ms.Image(data=Nominee,key="-IMAGE3-",subsample=3)]]
        Employee_Update_GUI = [[
            ms.Column([[ms.Frame("Employee Details", Employee_Details, font=fstyle)]]),
            ms.Column([
                [ms.Frame("Employee Photo", Employee_Image ,size=(200, 240), font=fstyle)],
                [ms.Frame("Signature",  Signature_Image,size=(200, 100), font=fstyle)],
                [ms.Frame(" Nominee Photo", Nominee_Image, size=(200, 240), font=fstyle)]])],
            [ms.Button("Update",key="updateemp", font=fstyle)]]
        return Employee_Update_GUI

    def Update_Employee(event, values):
        for i in range(1, 22):
            chk = True
            if values['u' + str(i)] == "":
                chk = False
                break
        for i in [24, 25]:
            chk = True
            if values['u' + str(i)] == "":
                chk = False
                break
        #print(chk)
        if chk == True:
            if values['u22']!="":
                try:
                    os.remove(r"C:\Twink_06MA\Image_Data\%s_img.jpg"%values['u2'])
                except:
                    pass
                try:
                    shutil.copy(values['u22'], r"C:\Twink_06MA\Image_Data\%s_img.jpg" % values['u2'])
                except:
                    pass
            if values['u23']!="":
                try:
                    os.remove(r"C:\Twink_06MA\Image_Data\%s_nimg.jpg"%values['u2'])

                except:
                    pass
                try:
                    shutil.copy(values['u23'], r"C:\Twink_06MA\Image_Data\%s_simg.jpg" % values['u2'])
                except:
                    pass

            if values['u26']!="":
                try:
                    os.remove(r"C:\Twink_06MA\Image_Data\%s_simg.jpg"%values['u2'])
                except:
                    pass
                try:
                    shutil.copy(values['u26'], r"C:\Twink_06MA\Image_Data\%s_simg.jpg" % values['u2'])
                except:
                    pass
            dict = {'employee_name': values['u1'],'designation':values['u3'],'esic_no':values['u4'],'uan_no':values['u5'],
                    'aadhar_no': values['u6'],'address': values['u7'],'marriage_status':'Yes' if values["m_yes"]==True else "No", 'f_sp_name': values['u9'],
                    'gender':"M" if values['m']==True else "F" if values['f']==True else "O" ,
                    'shift_work':'Yes' if values["yes"]==True else "No",'base_salary': values['u10'],
                    'shift_1_salary': values['u11'],'shift_2_salary': values['u12'],'shift_3_salary': values['u13'],
                    'phone_no': values['u14'],'blood_group':values['u15'],'bank_account_no': values['u16'], 'bank_name': values['u17'],
                    'ifsc_code': values['u18'],'branch': values['u19'],'date_of_birth': values['u20'],
                    'date_of_join': values['u21'],
                    'nominee_name': values['u24'],'nominee_phone_no': values['u25'],
                    'ET':"PF" if values['pf']==True else "Non PF",'office_staff':"yes" if values['o_staffu']==True else"no"}

            c_name=[key for key in dict]
            c_data=[dict[i] for i in dict]
            for i in range(len(c_name)):
                sql='UPDATE `twink_06ma`.`register` SET `%s` = "%s" WHERE (`emp_code` = "%s");' %(c_name[i],c_data[i],values['u2'] )
                mycursor.execute(sql)

            mydb.commit()

            ms.PopupTimed("Successfully updated",
                          title='Employee Added',
                          button_type=0,
                          auto_close=True,
                          auto_close_duration=1)
            uMenu.close()
            Menu["emp_data"].update(values=EmpdataFetch("PF"))
        else:
            ms.popup("Enter valid info..!")

    if event =="ccwin":
        ccwMenu = ms.Window("Add Crew", [[ms.Column(Cleaning_Crew_GUI(), scrollable=True, size=(960, 700), element_justification='centre')]])
        while True:
            event, values = ccwMenu.read()
            if event == ms.WIN_CLOSED:
                ccwMenu.close()
                break
            if event =="ccwadd":
                ccwMenu["add_frame"].update(visible=True)
            if event =="add_crow":
                if values['c_name'] and values['c_bkac.no'] and values['c_ph.no'] and values['c_pan.no'] !="":
                    sql ="INSERT INTO cleaning_crew ( crew_name,phone_no,pan_no,bank_account ) VALUES ( '%s','%s','%s','%s' )" % (values['c_name'],values['c_ph.no'],values['c_pan.no'],values['c_bkac.no'])
                    mycursor.execute(sql)
                    mydb.commit()
                    ccwMenu['ccw_data'].update(values=CCWFetch())
                    ccwMenu["add_frame"].update(visible=False)
                else:
                    ms.popup_auto_close("Fill the details", font=fstyle, no_titlebar=True)
            if event == "ccw_data":
                data = ccwMenu['ccw_data'].get()
                globals()['crow1'] = [data[row] for row in values[event]]
            if event =="Remove":
                chk = ms.popup_ok("Please Confirm to Delete", font=fstyle)
                if chk == "OK":
                    mycursor.execute("DELETE FROM `twink_06ma`.`cleaning_crew` WHERE (`UID` = %d);" % int(crow1[0][0]))
                    mydb.commit()
                    ccwMenu['ccw_data'].update(values=CCWFetch())
            if event =='c_ph.no':
                if len(values['c_ph.no']) > 10:
                    ccwMenu['c_ph.no'].update(background_color ="red")
                else:
                    ccwMenu['c_ph.no'].update(background_color=ms.DEFAULT_INPUT_ELEMENTS_COLOR)

    if event == 'empadd':
        eMenu = ms.Window("Add Employee", [
            [ms.Column(Employee_Add_GUI(), scrollable=True, size=(760, 700), element_justification='centre')]],
                          finalize=True)
        while True:
            event, values = eMenu.read()
            if event == ms.WIN_CLOSED:
                eMenu.close()
                break

            if event == 'add employee':
                Add_Employee(event, values)
                if values["pf"] == True:
                    Menu["emp_data"].update(values=EmpdataFetch("PF"))
                if values["non pf"] == True:
                    Menu["emp_data"].update(values=EmpdataFetch("Non PF"))
                    Menu["etcnge"].update(value=True)

            if event == "load pimg":
                filename = values["e22"]
                if os.path.exists(filename):
                    image = Image.open(values["e22"])
                    image.thumbnail((300, 300))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    eMenu["-IMAGE-"].update(data=bio.getvalue())

            if event == "e1":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e4":
                if values[event] != "":
                    try:
                        if int(values[event]) / int(values[event]) == 1:
                            #print("hi")
                            if len(values[event]) == 10:
                                #print(len(values[event]))
                                border(eMenu[event], "green")
                        if len(values[event]) > 10:
                            border(eMenu[event], "red")
                        if len(values[event]) < 10:
                            border(eMenu[event], None)
                        #print("X")
                    except ValueError:
                        border(eMenu[event], "red")
                    #print("lenght", len(values[event]))
            if event == "e5":
                if values[event] != "":
                    try:
                        if int(values[event]) / int(values[event]) == 1:
                            #print("hi")
                            if len(values[event]) == 10:
                                #print(len(values[event]))
                                border(eMenu[event], "green")
                        if len(values[event]) > 10:
                            border(eMenu[event], "red")
                        if len(values[event]) < 10:
                            border(eMenu[event], None)
                        #print("X")
                    except ValueError:
                        border(eMenu[event], "red")
                    #print("lenght", len(values[event]))
            if event == "e6":
                if values[event] != "":
                    if values[event].isalnum() == True and len(values[event]) == 10:
                        border(eMenu[event], "green")
                    if len(values[event]) > 10:
                        border(eMenu[event], "red")
                    if len(values[event]) < 10:
                        border(eMenu[event], None)
            if event == "e7":
                if values[event] != "":
                    try:
                        if int(values[event]) / int(values[event]) == 1:
                            #print("hi")
                            if len(values[event]) == 12:
                                #print(len(values[event]))
                                border(eMenu[event], "green")
                        if len(values[event]) > 12:
                            border(eMenu[event], "red")
                        if len(values[event]) < 12:
                            border(eMenu[event], None)
                        #print("X")
                    except ValueError:
                        border(eMenu[event], "red")
                    #print("lenght", len(values[event]))
            if event == "e8":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e9":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e10":
                try:
                    if values[event] != "":
                        if float(values[event]) / float(values[event]) == 1:
                            border(eMenu[event], "green")
                    if values[event] == "":
                        border(eMenu[event], None)
                except ValueError:
                    border(eMenu[event], "red")
            if event == "e11":
                try:
                    if values[event] != "":
                        if float(values[event]) / float(values[event]) == 1:
                            border(eMenu[event], "green")
                    if values[event] == "":
                        border(eMenu[event], None)
                except:
                    border(eMenu[event], "red")
            if event == "e12":
                try:
                    if values[event] != "":
                        if float(values[event]) / float(values[event]) == 1:
                            border(eMenu[event], "green")
                    if values[event] == "":
                        border(eMenu[event], None)
                except :
                    border(eMenu[event], "red")
            if event == "e13":
                try:
                    if values[event] != "":
                        if float(values[event]) / float(values[event]) == 1:
                            border(eMenu[event], "green")
                    if values[event] == "":
                        border(eMenu[event], None)
                except ValueError:
                    border(eMenu[event], "red")
            if event == "e14":

                if values[event] != "":
                    try:
                        if int(values[event]) / int(values[event]) == 1:
                            #print("hi")
                            if len(values[event]) == 10:
                                #print(len(values[event]))
                                border(eMenu[event], "green")
                        if len(values[event]) > 10:
                            border(eMenu[event], "red")
                        if len(values[event]) < 10:
                            border(eMenu[event], None)
                        #print("X")
                    except ValueError:
                        border(eMenu[event], "red")

            if event == "e16":
                if values[event] != "":
                    if values[event].isalnum() == True:
                        if len(values[event]) > 8 and len(values[event]) < 19:
                            border(eMenu[event], "green")
                    if len(values[event]) > 18:
                        border(eMenu[event], "red")
                    if len(values[event]) < 9:
                        border(eMenu[event], None)
                    if values[event].isalnum() == False:
                        border(eMenu[event], "red")
            if event == "e17":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e18":
                if values[event] != "":
                    if values[event].isalnum() == True and len(values[event]) == 11:
                        border(eMenu[event], "green")
                    if len(values[event]) > 11:
                        border(eMenu[event], "red")
                    if len(values[event]) < 11:
                        border(eMenu[event], None)
                    if values[event].isalnum() == False:
                        border(eMenu[event], "red")
            if event == "e19":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e20":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e21":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e22":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e23":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e24":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")
            if event == "e25":
                if values[event] != "":
                    try:
                        if int(values[event]) / int(values[event]) == 1:
                            #print("hi")
                            if len(values[event]) == 10:
                                #print(len(values[event]))
                                border(eMenu[event], "green")
                        if len(values[event]) > 10:
                            border(eMenu[event], "red")
                        if len(values[event]) < 10:
                            border(eMenu[event], None)
                        #print("X")
                    except ValueError:
                        border(eMenu[event], "red")
            if event == "e26":
                if values[event] != "":
                    border(eMenu[event], "green")
                else:
                    border(eMenu[event], "red")

            if event == "load simg":
                filename = values["e23"]
                if os.path.exists(filename):
                    image = Image.open(values["e23"])
                    image.thumbnail((300, 300))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    eMenu["-IMAGE2-"].update(data=bio.getvalue())

            if event == "load nimg":
                filename = values["e26"]
                if os.path.exists(filename):
                    image = Image.open(values["e26"])
                    image.thumbnail((300, 300))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    eMenu["-IMAGE3-"].update(data=bio.getvalue())

            if event == "pf":
                eMenu["e2"].update(value=Emp_code_Gen("PF"))

            if event == "non pf":
                eMenu["e2"].update(value=Emp_code_Gen("Non PF"))

            if event == "yes":
                eMenu["e11"].update(disabled=False)
                eMenu["e12"].update(disabled=False)
                eMenu["e13"].update(disabled=False)
                eMenu["e10"].update(disabled=True, value=0.00)

            if event == "no":
                eMenu["e11"].update(disabled=True, value=0.00)
                eMenu["e12"].update(disabled=True, value=0.00)
                eMenu["e13"].update(disabled=True, value=0.00)
                eMenu["e10"].update(disabled=False)

    if event =="etcnge":
        if values["etcnge"]==True:
           Menu["emp_data"].update(values=EmpdataFetch("Non PF") )
        if values["etcnge"] == False:
            Menu["emp_data"].update(values=EmpdataFetch("PF") )

    if event == "emp_data":
        data = Menu['emp_data'].get()
        globals()['crow'] = [data[row] for row in values[event]]
        #print(crow)

    if event =="Update Employee":
        chk = ms.popup_get_text("Enter password to proceed further ", password_char='*', size=(20, 1), font=fstyle,
                                keep_on_top=True)
        if chk == MasterPass:
            a=crow[0][0]
            uMenu = ms.Window("Update Employee",[[ms.Column( Employee_update_GUI(a),
                                                              scrollable=True, size=(800, 700),
                                                              element_justification='centre')]])
            while True:
                event, values = uMenu.read()
                #print(event)
                if event == ms.WIN_CLOSED:
                    uMenu.close()
                    break
                if event == 'updateemp':
                    Update_Employee(event, values)
                if event == "load pimg":
                    filename = values["u22"]
                    if os.path.exists(filename):
                        image = Image.open(values["u22"])
                        image.thumbnail((300, 300))
                        bio = io.BytesIO()
                        # Actually store the image in memory in binary
                        image.save(bio, format="PNG")
                        # Use that image data in order to
                        uMenu["-IMAGE-"].update(data=bio.getvalue())

                if event == "load simg":
                    filename = values["u23"]
                    if os.path.exists(filename):
                        image = Image.open(values["u23"])
                        image.thumbnail((300, 300))
                        bio = io.BytesIO()
                        # Actually store the image in memory in binary
                        image.save(bio, format="PNG")
                        # Use that image data in order to
                        uMenu["-IMAGE2-"].update(data=bio.getvalue())
                if event == "load nimg":
                    filename = values["u26"]
                    if os.path.exists(filename):
                        image = Image.open(values["u26"])
                        image.thumbnail((300, 300))
                        bio = io.BytesIO()
                        # Actually store the image in memory in binary
                        image.save(bio, format="PNG")
                        # Use that image data in order to
                        uMenu["-IMAGE3-"].update(data=bio.getvalue())
                if event == "PF":
                    uMenu["u2"].update(values=Emp_code_Gen("PF"))
                if event == "Non PF":
                    uMenu["u2"].update(values=Emp_code_Gen("Non PF"))
                if event == "yes":
                    print('X')
                    uMenu["u11"].update(disabled=False)
                    uMenu["u12"].update(disabled=False)
                    uMenu["u13"].update(disabled=False)
                    uMenu["u10"].update(disabled=True, value=0.00)
                if event == "no":
                    print('Y')
                    uMenu["u13"].update(disabled=True, value=0.00)
                    uMenu["u11"].update(disabled=True, value=0.00)
                    uMenu["u12"].update(disabled=True, value=0.00)
                    uMenu["u10"].update(disabled=False)
                if event=="u25":
                    if values["u25"]=="N":
                        uMenu["u26"].update(disabled=False)
                        uMenu["date3"].update(disabled=False)
                    if values["u25"] == "y":
                        uMenu["u26"].update(disabled=True)
                        uMenu["date3"].update(disabled=True)

    if event == "Remove":
        pwchk = ms.popup_get_text("Enter password to proceed further ", password_char='*', size=(20, 1), font=fstyle,
                                keep_on_top=True)
        if pwchk == MasterPass:
            chk = ms.popup_ok("Please Confirm to Delete", font=fstyle)
            if chk == "OK":
                mycursor.execute("UPDATE `register` SET `active_status` = 'N' WHERE (`emp_code` = '%s')" % crow[0][0])
                mydb.commit()
                Menu['emp_data'].update(values=EmpdataFetch("PF"))

    if event == "empexp":
        mycursor.execute("select emp_code, employee_name, designation, esic_no, uan_no, "
                         "pan_no,aadhar_no,address,marriage_status,f_sp_name,gender,date_of_join from register where active_status = 'Y'")
        db_data=[list(x) for x in mycursor.fetchall()]
        xl=openpyxl.load_workbook(r'C:\Twink_06MA\Master_Files\Emp_Exp.xlsx')
        xl.active=xl['Emp_Info']
        xlc=xl.active
        rowc=2
        colc=1
        for step in db_data:
            colc=1
            for i in step:
                xlc.cell(row=rowc,column=colc).value=i
                colc+=1
            rowc+=1
        xl.save(r'C:\Twink_06MA\Master_Files\Emp_Exp01.xlsx')
        os.system(r'C:\Twink_06MA\Master_Files\Emp_Exp01.xlsx')

    if event == 'empmail':
        mycursor.execute("select emp_code, employee_name, designation, esic_no, uan_no, "
                         "pan_no,aadhar_no,address,marriage_status,f_sp_name,gender,date_of_join from register where active_status = 'Y'")
        db_data=[list(x) for x in mycursor.fetchall()]
        xl=openpyxl.load_workbook(r'C:\Twink_06MA\Master_Files\Emp_Exp.xlsx')
        xl.active=xl['Emp_Info']
        xlc=xl.active
        rowc=2
        colc=1
        for step in db_data:
            colc=1
            for i in step:
                xlc.cell(row=rowc,column=colc).value=i
                colc+=1
            rowc+=1
        xl.save(r'C:\Twink_06MA\Master_Files\Emp_Exp01.xlsx')
        maillist = popup_select(mailid_fetch(False,""), select_multiple=True)
        for i in maillist:
            mail_content = "PFA"
            sender_address = 'asta.sunilindustries@gmail.com'
            sender_pass = 'uxzgkfvkdzuxwpad'
            # Setup the MIME
            receiver_address = mailid_fetch(True,i)
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = "Employee Register Output"
            message.attach(MIMEText(mail_content, 'plain'))
            attach_file_name = r'C:\Twink_06MA\Master_Files\Emp_Exp01.xlsx'
            attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            payload.add_header('Content-Disposition ', 'attachment',
                               filename='Employee_register.xlsx')
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
