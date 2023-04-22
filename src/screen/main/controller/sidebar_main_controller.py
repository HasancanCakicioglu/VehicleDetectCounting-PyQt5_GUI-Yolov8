import sys

import cvzone
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QStyle, QLabel, QTableWidgetItem, \
    QHeaderView

from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon, QBrush, QImage
from cv2 import cv2
from faker import Faker
from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.constants.assets.color_constants import Color_Constants
from src.screen.main.generate.sidebar_main_generate import Ui_MainWindow
from src.state_managment.checkBox_controller import CheckBoxController
from src.state_managment.overspeed_profile_controller import overspeed_Profile_Controller
from src.state_managment.speed_controller import Speed_Calculator
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

        self.ui.pushButton.clicked.connect(self.update_button_profile)

        self.ui.comboBox_model.currentTextChanged.connect(self.comboBox_model_func)
        self.model = AssetsConstants.get_model_path(assetsEnum.yolov8l.value)

        self.ui.tableWidget_plate.cellClicked.connect(self.on_table_cell_clicked)


        self.ui.pushButton_close.clicked.connect(self.pushButton_close_func)
        self.ui.comboBox_model.setCurrentText("Yolov8l")
        self.tableWidgetProfilePage()



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
        print("1")
        for dictionary in overspeed_Profile_Controller.plate:
            print("2")
            print(dictionary["plate_text"])
            print(cell_text)
            if dictionary["plate_text"][0][1] == cell_text:
                print("3")
                frame = dictionary["frame"]
                x1,y1,x2,y2 = dictionary["dimension1"]
                xmin,ymin,xmax,ymax = dictionary["dimension2"]

                cap = cv2.VideoCapture('assets/video/traffic.mp4')
                frame_number = frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                success, img = cap.read()
                print("4")
                if success:
                    print("4.1")
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

                    print("4.5")
                else:
                    print(f"Cannot read frame {frame_number}")
                print("6")
                cap.release()
                



    def update_button_profile(self):
        rowCount = self.tableWidget.rowCount()
        for row in range(rowCount):
            self.tableWidget.removeRow(0)



        for dictionary in overspeed_Profile_Controller.plate:
            maxSpeed=0
            print("palte text = "+str(dictionary['plate_text'][0][1]))
            row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_count)
            plate_text = str(dictionary['plate_text'][0][1])
            item = QTableWidgetItem(plate_text)
            self.tableWidget.setItem(row_count, 0, item)

            for speC in Speed_Calculator.vehicle_max_speed:
                if speC["id"]==dictionary["id"]:
                    maxSpeed=speC["max_speed"]

            if maxSpeed > Speed_Calculator.overspeed:
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


