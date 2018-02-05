import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import csv
import dns.resolver
from time import time
from datetime import datetime

gfilepath = ""
csv_num = []
csv_date = []
csv_time = []
csv_unix = []
csv_domain = []
csv_ip = []
csv_dns = []


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("CSV ver 1.0")
        self.resize(1580, 900)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(20,90,500, 665)
        self.tableWidget.setColumnCount(2)
        
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(100)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 350)      
        self.setTableWidgetData()

        self.csvTable = QTableWidget(self)
        self.csvTable.setGeometry(550, 90, 1000, 665)
        self.csvTable.setColumnCount(6)
        self.csvTable.setColumnWidth(0, 50)
        self.csvTable.setColumnWidth(1, 150)
        self.csvTable.setColumnWidth(2, 150)
        self.csvTable.setColumnWidth(3, 248)
        self.csvTable.setColumnWidth(4, 200)
        self.csvTable.setColumnWidth(5, 200)
        self.setcsvTableData()

        self.Title_SetTime = QLabel(self)
        self.Title_SetTime.setText('Set Time Range')
        self.Title_SetTime.setGeometry(550, 15, 100, 20)

        self.begin_Calendar = QDateEdit(self)
        self.begin_Calendar.setCalendarPopup(True)
        self.begin_Calendar.setGeometry(550, 40, 120, 30)
        self.begin_Calendar.setDisplayFormat('yyyy/MM/dd')

        self.begin_Clock = QTimeEdit(self)
        self.begin_Clock.setGeometry(680, 40, 100, 30)
        self.begin_Clock.setTime(QTime(0, 0, 0))

        self.wave = QLabel(self)
        self.wave.setText('~')
        self.wave.setGeometry(790, 40, 30, 30)

        self.end_Calendar = QDateEdit(self)
        self.end_Calendar.setCalendarPopup(True)
        self.end_Calendar.setGeometry(810, 40, 120, 30)
        self.end_Calendar.setDisplayFormat('yyyy/MM/dd')

        self.end_Clock = QTimeEdit(self)
        self.end_Clock.setGeometry(940, 40, 100, 30)
        self.end_Clock.setTime(QTime(24, 60, 0))
       
        self.Title_IPbox = QLabel(self)
        self.Title_IPbox.setGeometry(1050, 15, 200, 20)
        self.Title_IPbox.setText('Set IP')

        self.IPbox = QComboBox(self)
        self.IPbox.setGeometry(1050, 40, 200, 30)
        self.IPbox.addItem('All')

        self.Button_SetTime = QPushButton(self)
        self.Button_SetTime.setText('Set')
        self.Button_SetTime.setGeometry(1250, 40, 30, 30)

        self.Button_Open = QPushButton(self)
        self.Button_Open.setObjectName("Button_Open")
        self.Button_Open.setText("File Open")
        self.Button_Exit = QPushButton(self)
        self.Button_Exit.setObjectName("Button_Exiting")
        self.Button_Exit.setText("Exit")

        self.Button_Open.setGeometry(20, 20, 100, 50)
        self.Button_Exit.setGeometry(1450, 820, 100, 50)
        self.Button_Open.clicked.connect(self.pushButtonClicked)
        self.Button_Exit.clicked.connect(self.closeWindow)
        self.tableWidget.cellClicked.connect(self.viewCSVInfo)
        self.Button_SetTime.clicked.connect(self.SetTimeRange)

        self.SearchIP = QLabel(self)
        self.SearchIP.setText('SEARCH DNS FROM DOMAIN')

        Titlefont = QFont()
        Titlefont.setPointSize(15)
        Titlefont.setBold(True)
        self.SearchIP.setFont(Titlefont)
        self.SearchIP.setGeometry(20, 730, 300, 100)

        inputfont = QFont()
        inputfont.setPointSize(40)

        self.InputboxDomain = QLineEdit(self)
        self.InputboxDomain.setFont(inputfont)
        self.InputboxDomain.setGeometry(40, 800, 500, 80)

        self.Button_Search = QPushButton(self)
        self.Button_Search.setText('>')
        self.Button_Search.setGeometry(600, 815, 50, 50)
        self.Button_Search.clicked.connect(self.SearchIPfromDomain)

        self.ResultBoxIP = QLineEdit(self)
        self.ResultBoxIP.setFont(inputfont)
        self.ResultBoxIP.setGeometry(700, 800, 500, 80)
        
    def SearchIPfromDomain(self):
        domain = self.InputboxDomain.text()
        res = dns.resolver.Resolver()
        res.nameservers = ['8.8.8.8']
        answers = res.query(domain)

        for rdata in answers:
            self.ResultBoxIP.setText(rdata.address)
            break

    def setTableWidgetData(self):
        column_headers = ['Name', 'Path']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
    def setcsvTableData(self):
        column_headers = ['Num', 'Date', 'Time', 'Domain', 'IP', 'DNS']
        self.csvTable.setHorizontalHeaderLabels(column_headers)
    def pushButtonClicked(self):
        files = QFileDialog.getOpenFileNames(self,"Select one or more files to open","./","Images (*.csv)");
        for fname in files[0]:
            filename = fname.split('/')[-1]
            filepath = fname
            num_row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(num_row)
            self.tableWidget.setItem(num_row, 0, QTableWidgetItem(filename))
            self.tableWidget.setItem(num_row, 1, QTableWidgetItem(filepath))
            
    def SetTimeRange(self):
        begin_date = self.begin_Calendar.date()
        begin_time = self.begin_Clock.time()

        end_date = self.end_Calendar.date()
        end_time = self.end_Clock.time()

        be_year, be_month, be_day = begin_date.getDate()
        time_tuple = begin_time.toString().split(':')
        be_hour = time_tuple[0]
        be_minute = time_tuple[1]
        be_sec = time_tuple[2]

        end_year, end_month, end_day = end_date.getDate()
        time_tuple = end_time.toString().split(':')
        end_hour = time_tuple[0]
        end_minute = time_tuple[1]
        end_sec = time_tuple[2]

        be_date = str(be_year).zfill(4)+'-'+str(be_month).zfill(2)+'-'+str(be_day).zfill(2)
        be_time = str(be_hour).zfill(2)+':'+str(be_minute).zfill(2)+':'+str(be_sec).zfill(2)

        end_date = str(end_year).zfill(4)+'-'+str(end_month).zfill(2)+'-'+str(end_day).zfill(2)
        end_time = str(end_hour).zfill(2)+':'+str(end_minute).zfill(2)+':'+str(end_sec).zfill(2)

        temp = str(be_date)+" "+str(be_time)
        temptime = datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        be_unixtime = temptime.timestamp()

        temp = str(end_date)+" "+str(end_time)
        temptime = datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        end_unixtime = temptime.timestamp()

        index_ip = self.IPbox.currentText()

        for i in range(0, len(csv_unix)):
            if int(csv_unix[i]) >= int(be_unixtime) and int(csv_unix[i]) <= int(end_unixtime):
                if index_ip == "All":
                    self.csvTable.setRowHidden(i, False)
                elif index_ip == csv_ip[i]:
                    self.csvTable.setRowHidden(i, False)
                elif index_ip != csv_ip[i]:
                    self.csvTable.setRowHidden(i, True)
            else:
                self.csvTable.setRowHidden(i, True)
    def ConvertDate(self, timedata):
        date = timedata.split(' ')[0]
        return date

    def ConvertTime(self, timedata):
        raw_time = timedata.split(' ')[1].split(':')
        hour = raw_time[0]
        minute = raw_time[1]
        sec = raw_time[2].split('.')[0]

        modify_time = str(hour).zfill(2)+':'+str(minute).zfill(2)+':'+str(sec).zfill(2)
        return modify_time

    def SetBeginDateTime(self, datedata, timedata):
        date_tuple = datedata.split('-')
        year = date_tuple[0]
        mon = date_tuple[1]
        day = date_tuple[2]
        self.begin_Calendar.setDate(QDate(int(year), int(mon), int(day)))

        time_tuple = timedata.split(':')
        hour = time_tuple[0]
        minute = time_tuple[1]
        sec = time_tuple[2].split('.')[0]
        self.begin_Clock.setTime(QTime(int(hour), int(minute), int(sec)))


    def SetEndDateTime(self, datedata, timedata):
        date_tuple = datedata.split('-')
        year = date_tuple[0]
        mon = date_tuple[1]
        day = date_tuple[2]
        self.end_Calendar.setDate(QDate(int(year), int(mon), int(day)))

        time_tuple = timedata.split(':')
        hour = time_tuple[0]
        minute = time_tuple[1]
        sec = time_tuple[2].split('.')[0]
        self.end_Clock.setTime(QTime(int(hour), int(minute), int(sec)))

    def initglobal(self):
        global gfilepath
        global csv_num
        global csv_date
        global csv_time
        global csv_domain
        global csv_ip
        global csv_dns
        global csv_unix

        csv_num = []
        csv_date = []
        csv_time = []
        csv_domain = []
        csv_ip = []
        csv_dns = []
        csv_unix = []

    def viewCSVInfo(self, row, col):
        global gfilepath
        global csv_num
        global csv_date
        global csv_time
        global csv_unix
        global csv_domain
        global csv_ip
        global csv_dns
        self.initglobal()


        indexnum = row
        filepath = self.tableWidget.item(indexnum, 1)
        gfilepath =  filepath.text()
        f = open(filepath.text(), 'r', encoding='utf-8')
        fcsv = csv.reader(f)

        num_row = 0
        for line in fcsv:
            self.csvTable.insertRow(num_row)
            self.csvTable.setItem(num_row, 0, QTableWidgetItem(str(line[0])))
            csv_num.append(str(line[0]))

            date = self.ConvertDate(str(line[1]))
            self.csvTable.setItem(num_row, 1, QTableWidgetItem(date))
            csv_date.append(date)

            timedata = self.ConvertTime(str(line[1]))
            self.csvTable.setItem(num_row, 2, QTableWidgetItem(timedata))
            csv_time.append(timedata)

            unix = str(date)+" "+str(timedata)
            time1 = datetime.strptime(unix, "%Y-%m-%d %H:%M:%S")
            unixtime = time1.timestamp()
            csv_unix.append(unixtime)

            if num_row == 0:
                self.SetBeginDateTime(date, timedata)

            self.csvTable.setItem(num_row, 3, QTableWidgetItem(str(line[2])))
            csv_domain.append(str(line[2]))
            self.csvTable.setItem(num_row, 4, QTableWidgetItem(str(line[3])))
            csv_ip.append(str(line[3]))
            self.csvTable.setItem(num_row, 5, QTableWidgetItem(str(line[4])))
            csv_dns.append(str(line[4]))

            num_row = num_row+1
        self.SetEndDateTime(date, timedata)

        ip_array = list(set(csv_ip))

        for i in range(0, len(ip_array)):
            self.IPbox.addItem(str(ip_array[i]))

        f.close()

    def closeWindow(self):
        window.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()