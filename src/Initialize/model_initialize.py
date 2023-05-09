

from src.ai.plate_detection_controller import plateDetectionController
from src.database.database_sqlite3 import Driver
from src.state_managment.chosen_variable import chosenVariable
from src.state_managment.count_vehicle import count_vehicle_statistics
from src.state_managment.vehicle_statistic import vehicle_Statistic


def initialize():
    plateDetectionController.initialize()
    plateDetectionController.getInstance("assets/model/plate_detection/saved_model")
    vehicle_Statistic()
    count_vehicle_statistics()
    chosenVariable()

    Driver.save(Driver("","","",0,0,""))

