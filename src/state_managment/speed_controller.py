import math


def estimatedSpeed(location1,location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0],2) + math.pow(location2[1]-location1[1],2))

    ppm = 640 / 10
    d_meters = d_pixels / ppm
    fps = 18
    speed = d_meters * fps * 3.6
    return speed


class Speed_Calculator:
    def __init__(self):
        Speed_Calculator.vehicle_info  = []
        Speed_Calculator.vehicle_max_speed = []
        Speed_Calculator.overspeed= 40

    def add_vehicle_speed_info(self,id,veri):

        is_exist = False
        for dictionary in Speed_Calculator.vehicle_info:

            if dictionary["id"] == id:

                is_exist = True
                dictionary["list"] = dictionary["list"] + [veri]
                if len(dictionary["list"]) >= 2:
                    return estimatedSpeed(dictionary["list"][-2], dictionary["list"][-1])
                else:
                    return None
        if is_exist == False:
            Speed_Calculator.vehicle_info.append({"id": id, "list": [veri]})
            return None

    def add_max_vehicle_speed(self,id,max_speed):
        is_exist = False

        for dictionary in Speed_Calculator.vehicle_max_speed:
            if dictionary["id"] == id:
                is_exist = True

                dictionary["max_speed"] = max(dictionary["max_speed"],max_speed)

        if is_exist == False:
            Speed_Calculator.vehicle_max_speed.append({"id": id, "max_speed": max_speed})