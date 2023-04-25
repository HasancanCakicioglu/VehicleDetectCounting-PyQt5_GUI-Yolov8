

from src.ai.plate_detection_controller import plateDetectionController
from src.state_managment.vehicle_statistic import vehicle_Statistic


def initialize():
    plateDetectionController.initialize()
    plateDetectionController.getInstance("assets/model/plate_detection/saved_model")
    vehicle_Statistic()

