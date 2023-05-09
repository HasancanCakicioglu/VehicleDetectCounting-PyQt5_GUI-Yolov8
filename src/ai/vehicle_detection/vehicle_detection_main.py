import time

from PyQt5.QtGui import *
import numpy as np
from ultralytics import YOLO
import cv2
import math
import cvzone
import easyocr

from src.Utility.restrictive import restrictive
from src.Utility.resultTracker import result_tracker
from src.Utility.track.sort import Sort
from src.ai.plate_detection_controller import plateDetectionController
from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.constants.assets.color_constants import Color_Constants
from src.constants.carTypes import CarTypes
from src.state_managment.checkBox_controller import CheckBoxController
from src.state_managment.chosen_variable import chosenVariable
from src.state_managment.count_vehicle import count_vehicle_statistics
from src.state_managment.overspeed_profile_controller import overspeed_Profile_Controller
from src.state_managment.speed_controller import Speed_Calculator
from src.state_managment.vehicle_statistic import vehicle_Statistic


def vehicle_detection_counting(self):

    speed_Calcualtor= Speed_Calculator()
    overspeed = overspeed_Profile_Controller()
    res = result_tracker()

    self.cap = cv2.VideoCapture(self.image_path[0])
    model = YOLO(self.model)

    classNames = AssetsConstants.get_classnames()

    mask = cv2.imread(AssetsConstants.get_mask_path(assetsEnum.mask.value))
    mask1 = cv2.imread(AssetsConstants.get_mask_path(assetsEnum.mask.value))
    #print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #print(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #print(mask.shape)

    # mask= cv2.resize(mask, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # Tracking
    trackerCar = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    trackerMotorbike = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    trackerTruck = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    trackerBus = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    #[0, 597, 1920, 597]
    myLimit = chosenVariable.get_line()

    if myLimit == None:
        limits = [0,0,0,0]
    else:
        limits = myLimit




    totalCountCar = []
    totalCountMotorbike = []
    totalCountTruck = []
    totalCountBus=[]

    carGraphics = cv2.imread(AssetsConstants.get_image_path(assetsEnum.car.value), cv2.IMREAD_UNCHANGED)

    motorbikeGraphics = cv2.imread(AssetsConstants.get_image_path(assetsEnum.motorbike.value), cv2.IMREAD_UNCHANGED)

    busGraphics = cv2.imread(AssetsConstants.get_image_path(assetsEnum.bus.value), cv2.IMREAD_UNCHANGED)
    overlayWidthBus = busGraphics.shape[1]
    overlayHeightBus = busGraphics.shape[0]

    truckGraphics = cv2.imread(AssetsConstants.get_image_path(assetsEnum.truck.value), cv2.IMREAD_UNCHANGED)
    overlayWidthTruck = truckGraphics.shape[1]
    overlayHeightTruck = truckGraphics.shape[0]


    while self.ThreadActive:
        start_time = time.time()
        success, img = self.cap.read()
        heightImage, widthImage, channels = img.shape

        overspeed_punishment = chosenVariable.get_Speed_Limit()


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
        #print("remaninin time "+str(remaining_time))
        #print("frame count = "+str(frame_count))
        #print("current fraem = "+str(current_frame))
        if current_frame == frame_count-1:

            self.ThreadActive = False

            self.cap.release()

            self.quit()
            break


        if CheckBoxController.get_value_plate_detection() or CheckBoxController.get_value_vehicle_detection():
            mymask = chosenVariable.get_mask()
            if mymask == None:
                imgRegion=img
            else:
                imgRegion = cv2.bitwise_and(img, mask)

        if CheckBoxController.get_value_vehicle_detection():



            img = cvzone.overlayPNG(self.cap.read()[1], carGraphics, (0, 0))

            img = cvzone.overlayPNG(img, motorbikeGraphics, (0, 160))

            img = cvzone.overlayPNG(img, busGraphics, (widthImage - overlayWidthBus, 0))
            img = cvzone.overlayPNG(img, truckGraphics, (widthImage - overlayWidthTruck ,160))


            results = model(imgRegion, stream=True)


            detectionsCar = np.empty((0, 5))
            detectionsMotorbike = np.empty((0, 5))
            detectionsTruck = np.empty((0, 5))
            detectionsBus = np.empty((0, 5))

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

                    if conf<0.3:
                        continue

                    if currentClass == "car":
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detectionsCar = np.vstack((detectionsCar, currentArray))
                    elif currentClass == "motorbike":
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detectionsMotorbike = np.vstack((detectionsMotorbike, currentArray))
                    elif currentClass == "truck":
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detectionsTruck = np.vstack((detectionsTruck, currentArray))
                    elif currentClass == "bus":
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detectionsBus = np.vstack((detectionsBus, currentArray))

            resultsTracker = trackerCar.update(detectionsCar)
            resultsTrackerMotorbike = trackerMotorbike.update(detectionsMotorbike)
            resultsTrackerBus = trackerBus.update(detectionsBus)
            resultsTrackerTruck = trackerTruck.update(detectionsTruck)

            cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
            #totalCountCar,img=  res.resultTrackerDo(img=img,resultsTracker=resultsTracker,current_frame=current_frame,overspeed=overspeed,speed_Calcualtor=speed_Calcualtor,limits=limits,totalCountCar=totalCountCar)
            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cy = y1 + h // 2
                colorRect = Color_Constants.get_Purple_Color()
                blueSpeedColor = Color_Constants.get_Blue_Color()
                idColor = Color_Constants.get_Orange_Color()



                if CheckBoxController.get_value_plate_detection() and restrictive.plate_detection_restrictive(cy,heightImage):
                    b, xmin, ymin, xmax, ymax, ocr_result = plateDetectionController.predict(image_np=img[y1:y2, x1:x2],
                                                                                             id=id)

                    if b:
                        overspeed.add_overspeed_Profile_info(id=id, frame=current_frame, dimension1=[x1, y1, x2, y2],
                                                             dimension2=[xmin, ymin, xmax, ymax], plate_text=ocr_result)

                if CheckBoxController.get_value_speed_detection():

                    speed = speed_Calcualtor.add_vehicle_speed_info(id, [x1 + w / 2, y1 + h / 2])

                    if speed is not None:
                        speed_Calcualtor.add_max_vehicle_speed(id=id, max_speed=speed)
                        cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1 + w / 2)-20), max(35, y1-40)),
                                           scale=2, thickness=3, offset=10,colorR=blueSpeedColor)

                        if restrictive.speed_detection_restrictive(cy,heightImage):
                            vehicle_Statistic.add_Statistic_vehicle_speed_info(speed=speed, CarTypes=CarTypes.CAR)

                        if speed > overspeed_punishment:
                            colorRect = Color_Constants.get_Red_Color()

                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5, colorR=colorRect)
                cvzone.putTextRect(img, f' {int(id)} - Car', (max(0, x1), max(35, y1 - 5),),
                                   scale=2, thickness=3, offset=10,colorR=idColor)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                    if totalCountCar.count(id) == 0:
                        totalCountCar.append(id)
                        count_vehicle_statistics.add_Statistic_vehicle_count_type_info(CarTypes=CarTypes.CAR)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)



            for result in resultsTrackerMotorbike:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # print(result)
                w, h = x2 - x1, y2 - y1

                colorRect = Color_Constants.get_Purple_Color()

                if CheckBoxController.get_value_speed_detection():
                    speed = speed_Calcualtor.add_vehicle_speed_info(id, [x1 + w / 2, y1 + h / 2])

                    if speed is not None:
                        cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1 + w / 2)-20), max(35, y1)-40),
                                           scale=2, thickness=3, offset=10,colorR=blueSpeedColor)
                        if speed > overspeed_punishment:
                            colorRect = Color_Constants.get_Red_Color()
                        if restrictive.speed_detection_restrictive(cy, heightImage):
                            vehicle_Statistic.add_Statistic_vehicle_speed_info(speed=speed, CarTypes=CarTypes.MOTORBIKE)


                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=colorRect)
                cvzone.putTextRect(img, f' {int(id)} - Motorbike', (max(0, x1), max(35, y1)),
                                   scale=2, thickness=3, offset=10,colorR=idColor)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                    if totalCountMotorbike.count(id) == 0:
                        totalCountMotorbike.append(id)
                        count_vehicle_statistics.add_Statistic_vehicle_count_type_info(CarTypes=CarTypes.MOTORBIKE)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)


            for result in resultsTrackerBus:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cy = y1 + h // 2
                colorRect = Color_Constants.get_Purple_Color()

                if CheckBoxController.get_value_plate_detection() and 900 > cy > 500:
                    b, xmin, ymin, xmax, ymax, ocr_result = plateDetectionController.predict(image_np=img[y1:y2, x1:x2],
                                                                                             id=id)

                    if b:
                        overspeed.add_overspeed_Profile_info(id=id, frame=current_frame, dimension1=[x1, y1, x2, y2],
                                                             dimension2=[xmin, ymin, xmax, ymax], plate_text=ocr_result)

                if CheckBoxController.get_value_speed_detection():

                    speed = speed_Calcualtor.add_vehicle_speed_info(id, [x1 + w / 2, y1 + h / 2])

                    if speed is not None:
                        speed_Calcualtor.add_max_vehicle_speed(id=id, max_speed=speed)
                        cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1 + w / 2)-20), max(35, y1-40)),
                                           scale=2, thickness=3, offset=10,colorR=blueSpeedColor)

                        if restrictive.speed_detection_restrictive(cy, heightImage):
                            vehicle_Statistic.add_Statistic_vehicle_speed_info(speed=speed, CarTypes=CarTypes.BUS)

                        if speed > overspeed_punishment:
                            colorRect = Color_Constants.get_Red_Color()

                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5, colorR=colorRect)
                cvzone.putTextRect(img, f' {int(id)} - Bus', (max(0, x1), max(35, y1 - 5)),
                                   scale=2, thickness=3, offset=10,colorR=idColor)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                    if totalCountBus.count(id) == 0:
                        totalCountBus.append(id)
                        count_vehicle_statistics.add_Statistic_vehicle_count_type_info(CarTypes=CarTypes.BUS)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)


            for result in resultsTrackerTruck:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cy = y1 + h // 2
                colorRect = Color_Constants.get_Purple_Color()

                if CheckBoxController.get_value_plate_detection() and 900 > cy > 500:
                    b, xmin, ymin, xmax, ymax, ocr_result = plateDetectionController.predict(image_np=img[y1:y2, x1:x2],
                                                                                             id=id)

                    if b:
                        overspeed.add_overspeed_Profile_info(id=id, frame=current_frame, dimension1=[x1, y1, x2, y2],
                                                             dimension2=[xmin, ymin, xmax, ymax], plate_text=ocr_result)

                if CheckBoxController.get_value_speed_detection():

                    speed = speed_Calcualtor.add_vehicle_speed_info(id, [x1 + w / 2, y1 + h / 2])

                    if speed is not None:
                        speed_Calcualtor.add_max_vehicle_speed(id=id, max_speed=speed)
                        cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1 + w / 2)-20), max(35, y1-40)),
                                           scale=2, thickness=3, offset=10,colorR=blueSpeedColor)

                        if restrictive.speed_detection_restrictive(cy, heightImage):
                            vehicle_Statistic.add_Statistic_vehicle_speed_info(speed=speed, CarTypes=CarTypes.TRUCK)

                        if speed > overspeed_punishment:
                            colorRect = Color_Constants.get_Red_Color()

                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5, colorR=colorRect)
                cvzone.putTextRect(img, f' {int(id)} - Truck', (max(0, x1), max(35, y1 - 5)),
                                   scale=2, thickness=3, offset=10,colorR=idColor)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                    if totalCountTruck.count(id) == 0:
                        totalCountTruck.append(id)
                        count_vehicle_statistics.add_Statistic_vehicle_count_type_info(CarTypes=CarTypes.TRUCK)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            # cvzone.putTextRect(img, f' Count: {len(totalCount)}', (50, 50))
            cv2.putText(img, str(len(totalCountCar)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

            cv2.putText(img, str(len(totalCountMotorbike)), (255, 280), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

            cv2.putText(img, str(len(totalCountBus)), (int(widthImage - (overlayWidthBus/1.5)), 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

            cv2.putText(img, str(len(totalCountTruck)), (int(widthImage - (overlayWidthTruck/1.5)), 280), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

            # new_size = (1000, 500)  # Yeni boyut
            # resized_img = cv2.resize(img, new_size)

            # cv2.imshow("ImageRegion", imgRegion)

            # if CheckBoxController.get_value_plate_detection():
            #    img = plateDetectionController.predict(image_np=img)

        height, width, channel = img.shape

        convertToQtFormat = QImage(img.data, width, height, QImage.Format_RGB888)

        # 840 , 580
        pic = convertToQtFormat.scaled(939, 481)

        self.ImageUpdate.emit(pic)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"İşlem {elapsed_time:.4f} saniye sürdü.")


    self.cap.release()


