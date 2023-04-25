import cvzone
from cv2 import cv2

from src.ai.plate_detection_controller import plateDetectionController
from src.constants.assets.color_constants import Color_Constants
from src.state_managment.checkBox_controller import CheckBoxController
from src.state_managment.speed_controller import Speed_Calculator


class result_tracker:
    def __init__(self):
        pass


    def resultTrackerDo(self,resultsTracker,current_frame,img,overspeed,speed_Calcualtor,limits,totalCountCar):

        for result in resultsTracker:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cy = y1 + h // 2
            colorRect = Color_Constants.get_Purple_Color()

            if CheckBoxController.get_value_plate_detection() and 900 > cy > 500:
                b, xmin, ymin, xmax, ymax, ocr_result = plateDetectionController.predict(image_np=img[y1:y2, x1:x2],
                                                                                         id=id)
                print("frame = " + str(current_frame) + "," + str(x1 + xmin) + "," + str(x1 + xmax) + "," + str(
                    y1 + ymin) + "," + str(y1 + ymax))
                if b:
                    overspeed.add_overspeed_Profile_info(id=id, frame=current_frame, dimension1=[x1, y1, x2, y2],
                                                         dimension2=[xmin, ymin, xmax, ymax], plate_text=ocr_result)

            if CheckBoxController.get_value_speed_detection():

                speed = speed_Calcualtor.add_vehicle_speed_info(id, [x1 + w / 2, y1 + h / 2])

                if speed is not None:
                    speed_Calcualtor.add_max_vehicle_speed(id=id, max_speed=speed)
                    cvzone.putTextRect(img, f' {int(speed)}/KM', (max(0, int(x1 + w / 2)), max(35, y1)),
                                       scale=2, thickness=3, offset=10)

                    if speed > Speed_Calculator.overspeed:
                        colorRect = Color_Constants.get_Red_Color()

            cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5, colorR=colorRect)
            cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1 - 5)),
                               scale=2, thickness=3, offset=10)

            cx, cy = x1 + w // 2, y1 + h // 2
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            if limits[0] < cx < limits[2] and limits[1] - 30 < cy < limits[1] + 30:

                if totalCountCar.count(id) == 0:
                    totalCountCar.append(id)
                    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            return totalCountCar,img