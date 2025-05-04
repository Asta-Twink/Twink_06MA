import os
from num2words import num2words

# ___Get the current working directory___
def Run_Project():
    global ldir,config,Mod_Work
    # dir = fr"{os.getcwd()}\_internal"
    dir = fr"D:\Twink_SourceCode\06MA\_internal"
    file_path = [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith('.txt')][0]
    with open(file_path, 'r') as file:
        lines = file.readlines()
    config = []
    for line in lines:
        values = line.strip().split()
        config.extend(values)
    if config[0] =='1': Mod_Work=False; ldir = fr"{os.getcwd()}\_internal"
    else:Mod_Work=True; ldir = config[1]

Run_Project()

#_________ Qt Imports _________
from PyQt5 import \
    QtCore, \
    QtGui, \
    QtWidgets as Qwid, \
    uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem as T_itm
from PyQt5.QtWidgets import \
    QComboBox, \
    QCompleter,\
    QShortcut, \
    QAction
from PyQt5.QtCore import \
    QSortFilterProxyModel,\
    Qt,QCoreApplication, \
    QDate, \
    QByteArray, \
    QBuffer,\
    QIODevice
from PyQt5.QtCore import \
    QSortFilterProxyModel,\
    Qt,QCoreApplication, \
    QDate, \
    QByteArray, \
    QBuffer,\
    QIODevice
from PyQt5.QtGui import \
    QPixmap, \
    QImage,\
    QKeySequence,\
    QImageReader,\
    QColor,\
    QFont
from mysql.connector.locales.eng import client_error
from mysql.connector.plugins import caching_sha2_password
# ___Generic Import Statements___
import mysql.connector,\
    openpyxl,\
    sys,\
    win32com.client,\
    traceback,\
    inspect,\
    calendar, \
    pandas as pd

from PIL import Image
from io import BytesIO
import subprocess
#_________ DateTime Imports _________
from datetime import datetime,\
    date,\
    timedelta,\
    time
import datetime as dt

# ___Exception Handling___
def Show_Error(title, message):#Show an error Message
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Warning)
    error_box.setWindowTitle(title)
    error_box.setText(message)
    error_box.exec_()

