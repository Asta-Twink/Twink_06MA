# ___StandAlone INIT___
import traceback
from Env import *
if Mod_Work == True:SAR = True
else: SAR = False

@Exception_Handle
def Register_FN(Rgtr):
    globals()["Blob_Image_Nomi"] = None
    globals()["Blob_Image_Sign"] = None
    globals()["Blob_Image_Emp"] = None
    Customer_List = DB_Fetch(dbc,
                             "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y'  and  ET = 'PF' order by UID",
                             False, "LOL")
    Adjust_Table_Width(Rgtr.OQTB_EmployeeList, [100, 300, 75,75, 100])
    Push_Table_Values(Rgtr.OQTB_EmployeeList, Customer_List, False)

    @Exception_Handle
    def Temp_View_pwd():
        pwd.Pwd_txt.clear()
        pwd.Pwd_txt.setEchoMode(QLineEdit.Password)
        Rgtr.NonPFTOPF.setVisible(True)
        if Rgtr.Temp_View.isChecked() == True:
            def Pwd_Connect():
                pwd.close()
                if pwd.Pwd_txt.text() == "AstA":
                    globals()["Blob_Image_Nomi"] = None
                    globals()["Blob_Image_Sign"] = None
                    globals()["Blob_Image_Emp"] = None
                    Customer_List = DB_Fetch(dbc,
                                             "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y'  and  ET = 'Non PF' order by UID",
                                             False, "LOL")
                    Adjust_Table_Width(Rgtr.OQTB_EmployeeList, [100, 300, 75, 75, 100])
                    Push_Table_Values(Rgtr.OQTB_EmployeeList, Customer_List, False)

                    def NonPF_To_PF_Convert():
                        table_list=[]

                        new_id = Emp_code_Gen(True)
                        try:

                            sql = fr"UPDATE register SET emp_code = '{new_id}', ET = 'PF' WHERE UID = '{globals()['product_list'][0]}' and emp_code = '{globals()['Product_Master_Data']}'";
                            DB_Cmt(dbc,db,sql,False)
                            output = []
                            myresult = DB_Fetch(dbc,"Show Tables",False,"LOE")
                            for step in myresult:

                                try:
                                    a = int(step.split("_")[1])
                                    if a == 2023:
                                        output.append(step)

                                except:
                                    pass
                            output.append('advance_details')
                            for step in output:
                                try:
                                    sql = fr"UPDATE {step} SET empcode = '{new_id}' WHERE empcode = '{globals()['Product_Master_Data']}'";
                                    DB_Cmt(dbc, db, sql, False)
                                except Exception as e:
                                    print(e)
                                    pass

                            Customer_List = DB_Fetch(dbc,
                                                     "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y'  and  ET = 'Non PF' order by UID",
                                                     False, "LOL")
                            Push_Table_Values(Rgtr.OQTB_EmployeeList, Customer_List, False)
                            Adjust_Table_Width(Rgtr.OQTB_EmployeeList, [100, 300, 75, 75, 100])

                        except Exception as e:
                            print(e)
                            print("hello","imnot working")
                    Rgtr.NonPFTOPF.clicked.connect(lambda: NonPF_To_PF_Convert())

            pwd.show()
            pwd.OK_Btn.clicked.connect(lambda: Pwd_Connect())
        else:
            Customer_List = DB_Fetch(dbc,
                                     "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y'  and  ET = 'PF' order by UID",
                                     False, "LOL")

            Push_Table_Values(Rgtr.OQTB_EmployeeList, Customer_List, False)

        # if Rgtr.Temp_View.isChecked() == True:
        #     pwd.close()
        #     if pwd.Pwd_txt.text() == "AstA":
        #         Rgtr.NonPFTOPF.setVisible(True)
        #
        #         def NonPF_To_PF_Convert():
        #             print("Nonto")
        #             pass
        #
        #
        #
        #
        #     Rgtr.NonPFTOPF.clicked.connect(lambda: NonPF_To_PF_Convert())

    # Fetch_Table_individual_details
    @Exception_Handle
    def Fetch_tbl(row, column):

        Rgtr.OQCB_Dept.clear()
        Rgtr.OQCB_BloodGroup.clear()
        Rgtr.OQCB_Team.clear()
        Rgtr.OQL_EmpPhoto.clear()
        Rgtr.OQL_SignPhoto.clear()
        Rgtr.OQL_NomPhoto.clear()
        try:
            Cus_index = Fetch_Table_Values(Rgtr.OQTB_EmployeeList)
            Ind_detail = DB_Fetch(dbc, f"select * from register where emp_code ='{Cus_index[row][0]}'", False, "LOE")
            print(Ind_detail)
            print(len(Ind_detail))
            Rgtr.IQLE_EmpName.setText(Ind_detail[1])
            Rgtr.IQLE_EmpCode.setText(Ind_detail[2])
            Rgtr.OQCB_Dept.addItem(Ind_detail[3])
            Rgtr.IQLE_ESIC.setText(Ind_detail[4])
            Rgtr.IQLE_UAN.setText(Ind_detail[5])
            Rgtr.IQLE_PAN.setText(Ind_detail[6])
            Rgtr.IQLE_Aadhar.setText(Ind_detail[7])
            Rgtr.IQTE_Address.setText(Ind_detail[8])
            if Ind_detail[9] == 'Yes':
                Rgtr.IQRB_MrdYes.setChecked(True)
                Rgtr.IQRB_MrdNo.setChecked(False)
            else:
                Rgtr.IQRB_MrdNo.setChecked(True)
                Rgtr.IQRB_MrdYes.setChecked(False)
            Rgtr.IQLE_FatherSpouse.setText(Ind_detail[10])
            if Ind_detail[11] == 'M':
                Rgtr.IQRB_Male.setChecked(True)
            elif Ind_detail[11] == 'F':
                Rgtr.IQRB_Female.setChecked(True)
            else:
                Rgtr.IQRB_Other.setChecked(True)
            if Ind_detail[12] == 'Yes':
                Rgtr.IQRB_ShiftwrkYes.setChecked(True)
                Rgtr.IQRB_ShiftWrkNo.setChecked(False)
            else:
                Rgtr.IQRB_ShiftWrkNo.setChecked(True)
                Rgtr.IQRB_ShiftwrkYes.setChecked(False)
            Rgtr.IQLE_Shift1Salary.setText(str(Ind_detail[13]))
            Rgtr.IQLEShift2Salary.setText(str(Ind_detail[14]))
            Rgtr.IQLE_Shift3Salary.setText(str(Ind_detail[15]))
            Rgtr.IQLE_PhoneNo.setText(str(Ind_detail[16]))
            Rgtr.OQCB_BloodGroup.addItem(str(Ind_detail[17]))
            Rgtr.IQLE_BankAcNo.setText(str(Ind_detail[18]))
            Rgtr.IQLE_BankName.setText(str(Ind_detail[19]))
            Rgtr.IQLE_IFSC.setText(str(Ind_detail[20]))
            Rgtr.IQLE_Branch.setText(str(Ind_detail[21]))
            DoB = str(Ind_detail[22])
            DoJ = str(Ind_detail[23])
            Rgtr.OQDE_DOB.setDate(QDate.fromString(DoB, 'yyyy-MM-dd'))
            Rgtr.OQDE_DOJ.setDate(QDate.fromString(DoJ, 'yyyy-MM-dd'))
            Rgtr.IQLE_NomineeName.setText(str(Ind_detail[27]))
            Rgtr.IQLE_NomineePhNo.setText(str(Ind_detail[28]))
            if Ind_detail[30] == 'PF':
                Rgtr.IQRB_PF.setChecked(True)
                Rgtr.IQRB_NonPF.setChecked(False)
            else:
                Rgtr.IQRB_NonPF.setChecked(True)
                Rgtr.IQRB_PF.setChecked(False)
            if Ind_detail[31] == 'Y':
                Rgtr.OQC_OfficeStaff.setChecked(True)
            else:
                Rgtr.OQC_OfficeStaff.setChecked(False)
            Rgtr.OQCB_Team.addItem(Ind_detail[32])
            # Rgtr.OQL_EmpPhoto.setPixmap(QPixmap(fr"F:\Twink_AWM\Photos\{Ind_detail[2]}"))
            # Rgtr.OQL_EmpPhoto.setScaledContents(True)
            # print(type(Ind_detail[25]))
            # print(Ind_detail[25], "this is me")
            if Ind_detail[25] != bytes(b'...'):
                try:
                    pixmap = get_pixmap_from_blob(Ind_detail[25])
                    Rgtr.OQL_EmpPhoto.setPixmap(pixmap)
                    Rgtr.OQL_EmpPhoto.setScaledContents(True)
                except:
                    Rgtr.OQL_EmpPhoto.clear()
                    print("emp_name")
                try:
                    pixmap_Sig = get_pixmap_from_blob(Ind_detail[26])
                    Rgtr.OQL_SignPhoto.setPixmap(pixmap_Sig)
                    Rgtr.OQL_SignPhoto.setScaledContents(True)
                except:
                    Rgtr.OQL_SignPhoto.clear()
                try:
                    pixmap_Nomi = get_pixmap_from_blob(Ind_detail[29])
                    Rgtr.OQL_NomPhoto.setPixmap(pixmap_Nomi)
                    Rgtr.OQL_NomPhoto.setScaledContents(True)
                except:
                    Rgtr.OQL_NomPhoto.clear()
                    print("nomini")
            globals()["Product_Master_Data"] = Cus_index[row][0]
            globals()["product_list"]=Ind_detail
            print(globals()["product_list"],"its me ")
            # print(globals()["Product_Master_Data"])
        except Exception as e:
            traceback.print_exc()

    # Update_values
    @Exception_Handle
    def Enable_Update():
        # globals()["product_list"]
        # Rgtr.OQCB_Team.addItem(globals()["product_list"][32])
        # print(globals()["product_list"])
        Rgtr.GB_Add_Emp.setChecked(False)

        Rgtr.OQCB_Team.addItems(Team)
        Rgtr.OQCB_Dept.addItems(Dept)
        Rgtr.OQCB_BloodGroup.addItems(Blod_grp)
        Rgtr.IQLE_EmpName.setReadOnly(not Rgtr.IQLE_EmpName.isReadOnly())
        Rgtr.OQCB_Dept.setEnabled(True)
        Rgtr.IQLE_ESIC.setReadOnly(not Rgtr.IQLE_ESIC.isReadOnly())
        Rgtr.IQLE_UAN.setReadOnly(not Rgtr.IQLE_UAN.isReadOnly())
        Rgtr.IQLE_PAN.setReadOnly(not Rgtr.IQLE_PAN.isReadOnly())
        Rgtr.IQLE_Aadhar.setReadOnly(not Rgtr.IQLE_Aadhar.isReadOnly())
        Rgtr.IQTE_Address.setReadOnly(not Rgtr.IQTE_Address.isReadOnly())
        # Rgtr.IQRB_MrdYes.setEnabled(not Rgtr.IQRB_MrdYes.isEnabled())
        # Rgtr.IQRB_MrdNo.setEnabled(not Rgtr.IQRB_MrdNo.isEnabled())
        # Rgtr.IQRB_Male.setEnabled(not Rgtr.IQRB_Male.isEnabled())
        # Rgtr.IQRB_Female.setEnabled(not Rgtr.IQRB_Female.isEnabled())
        # Rgtr.IQRB_Other.setEnabled(not Rgtr.IQRB_Other.isEnabled())
        Rgtr.IQLE_FatherSpouse.setReadOnly(not Rgtr.IQLE_FatherSpouse.isReadOnly())
        Rgtr.IQLE_Shift1Salary.setReadOnly(not Rgtr.IQLE_Shift1Salary.isReadOnly())
        Rgtr.IQLEShift2Salary.setReadOnly(not Rgtr.IQLEShift2Salary.isReadOnly())
        Rgtr.IQLE_Shift3Salary.setReadOnly(not Rgtr.IQLE_Shift3Salary.isReadOnly())
        Rgtr.IQLE_PhoneNo.setReadOnly(not Rgtr.IQLE_PhoneNo.isReadOnly())
        Rgtr.OQCB_BloodGroup.setEnabled(True)
        Rgtr.IQLE_BankAcNo.setReadOnly(not Rgtr.IQLE_BankAcNo.isReadOnly())
        Rgtr.IQLE_BankName.setReadOnly(not Rgtr.IQLE_BankName.isReadOnly())
        Rgtr.IQLE_IFSC.setReadOnly(not Rgtr.IQLE_IFSC.isReadOnly())
        Rgtr.IQLE_Branch.setReadOnly(not Rgtr.IQLE_Branch.isReadOnly())
        Rgtr.OQDE_DOB.setReadOnly(not Rgtr.OQDE_DOB.isReadOnly())
        Rgtr.OQDE_DOJ.setReadOnly(not Rgtr.OQDE_DOJ.isReadOnly())
        Rgtr.IQLE_NomineeName.setReadOnly(not Rgtr.IQLE_NomineeName.isReadOnly())
        Rgtr.IQLE_NomineePhNo.setReadOnly(not Rgtr.IQLE_NomineePhNo.isReadOnly())
        # Rgtr.IQRB_PF.setEnabled(not Rgtr.IQRB_PF.isEnabled())
        # Rgtr.IQRB_NonPF.setEnabled(not Rgtr.IQRB_NonPF.isEnabled())
        # Rgtr.OQC_OfficeStaff.setEnabled(not Rgtr.OQC_OfficeStaff.isEnabled())
        # Rgtr.OQCB_Team.setEnabled(not Rgtr.OQCB_Team.isEnabled())
        Rgtr.IQRB_MrdYes.setEnabled(True)
        Rgtr.IQRB_MrdNo.setEnabled(True)
        Rgtr.IQRB_Male.setEnabled(True)
        Rgtr.IQRB_Female.setEnabled(True)
        Rgtr.IQRB_Other.setEnabled(True)
        Rgtr.IQRB_ShiftwrkYes.setEnabled(True)
        Rgtr.IQRB_ShiftWrkNo.setEnabled(True)
        Rgtr.IQRB_PF.setEnabled(False)
        Rgtr.IQRB_NonPF.setEnabled(False)
        Rgtr.OQC_OfficeStaff.setEnabled(True)
        Rgtr.OQCB_Team.setEnabled(True)
        Rgtr.IQPB_PhotoBrowse.setEnabled(True)
        Rgtr.OQL_Sign.setEnabled(True)
        Rgtr.IQPB_NomPhotoBrowse.setEnabled(True)
        print("hello")

    @Exception_Handle
    def Enable_Add():

        Rgtr.GB_UpdateEmp.setChecked(False)

        Rgtr.IQLE_EmpCode.clear()
        Rgtr.IQLE_EmpName.clear()
        Rgtr.OQCB_Dept.clear()
        Rgtr.IQLE_ESIC.clear()
        Rgtr.IQLE_UAN.clear()
        Rgtr.IQLE_PAN.clear()
        Rgtr.IQLE_Aadhar.clear()
        Rgtr.IQTE_Address.clear()
        Rgtr.IQRB_MrdYes.setChecked(False)
        Rgtr.IQRB_MrdNo.setChecked(False)
        Rgtr.IQRB_Male.setChecked(False)
        Rgtr.IQRB_Female.setChecked(False)
        Rgtr.IQRB_Other.setChecked(False)
        Rgtr.IQRB_ShiftwrkYes.setChecked(False)
        Rgtr.IQRB_ShiftWrkNo.setChecked(False)
        Rgtr.IQRB_PF.setEnabled(True)
        Rgtr.IQRB_NonPF.setEnabled(True)
        Rgtr.IQRB_PF.setChecked(False)
        Rgtr.IQRB_NonPF.setChecked(False)
        Rgtr.OQC_OfficeStaff.setChecked(False)
        Rgtr.IQLE_FatherSpouse.clear()
        Rgtr.IQLE_Shift1Salary.clear()
        Rgtr.IQLEShift2Salary.clear()
        Rgtr.IQLE_Shift3Salary.clear()
        Rgtr.IQLE_PhoneNo.clear()
        Rgtr.OQCB_BloodGroup.clear()
        Rgtr.IQLE_BankAcNo.clear()
        Rgtr.IQLE_BankName.clear()
        Rgtr.IQLE_IFSC.clear()
        Rgtr.IQLE_Branch.clear()
        Rgtr.OQDE_DOB.setDate(QtCore.QDate.currentDate())
        Rgtr.OQDE_DOJ.setDate(QtCore.QDate.currentDate())
        Rgtr.IQLE_NomineeName.clear()
        Rgtr.IQLE_NomineePhNo.clear()
        Rgtr.OQCB_Team.clear()
       #-----------------------------------
        Rgtr.OQCB_Dept.addItems(Dept)
        Rgtr.OQCB_Team.addItems(Team)
        Rgtr.OQCB_BloodGroup.addItems(Blod_grp)
        Rgtr.IQLE_EmpName.setReadOnly(not Rgtr.IQLE_EmpName.isReadOnly())
        Rgtr.IQLE_EmpCode.setEnabled(False)
        Rgtr.IQLE_EmpCode.setText(Emp_code_Gen(True))
        # Rgtr.OQCB_Dept.setEnabled(not Rgtr.OQCB_Dept.isEnabled())
        Rgtr.IQLE_ESIC.setReadOnly(not Rgtr.IQLE_ESIC.isReadOnly())
        Rgtr.IQLE_UAN.setReadOnly(not Rgtr.IQLE_UAN.isReadOnly())
        Rgtr.IQLE_PAN.setReadOnly(not Rgtr.IQLE_PAN.isReadOnly())
        Rgtr.IQLE_Aadhar.setReadOnly(not Rgtr.IQLE_Aadhar.isReadOnly())
        Rgtr.IQTE_Address.setReadOnly(not Rgtr.IQTE_Address.isReadOnly())
        Rgtr.OQL_EmpPhoto.clear()
        Rgtr.OQL_SignPhoto.clear()
        Rgtr.OQL_NomPhoto.clear()
        Rgtr.OQL_EmpPhoto.setText("")
        Rgtr.OQL_SignPhoto.setText("")
        Rgtr.OQL_NomPhoto.setText("")

        Rgtr.IQRB_MrdYes.setEnabled(not Rgtr.IQRB_MrdYes.isEnabled())
        Rgtr.IQRB_MrdNo.setEnabled(not Rgtr.IQRB_MrdNo.isEnabled())
        Rgtr.IQRB_Male.setEnabled(not Rgtr.IQRB_Male.isEnabled())
        Rgtr.IQRB_Female.setEnabled(not Rgtr.IQRB_Female.isEnabled())
        Rgtr.IQRB_Other.setEnabled(not Rgtr.IQRB_Other.isEnabled())
        Rgtr.IQRB_ShiftwrkYes.setEnabled(not Rgtr.IQRB_ShiftwrkYes.isEnabled())
        Rgtr.IQRB_ShiftWrkNo.setEnabled(not Rgtr.IQRB_ShiftWrkNo.isEnabled())
        Rgtr.OQC_OfficeStaff.setEnabled(not Rgtr.OQC_OfficeStaff.isEnabled())

        # Rgtr.IQRB_PF.setEnabled(not Rgtr.IQRB_PF.isEnabled())
        # Rgtr.IQRB_NonPF.setEnabled(not Rgtr.IQRB_NonPF.isEnabled())
        # Rgtr.OQC_OfficeStaff.setEnabled(not Rgtr.OQC_OfficeStaff.isEnabled())
        # Rgtr.IQRB_OffficeSTFNo.setEnabled(not Rgtr.IQRB_OffficeSTFNo.isEnabled())
        # Rgtr.OQCB_Team.setEnabled(not Rgtr.OQCB_Team.isEnabled())
        # Rgtr.IQLE_Reason.setReadOnly(not Rgtr.IQLE_Reason.isReadOnly())


        Rgtr.IQLE_FatherSpouse.setReadOnly(not Rgtr.IQLE_FatherSpouse.isReadOnly())
        Rgtr.IQLE_Shift1Salary.setReadOnly(not Rgtr.IQLE_Shift1Salary.isReadOnly())
        Rgtr.IQLEShift2Salary.setReadOnly(not Rgtr.IQLEShift2Salary.isReadOnly())
        Rgtr.IQLE_Shift3Salary.setReadOnly(not Rgtr.IQLE_Shift3Salary.isReadOnly())
        Rgtr.IQLE_PhoneNo.setReadOnly(not Rgtr.IQLE_PhoneNo.isReadOnly())
        # Rgtr.OQCB_BloodGroup.setEnabled(not Rgtr.OQCB_BloodGroup.isEnabled())
        Rgtr.IQLE_BankAcNo.setReadOnly(not Rgtr.IQLE_BankAcNo.isReadOnly())
        Rgtr.IQLE_BankName.setReadOnly(not Rgtr.IQLE_BankName.isReadOnly())
        Rgtr.IQLE_IFSC.setReadOnly(not Rgtr.IQLE_IFSC.isReadOnly())
        Rgtr.IQLE_Branch.setReadOnly(not Rgtr.IQLE_Branch.isReadOnly())
        Rgtr.OQDE_DOB.setReadOnly(not Rgtr.OQDE_DOB.isReadOnly())
        Rgtr.OQDE_DOJ.setReadOnly(not Rgtr.OQDE_DOJ.isReadOnly())
        Rgtr.IQLE_NomineeName.setReadOnly(not Rgtr.IQLE_NomineeName.isReadOnly())
        Rgtr.IQLE_NomineePhNo.setReadOnly(not Rgtr.IQLE_NomineePhNo.isReadOnly())

        Rgtr.IQPB_PhotoBrowse.setEnabled(True)
        Rgtr.OQL_Sign.setEnabled(True)
        Rgtr.IQPB_NomPhotoBrowse.setEnabled(True)

        print("hello")

    @Exception_Handle
    def Update_Emp_Details():


        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MSeGa@1109',
            database='twink_06ma'
        )

        if globals()["Blob_Image_Nomi"] != None:
            cursor = conn.cursor()
            insert_query_Nomi = "UPDATE register SET nominee_photo = %s WHERE emp_code = %s"
            data_Nomi = (globals()["Blob_Image_Nomi"], globals()["Product_Master_Data"])
            cursor.execute(insert_query_Nomi, data_Nomi)
            conn.commit()
            cursor.close()
            conn.close()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MSeGa@1109',
            database='twink_06ma'
        )

        if globals()["Blob_Image_Sign"] != None:
            insert_query_Sign = "UPDATE register SET signature = %s WHERE emp_code = %s"
            data_Sign = (globals()["Blob_Image_Sign"], globals()["Product_Master_Data"])
            cursor = conn.cursor()
            cursor.execute(insert_query_Sign, data_Sign)
            conn.commit()
            cursor.close()
            conn.close()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MSeGa@1109',
            database='twink_06ma'
        )

        if globals()["Blob_Image_Emp"] != None:
            cursor = conn.cursor()
            insert_query_Emp = "UPDATE register SET photo = %s WHERE emp_code = %s"
            data_Emp = (globals()["Blob_Image_Emp"], globals()["Product_Master_Data"])
            cursor.execute(insert_query_Emp, data_Emp)
            conn.commit()
            cursor.close()
            conn.close()




        DOB_Date = Rgtr.OQDE_DOB.date().toString(Qt.ISODate)
        DOJ_Date = Rgtr.OQDE_DOJ.date().toString(Qt.ISODate)


        if Rgtr.IQRB_MrdYes.isChecked():
            Mar = 'Yes'
        else:
            Mar = 'No'
        if Rgtr.IQRB_ShiftwrkYes.isChecked():
            Shift = 'Yes'
        else:
            Shift = 'No'
        if Rgtr.OQC_OfficeStaff.isChecked():
            Office = 'Y'
        else:
            Office = 'N'
        if Rgtr.IQRB_PF.isChecked():
            PF = 'PF'
        else:
            PF = 'Non PF'
        if Rgtr.IQRB_Male.isChecked():
            Gnd = "M"
        elif Rgtr.IQRB_Female.isChecked():
            Gnd = "F"
        else:
            Gnd = "O"
        dict = {
            'employee_name': Rgtr.IQLE_EmpName.text(),
            'designation': Rgtr.OQCB_Dept.currentText(),
            'esic_no': Rgtr.IQLE_ESIC.text(),
            'uan_no': Rgtr.IQLE_UAN.text(),
            'pan_no': Rgtr.IQLE_PAN.text(),
            'aadhar_no': Rgtr.IQLE_Aadhar.text(),
            'address': Rgtr.IQTE_Address.toPlainText(),
            'marriage_status': Mar,
            'f_sp_name': Rgtr.IQLE_FatherSpouse.text(),
            'gender': Gnd,
            'shift_work': Shift,
            'shift_1_salary': Rgtr.IQLE_Shift1Salary.text(),
            'shift_2_salary': Rgtr.IQLEShift2Salary.text(),
            'shift_3_salary': Rgtr.IQLE_Shift3Salary.text(),
            'phone_no': Rgtr.IQLE_PhoneNo.text(),
            'blood_group': Rgtr.OQCB_BloodGroup.currentText(),
            'bank_account_no': Rgtr.IQLE_BankAcNo.text(),
            'bank_name': Rgtr.IQLE_BankName.text(),
            'ifsc_code': Rgtr.IQLE_IFSC.text(),
            'branch': Rgtr.IQLE_Branch.text(),
            'date_of_birth': DOB_Date,
            'date_of_join': DOJ_Date,
            # 'photo' : globals()["Blob_Image"],
            # 'signature' : Rgtr.OQL_SignPhoto.pixmap(),
            # 'nominee_photo' : Rgtr.OQL_NomPhoto.pixmap(),
            'nominee_name': Rgtr.IQLE_NomineeName.text(),
            'nominee_phone_no': Rgtr.IQLE_NomineePhNo.text(),
            'ET': PF,
            'office_staff': Office,
            'team': Rgtr.OQCB_Team.currentText(),
        }
        c_dict = {
            'emp_code': globals()["Product_Master_Data"],
        }
        DB_Update_Dict(dbc, db, dict, c_dict, "register", False)
        Customer_List = DB_Fetch(dbc,
                                 "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y' order by UID",
                                 False, "LOL")
        Push_Table_Values(Rgtr.OQTB_EmployeeList, Customer_List, False)
        Adjust_Table_Width(Rgtr.OQTB_EmployeeList, [100, 300, 75,75, 100])
        globals()["Blob_Image_Nomi"] = None
        globals()["Blob_Image_Sign"] = None
        globals()["Blob_Image_Emp"] = None

    @Exception_Handle
    def Add_Emp_Details():


        DOB_Date = Rgtr.OQDE_DOB.date().toString(Qt.ISODate)
        DOJ_Date = Rgtr.OQDE_DOJ.date().toString(Qt.ISODate)


        # try:
        #     globals()["Blob_Image_Nomi"]
        # except:
        #     print("nomi")
        #     filepath=fr"F:\Twink_AWM\Temp\No Image.jpg"
        #     original_image_data = read_image(filepath)
        #     new_width, new_height = 500, 300
        #     resized_image_data = resize_image(original_image_data, new_width, new_height)
        #     pixmap = QPixmap()
        #     pixmap.loadFromData(resized_image_data)
        #     Rgtr.OQL_NomPhoto.setPixmap(pixmap)
        #     globals()["Blob_Image_Nomi"] = original_image_data
        #
        # try:
        #     globals()["Blob_Image_Sign"]
        # except:
        #     globals()["Blob_Image_Sign"]=""
        #
        # try:
        #     globals()["Blob_Image_Emp"]
        # except:
        #     print("emp")
        #     filepath = fr"F:\Twink_AWM\Temp\No Image.jpg"
        #     original_image_data = read_image(filepath)
        #     new_width, new_height = 500, 300
        #     resized_image_data = resize_image(original_image_data, new_width, new_height)
        #     pixmap = QPixmap()
        #     pixmap.loadFromData(resized_image_data)
        #     Rgtr.OQL_EmpPhoto.setPixmap(pixmap)
        #     globals()["Blob_Image_Emp"] = original_image_data

        DOB_Date = Rgtr.OQDE_DOB.date().toString(Qt.ISODate)
        DOJ_Date = Rgtr.OQDE_DOJ.date().toString(Qt.ISODate)


        if Rgtr.IQRB_MrdYes.isChecked():
            Mar = 'Yes'
        else:
            Mar = 'No'
        if Rgtr.IQRB_ShiftwrkYes.isChecked():
            Shift = 'Yes'
        else:
            Shift = 'No'
        if Rgtr.OQC_OfficeStaff.isChecked():
            Office = 'Y'
        else:
            Office = 'N'
        if Rgtr.IQRB_PF.isChecked():
            PF = 'PF'
        else:
            PF = 'Non PF'
        if Rgtr.IQRB_Male.isChecked():
            Gnd = "M"
        elif Rgtr.IQRB_Female.isChecked():
            Gnd = "F"
        else:
            Gnd = "O"
        dict = {
            'employee_name': Rgtr.IQLE_EmpName.text(),
            'emp_code': Rgtr.IQLE_EmpCode.text(),
            'designation': Rgtr.OQCB_Dept.currentText(),
            'esic_no': Rgtr.IQLE_ESIC.text(),
            'uan_no': Rgtr.IQLE_UAN.text(),
            'pan_no': Rgtr.IQLE_PAN.text(),
            'aadhar_no': Rgtr.IQLE_Aadhar.text(),
            'address': Rgtr.IQTE_Address.toPlainText(),
            'marriage_status': Mar,
            'f_sp_name': Rgtr.IQLE_FatherSpouse.text(),
            'gender': Gnd,
            'shift_work': Shift,
            'shift_1_salary': Rgtr.IQLE_Shift1Salary.text(),
            'shift_2_salary': Rgtr.IQLEShift2Salary.text(),
            'shift_3_salary': Rgtr.IQLE_Shift3Salary.text(),
            # 'photo':globals()["Blob_Image_Emp"],
            # 'signature': globals()["Blob_Image_Sign"],
            # 'nominee_photo': globals()["Blob_Image_Nomi"],
            'phone_no': Rgtr.IQLE_PhoneNo.text(),
            'blood_group': Rgtr.OQCB_BloodGroup.currentText(),
            'bank_account_no': Rgtr.IQLE_BankAcNo.text(),
            'bank_name': Rgtr.IQLE_BankName.text(),
            'ifsc_code': Rgtr.IQLE_IFSC.text(),
            'branch': Rgtr.IQLE_Branch.text(),
            'date_of_birth': DOB_Date,
            'date_of_join': DOJ_Date,
            'nominee_name': Rgtr.IQLE_NomineeName.text(),
            'nominee_phone_no': Rgtr.IQLE_NomineePhNo.text(),
            'ET': PF,
            'office_staff': Office,
            'team': Rgtr.OQCB_Team.currentText(),
        }

        DB_Push_Dict(dbc, db, dict, "register", False)

        Customer_List = DB_Fetch(dbc,
                                 "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y' order by UID",
                                 False, "LOL")
        Push_Table_Values(Rgtr.OQTB_EmployeeList, Customer_List, False)
        DB_Creation(Cur_Date_NF, False)


        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MSeGa@1109',
            database='twink_06ma'
        )

        if globals()["Blob_Image_Nomi"] != None:
            cursor = conn.cursor()
            insert_query_Nomi = "UPDATE register SET nominee_photo = %s WHERE emp_code = %s"
            data_Nomi = (globals()["Blob_Image_Nomi"], Rgtr.IQLE_EmpCode.text())
            cursor.execute(insert_query_Nomi, data_Nomi)
            conn.commit()
            cursor.close()
            conn.close()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MSeGa@1109',
            database='twink_06ma'
        )

        if globals()["Blob_Image_Sign"] != None:
            insert_query_Sign = "UPDATE register SET signature = %s WHERE emp_code = %s"
            data_Sign = (globals()["Blob_Image_Sign"], Rgtr.IQLE_EmpCode.text())
            cursor = conn.cursor()
            cursor.execute(insert_query_Sign, data_Sign)
            conn.commit()
            cursor.close()
            conn.close()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MSeGa@1109',
            database='twink_06ma'
        )

        if globals()["Blob_Image_Emp"] != None:
            cursor = conn.cursor()
            insert_query_Emp = "UPDATE register SET photo = %s WHERE emp_code = %s"
            data_Emp = (globals()["Blob_Image_Emp"], Rgtr.IQLE_EmpCode.text())
            cursor.execute(insert_query_Emp, data_Emp)
            conn.commit()
            cursor.close()
            conn.close()
        globals()["Blob_Image_Nomi"] = None
        globals()["Blob_Image_Sign"] = None
        globals()["Blob_Image_Emp"] = None

    @Exception_Handle
    def Right_Click_Menu(pos):
        row = Rgtr.OQTB_EmployeeList.selectedIndexes()
        R_menu = QMenu()
        Remove = QAction("Remove", R_menu)
        Revert = QAction("Revert", R_menu)
        R_menu.addAction(Remove)
        R_menu.addAction(Revert)
        pos = Rgtr.OQTB_EmployeeList.mapToGlobal(pos)
        Remove.triggered.connect(lambda: Delete_Employee(row[0].row()))
        Revert.triggered.connect(lambda: Revert_Employee())
        R_menu.exec_(pos)

    @Exception_Handle
    def Delete_Employee(index):
        dict = {
            'Active_status': "N"
        }
        Employee = Fetch_Table_Values(Rgtr.OQTB_EmployeeList)[index][0]

        c_dict = {
            'emp_code': Employee
        }

        if UI_Confirmation(UI_Confirm_Win, f"Please confirm to delete the Employee :< {Employee} >:"):
            DB_Update_Dict(dbc, db, dict, c_dict, 'register', True)
            Employee_Master_Data = DB_Fetch(dbc,
                             "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y' order by UID",
                             False, "LOL")
            Push_Table_Values(Rgtr.OQTB_EmployeeList, Employee_Master_Data, False)

    @Exception_Handle
    def Revert_Employee():
            @Exception_Handle
            def Revert_DB_Push():
                temp = Rvt.OQTB_EmpRevert.selectedItems()
                if UI_Confirmation(UI_Confirm_Win, f"Please confirm to revert the Selected Employee"):
                    for step in temp:
                        dict = {
                            'active_status': "Y"
                        }
                        Employee = Fetch_Table_Values(Rvt.OQTB_EmpRevert)[step.row()][1]

                        c_dict = {
                            'UID': Fetch_Employee_ID(Employee)
                        }

                        DB_Update_Dict(dbc, db, dict, c_dict, 'register', False)
                    Push_Table_Values(Rvt.OQTB_EmpRevert,
                                      DB_Fetch(dbc,
                                               'select emp_code,employee_name,designation,phone_no from register where active_status = "N"',
                                               False, "LOL"), False)
                Employee_Master_Data = DB_Fetch(dbc,
                                                "select emp_code,employee_name,gender,blood_group,phone_no from register where active_status = 'Y' order by UID",
                                                False, "LOL")
                Push_Table_Values(Rgtr.OQTB_EmployeeList, Employee_Master_Data, False)


            Adjust_Table_Width(Rvt.OQTB_EmpRevert,(150,300,180,150))
            Push_Table_Values(Rvt.OQTB_EmpRevert,
                              DB_Fetch(dbc,
                                       'select emp_code,employee_name,designation,phone_no from register where active_status = "N"',
                                       False, "LOL"), False)
            Rvt.show()
            Rvt.IQDB_EmpRevert.accepted.connect(lambda: Revert_DB_Push())
            Rvt.IQDB_EmpRevert.rejected.connect(lambda: Rvt.close())

    @Exception_Handle
    def read_image(file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    @Exception_Handle
    def open_file_dialog_Emp_Img():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        file_dialog.setWindowTitle("Select an Image")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            original_image_data = read_image(selected_file)
            new_width, new_height = 500, 300
            resized_image_data = resize_image(original_image_data, new_width, new_height)
            pixmap = QPixmap()
            pixmap.loadFromData(resized_image_data)
            Rgtr.OQL_EmpPhoto.setPixmap(pixmap)
            globals()["Blob_Image_Emp"] = resized_image_data

    @Exception_Handle
    def open_file_dialog_Emp_Sign():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        file_dialog.setWindowTitle("Select an Image")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            original_image_data = read_image(selected_file)
            new_width, new_height = 200, 300
            resized_image_data = resize_image(original_image_data, new_width, new_height)
            pixmap = QPixmap()
            pixmap.loadFromData(resized_image_data)
            Rgtr.OQL_SignPhoto.setPixmap(pixmap)
            globals()["Blob_Image_Sign"] = resized_image_data

    @Exception_Handle
    def open_file_dialog_Emp_Nomi():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        file_dialog.setWindowTitle("Select an Image")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            original_image_data = read_image(selected_file)
            new_width, new_height = 500, 300
            resized_image_data = resize_image(original_image_data, new_width, new_height)
            pixmap = QPixmap()
            pixmap.loadFromData(resized_image_data)
            Rgtr.OQL_NomPhoto.setPixmap(pixmap)
            globals()["Blob_Image_Nomi"] = resized_image_data

    @Exception_Handle
    def get_pixmap_from_blob(blob_data):
        # Convert the blob data to a QPixmap
        try:
            img = Image.open(BytesIO(blob_data))
            img = img.convert("RGB")  # Convert image mode if needed (PIL related)
            img.save("temp_image.jpg")  # Save the temporary image
            pixmap = QPixmap("temp_image.jpg")  # Load the temporary image as QPixmap
            return pixmap
        except:
            print("No BLOB")

    # ___Right Click Menu___

    Rgtr.NonPFTOPF.setVisible(False)
    Rgtr.OQTB_EmployeeList.cellClicked.connect(Fetch_tbl)

    Rgtr.IQPB_Update.clicked.connect(lambda: Update_Emp_Details())
    Rgtr.GB_UpdateEmp.clicked.connect(lambda: Enable_Update())
    Rgtr.GB_Add_Emp.clicked.connect(lambda: Enable_Add())
    Rgtr.IQPB_Add.clicked.connect(lambda: Add_Emp_Details())




    Rgtr.OQTB_EmployeeList.setContextMenuPolicy(Qt.CustomContextMenu)
    Rgtr.OQTB_EmployeeList.customContextMenuRequested.connect(Right_Click_Menu)




    Rgtr.IQRB_PF.toggled.connect(lambda: Rgtr.IQLE_EmpCode.setText(Emp_code_Gen(True)))
    Rgtr.IQRB_NonPF.toggled.connect(lambda: Rgtr.IQLE_EmpCode.setText(Emp_code_Gen(False)))

    Rgtr.IQPB_PhotoBrowse.clicked.connect(lambda: open_file_dialog_Emp_Img())
    Rgtr.OQL_Sign.clicked.connect(lambda: open_file_dialog_Emp_Sign())
    Rgtr.IQPB_NomPhotoBrowse.clicked.connect(lambda: open_file_dialog_Emp_Nomi())
    Rgtr.Temp_View.stateChanged.connect(lambda: Temp_View_pwd())
    # Rgtr.Temp_View.stateChanged.connect(lambda: NonPF_To_PF_Convert_Flow())
    # Rgtr.NonPFTOPF.clicked.connect(lambda :NonPF_To_PF_Convert())

# ___StandAlone Running___
if SAR == True:
    Register_FN(Rgtr)
    Rgtr.show()
    sys.exit(app.exec_())
