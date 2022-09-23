from Env import *

def Master_User_GUI():

        layout_1=[
                  [ms.Frame("User Data",
                            [[ms.Button("Add",key="add_user",font=fstyle),],[ms.Table(values=MUWFetch(),
                                       headings=["UID", "Name", "Password"],
                                       justification='centre', enable_events=True, auto_size_columns=False,
                                       row_height=30,num_rows=15,
                                       col_widths=[20, 40, 40],
                                       right_click_selects=True,
                                       right_click_menu=[[], ["Remove "]],
                                       enable_click_events=True, size=(swi - 100, shi - 300), key="user_data",
                                       font=fstyle)]],
                            font=fstyle, element_justification='left')],
                  [ms.Frame("Adding Mater_User", [
                      [ms.Text("Name", size=(20, 1)), ms.Sizer(45, 0),ms.Text("Password", size=(20, 1))],
                      [ms.Input("", size=(20, 1), do_not_clear=False, key='u_name', font=fstyle), ms.Sizer(5, 0),
                       ms.Input("", size=(20, 1), do_not_clear=False, key='u_password', font=fstyle),
                       ms.Button("Add", font=fstyle, key="add_user1")]], visible=False, key="add_user2")]]
        layout_2=[
                  [ms.Frame("Work Discription",
                            [[ms.Button("Add",key="add_wrkdsp",font=fstyle),],[ms.Table(values=CCWORKFetch(),
                                       headings=["WID","Discription", "Amount"],
                                       justification='centre', enable_events=True, auto_size_columns=False,
                                       row_height=30,num_rows=15,
                                       col_widths=[10,70,30],
                                       right_click_selects=True,
                                       right_click_menu=[[], [" Remove"]],
                                       enable_click_events=True, size=(swi - 100, shi - 300), key="wrk_data",
                                       font=fstyle)]],
                    font=fstyle, element_justification='left')],
                  [ms.Frame("Adding Work", [
                      [ms.Text("Discription", size=(20, 1)), ms.Sizer(360, 0),ms.Text("Amount", size=(20, 1))],
                      [ms.Multiline("", size=(50, 2), do_not_clear=False, key='cc_wrk', font=fstyle),
                       ms.Input("", size=(20, 1), do_not_clear=False, key='amount', font=fstyle),
                       ms.Button("Add", font=fstyle, key="add_wdsp")]], visible=False, key="add_discription")]]
        layout_2a = [
            [ms.Frame("Department Information",
                      [[ms.Button("Add", key="add_dpdsp", font=fstyle), ],
                       [ms.Table(values=DepListFetch(),
                                 headings=["WID", "Discription","Per Day Wage"],
                                 justification='centre',
                                 enable_events=True,
                                 auto_size_columns=False,
                                 row_height=30, num_rows=15,
                                 col_widths=[10, 70, 30],
                                 right_click_selects=True,
                                 right_click_menu=[[],
                                                   [" Remove"]],
                                 enable_click_events=True,
                                 size=(swi - 100, shi - 300),
                                 key="dp_data",
                                 font=fstyle)]],
                      font=fstyle, element_justification='left')],
            [ms.Frame("Adding Department", [
                [ms.Text("Department Name", size=(20, 1),font=fstyle), ms.Sizer(330, 0),
                 ms.Text("Per Day Wage", size=(20, 1),font=fstyle)],
                [ms.Input("", size=(50, 2), do_not_clear=False, key='dp_wrk', font=fstyle),
                 ms.Input("", size=(20, 1), do_not_clear=False, key='dp_amount', font=fstyle),
                 ms.Button("Add", font=fstyle, key="add_dpsp")]], visible=False, key="add_dpdesc",font=fstyle)]]
        layout_3 = [
                    [ms.Frame("Mail list",
                              [[ms.Button("Add", key="add_mail",font=fstyle),],[ms.Table(values=MAILFetch(),
                                         headings=["UID","Name","Designation","Mail ID"],
                                         justification='centre', enable_events=True, auto_size_columns=False,
                                         row_height=30,
                                         col_widths=[10, 45, 30, 55],
                                         right_click_selects=True,
                                         num_rows=15,
                                         right_click_menu=[[], [" Remove "]],
                                         enable_click_events=True, size=(swi - 100, shi - 300), key="mail_data",
                                         font=fstyle)]],
                              font=fstyle, element_justification='left')],
                    [ms.Frame("Adding Mail_User", [
                        [ms.Text("Name", size=(20, 1)), ms.Sizer(95, 0),ms.Text("Designation", size=(20, 1)), ms.Sizer(45, 0), ms.Text("Mail ID", size=(20, 1))],
                        [ms.Input("", size=(25, 1), do_not_clear=False, key='ml_name', font=fstyle),
                         ms.Input("", size=(20, 1), do_not_clear=False, key='designation', font=fstyle),
                         ms.Input("", size=(25, 1), do_not_clear=False, key='mail_id', font=fstyle),
                         ms.Button("Add", font=fstyle, key="add_mail_list")]], visible=False, key="add_mail_user")]]
        layout=[[ms.TabGroup([[ms.Tab("User Details",layout_1,element_justification='center')],
                              [ms.Tab("CC Work List",layout_2,element_justification='center')],
                              [ms.Tab("Department List", layout_2a, element_justification='center')],
                              [ms.Tab("Mail ID",layout_3,element_justification='center')]],font=fstyle,size=(swi-50,shi-50))]]
        return layout

