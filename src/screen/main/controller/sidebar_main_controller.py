import sys

import cvzone
from PyQt5.QtChart import QChartView, QLineSeries, QPieSeries, QChart, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QStyle, QLabel, QTableWidgetItem, \
    QHeaderView, QVBoxLayout, QWidget, QScrollArea

from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon, QBrush, QImage, QPainter
from cv2 import cv2
from faker import Faker

from src.components.Charts.charts_controller import charts_Controller
from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.constants.assets.color_constants import Color_Constants
from src.constants.carTypes import CarTypes
from src.screen.main.generate.sidebar_main_generate import Ui_MainWindow
from src.state_managment.checkBox_controller import CheckBoxController
from src.state_managment.chosen_variable import chosenVariable
from src.state_managment.count_vehicle import count_vehicle_statistics
from src.state_managment.overspeed_profile_controller import overspeed_Profile_Controller
from src.state_managment.speed_controller import Speed_Calculator
from src.state_managment.vehicle_statistic import vehicle_Statistic
from src.thread.video_player import videoPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.home_btn_2.setChecked(True)



        self.ui.home_btn_1.setStyleSheet("QPushButton:checked { color: blue; }")

        self.videoPlayer = None
        self.ui.select_video_pushButton.clicked.connect(self.selectVideo)

        self.ui.checkBox_vehicledetection.clicked.connect(self.checkBox_vehicle_detection)
        self.ui.checkBox_platedetection.clicked.connect(self.checkBox_plate_detection)
        self.ui.checkBox_speeddetection.clicked.connect(self.checkBox_speed_detection)
        self.initializeComboBoxes()
        self.ui.pushButton.clicked.connect(self.update_button_profile)


        self.ui.comboBox_model.currentTextChanged.connect(self.comboBox_model_func)
        self.model = AssetsConstants.get_model_path(assetsEnum.yolov8l.value)

        self.ui.comboBox_mask.currentTextChanged.connect(self.comboBox_mask_func)
        self.ui.comboBox_count_line.currentTextChanged.connect(self.comboBox_line_func)

        self.ui.tableWidget_plate.cellClicked.connect(self.on_table_cell_clicked)


        self.ui.pushButton_close.clicked.connect(self.pushButton_close_func)
        self.ui.comboBox_model.setCurrentText("Yolov8l")
        self.tableWidgetProfilePage()

        self.ui.lineEdit_speed_punshment.textChanged.connect(self.on_line_edit_changed)


    def on_line_edit_changed(self,text):
        chosenVariable.set_Speed_Limit(int(text))



    def initializeComboBoxes(self):

        self.ui.comboBox_mask.addItems(chosenVariable.get_List_MASK_NAME())
        self.ui.comboBox_count_line.addItems(chosenVariable.get_List_LINE_NAME())



    def comboBox_mask_func(self,text):
        chosenVariable.controlMask(text=text)

    def comboBox_line_func(self,text):
        chosenVariable.controlLine(text=text)


    def on_table_cell_clicked(self,row, column):
        item = self.tableWidget.item(row, column)

        isim, soyisim, yas, cinsiyet, tc = self.create_fake_data()
        profile = None
        if cinsiyet == "man":
            profile = "assets/image/man_profile.png"
        else:
            profile = "assets/image/women_profile.png"

        self.initialize_Profile_Page(isim, soyisim, yas, cinsiyet, tc, profile,None)
        cell_text = item.text()

        self.ui.label_plate_write.setText(cell_text)

        for dictionary in overspeed_Profile_Controller.plate:

            print(dictionary["plate_text"])
            print(cell_text)
            if dictionary["plate_text"][0][1] == cell_text:

                frame = dictionary["frame"]
                x1,y1,x2,y2 = dictionary["dimension1"]
                xmin,ymin,xmax,ymax = dictionary["dimension2"]

                cap = cv2.VideoCapture('assets/video/traffic.mp4')
                frame_number = frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                success, img = cap.read()

                if success:

                    #crop_img = img[(y1+ymin):(y1+ymax), (x1+xmin):(x1+xmax)]
                    crop_img = img[y1:y2, x1:x2]
                    new_crop_img = crop_img[ymin:ymax, xmin:xmax]
                    resized_img = cv2.resize(new_crop_img, ((xmax-xmin)*4,(ymax-ymin)*4))
                    imgPlate = resized_img
                    qImg = QPixmap(QImage(imgPlate.data, imgPlate.shape[1], imgPlate.shape[0], imgPlate.strides[0], QImage.Format_RGB888))
                    self.ui.label_plate_detection_image.setPixmap(qImg)
                    self.ui.label_plate_detection_image.setScaledContents(True)
                    self.ui.label_plate_detection_image.setAlignment(Qt.AlignCenter)

                    #resized_img = cv2.resize(crop_img, (300, 80))
                    imgVehicle = img
                    cvzone.cornerRect(img, (x1, y1, x2-x1,y2-y1), l=9, rt=5, colorR=Color_Constants.get_Purple_Color())
                    qImgVehicle = QPixmap(QImage(imgVehicle.data, imgVehicle.shape[1], imgVehicle.shape[0], imgVehicle.strides[0],
                                          QImage.Format_RGB888))
                    self.ui.label_camera_vehicle_image.setPixmap(qImgVehicle)
                    self.ui.label_camera_vehicle_image.setScaledContents(True)
                    self.ui.label_camera_vehicle_image.setAlignment(Qt.AlignCenter)


                else:
                    print(f"Cannot read frame {frame_number}")

                cap.release()
                



    def update_button_profile(self):
        try:
            i = overspeed_Profile_Controller.plate
        except:
            print("return None")
            return None

        rowCount = self.tableWidget.rowCount()
        for row in range(rowCount):
            self.tableWidget.removeRow(0)



        for dictionary in overspeed_Profile_Controller.plate:
            maxSpeed=0

            row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_count)
            plate_text = str(dictionary['plate_text'][0][1])
            item = QTableWidgetItem(plate_text)
            self.tableWidget.setItem(row_count, 0, item)

            for speC in Speed_Calculator.vehicle_max_speed:
                if speC["id"]==dictionary["id"]:
                    maxSpeed=speC["max_speed"]

            if maxSpeed > chosenVariable.get_Speed_Limit():
                brush = Color_Constants.get_Red_QBrush_Color()
            else:
                brush = Color_Constants.get_Green_QBrush_Color()
            item.setBackground(brush)




        isim, soyisim, yas, cinsiyet, tc = self.create_fake_data()
        profile = None
        if cinsiyet == "man":
            profile = "assets/image/man_profile.png"
        else:
            profile = "assets/image/women_profile.png"

        self.initialize_Profile_Page(isim, soyisim, yas, cinsiyet, tc, profile,None)


    def tableWidgetProfilePage(self):
        self.tableWidget = self.ui.tableWidget_plate
        # Sütun ismi belirleme
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['Plate License'])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        # Arka plan rengi ayarlama
        self.tableWidget.setStyleSheet("background-color: transparent;")

    def initialize_Profile_Page(self,name,surname,age,gender,tc,profile,img):

        self.ui.label_name.setText(name)

        self.ui.label_surname.setText(surname)

        self.ui.label_age.setText(age)

        self.ui.label_gender.setText(gender)

        self.ui.label_tc.setText(tc)

        pixmap1 = QPixmap(profile)
        self.ui.profil_photo.setPixmap(pixmap1)
        self.ui.profil_photo.setScaledContents(True)
        self.ui.profil_photo.setAlignment(Qt.AlignCenter)

        if img is not None:
            pixmap2 = QPixmap(img)
            self.ui.label_camera_vehicle_image.setPixmap(pixmap2)
            self.ui.label_camera_vehicle_image.setScaledContents(True)
            self.ui.label_camera_vehicle_image.setAlignment(Qt.AlignCenter)



    def pushButton_close_func(self):
        self.CancelFeed()

    def comboBox_model_func(self,model):

        if model == "Yolov8n":
            self.model = "assets/model/yolov8n.pt"
        elif model == "Yolov8s":
            self.model = "assets/model/yolov8s.pt"
        elif model == "Yolov8l":
            self.model = "assets/model/yolov8l.pt"
        elif model == "Yolov8sCustom":
            self.model = "assets/model/best.pt"
        else:
            self.model = "assets/model/yolov8l.pt"


    def checkBox_vehicle_detection(self,checked):
        if checked:
            CheckBoxController.set_value_vehicle_detection(True)
        else:
            CheckBoxController.set_value_vehicle_detection(False)

    def checkBox_plate_detection(self,checked):
        if checked:
            CheckBoxController.set_value_plate_detection(True)
        else:
            CheckBoxController.set_value_plate_detection(False)

    def checkBox_speed_detection(self,checked):
        if checked:
            CheckBoxController.set_value_speed_detection(True)
        else:
            CheckBoxController.set_value_speed_detection(False)

    def selectVideo(self):

        fname = QFileDialog.getOpenFileName(self, 'Video Seç', '.', 'Video Dosyaları (*.mp4 *.avi)')
        print("video = "+str(fname))
        if fname[0].__contains__(".mp4"):

            self.videoPlayer = videoPlayer(fname, self.model)
            self.videoPlayer.start()
            self.videoPlayer.ImageUpdate.connect(self.ImageUpdateSlot)





    def ImageUpdateSlot(self,Image):
        self.ui.label_page1_video.setPixmap(QPixmap.fromImage(Image))


    def CancelFeed(self):
        if self.videoPlayer.isRunning():
            self.videoPlayer.stop()
        self.ui.label_page1_video.clear()




    def on_search_btn_clicked(self):
            self.ui.stackedWidget.setCurrentIndex(5)
            search_text = self.ui.search_input.text().strip()
            if search_text:
             self.ui.label_7.setText(search_text)

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed

    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                   + self.ui.full_menu_widget.findChildren(QPushButton)
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_statistic_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)



    def on_statistic_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)



        frame = self.ui.frame_static_page
        if frame.layout() is not None:
            for i in reversed(range(frame.layout().count())):
                widgetToRemove = frame.layout().itemAt(i).widget()
                frame.layout().removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)

        car =0
        motor=0
        bus =0
        truck =0

        for dictionary in count_vehicle_statistics.vehicle_count_type_info:
            if dictionary["cartypes"]==CarTypes.CAR.value:
                car = dictionary["count"]
            if dictionary["cartypes"]==CarTypes.MOTORBIKE.value:
                motor = dictionary["count"]
            if dictionary["cartypes"]==CarTypes.BUS.value:
                bus = dictionary["count"]
            if dictionary["cartypes"]==CarTypes.TRUCK.value:
                truck = dictionary["count"]


        series1 = QPieSeries()
        series1.append("Motorbike", motor)
        series1.append("Car", car)
        series1.append("Bus", bus)
        series1.append("Truck", truck)



        set0 = QBarSet('Low')
        set1 = QBarSet('Average')
        set2 = QBarSet('High')



        lowc,averagec,highc = vehicle_Statistic.gets_low_average_high_speed(CarTypes=CarTypes.CAR)
        lowm, averagem, highm = vehicle_Statistic.gets_low_average_high_speed(CarTypes=CarTypes.MOTORBIKE)
        lowb, averageb, highb = vehicle_Statistic.gets_low_average_high_speed(CarTypes=CarTypes.BUS)
        lowt, averaget, hight = vehicle_Statistic.gets_low_average_high_speed(CarTypes=CarTypes.TRUCK)


        set0.append([lowc, lowm, lowb,lowt])
        set1.append([averagec,averagem, averageb,averaget])
        set2.append([highc,highm,highb,hight])

        series2 = QBarSeries()
        series2.append(set0)
        series2.append(set1)
        series2.append(set2)


        # Create two QChartView widgets and set their series
        chartView1 = QChartView()
        chartView1c = chartView1.chart()
        chart1 = QChart()
        chartView1c.addSeries(series1)
        chartView1.setRenderHint(QPainter.Antialiasing)
        chartView1c.setTitle("Vehicle Counts")
        chartView1c.setAnimationOptions(QChart.SeriesAnimations)

        chartView2 = QChartView()
        chartView2c = chartView2.chart()

        chartView2c.addSeries(series2)

        chartView2.setRenderHint(QPainter.Antialiasing)

        chartView2c.setTitle("Speed Average")
        chartView2c.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['Car', 'MotorBike', 'Truck',"Bus"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chartView2c.createDefaultAxes()
        chartView2c.setAxisX(axis, series2)

        chartView1.setFixedSize(self.ui.frame_static_page.width()/1.1, self.ui.frame_static_page.height() / 1.1)
        chartView2.setFixedSize(self.ui.frame_static_page.width()/1.1, self.ui.frame_static_page.height() / 1.1)

        # Create a QVBoxLayout and add the QChartViews to it
        layout = QVBoxLayout()
        layout.addWidget(chartView1)
        layout.addWidget(chartView2)

        # Create a QWidget to hold the QVBoxLayout
        widget = QWidget()
        widget.setLayout(layout)

        # Create a QScrollArea and set its widget to the QWidget
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)

        # Set the main window's layout to the QScrollArea
        self.ui.frame_static_page.setLayout(QVBoxLayout())
        self.ui.frame_static_page.layout().addWidget(scrollArea)

    def on_settings_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)



    def on_settings_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)





    def create_fake_data(self):
        faker = Faker()

        isim = faker.first_name()
        soyisim = faker.last_name()
        yas = str(faker.random_int(min=18, max=65))
        cinsiyet = faker.random_element(elements=('man', 'women'))
        tc = faker.ssn()

        return isim,soyisim,yas,cinsiyet,tc


