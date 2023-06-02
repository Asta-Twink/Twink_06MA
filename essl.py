from Env import *
import datetime
from datetime import datetime
def atn_create(inp):
    mycursor.execute("select empcode,TIME_TO_SEC(ltime)/60 from essl_logs where ldate='%s' ORDER BY empcode"%inp )
    at_data=[list(x) for x in mycursor.fetchall()]
    #print(at_data)

    mycursor.execute("select distinct(empcode) from essl_logs where ldate='%s' ORDER BY empcode"%inp  )
    ec_data=list(sum(mycursor.fetchall(),()))
    #(ec_data)
    oplist=[]
    temp=[]
    for step in ec_data:
        for st in at_data:
            if step == st[0]:
                temp.append(st[1])
        oplist.append([step,sorted(temp)])
        temp=[]
    print(oplist)
    opdict={}
    for step in oplist:
        print(step[0])
        if "TEMP" in str(step[0]):
            print("X")
            step[0]="SIL"+str(step[0])
        print(step[0])
        try:
            if step[1][0] < 1300 and step[1][len(step)-1]-step[1][0] < 800:
                hourspent=(step[1][len(step[1])-1]-step[1][0])/60
                print(step,hourspent)
                ot=hourspent-8 if hourspent > 7 else hourspent
                ot = 0 if ot < 0.5 else round(ot,0)
                if hourspent > 7:
                    if step[1][0]>700:
                        var="2"
                    else:
                        var="1"
                else:
                    var="0"
                    if step[1][0] > 700 and ot > 0:
                        ot = "2/" + str(ot)
                    else:
                        ot = "1/" + str(ot)

                step[1]= [var,ot]
            else:
                mycursor.execute("select TIME_TO_SEC(ltime)/60 from essl_logs where ldate = '%s' and"
                                 " empcode = '%s' and TIME_TO_SEC(ltime)/60 < 700"%
                                 (datetime.strftime(datetime.strptime(inp,"%Y-%m-%d")+dp.timedelta(days=1),"%Y-%m-%d"),step[0]))
                db_data=list(sum(mycursor.fetchall(),()))
                step[1]=[step[1][len(step)-1]]
                step[1]=sorted(step[1]+db_data)
                #print(step[1])
                hourspent=((1440-step[1][len(step[1])-1])+step[1][0])/60
                ot=hourspent-8 if hourspent > 7 else hourspent
                ot = 0 if ot < 0.5 else round(ot,0)
                if hourspent > 7:
                    var = "3"
                else:
                    var = "0"
                    if ot > 0:
                        ot = "3/" + str(ot)
                step[1]= [var ,ot]
            opdict[step[0]]=step[1]
        except Exception as e:
            print(e)
            pass
    #print(oplist)
    print(opdict)
    return opdict
#atn_create("2022-12-17")






