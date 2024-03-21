# __StandAlone INIT__
import os
from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Advance_Amt(Adv):
    print(Cur_Date_YM)
    Emp_List= DB_Fetch(
                       "select employee_name, emp_code from register where active = 'Y' order by UID",
                             False, "DIC")
    Emp_Lists = DB_Fetch(
                        "select employee_name from register where active = 'Y' order by UID",
                        False, "LOE")

    Adjust_Table_Width(Adv.IQTB_AdvanceDetails, [10, 10, 50, 15])
    Emp_Adv_List = DB_Fetch(
                            fr"SELECT DATE_FORMAT(advance_details.exdate,'%d-%m-%Y'), advance_details.empcode,"
                                 fr"register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code" 
                                fr" WHERE advance_details.exdate LIKE '{Cur_Date_YM}%';",False,"LOL")

    Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)

    @Exception_Handle
    def Date_Filter():
        globals()["table"] = True
        Adv.IQCB_NameFilter.clear()
        Date_Chg = Adv.IQDE_DateFilter.date().toString(Qt.ISODate)
        Emp_Adv_List = DB_Fetch(
                                fr"SELECT DATE_FORMAT(advance_details.exdate,'%d-%m-%Y'), advance_details.empcode, register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                fr" WHERE advance_details.exdate LIKE '{Date_Chg[:-3]}%'",
                                False, "LOL")
        Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)
        Adv.IQCB_NameFilter.addItem("")
        Employee = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
        emp = Fetch_Table_Values_SPL_Col(Adv.IQTB_AdvanceDetails, 2)
        # print(emp,"emp")
        Adv.IQCB_NameFilter.addItems(emp)
        Total_tbl = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
        # print(Adv.IQCB_NameFilter.currentText(),"hello")
        globals()["Total_tbl"] = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
        # Adv.IQCB_NameFilter.addItems({item for i in emp for item in i})
        globals()["table"] = False

    @Exception_Handle
    def Filter_Thou_Name():
        try:
            print(Emp_List[Adv.IQCB_EmpName.currentText()])
            Adv.IQL_EmpCode.setText(Emp_List[Adv.IQCB_EmpName.currentText()])
        except Exception as e:
            print(e)

    @Exception_Handle
    def Filter_Tbl_Name():
        if globals()["table"] == True:
            print("im active")
            if Adv.IQCB_NameFilter.currentText() !="":
                Fil_Name = Adv.IQCB_NameFilter.currentText()
                Fil_Name_List = DB_Fetch(
                                        fr"SELECT DATE_FORMAT(advance_details.exdate,'%d-%m-%Y'), advance_details.empcode, register.employee_name, advance_details.amount"
                                        fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                        fr" WHERE  register.employee_name = '{Fil_Name} ';",
                                        False, "LOL")
                print(Fil_Name_List,"name")
                Push_Table_Values(Adv.IQTB_AdvanceDetails, Fil_Name_List ,False)
            else:
                Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)
        if globals()["table"] == False:
            Fil_Name = Adv.IQCB_NameFilter.currentText()
            table_data_fitr=[]
            print(globals()["Total_tbl"],"santha")
            print(Fil_Name,"what")
            if Fil_Name != "":
                for i in range(len(globals()["Total_tbl"])):
                    if globals()["Total_tbl"][i][2]== Fil_Name:
                        table_data_fitr.append(globals()["Total_tbl"][i])
                Push_Table_Values(Adv.IQTB_AdvanceDetails,table_data_fitr,False)
            else:
                Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)

    @Exception_Handle
    def Generate_Adv_TBL():
        try:
            name = Adv.IQCB_EmpName.currentText()
            emp_Id = Adv.IQL_EmpCode.text()
            date = Adv.IQDE_AdvanceDate.date().toString(Qt.ISODate)
            Adv_Amt = Adv.IQLE_Amount.text()
            print(name,emp_Id,date,Adv_Amt)
            uid = DB_Fetch(
                     "SELECT MAX(uid) FROM advance_details",
                     False, "LOE")
            if uid[0] is None:
                uid[0]=1

            dict = {
                'empcode': Adv.IQL_EmpCode.text(),
                'exdate': Adv.IQDE_AdvanceDate.date().toString(Qt.ISODate),
                'amount': Adv.IQLE_Amount.text(),
            }
            DB_Push_Dict( dict, "advance_details", False)
            Emp_Adv_List = DB_Fetch(
                                    fr"SELECT DATE_FORMAT(advance_details.exdate,'%d-%m-%Y'), advance_details.empcode, register.employee_name, advance_details.amount"
                                    fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                    fr" WHERE advance_details.exdate LIKE '{Cur_Date_YM}%';",
                                    False, "LOL")
            Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)
            Adv.IQCB_EmpName.clear()
            Adv.IQL_EmpCode.clear()
            Adv.IQDE_AdvanceDate.setDate(QtCore.QDate.currentDate())
            Adv.IQLE_Amount.clear()
            Adv.IQCB_EmpName.addItems(["----Select the Employee---"] + Emp_Lists)

            sql = fr"select empcode, register.employee_name, SUM(amount) AS total_amount, '0.0' from advance_details inner join " \
                  "register on advance_details.empcode = register.emp_code GROUP BY empcode order by empcode"
            Push_Table_Values(Wge.IQTB_AdvanceDetail, DB_Fetch(sql, False, "LOL"), False)
            for row in range(Wge.IQTB_AdvanceDetail.rowCount()):
                item = Wge.IQTB_AdvanceDetail.item(row, 3)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
        except Exception as e:
            print(e)

    @Exception_Handle
    def Right_Click_Menu(pos):
        row = Adv.IQTB_AdvanceDetails.selectedIndexes()
        # print(row)
        R_menu = QMenu()
        Remove = QAction("Delete", R_menu)
        # Revert = QAction("Revert", R_menu)
        R_menu.addAction(Remove)
        # R_menu.addAction(Revert)
        pos = Adv.IQTB_AdvanceDetails.mapToGlobal(pos)
        Remove.triggered.connect(lambda: Delete_Employee(row[0].row()))
        # print(row[0].row())
        # Revert.triggered.connect(lambda: Revert_Employee())
        R_menu.exec_(pos)

    @Exception_Handle
    def Delete_Employee(index):
        Employee = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)[index]
        Del_Emp = DB_Fetch(
                        fr"select uid from advance_details where exdate = '{Employee[0]} ' and  empcode ='{Employee[1]}' and amount = {Employee[3]} ",
                        False, "LOE")
        # print(Del_Emp[0])
        dict = {
            'uid': Del_Emp[0]
        }

        if UI_Confirmation(UI_Confirm_Win, f"Please confirm to delete the Advance :< {Employee} >:"):
            DB_Delete_Dict(dict, 'advance_details', False)
        #
        Emp_Adv_List = DB_Fetch(
                                fr"SELECT DATE_FORMAT(advance_details.exdate,'%d-%m-%Y'), advance_details.empcode, register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                fr" WHERE advance_details.exdate LIKE '{Cur_Date_YM}%';",
                                False, "LOL")
        Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)
        sql = fr"select empcode, register.employee_name, SUM(amount) AS total_amount, '0.0' from advance_details inner join " \
              "register on advance_details.empcode = register.emp_code GROUP BY empcode order by empcode"
        Push_Table_Values(Wge.IQTB_AdvanceDetail, DB_Fetch(sql, False, "LOL"), False)
        for row in range(Wge.IQTB_AdvanceDetail.rowCount()):
            item = Wge.IQTB_AdvanceDetail.item(row, 3)
            if item:
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    Adv.IQDE_DateFilter.setDate(QtCore.QDate.currentDate())
    Adv.IQDE_AdvanceDate.setDate(QtCore.QDate.currentDate())
    Adv.IQCB_EmpName.addItem("--Select the Employee--")
    Dynamic_Filter_ComboBox(Adv.IQCB_EmpName)
    Adv.IQCB_EmpName.addItems(Emp_Lists)
    Adv.IQPB_Generate.clicked.connect(lambda: Generate_Adv_TBL())
    Adv.IQDE_DateFilter.dateChanged.connect(lambda: Date_Filter())
    Adv.IQCB_EmpName.activated.connect(lambda: Filter_Thou_Name())
    Adv.IQCB_NameFilter.activated.connect(lambda: Filter_Tbl_Name())
    Adv.IQCB_NameFilter.addItem("")
    Adv.IQCB_NameFilter.addItems(Emp_Lists)
    Dynamic_Filter_ComboBox(Adv.IQCB_NameFilter)

    Adv.IQTB_AdvanceDetails.setContextMenuPolicy(Qt.CustomContextMenu)
    Adv.IQTB_AdvanceDetails.customContextMenuRequested.connect(Right_Click_Menu)
    globals()["table"] = True

#__StandAlone Running__
if SAR == True:
    Advance_Amt(Adv)
    Adv.show()
    sys.exit(app.exec_())