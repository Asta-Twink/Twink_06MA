# ___StandAlone INIT___
import traceback
from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Master_FN(Mtr):
    Dep_List = DB_Fetch("Select UID, description  from dep_list",False, "LOL")
    Adjust_Table_Width(Mtr.IQTB_DeptInfo, [0, 40])
    Push_Table_Values(Mtr.IQTB_DeptInfo, Dep_List, False)
    Dep_Mail = DB_Fetch("Select * from mail_list",False, "LOL")
    Adjust_Table_Width(Mtr.IQTB_MailInfo, [0, 20, 10,35])
    Push_Table_Values(Mtr.IQTB_MailInfo, Dep_Mail, False)
    Adjust_Table_Width(Mtr.IQTB_IncentiveInfo, [0,20, 50])
    Push_Table_Values(Mtr.IQTB_IncentiveInfo,
                      DB_Fetch("select UID, total_days, Incentive from incentive_list", False,"LOL"), False)


    @Exception_Handle
    def Right_Click_Menu_Dept(pos):
        row = Mtr.IQTB_DeptInfo.selectedIndexes()
        R_menu = QMenu()
        Add = QAction("Add", R_menu)
        Update = QAction("Update", R_menu)
        R_menu.addAction(Add)
        R_menu.addAction(Update)
        pos = Mtr.IQTB_DeptInfo.mapToGlobal(pos)
        Add.triggered.connect(lambda: Add_Dept())
        Update.triggered.connect(lambda: Update_Dept())
        R_menu.exec_(pos)

    @Exception_Handle
    def Add_Dept():
        try:
            # Mtr.IQCB_DeptName.clear()
            Mtr.IQLE_Designation.clear()
            Mtr.GrpBox_DeptAdd.setVisible(True)
            Mtr.IQPB_DeptAdd.setEnabled(True)
            Mtr.IQPB_DeptUpdate.setEnabled(False)
            CB_List = []
            for i in range(len(Dep_List)):
                CB_List.append(Dep_List[i][1])
        except Exception as e:
            traceback.print_exc()

    @Exception_Handle
    def Update_Dept():
        # Mtr.IQCB_DeptName.clear()
        Mtr.IQLE_Designation.clear()
        Mtr.GrpBox_DeptAdd.setVisible(True)
        Mtr.IQPB_DeptUpdate.setEnabled(True)
        Mtr.IQPB_DeptAdd.setEnabled(False)
        selected_items = Mtr.IQTB_DeptInfo.selectedItems()
        if selected_items:
            selected_item = selected_items[0].row()
            Rgt_tbl = Fetch_Table_Values(Mtr.IQTB_DeptInfo)
            Rgt_tbl[selected_item][0]

            Mtr.IQLE_Designation.setText(Rgt_tbl[selected_item][1])
            globals()["UID"] = Rgt_tbl[selected_item][0]
            # globals()["Dept"] = Rgt_tbl[selected_item][1]
            globals()["Designation"] = Rgt_tbl[selected_item][1]

    @Exception_Handle
    def Update_Dept_Upd():
        if UI_Confirmation(UI_Confirm_Win, fr"Please confirm do you want to Update the {Mtr.IQLE_Designation.text()}"):
            dict = {
                'description': Mtr.IQLE_Designation.text(),
            }
            c_dict = {
                'UID': globals()["UID"],
            }
            DB_Update_Dict(dict, c_dict, "dep_list", False)
            Dep_List = DB_Fetch("Select UID, description  from dep_list",False, "LOL")
            Adjust_Table_Width(Mtr.IQTB_DeptInfo, [0, 35])
            Push_Table_Values(Mtr.IQTB_DeptInfo, Dep_List, False)
            # DB_Creation(Cur_Date_NF, False)
            UI_Confirmation(UI_Confirm_Win, "Data has been Updated Successfully")
            Mtr.GrpBox_DeptAdd.setVisible(False)
            Mtr.IQPB_DeptUpdate.setEnabled(False)

    @Exception_Handle
    def Add_Depart_In_Tbl():
        Maxi_UID = DB_Fetch("Select Max(UID)+1 from dep_list", False, "LOE")
        if UI_Confirmation(UI_Confirm_Win, fr"Please confirm do you want to Add ' {Mtr.IQLE_Designation.text()}'"):
            dict = {
                'UID' : Maxi_UID[0],
                'description': Mtr.IQLE_Designation.text(),
            }
            DB_Push_Dict(dict, "dep_list", True)
            Dep_List = DB_Fetch("Select UID, description  from dep_list",False, "LOL")
            Adjust_Table_Width(Mtr.IQTB_DeptInfo, [0, 35])
            Push_Table_Values(Mtr.IQTB_DeptInfo, Dep_List, False)
            # DB_Creation(Cur_Date_NF, False)
            UI_Confirmation(UI_Confirm_Win, "Data has been added Successfully")
        # Mtr.IQCB_DeptName.clear()
        Mtr.IQLE_Designation.clear()
        Mtr.IQPB_DeptAdd.setEnabled(False)
        Mtr.GrpBox_DeptAdd.setVisible(False)

    @Exception_Handle
    def Right_Click_Menu_Mail(pos):
        row = Mtr.IQTB_DeptInfo.selectedIndexes()
        R_menu = QMenu()
        Add = QAction("Add", R_menu)
        Update = QAction("Update", R_menu)
        R_menu.addAction(Add)
        R_menu.addAction(Update)
        pos = Mtr.IQTB_MailInfo.mapToGlobal(pos)
        Add.triggered.connect(lambda: Add_Dept_Mail())
        Update.triggered.connect(lambda: Update_Dept_Mail())
        R_menu.exec_(pos)

    @Exception_Handle
    def Add_Dept_Mail():
        globals()["common"] = "Add"
        Mtr.GrpBox_MailAdd.setVisible(True)
        Mtr.IQLE_Name.clear()
        Mtr.IQCB_Designation.clear()
        Mtr.IQLE_MailID.clear()
        CB_List = []
        for i in range(len(Dep_List)):
            CB_List.append(Dep_List[i][1])
        Mtr.IQCB_Designation.addItems(set(CB_List))

    @Exception_Handle
    def Update_Dept_Mail():
        globals()["common"] = "Update"
        Mtr.GrpBox_MailAdd.setVisible(True)
        Mtr.IQLE_Name.clear()
        Mtr.IQCB_Designation.clear()
        Mtr.IQLE_MailID.clear()
        selected_items = Mtr.IQTB_MailInfo.selectedItems()
        if selected_items:
            selected_item = selected_items[0].row()
            Rgt_tbl = Fetch_Table_Values(Mtr.IQTB_MailInfo)
            print(Rgt_tbl[selected_item][0], "UID")
            Mtr.IQLE_Name.setText(Rgt_tbl[selected_item][1])
            Mtr.IQCB_Designation.addItem(Rgt_tbl[selected_item][2])
            Mtr.IQLE_MailID.setText(Rgt_tbl[selected_item][3])
            globals()["UIDMail"] = Rgt_tbl[selected_item][0]
            globals()["Person"] = Rgt_tbl[selected_item][1]
            globals()["design"] = Rgt_tbl[selected_item][2]
            globals()["mail"] = Rgt_tbl[selected_item][3]

    @Exception_Handle
    def MailAddUpdate():
        Dep_List1 = DB_Fetch("Select max(UID)+1 from mail_list", False, "LOE")[0]
        # print(Dep_List1)
        if Dep_List1 is None:
            Dep_List1 = 1
        if globals()["common"] == "Add":
            if UI_Confirmation(UI_Confirm_Win,
                               fr"Please confirm do you want to Add the{Mtr.IQLE_Name.text()} and {Mtr.IQLE_MailID.text()}"):
                dict = {
                    'UID': Dep_List1,
                    'name_': Mtr.IQLE_Name.text(),
                    'designation': Mtr.IQCB_Designation.currentText(),
                    'mail_id' : Mtr.IQLE_MailID.text(),
                }

                DB_Push_Dict(dict, "mail_list", True)
                Dep_List = DB_Fetch("Select * from mail_list", False, "LOL")
                Adjust_Table_Width(Mtr.IQTB_MailInfo, [0, 20,20,40])
                Push_Table_Values(Mtr.IQTB_MailInfo, Dep_List, False)
                UI_Confirmation(UI_Confirm_Win, "Data added Successfully")
            Mtr.GrpBox_MailAdd.setVisible(False)
            Mtr.IQLE_Name.clear()
            Mtr.IQCB_Designation.clear()
            Mtr.IQLE_MailID.clear()
            globals()["common"] = None

        if globals()["common"] == "Update":
            if UI_Confirmation(UI_Confirm_Win,
                               fr"Please confirm do you want to Update the the data"):
                if Mtr.IQLE_Name.text() and Mtr.IQLE_MailID.text() is not None:
                    dict = {
                        'name_': Mtr.IQLE_Name.text() ,
                        'mail_id' : Mtr.IQLE_MailID.text(),
                    }
                    c_dict = {
                        'UID': globals()["UIDMail"],
                    }
                    DB_Update_Dict(dict, c_dict, "mail_list", False)
                    Dep_List = DB_Fetch("Select * from mail_list", False, "LOL")
                    Adjust_Table_Width(Mtr.IQTB_MailInfo, [0, 20,20,40])
                    Push_Table_Values(Mtr.IQTB_MailInfo, Dep_List, False)
                    # DB_Creation(Cur_Date_NF, False)
                    UI_Confirmation(UI_Confirm_Win, "Data has been Updated Successfully")
                    Mtr.GrpBox_MailAdd.setVisible(False)
                    Mtr.IQLE_Name.clear()
                    Mtr.IQCB_Designation.clear()
                    Mtr.IQLE_MailID.clear()
                    globals()["common"] = None

    @Exception_Handle
    def Update_Incentive():
        if Mtr.IQCB_Incentive.isChecked():
            # Mtr.IQTB_IncentiveInfo.setReadOnly(True)
            Mtr.IQPB_IncentiveUpdate.setEnabled(True)
            Adjust_Table_Width(Mtr.IQTB_IncentiveInfo, [0,20, 50])
            Push_Table_Values(Mtr.IQTB_IncentiveInfo,
                              DB_Fetch("select UID, total_days, Incentive from incentive_list", False, "LOL"), True)
        else:
            # Mtr.IQTB_IncentiveInfo.setReadOnly(False)
            Mtr.IQPB_IncentiveUpdate.setEnabled(False)
            Adjust_Table_Width(Mtr.IQTB_IncentiveInfo, [0, 20, 50])
            Push_Table_Values(Mtr.IQTB_IncentiveInfo,
                              DB_Fetch("select UID, total_days, Incentive from incentive_list", False, "LOL"), False)

    @Exception_Handle
    def Update_Incentive_DB(row):
        row = Mtr.IQTB_IncentiveInfo.selectedIndexes()[0].row()
        # print(row)
        data = Fetch_Table_Values(Mtr.IQTB_IncentiveInfo)[row]
        # print(data)

        dict = {
            'total_days': data[1],
            'Incentive': data[2],
        }
        c_dict = {
            'UID': data[0],
        }
        DB_Update_Dict(dict,c_dict, 'incentive_list', False)
        Adjust_Table_Width(Mtr.IQTB_IncentiveInfo, [0, 20, 50])
        Push_Table_Values(Mtr.IQTB_IncentiveInfo,
                          DB_Fetch("select UID, total_days, Incentive from incentive_list", False, "LOL"), False)
        Mtr.IQCB_Incentive.setChecked(False)











    # ___StandAlone Running___
    #------Department_List-------
    Mtr.IQPB_DeptAdd.clicked.connect(lambda : Add_Depart_In_Tbl())
    Mtr.IQPB_DeptUpdate.clicked.connect(lambda : Update_Dept_Upd())
    Mtr.IQTB_DeptInfo.setContextMenuPolicy(Qt.CustomContextMenu)
    Mtr.IQTB_DeptInfo.customContextMenuRequested.connect(Right_Click_Menu_Dept)
    Mtr.GrpBox_DeptAdd.setVisible(False)
    Mtr.IQPB_DeptAdd.setEnabled(False)
    Mtr.IQPB_DeptUpdate.setEnabled(False)


    #------Mail-Adding------
    globals()["common"] = None
    Mtr.GrpBox_MailAdd.setVisible(False)
    Mtr.IQTB_MailInfo.setContextMenuPolicy(Qt.CustomContextMenu)
    Mtr.IQTB_MailInfo.customContextMenuRequested.connect(Right_Click_Menu_Mail)
    Mtr.IQPB_MailAddUpdate.clicked.connect(lambda : MailAddUpdate())

    Mtr.IQCB_Incentive.stateChanged.connect(lambda:Update_Incentive())
    Mtr.IQPB_IncentiveUpdate.clicked.connect(Update_Incentive_DB)




if SAR == True:
    Master_FN(Mtr)
    Mtr.show()
    sys.exit(app.exec_())
