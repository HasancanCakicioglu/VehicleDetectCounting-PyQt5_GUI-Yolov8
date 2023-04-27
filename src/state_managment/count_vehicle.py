from src.constants.carTypes import CarTypes


class count_vehicle_statistics:
    def __init__(self):
        count_vehicle_statistics.vehicle_count_type_info = []

    @staticmethod
    def add_Statistic_vehicle_count_type_info(CarTypes:CarTypes):

        is_exist = False
        for dictionary in count_vehicle_statistics.vehicle_count_type_info:
            if CarTypes.value == dictionary["cartypes"]:
                is_exist = True
                dictionary["count"]=dictionary["count"]+1


        if is_exist is False:
            count_vehicle_statistics.vehicle_count_type_info.append({"cartypes": CarTypes.value, "count": 1})
