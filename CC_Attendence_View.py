from Env import *
def CC_View_GUI():
    mycursor.execute("select wrk_date,crew_name,discription from cc_attendence as catd "
                     "inner join cleaning_crew as cc on catd.UID  = cc.UID "
                     "inner join cc_work_list as cwl on catd.WID =cwl.WID ")
    globals()['cv_data']=[list(x) for x in mycursor.fetchall()]
    mycursor.execute("select discription from cc_work_list")
    f_dis=list(sum(mycursor.fetchall(),()))
    mycursor.execute("select crew_name from cleaning_crew")
    f_name = list(sum(mycursor.fetchall(), ()))
    C_view=[ms.Table(values=cv_data, headings=["Date","Name","Discription"],
                justification='centre', enable_events=True,
                auto_size_columns=False,
                row_height=20,
                col_widths=[13,30,80],
                num_rows=28,
                font=fstyle,
                enable_click_events=True, key="cc_view")]
    layout = [[
               ms.Sizer(70,0),
               ms.Text("Date", font=fstyle, justification='left',size=(7, 1)),
               ms.Sizer(150,0),
               ms.Text("Name", font=fstyle, size=(7, 1)),
               ms.Sizer(500,0),
               ms.Text("Discription", font=fstyle, size=(13, 1))],
              [ms.Sizer(88,0),ms.CalendarButton(" ",image_data=chse, target='cvf_date', format="%y-%m-%d"),
               ms.Input("", enable_events=True, size=(13, 1),pad=(0,0), font=fstyle, key='cvf_date'),
               ms.Combo(f_name, enable_events=True, size=(28, 1),pad=(0,0), font=fstyle, key='cvf_name'),
               ms.Combo(f_dis, enable_events=True, size=(79, 1),pad=(0,0), font=fstyle, key='cvf_dis')],
              [ms.Frame("Output", layout=[C_view,
               [ms.Button("Export", key='cc_export', font=fstyle)],], size=(swi - 70, shi - 100), font=fstyle, element_justification='center')]
              ]
    return layout
def c_view_db(event,values,Menu):
    if event == 'cvf_date':
        Menu['cvf_name'].update(value=" ")
        Menu['cvf_dis'].update(value=" ")
        mycursor.execute("select wrk_date,crew_name,discription from cc_attendence  as catd "
                         "inner join cleaning_crew as cc on catd.UID  = cc.UID "
                         "inner join cc_work_list as cwl on catd.WID =cwl.WID where wrk_date='%s'" % values['cvf_date'])
        globals()['cv_data']=[list(x) for x in mycursor.fetchall()]
        Menu["cc_view"].update(values=cv_data)
    if event == "cvf_name":
        Menu['cvf_date'].update(value=" ")
        Menu['cvf_dis'].update(value=" ")
        mycursor.execute("select wrk_date,crew_name,discription from cc_attendence  as catd "
                         "inner join cleaning_crew as cc on catd.UID  = cc.UID "
                         "inner join cc_work_list as cwl on catd.WID =cwl.WID where crew_name='%s'" % values['cvf_name'])
        globals()['cv_data'] = [list(x) for x in mycursor.fetchall()]
        Menu["cc_view"].update(values=cv_data)
    if event == "cvf_dis":
        Menu['cvf_name'].update(value=" ")
        Menu['cvf_date'].update(value=" ")
        mycursor.execute("select wrk_date,crew_name,discription from cc_attendence  as catd "
                         "inner join cleaning_crew as cc on catd.UID  = cc.UID "
                         "inner join cc_work_list as cwl on catd.WID =cwl.WID where discription='%s'" % values['cvf_dis'])
        globals()['cv_data'] = [list(x) for x in mycursor.fetchall()]
        Menu["cc_view"].update(values=cv_data)
    if event == "cc_export":
        mycursor.execute("select discription,amount from cc_work_list ")
        db_data=[list(x) for x in mycursor.fetchall()]
        amnt_data={}
        for i in db_data:
            amnt_data.update({i[0]:i[1]})
        data = cv_data
        xl = openpyxl.load_workbook(filename=r'C:\Twink_06MA\Master_Files\Cleaning_crew_Atd_view.xlsx')
        xlc = xl.active
        crow = 2
        for part in data:
            part.append(amnt_data.get(part[2]))
            ccol = 1
            for i in part:
                xlc.cell(row=crow, column=ccol).value = i
                ccol += 1
            crow += 1
        xl.save(filename=r'C:\Twink_06MA\Master_Files\CC_ATD_1.xlsx')
        os.system(r'C:\Twink_06MA\Master_Files\CC_ATD_1.xlsx')

#v6.1