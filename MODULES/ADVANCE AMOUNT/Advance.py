# __StandAlone INIT__
import os

from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Advance_Amt(Adv):
    print("Start")
    Emp_List= DB_Fetch(dbc,
                       "select employee_name, emp_code from register where active_status = 'Y' order by UID",
                             False, "DIC")
    Emp_Lists = DB_Fetch(dbc,
                        "select employee_name from register where active_status = 'Y' order by UID",
                        False, "LOE")

    Adjust_Table_Width(Adv.IQTB_AdvanceDetails, [125, 150, 225, 175])
    Emp_Adv_List = DB_Fetch(dbc,
                            fr"SELECT advance_details.exdate, advance_details.empcode, register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code" 
                                fr" WHERE advance_details.exdate LIKE '{Cur_Date_YM}%';",
                            False,"LOL")
    Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)


    @Exception_Handle
    def Date_Filter():
        Adv.IQCB_NameFilter.clear()
        Date_Chg = Adv.IQDE_DateFilter.date().toString(Qt.ISODate)
        Emp_Adv_List = DB_Fetch(dbc,
                                fr"SELECT advance_details.exdate, advance_details.empcode, register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                fr" WHERE advance_details.exdate LIKE '{Date_Chg[:-3]}%';",
                                False, "LOL")
        Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)
        Adv.IQCB_NameFilter.addItem("")
        Employee = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
        emp = Fetch_Table_Values_Col(Adv.IQTB_AdvanceDetails, 2)
        Total_tbl = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
        Adv.IQCB_NameFilter.addItems({item for i in emp for item in i})

    @Exception_Handle
    def Filter_Thou_Name():
        try:
            print(Emp_List[Adv.IQCB_EmpName.currentText()])
            Adv.IQL_EmpCode.setText(Emp_List[Adv.IQCB_EmpName.currentText()])
        except Exception as e:
            print(e)

    @Exception_Handle
    def Filter_Tbl_Name():
        Fil_Name = Adv.IQCB_NameFilter.currentText()
        Fil_Name_List = DB_Fetch(dbc,
                                fr"SELECT advance_details.exdate, advance_details.empcode, register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                fr" WHERE  register.employee_name = '{Fil_Name}';",
                                False, "LOL")
        Push_Table_Values(Adv.IQTB_AdvanceDetails, Fil_Name_List ,False)
        # print(Fil_Name)
        # print(Fil_Name_List)
        # Master_Filter=[]
        # i=0
        # while(len(Total_tbl)>i):
        #     if Fil_Name.lower() in  Total_tbl[i][2].lower():
        #         print(Total_tbl[i][2])
        #         Master_Filter.append(Total_tbl[i])
        #     i = i+1
        #     print(i)
        # print(Master_Filter)
        # Push_Table_Values(Adv.IQTB_AdvanceDetails, Master_Filter, False)

    @Exception_Handle
    def Generate_Adv_TBL():
        try:
            name = Adv.IQCB_EmpName.currentText()
            emp_Id = Adv.IQL_EmpCode.text()
            date = Adv.IQDE_AdvanceDate.date().toString(Qt.ISODate)
            Adv_Amt = Adv.IQLE_Amount.text()
            print(name,emp_Id,date,Adv_Amt)
            uid = DB_Fetch(dbc,
                     "SELECT MAX(uid) FROM advance_details",
                     False, "LOE")
            dict = {
                'uid' : int(uid[0])+1,
                'empcode': Adv.IQL_EmpCode.text(),
                'exdate': Adv.IQDE_AdvanceDate.date().toString(Qt.ISODate),
                'amount': Adv.IQLE_Amount.text(),
            }
            DB_Push_Dict(dbc, db, dict, "advance_details", False)
            Emp_Adv_List = DB_Fetch(dbc,
                                    fr"SELECT advance_details.exdate, advance_details.empcode, register.employee_name, advance_details.amount"
                                    fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                    fr" WHERE advance_details.exdate LIKE '{Cur_Date_YM}%';",
                                    False, "LOL")
            Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)
            Adv.IQCB_EmpName.clear()
            Adv.IQL_EmpCode.clear()
            Adv.IQDE_AdvanceDate.setDate(QtCore.QDate.currentDate())
            Adv.IQLE_Amount.clear()
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
        Del_Emp = DB_Fetch(dbc,
                        fr"select uid from advance_details where exdate = '{Employee[0]} ' and  empcode ='{Employee[1]}' and amount = {Employee[3]} ",
                        False, "LOE")
        # print(Del_Emp[0])
        dict = {
            'uid': Del_Emp[0]
        }
        # print(index)
        # print(Employee)
        if UI_Confirmation(UI_Confirm_Win, f"Please confirm to delete the Employee :< {Employee} >:"):
            DB_Delete_Dict(dbc, db, dict, 'advance_details', False)
        #
        Emp_Adv_List = DB_Fetch(dbc,
                                fr"SELECT advance_details.exdate, advance_details.empcode, register.employee_name, advance_details.amount"
                                fr" FROM advance_details INNER JOIN register ON advance_details.empcode = register.emp_code"
                                fr" WHERE advance_details.exdate LIKE '{Cur_Date_YM}%';",
                                False, "LOL")
        Push_Table_Values(Adv.IQTB_AdvanceDetails, Emp_Adv_List, False)


    Adv.IQDE_DateFilter.setDate(QtCore.QDate.currentDate())
    Adv.IQDE_AdvanceDate.setDate(QtCore.QDate.currentDate())
    Adv.IQCB_EmpName.addItem("")
    Dynamic_Filter_ComboBox(Adv.IQCB_EmpName)
    Adv.IQCB_EmpName.addItems(Emp_Lists)
    Adv.IQPB_Generate.clicked.connect(lambda: Generate_Adv_TBL())
    Adv.IQDE_DateFilter.dateChanged.connect(lambda: Date_Filter())
    Adv.IQCB_EmpName.activated.connect(lambda: Filter_Thou_Name())
    Adv.IQCB_NameFilter.activated.connect(lambda: Filter_Tbl_Name())

    Adv.IQCB_NameFilter.addItem("")
    # Employee = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
    # emp = Fetch_Table_Values_Col(Adv.IQTB_AdvanceDetails,2)
    # Total_tbl = Fetch_Table_Values(Adv.IQTB_AdvanceDetails)
    Adv.IQCB_NameFilter.addItems(Emp_Lists)
    # {item for i in emp for item in i}
    Dynamic_Filter_ComboBox(Adv.IQCB_NameFilter)

    Adv.IQTB_AdvanceDetails.setContextMenuPolicy(Qt.CustomContextMenu)
    Adv.IQTB_AdvanceDetails.customContextMenuRequested.connect(Right_Click_Menu)

#__StandAlone Running__
if SAR == True:
    Advance_Amt(Adv)
    Adv.show()
    sys.exit(app.exec_())