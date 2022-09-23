from Env import *
def crew_att_gui():
    datalist=[[ms.Sizer(300,0),ms.Text("UID",justification= 'center',size=(10,1),relief= 'raised',font=fstylehd),
                   ms.Text("Name",justification= 'center',relief= 'raised',size=(32,1),font=fstylehd),
                   ms.Text("Discription",justification= 'center',relief= 'raised',size=(40,1),font=fstylehd),
                  ]]
    mycursor.execute('select UID,crew_name from cleaning_crew')
    globals()['cclistpy']=[list(x) for x in mycursor.fetchall()]
    mycursor.execute("select discription from cc_work_list")
    crew_dis=list(sum(mycursor.fetchall(),()))
    for i in range (len(cclistpy)):
            sub1=ms.Column([[ms.Sizer(300,0),
                  ms.Input(cclistpy[i][0],font=fstyle,key='cc_uid'+str(i),size=(10,1),disabled=True,justification='center',
                           disabled_readonly_background_color=ms.theme_background_color(),border_width= 0),ms.Sizer(130,0),
                  ms.Input(cclistpy[i][1],font=fstyle,key='cc_name'+str(i),size=(10,1),disabled=True,justification='center',
                           disabled_readonly_background_color=ms.theme_background_color(),border_width= 0),
                  ms.Sizer(140,0),
                  ms.Combo(values=crew_dis,font=fstyle,key='cc_dis'+str(i),size=(40,1))],[ms.Sizer(320,0),ms.HSeparator()]],visible= True,key='atpsy'+str(i))
            datalist.append([sub1])
    layout = [
        [ms.Text("Crew Attendance Register", font=fstylehd)],
        [ms.Text("Entry Person", font=fstyle, size=(12, 1)),
         ms.Combo(values=user_name(), font=fstyle, size=(20, 1), key='cc_atpers'), ms.Sizer(swi - 650, 0),
         ms.Text("Date", font=fstyle, size=(5, 1)), ms.InputText("", size=(15, 1), font=fstyle, key="cc_atpdate"),
         ms.CalendarButton(" ", target='cc_atpdate', format="%Y/%m/%d", location=(1250, 100))],
        [ms.Frame("Entry", layout=[[ms.Column(datalist, scrollable=True, vertical_scroll_only=True, visible=True,
                                              size=(swi - 70, shi - 220), key='cc_atppf')]],
                  font=fstyle, size=(swi - 50, shi - 150))],
        [ms.Input("",size=(15, 1), font=fstyle, password_char="*", key='cc_atppw')],
        [ms.Button("Update", font=fstyle, key='cc_atpupdate')
         ]]
    return layout
def cc_att_(event,values,Menu):
    if event == 'cc_atpupdate':
        print(values['cc_atpers'])
        print("ckecking", user_pass(values['cc_atpers'])[0][0])
        if values['cc_atppw'] == user_pass(values['cc_atpers'])[0][0]:
            ccatdata = []
            mycursor.execute("select WID,discription from cc_work_list " )
            dis=[list(x) for x in mycursor.fetchall()]
            for i in range(len(cclistpy)):
                data = []
                data.append(values['cc_uid' + str(i)])
                data.append(values["cc_atpdate"])
                for j in range (0,len(dis)):
                  #print("i",values['cc_dis' + str(i)])
                  if values['cc_dis' + str(i)] == dis[j][1]:
                      data.append(dis[j][0])
                ccatdata.append(data)
                print("s",ccatdata)
            for i in range (len(cclistpy)):
                mycursor.execute("INSERT INTO `twink_06ma`.`cc_attendence`(`UID`,`wrk_date`,`WID`) values ('%s','%s','%s')" % (ccatdata[i][0],ccatdata[i][1],ccatdata[i][2]))
            mydb.commit()
            ms.popup_auto_close("Updated Successfully", auto_close_duration=1)

        else:
            ms.popup_auto_close("Wrong Password", auto_close_duration=1)

#v6.1