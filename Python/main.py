from MySQLdb import Time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import time
import os
from __default__ import *
from user_create import Ui_user_create
from user_delete import Ui_user_delete
from user_face import Ui_user_face
from sign_in import Ui_user_sign_in
from DB.filelist import *
from DB.user_list import user_list
import DB.appfilesave as appsave
from datetime import timedelta, datetime


weeklist = daylist = []
first = Attendance_date ######
curr = datetime.now()
user_list(host, port, user, password)

for i in range(0, 5):
    second = first + timedelta(weeks=i)
    weeklist.append(second)
    daylist.append(second.date())
try:
    currlimit = weeklist[daylist.index(curr.date())]
except:
    currlimit = None
        
class Photo_data_recv(QtCore.QThread): 
    '''안드로이드에서 전송한 사진을 다운로드 후 유사도 측정 후 매칭 여부에 따라 피클파일 추가'''
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent = None):
        super(Photo_data_recv, self).__init__(parent)

    def run(self):
        file_list = new_list = delete_list = []
        while True:
            filelist()
            for (root, directories, files) in os.walk(Photo_Path):
                for file in files:
                    if ".jpg" in file:
                        file_list.append(str(file[0:8]))
            if file_list == []:
                None
            else:
                for v in file_list:
                    if v not in new_list:            
                        new_list.append(v)
                print("신규 학번 : "+ str(new_list))        
                for z in new_list:
                    appsave.app_verify(z)
                    
                user_list()
                new_list.clear()
                file_list.clear()
            
            delete_list = delete_userlist()     ####
            print(delete_list)
            if delete_list == []:
                None
            else:
                for i in delete_list:
                    delete_pickle(i)
                user_list()
            time.sleep(10)
class Ui_MainWindow(object):
    def Late(self):
        global daylist, weeklist
        daylist = weeklist = []
        for i in range(0, 5):
            abc = datetime.now()
            cba = datetime(first.year, first.month, first.day, (abc.hour-1))
            second = cba + timedelta(weeks=i)
            weeklist.append(second)
            daylist.append(second.date())
        try:
            currlimit = weeklist[daylist.index(curr.date())]
            self.Present_Time.setText("수업 시간 : "+ str(currlimit))
        except:
            self.Present_Time.setText("수업 시간 : None")
            
    def Absent(self):
        global daylist, weeklist
        daylist = weeklist = []
        for i in range(0,5):
            abc = datetime.now()
            cba = datetime(first.year, first.month, first.day, (abc.hour-4))
            second = cba + timedelta(weeks=i)
            weeklist.append(second)
            daylist.append(second.date())
        try:
            currlimit = weeklist[daylist.index(curr.date())]
            self.Present_Time.setText("수업 시간 : "+ str(currlimit))
        except:
            self.Present_Time.setText("수업 시간 : None")
            
    def Attend(self):
        global daylist, weeklist
        daylist = weeklist = []
        for i in range(0, 5):
            abc = datetime.now()
            cba = datetime(first.year, first.month, first.day, (abc.hour+1))
            second = cba + timedelta(weeks=i)
            weeklist.append(second)
            daylist.append(second.date())
        try:
            currlimit = weeklist[daylist.index(curr.date())]
            self.Present_Time.setText("수업 시간 : "+ str(currlimit))
        except:
            self.Present_Time.setText("수업 시간 : None")
    def sign_in_window(self):   
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_sign_in()
        self.ui.setupUi(self.window)
        self.window.show()#창전환
    def sign_up_window(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_create()
        self.ui.setupUi(self.window)
        self.window.show()#창전환
    def delete_user_window(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_delete()
        self.ui.setupUi(self.window)
        self.window.show()#창전환
    def face_matching_window(self):
        global daylist, weeklist
        lines = [] # 학번 이름이 저장된 리스트
        with open(r"Python\DB\User_List.txt") as f: 
            lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        print("이름:",lines)
        self.window = QtWidgets.QDialog()
        self.ui = Ui_user_face(daylist, weeklist)
        self.ui.setupUi(self.window)
        self.window.show()  # 창전환
    def setupUi(self, MainWindow):          
        MainWindow.setObjectName("메인")
        MainWindow.resize(1920, 1080)
        self.File_path = None
        self.Photo_data_R = Photo_data_recv()
        self.Photo_data_R.start()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Late_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.Late_Btn.setGeometry(QtCore.QRect(1670, 100, 211, 45))
        self.Late_Btn.setObjectName("Late_Btn")
        self.Absent_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.Absent_Btn.setGeometry(QtCore.QRect(1670, 150, 211, 45))
        self.Absent_Btn.setObjectName("Absent_Btn")
        self.Attend_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.Attend_Btn.setGeometry(QtCore.QRect(1670, 50, 211, 45))
        self.Attend_Btn.setObjectName("Attend_Btn")
        self.User_del = QtWidgets.QPushButton(self.centralwidget)
        self.User_del.setGeometry(QtCore.QRect(1430, 890, 211, 91))
        self.User_del.setObjectName("User_del")
        self.Logo = QtWidgets.QLabel(self.centralwidget)
        self.Logo.setGeometry(QtCore.QRect(10, 920, 218, 60))
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.User_create = QtWidgets.QPushButton(self.centralwidget)
        self.User_create.setGeometry(QtCore.QRect(1190, 890, 211, 91))
        self.User_create.setObjectName("User_create")
        self.User_face = QtWidgets.QPushButton(self.centralwidget)
        self.User_face.setGeometry(QtCore.QRect(950, 890, 211, 91))
        self.User_face.setObjectName("User_face")
        self.User_login = QtWidgets.QPushButton(self.centralwidget)
        self.User_login.setGeometry(QtCore.QRect(1670, 890, 211, 91))
        self.User_login.setObjectName("User_login")
        self.Present_Time = QtWidgets.QLabel(self.centralwidget)
        self.Present_Time.setGeometry(QtCore.QRect(1670, 10, 211, 30))
        self.Present_Time.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "메인"))
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint) #시연할때만
        self.User_del.setText(_translate("MainWindow", "사용자 삭제"))  
        self.User_create.setText(_translate("MainWindow", "사용자 등록"))
        self.User_face.setText(_translate("MainWindow", "출석하기"))
        self.User_login.setText(_translate("MainWindow", "관리자 모드"))
        self.Late_Btn.setText(_translate("MainWindow", "지각"))
        self.Absent_Btn.setText(_translate("MainWindow", "결석"))
        self.Attend_Btn.setText(_translate("MainWindow", "출석"))
        self.Present_Time.setText(_translate("MainWindow", "수업 시간 : "+str(currlimit)))
        self.User_create.clicked.connect(lambda: self.sign_up_window())
        self.User_del.clicked.connect(lambda : self.delete_user_window())
        self.User_face.clicked.connect(lambda : self.face_matching_window())
        self.User_login.clicked.connect(lambda : self.sign_in_window())
        self.Attend_Btn.clicked.connect(lambda : self.Attend())
        self.Late_Btn.clicked.connect(lambda : self.Late())
        self.Absent_Btn.clicked.connect(lambda : self.Absent())
        Logo =QPixmap('./Logo/Logo.png')
        self.Logo.setPixmap(Logo)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    File = open(r".\Python\Ui\Devsion.qss", 'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())