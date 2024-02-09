#___Import Statements__
from Env import *

#___QT_Window_Creation___
Twink_UI = uic.loadUi(fr'{ldir}\MODULES\BASE_WIN\UI-BaseWin_AWM.ui')
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

# ___QT Window Initialization___
Twink_UI.show()
sys.exit(app.exec_())
