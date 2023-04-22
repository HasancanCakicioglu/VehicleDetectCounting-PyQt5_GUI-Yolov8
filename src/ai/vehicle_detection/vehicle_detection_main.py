import time

from PyQt5.QtGui import *
import numpy as np
from ultralytics import YOLO
import cv2
import math
import cvzone
import easyocr
from src.Utility.track.sort import Sort
from src.ai.plate_detection_controller import plateDetectionController
from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.constants.assets.color_constants import Color_Constants
from src.state_managment.checkBox_controller import CheckBoxController
from src.state_managment.overspeed_profile_controller import overspeed_Profile_Controller
from src.state_managment.speed_controller import Speed_Calculator


def vehicle_detection_counting(self):

    speed_Calcualtor= Speed_Calculator()
    overspeed = overspeed_Profile_Controller()

    self.cap = cv2.VideoCapture(self.image_path[0])
    model = YOLO(self.model)

    classNames = AssetsConstants.get_classnames()

    mask = cv2.imread(AssetsConstants.get_mask_path(assetsEnum.mask.value))
    #print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #print(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #print(mask.shape)

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
        start_time = time.time()
        success, img = self.cap.read()


        frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        remaining_time = (frame_count - current_frame) / fps

        #imgG = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #plates = plate_cascade.detectMultiScale(imgG,1.1,4, minSize=(5, 5), maxSize=(200, 200))
        #for (x, y, w, h) in plates:
        #    print("girdi"+str(plates))
        #    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # video bittiğinde
        if current_frame == frame_count:
            self.ThreadActive = False
            self.cap.release()
            self.quit()
            break



        if CheckBoxController.get_value_plate_detection() or CheckBoxController.get_value_vehicle_detection():
            imgRegion = cv2.bitwise_and(img, mask)



        if CheckBoxController.get_value_vehicle_detection():
            print("5")
            print("vehicle detection")

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
                    # w, h = x2 - x1, y2 - y1

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
                w, h = x2 - x1, y2 - y1
                cy = y1 + h // 2
                colorRect = Color_Constants.get_Purple_Color()

                if CheckBoxController.get_value_plate_detection() and 900 > cy > 500:
                    b,xmin, ymin,xmax, ymax ,ocr_result= plateDetectionController.predict(image_np=img[y1:y2, x1:x2],id=id)
                    print("frame = "+str(current_frame)+","+str(x1+xmin)+","+str(x1+xmax)+","+str(y1+ymin)+","+str(y1+ymax))
                    if b:
                        overspeed.add_overspeed_Profile_info(id=id, frame=current_frame, dimension1=[x1, y1, x2, y2],
                                                             dimension2=[xmin, ymin, xmax, ymax], plate_text=ocr_result)

                if CheckBoxController.get_value_speed_detection():

                    speed = speed_Calcualtor.add_vehicle_speed_info(id,[x1+w/2,y1+h/2])

                    if speed is not None:
                        speed_Calcualtor.add_max_vehicle_speed(id=id,max_speed=speed)
                        cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1+w/2)), max(35, y1)),
                                        scale=2, thickness=3, offset=10)

                        if speed > Speed_Calculator.overspeed:
                            colorRect = Color_Constants.get_Red_Color()

                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5, colorR=colorRect)
                cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1-5)),
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

                colorRect = Color_Constants.get_Purple_Color()

                if CheckBoxController.get_value_speed_detection():
                    speed = speed_Calcualtor.add_vehicle_speed_info(id,[x1+w/2,y1+h/2])

                    if speed is not None:
                        cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1+w/2)), max(35, y1)),
                                        scale=2, thickness=3, offset=10)
                        if speed > Speed_Calculator.overspeed:
                            colorRect = Color_Constants.get_Red_Color()

                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=colorRect)
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


        #if CheckBoxController.get_value_plate_detection():
        #    img = plateDetectionController.predict(image_np=img)

        height, width, channel = img.shape

        convertToQtFormat = QImage(img.data, width, height, QImage.Format_RGB888)

        # 840 , 580
        pic = convertToQtFormat.scaled(939, 481)

        self.ImageUpdate.emit(pic)


        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"İşlem {elapsed_time:.4f} saniye sürdü.")