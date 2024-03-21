#___Import Statements__
from Env import *

import time



#___QT_Window_Creation___
Twink_UI = uic.loadUi(fr'{ldir}\MODULES\BASE_WIN\UI-BaseWin_AWM.ui')
Twink_UI.setWindowTitle('Twink_06MA : Sunil Industries Limited')

Twink_UI.OQL_ProgressBar.setValue(100)
Twink_UI.OQL_CurrentDate.setText(Cur_Date_NF)

# ___Stack Window (Module) Initialization___
Twink_UI.BseM_Stack.removeWidget(Twink_UI.NEX_Stack1)
Twink_UI.BseM_Stack.removeWidget(Twink_UI.NEX_Stack2)

# #_________Home_________
Twink_UI.BseM_Stack.addWidget(Home)
original_image_data = read_image(fr'{ldir}\EXTERNAL\SIL.PNG')
pixmap = QPixmap()
pixmap.loadFromData(original_image_data)
Home.label.setPixmap(pixmap)
Twink_UI.actionHome.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(0))
# #_________Register Module _________
Twink_UI.BseM_Stack.addWidget(Rgtr)
Twink_UI.actionRegister.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(1))
from MODULES.REGISTER import Register
Register.Register_FN(Rgtr)
# #_________Attendance Module _________

Twink_UI.BseM_Stack.addWidget(AttnPush)
Twink_UI.BseM_Stack.addWidget(AttnView)
Twink_UI.actionCreate.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(2))
Twink_UI.actionView.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(3))
from MODULES.ATTENDANCE import Attendance
Attendance.Attendance_Push_FN(AttnPush)
Attendance.Attendance_View_Fn(AttnView)


# #_________Punch Build Module_________
Twink_UI.BseM_Stack.addWidget(PnchBld)
Twink_UI.BseM_Stack.addWidget(PrsPnchTrck)
Twink_UI.actionPunchTrack.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(4))
Twink_UI.actionPersPunchTrack.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(5))
from MODULES.PUNCH_BUILD import Punch_Build
Punch_Build.Punch_Build_FN(PnchBld,PrsPnchTrck)

# #_________ Advance Module _________
Twink_UI.BseM_Stack.addWidget(Adv)
Twink_UI.actionAdvance.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(6))
from MODULES.ADVANCE import Advance
Advance.Advance_Amt(Adv)

# #_________ Master Module _________
Twink_UI.BseM_Stack.addWidget(Mtr)
Twink_UI.actionMater_User.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(7))
from MODULES.MASTER_LIST import Master
Master.Master_FN(Mtr)

# #_________ Wage Module _________
Twink_UI.BseM_Stack.addWidget(Wge)
Twink_UI.actionGenerateWage.triggered.connect(lambda: Twink_UI.BseM_Stack.setCurrentIndex(8))
from MODULES.WAGE import Wage_Calculation
Wage_Calculation.Wage_FN(Wge)


# BaseWin Network
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE


def ping_speed(ip_address):
    try:
        result = subprocess.run(['ping', ip_address, '-n', '1', '-w', '500'], capture_output=True, text=True,
                                startupinfo=startupinfo)

        if result.returncode == 0:
            rtt_pattern = r"Average = (\d+)ms"
            match = re.search(rtt_pattern, result.stdout)
            if match:
                speed = int(match.group(1))
                return speed
            else:
                return None
        else:
            print("Error executing ping command:", result.stderr)
            return
    except Exception as e:
        print("Error:", e)
        return None

# IP address to ping
ip_address = config[4]

# Network Icons
Twink_UI.IQL_DB_Connection.setScaledContents(True)
CloudConnect = QPixmap(f"{ldir}\MODULES\BASE_WIN\icons\Cloud_Connect.png")
CloudDisconnect = QPixmap(f"{ldir}\MODULES\BASE_WIN\icons\Cloud_Disconnect.png")
Home = QPixmap(f"{ldir}\MODULES\BASE_WIN\icons\Home_Preview.png")


def ping_loop():
    while True:
        if config[2] == "CLOUD":
            speed = ping_speed(ip_address)
            if speed is not None:
                Twink_UI.IQL_DB_Connection.setPixmap(CloudConnect)
                # Change color based on ping speed
                if speed <= 10:
                    Twink_UI.IQL_Point1.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point2.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point3.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point4.setStyleSheet("background-color: black;")
                elif 10 <= speed <= 50:
                    Twink_UI.IQL_Point1.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point2.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point3.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point4.setStyleSheet("background-color: white;")
                elif 50 <= speed <= 100:
                    Twink_UI.IQL_Point1.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point2.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point3.setStyleSheet("background-color: white;")
                    Twink_UI.IQL_Point4.setStyleSheet("background-color: white;")
                else:
                    Twink_UI.IQL_Point1.setStyleSheet("background-color: black;")
                    Twink_UI.IQL_Point2.setStyleSheet("background-color: White;")
                    Twink_UI.IQL_Point3.setStyleSheet("background-color: white;")
                    Twink_UI.IQL_Point4.setStyleSheet("background-color: white;")
            else:
                Twink_UI.IQL_DB_Connection.setPixmap(CloudDisconnect)
                Twink_UI.IQL_Point1.setStyleSheet("background-color: white;")
                Twink_UI.IQL_Point2.setStyleSheet("background-color: white;")
                Twink_UI.IQL_Point3.setStyleSheet("background-color: white;")
                Twink_UI.IQL_Point4.setStyleSheet("background-color: white;")


        else:
            Twink_UI.IQL_DB_Connection.setPixmap(Home)
        time.sleep(1)

ping_thread = threading.Thread(target=ping_loop)
ping_thread.daemon = True
ping_thread.start()


# ___QT Window Initialization___
Twink_UI.show()
sys.exit(app.exec_())
