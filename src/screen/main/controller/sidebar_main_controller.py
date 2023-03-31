import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QStyle

from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon

from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.screen.main.generate.sidebar_main_generate import Ui_MainWindow
from src.state_managment.checkBox_controller import CheckBoxController
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

        self.ui.comboBox_model.currentTextChanged.connect(self.comboBox_model_func)
        self.model = AssetsConstants.get_model_path(assetsEnum.yolov8l.value)


        self.ui.pushButton_close.clicked.connect(self.pushButton_close_func)
        self.ui.comboBox_model.setCurrentText("Yolov8l")


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
            CheckBoxController.set_value(True)
        else:
            CheckBoxController.set_value(False)


    def selectVideo(self):

        fname = QFileDialog.getOpenFileName(self, 'Video Seç', '.', 'Video Dosyaları (*.mp4 *.avi)')

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


