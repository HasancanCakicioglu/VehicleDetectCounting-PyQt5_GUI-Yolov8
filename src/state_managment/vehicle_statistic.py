from src.constants.carTypes import CarTypes


class vehicle_Statistic:
    def __init__(self):
        vehicle_Statistic.vehicle_count_info = []
        vehicle_Statistic.vehicle_speed_info = []


    @staticmethod
    def add_Statistic_vehicle_speed_info(speed,CarTypes:CarTypes):

        if speed <5:
            return None
        is_exist = False
        for dictionary in vehicle_Statistic.vehicle_speed_info:
            if CarTypes.value == dictionary["cartypes"]:
                is_exist = True

                if (speed < dictionary["speed"][-1] * 150 / 100) or (speed < 20):
                    dictionary["speed"] = dictionary["speed"] + [speed]
                else:
                    dictionary["speed"] = dictionary["speed"] + [dictionary["speed"][-1] * 150 / 100]


        if is_exist is False:
            vehicle_Statistic.vehicle_speed_info.append({"cartypes": CarTypes.value, "speed": [speed]})

    @staticmethod
    def gets_low_average_high_speed(CarTypes:CarTypes):
        low=0
        average=0
        high=0

        for dictionary in vehicle_Statistic.vehicle_speed_info:

            if CarTypes.value == dictionary["cartypes"]:
                speed_list = dictionary["speed"]
                low = min(speed_list)
                average = sum(speed_list) / len(speed_list)
                high=max(speed_list)

        return low,average,high