def Exception_Handle(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_info = traceback.format_exc()
            calling_frame = inspect.currentframe().f_back
            file_name = calling_frame.f_code.co_filename
            line_number = calling_frame.f_lineno
            error_message = f"Error in function {func.__name__} (called from {file_name} line {line_number}):\n{exc_info}"
            print('error_message',error_message)
            Show_Error("ERROR:", error_message)
    return wrapper

def Window_Holder(window):
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window.destroyed.connect(app.quit)
    app.exec_()

app = Qwid.QApplication(sys.argv)
Twink_UI = uic.loadUi(fr'{ldir}\F2_MODULES\BASE_WIN\UI-Base_Win.ui')
UI_Confirm_Win = uic.loadUi(fr'{ldir}\F2_MODULES\BASE_WIN\UI-Confirmation_Win.ui')

@Exception_Handle
def Return_Confirmatiom(temp, stmnt):
    global UI_Confirm
    UI_Confirm=stmnt
    temp.close()

@Exception_Handle
def UI_Confirmation(temp,inp):
    temp.NEX_Message.setText(inp)
    temp.IQDB_Confirmation.accepted.connect(lambda : Return_Confirmatiom(temp,True))
    temp.IQDB_Confirmation.rejected.connect(lambda : Return_Confirmatiom(temp,False))
    temp.exec_()
    Window_Holder(temp)
    try:
        return UI_Confirm
    except:
        pass

# ___DB Functions___
@Exception_Handle
def DB_Connect(cred):
    MySQL_database = mysql.connector.connect(host=cred['host'], user=cred['user'], passwd=cred['password'],
                                             database=cred['database'],port = cred['port'])
    db_con = MySQL_database.cursor()
    return db_con,MySQL_database

# ___Database Dictioanry___
Local_DB = \
    {
        'host': 'localhost',
        'user': 'root',
        'password': 'MSeGa@1109',
        'database': config[3],
        "port":3306
    }
Cloud_DB = \
    {
        'host': config[4],
        'user': config[5],
        'password':config[6],
        'database':  config[3],
        'port':config[7]
    }
# // Use """ db """ as variable for all db connections
if config[2]=="LOCAL":
    dbase = DB_Connect(Local_DB)
if config[2]=="CLOUD":
    dbase = DB_Connect(Cloud_DB)
dbc = dbase[0]
db = dbase[1]

@Exception_Handle
def DB_Exe(sql,prnt):
    if prnt == True:
        print(sql)
    dbc.execute(sql)

@Exception_Handle
def DB_Cmt(sql,prnt):
    if prnt == True:
        print(sql)
    dbc.execute(sql)
    db.commit()

def DB_Cmt_WOE(sql,prnt):
    if prnt == True:
        print(sql)
    dbc.execute(sql)
    db.commit()

@Exception_Handle
def DB_Fetch(sql,prnt,type):
    if prnt == True:
        print(sql)
    dbc.execute(sql)
    if type == "LOE":
        return list(sum(dbc.fetchall(),()))
    if type == "LOL":
        return [list(x) for x in dbc.fetchall()]
    if type == "DIC":
        try:
            return {key: value for key, value in [list(x) for x in dbc.fetchall()]}
        except: return None

@Exception_Handle
def DB_TBL_Fetch(tbl,indexlist,active):
    if active == True:
        dbc.execute(f'select * from {tbl} where active ="Y"')
    if active == False:
        dbc.execute(f'select * from {tbl} where active ="N"')
    if active == None:
        dbc.execute(f'select * from {tbl}')

    data=[list(x) for x in dbc.fetchall()]
    if indexlist == True:
        return data
    if isinstance(indexlist, int):
        return [inner_list[:indexlist] for inner_list in data]
    if isinstance(indexlist, list):
        return [[inner_list[index] for index in indexlist] for inner_list in data]

@Exception_Handle
def DB_Push_Dict(dict,tbl_nm,prnt):
    placeholders = ', '.join([f'"{element}"' for element in dict.values()])
    columns = ', '.join(dict.keys())
    sql = f"INSERT INTO {tbl_nm} ( {columns} ) VALUES ( {placeholders} )"
    DB_Cmt(sql,prnt)

@Exception_Handle
def DB_Delete_Dict(dict,tbl_nm,prnt):
    c_dict = ' AND '.join([f"{key} = '{value}'" for key, value in dict.items()])
    sql = f"DELETE FROM {tbl_nm} WHERE {c_dict};"
    DB_Cmt(sql,prnt)

@Exception_Handle
def DB_Update_Dict(dict,c_dict,tbl_nm,prnt):
    dict =', '.join([f"{key} = '{value}'" for key, value in dict.items()])
    c_dict = ' AND '.join([f"{key} = '{value}'" for key, value in c_dict.items()])
    sql = f" UPDATE {tbl_nm} SET {dict} WHERE {c_dict} LIMIT 1"
    DB_Cmt(sql, prnt)

def DB_Update_Dict_WOL(dict,c_dict,tbl_nm,prnt):
    dict =', '.join([f"{key} = '{value}'" for key, value in dict.items()])
    c_dict = ' AND '.join([f"{key} = '{value}'" for key, value in c_dict.items()])
    sql = f" UPDATE {tbl_nm} SET {dict} WHERE {c_dict} "
    DB_Cmt(sql, prnt)

#CMD to Use Root Dir
@Exception_Handle
def Use_Root_Dir():
    os.chdir(ldir)

#___Time Functions___
def Mysql_Date(inp):
    try:
        dateform = datetime.strptime(inp, '%d/%m/%Y')
    except:
        dateform = datetime.strptime(inp, '%d-%m-%Y')
    return dateform.strftime('%Y-%m-%d')

Cur_Date = datetime.today()
Cur_date_M = Cur_Date.strftime("%m")
Cur_Date_NF = Cur_Date.strftime("%d-%m-%Y")
Cur_Date_SQL = Cur_Date.strftime("%Y-%m-%d")
Cur_Date_DD =  Cur_Date.strftime("%d")
Cur_Date_MM =  Cur_Date.strftime("%m")
Cur_Date_YR =  Cur_Date.strftime("%Y")
Cur_Date_MY = Cur_Date.strftime("%m-%Y")
Cur_Date_YM = Cur_Date.strftime("%Y-%m")
Cur_Date_MMW =  Cur_Date.strftime("%B")
sqlformat = 'yyyy-MM-dd'
Cur_Date_NFR = Cur_Date.strftime("%d%m%H%M")

def Nomrmal_Date(inp):
    return inp.strftime('%d-%m-%Y')

# def Time_Difference_Behind(date2_str,date1_str):
#     time_format = "%H:%M"
#
#     date1 = datetime.strptime(date1_str, time_format)
#     date2 = datetime.strptime(date2_str, time_format) + timedelta(days=1)  # Add one day to the second date
#
#     time_difference = date2 - date1
#     return time_difference.total_seconds() / 3600

#QT Functions
#___Fetch_Table_Values___
@Exception_Handle
def Fetch_Table_Values(inp):
    values = []
    for row in range(inp.rowCount()):
        row_data = []
        for column in range(inp.columnCount()):
            item = inp.item(row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                tempitem = inp.cellWidget(row, column)
                if str(tempitem)[17:26] == "QCheckBox":
                    row_data.append(tempitem.isChecked())
                elif str(tempitem)[17:25] == "QSpinBox":
                    row_data.append(tempitem.value())
                elif str(tempitem)[17:26] == "QDateEdit":
                    row_data.append(tempitem.date().toString("dd-MM-yyyy"))
                elif str(tempitem)[17:26] == "QComboBox":
                    row_data.append(tempitem.currentText())
                else:
                    row_data.append("")
        values.append(row_data)
    return values

@Exception_Handle
def Fetch_ListBox_Values(output):
    list_values = []
    for index in range(output.count()):
        item = output.item(index)
        list_values.append(item.text())
    return list_values

@Exception_Handle
def Dynamic_Filter_ComboBox(combo_box):
    combo_box.setFocusPolicy(Qt.StrongFocus)
    combo_box.setEditable(True)
    pFilterModel = QSortFilterProxyModel(combo_box)
    pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
    pFilterModel.setSourceModel(combo_box.model())
    completer = QCompleter(pFilterModel, combo_box)
    completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
    combo_box.setCompleter(completer)

    def on_completer_activated(text):
        if text:
            index = combo_box.findText(text)
            combo_box.setCurrentIndex(index)
            combo_box.activated[str].emit(combo_box.itemText(index))
    combo_box.lineEdit().textEdited.connect(pFilterModel.setFilterFixedString)
    completer.activated.connect(on_completer_activated)

@Exception_Handle
def Push_Table_Values(element, data, edit):
    element.setSortingEnabled(False)
    element.clearContents()
    element.setRowCount(0)
    try:
        element.setRowCount(len(data))
        if len(data[0])>0:
            element.setColumnCount(len(data[0]))
    except:return
    for i in range(len(data)):
        for j in range(len(data[i])):
            if str(type(data[i][j]))[:23] == "<class 'PyQt5.QtWidgets":
                element.setCellWidget (i, j,data[i][j])
            else:
                temp = T_itm(str(data[i][j]))
                if isinstance(edit,list):
                    if j not in edit:
                        temp.setFlags(temp.flags() & ~Qt.ItemIsEditable)
                if edit == False:
                    temp.setFlags(temp.flags() & ~Qt.ItemIsEditable)
                element.setItem(i,j,temp)
    element.setSortingEnabled(True)

@Exception_Handle
def Adjust_Table_Width(element,col_width):
    fixed_font = QFont("Courier New", 10)
    for i, width in enumerate(col_width):
        element.setColumnWidth(i, fixed_font.pointSize() * width)

@Exception_Handle
def Filter_Table_Data(element,src_txt,data,col):
    if element.horizontalHeader().sortIndicatorSection() < len(data[0]):
        col=element.horizontalHeader().sortIndicatorSection()
    temp=[]
    for step in data:
        if str(src_txt).lower()in str(step[col]).lower():
            temp.append(step)
    element.setSortingEnabled(False)
    Push_Table_Values(element,temp,False)

# @Exception_Handle
# def Qtdate_strt(inp):
#     Date_temp = inp.date().toString(Qt.ISODate)
#     Date_splt = Date_temp.split("-")
#     Date_Join = Date_splt[2],Date_splt[1],Date_splt[0]
#     Date_Dispy = "-".join(Date_Join)
#     # Inv_Mtr.OQL_PreviewPODate.setText(Date_Dispy)
#     return Date_Dispy
#
# @Exception_Handle
# def Nf_Date(inp):
#     return inp.strftime('%d-%m-%Y')

@Exception_Handle
def Format_Table_Column(TBL,col,color):
    # Change the color of the entire column
    for step in col:
        for row in range(TBL.rowCount()-1):
            item = TBL.item(row, step)
            item.setBackground(color)

# @Exception_Handle
# def Fetch_Table_Values_SPL(inp):#___Fetch_Table_Values___
#     values = []
#     for row in range(inp.rowCount()):
#         row_data = []
#         for column in range(inp.columnCount()):
#             item = inp.item(row, column)
#             if item is not None:
#                 row_data.append(item.text())
#             else:
#                 row_data.append("")
#         values.append(row_data)
#     return values

@Exception_Handle
def Export_to_excel(Table,file_name):
    headings_list = []
    for col in range(Table.columnCount()):
        item = Table.horizontalHeaderItem(col)
        headings_list.append(item.text())
    export_data = Fetch_Table_Values(Table)
    df = pd.DataFrame(export_data, columns=headings_list)
    df.to_csv(fr'{ldir}\Export\{file_name}.csv')
    subprocess.run(['start', 'excel', fr'{ldir}\Export\{file_name}.csv'], shell=True, check=True)

@Exception_Handle
def Export_to_excel_Mail(Table,file_name):
    headings_list = []
    for col in range(Table.columnCount()):
        item = Table.horizontalHeaderItem(col)
        headings_list.append(item.text())
    export_data = Fetch_Table_Values(Table)
    df = pd.DataFrame(export_data, columns=headings_list)
    df.to_csv(fr'{ldir}\Export\{file_name}.csv')

# @Exception_Handle
# def Fetch_Table_Values_SPL_Col(inp,Col):#___Fetch_Table_Values___
#     values = []
#     for row in range(inp.rowCount()):
#         item = inp.item(row, Col)
#         if item is not None:
#             values.append(item.text())
#         else:
#             values.append("")
#     return values

@Exception_Handle
def Update_Property(inp,mode,name,stat):
    data = inp.findChildren(QWidget)
    for step in data:
        if mode == "Readonly":
            if name in step.objectName():
                step.setReadOnly(stat)
        elif mode == "Enable":
            if name in step.objectName():
                step.setEnabled(stat)
        elif mode=="Visible":
            if name in step.objectName():
                step.setVisible(stat)
        elif mode=="Clear":
            if name in step.objectName():
                step.clear()

class NoDoubleClickDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, role=Qt.DisplayRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, role=Qt.EditRole)

def ConvertCurrencyToWords(amount):
    # Split the amount into rupees and paise
    rupees, paise = str(amount).split('.')
    # Convert rupees to words
    rupees_words = num2words(int(rupees))
    # Convert paise to words
    if paise == '00' or paise =='0':
        paise_words = 'zero'
    else:
        paise_words = num2words(int(paise))
    # Format the result
    if paise == '00' or paise =='0':
        result = f"{rupees_words} rupees only"
    else:
        result = f"{rupees_words} rupees and {paise_words} paise only"

    return result