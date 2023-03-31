from PyQt5.QtGui import *
from PyQt5.QtCore import *
import torch
from src.ai.vehicle_detection.vehicle_detection_main import vehicle_detection_counting


class videoPlayer(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, image_path,model):
        super().__init__()
        self.image_path = image_path
        self.model = model

    def run(self):
        self.ThreadActive = True
        #self.cap = cv2.VideoCapture("traffic.mp4")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Kodunuz {} üzerinde çalışıyor.".format(device))

        vehicle_detection_counting(self)
        self.cap.release()
        self.quit()

    def stop(self):
        self.ThreadActive = False

