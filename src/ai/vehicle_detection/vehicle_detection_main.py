from PyQt5.QtGui import *
import numpy as np
from ultralytics import YOLO
import cv2
import math
import cvzone
from src.Utility.track.sort import Sort
from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.state_managment.checkBox_controller import CheckBoxController


def vehicle_detection_counting(self):

    self.cap = cv2.VideoCapture(self.image_path[0])

    model = YOLO(self.model)

    classNames = AssetsConstants.get_classnames()

    mask = cv2.imread(AssetsConstants.get_mask_path(assetsEnum.mask.value))
    print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(mask.shape)

    # mask= cv2.resize(mask, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # Tracking
    trackerCar = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    trackerMotorbike = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    limits = [0, 597, 1920, 597]
    totalCountCar = []
    totalCountMotorbike = []

    carGraphics = cv2.imread(AssetsConstants.get_image_path(assetsEnum.car.value), cv2.IMREAD_UNCHANGED)

    motorbikeGraphics = cv2.imread(AssetsConstants.get_image_path(assetsEnum.motorbike.value), cv2.IMREAD_UNCHANGED)

    while self.ThreadActive:
        success, img = self.cap.read()

        frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        remaining_time = (frame_count - current_frame) / fps

        # video bittiğinde
        if current_frame == frame_count:
            self.ThreadActive = False
            self.cap.release()
            self.quit()
            break
        if CheckBoxController.get_value():
            imgRegion = cv2.bitwise_and(img, mask)

            img = cvzone.overlayPNG(self.cap.read()[1], carGraphics, (0, 0))

            img = cvzone.overlayPNG(img, motorbikeGraphics, (0, 160))

            results = model(imgRegion, stream=True)

            detectionsCar = np.empty((0, 5))
            detectionsMotorbike = np.empty((0, 5))

            # 1 - x
            # 2 - y
            # 3 - genişlik
            # 4 - yükseklik
            # 5 - olasılık skoru

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                    w, h = x2 - x1, y2 - y1

                    # Confidence
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    # Class Name
                    cls = int(box.cls[0])
                    currentClass = classNames[cls]

                    if currentClass == "car" or currentClass == "truck" or currentClass == "bus" \
                            and conf > 0.3:
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detectionsCar = np.vstack((detectionsCar, currentArray))
                    elif currentClass == "motorbike":
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detectionsMotorbike = np.vstack((detectionsMotorbike, currentArray))

            resultsTracker = trackerCar.update(detectionsCar)
            resultsTrackerMotorbike = trackerMotorbike.update(detectionsMotorbike)

            cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # print(result)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                                   scale=2, thickness=3, offset=10)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                    if totalCountCar.count(id) == 0:
                        totalCountCar.append(id)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)
            for result in resultsTrackerMotorbike:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # print(result)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                                   scale=2, thickness=3, offset=10)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                    if totalCountMotorbike.count(id) == 0:
                        totalCountMotorbike.append(id)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            # cvzone.putTextRect(img, f' Count: {len(totalCount)}', (50, 50))
            cv2.putText(img, str(len(totalCountCar)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

            cv2.putText(img, str(len(totalCountMotorbike)), (255, 280), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

            # new_size = (1000, 500)  # Yeni boyut
            # resized_img = cv2.resize(img, new_size)

            # cv2.imshow("ImageRegion", imgRegion)

        height, width, channel = img.shape

        convertToQtFormat = QImage(img.data, width, height, QImage.Format_RGB888)

        # 840 , 580
        pic = convertToQtFormat.scaled(939, 481)

        self.ImageUpdate.emit(pic)