def Master_User(Menu,event,values):
    if event =="add_user":
        chk = ms.popup_get_text("Enter password to add user ", password_char='*', size=(10, 1), font=fstyle, keep_on_top=True)
        if chk == MasterPass:
            Menu["add_user2"].update(visible=True)
    if event =="add_wrkdsp":
        Menu["add_discription"].update(visible=True)
    if event =="add_mail":
        Menu["add_mail_user"].update(visible=True)
    if event == "add_dpdsp":
        chk = ms.popup_get_text("Enter password to Proceed", password_char='*', size=(10, 1), font=fstyle,
                                 keep_on_top=True)
        if chk == MasterPass:
            Menu["add_dpdesc"].update(visible=True)
    if event == 'add_dpsp':
        sql = "INSERT INTO dep_list ( description,Wage_pd ) VALUES ( '%s','%s')" % (
        values['dp_wrk'], values['dp_amount'])
        mycursor.execute(sql)
        mydb.commit()
        Menu["dp_data"].update(values=DepListFetch())
        Menu["add_dpdesc"].update(visible=False)
        ms.popup_auto_close("Added Successfully",font=fstyle)
    if event == "add_user1":
        if values["u_name"] and values["u_password"] !="":
            sql = "INSERT INTO user_details ( user_name,user_password ) VALUES ( '%s','%s')" % (
            values["u_name"], values["u_password"])
            mycursor.execute(sql)
            mydb.commit()
            Menu["user_data"].update(values=MUWFetch())
            Menu["add_user2"].update(visible=False)
            ms.popup_auto_close("Added Successfully", font=fstyle)
    if event == "add_wdsp":
        if values['cc_wrk'] and values['amount'] !="":
            sql = "INSERT INTO cc_work_list ( discription,amount ) VALUES ( '%s','%s')" % (values['cc_wrk'], values['amount'])
            mycursor.execute(sql)
            mydb.commit()
            Menu["wrk_data"].update(values=CCWORKFetch())
            Menu["add_discription"].update(visible=False)
            ms.popup_auto_close("Added Successfully", font=fstyle)
    if event == "add_mail_list":
        if values['ml_name'] and values['designation'] and values['mail_id'] !="":
            sql = "INSERT INTO mail_list (name_,designation,mail_id ) VALUES ( '%s','%s','%s')" % (
            values['ml_name'], values['designation'],values['mail_id'])
            mycursor.execute(sql)
            mydb.commit()
            Menu["mail_data"].update(values=MAILFetch())
            Menu["add_mail_user"].update(visible=False)
            ms.popup_auto_close("Added Successfully", font=fstyle)
    if event == "Remove ":
        chk = ms.popup_get_text("Enter password to remove user ", password_char='*', size=(10,1), font=fstyle, no_titlebar=True, keep_on_top=True)
        if chk == MasterPass:
            mycursor.execute("DELETE FROM user_details WHERE UID='%s'" % remove_data(Menu,"user_data",values)[0][0])
            mydb.commit()
            Menu["user_data"].update(values=MUWFetch())
            ms.popup_auto_close("Removed Successfully", font=fstyle)
        else:
            ms.popup_auto_close("Wrong Password",no_titlebar=True, auto_close_duration=2)
    if event == " Remove":
        chk = ms.popup_ok("Please Confirm to Delete", font=fstyle)
        if chk == "OK":
            mycursor.execute("DELETE FROM cc_work_list WHERE WID='%s'" % remove_data(Menu,"wrk_data",values)[0][0])
            mydb.commit()
            Menu["user_data"].update(values=CCWORKFetch())
            ms.popup_auto_close("Removed Successfully", font=fstyle)
    if event == " Remove ":
        chk = ms.popup_ok("Please Confirm to Delete", font=fstyle)
        if chk == "OK":
            mycursor.execute("DELETE FROM mail_list WHERE UID='%s'" % remove_data(Menu,"mail_data",values)[0][0])
            mydb.commit()
            Menu["mail_data"].update(values=MAILFetch())
            ms.popup_auto_close("Removed Successfully", font=fstyle)


'''Menu = ms.Window("Add Employee", [[ms.Column(Master_User_GUI(), scrollable=True, size=(960, 700), element_justification='centre')]], finalize=True)
while True:
    event, values = Menu.read()
    if event == ms.WIN_CLOSED:
        Menu.close()
        break
    Master_User(Menu, event, values)
'''

#v6.1