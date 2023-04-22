

class CheckBoxController:
    _vehicle_detection = False
    _plate_detection = False
    _speed_detection = False

    @classmethod
    def set_value_vehicle_detection(cls, new_value):
        if isinstance(new_value, bool):
            cls._vehicle_detection = new_value
        else:
            raise TypeError("Değer bir boolean olmalıdır.")

    @classmethod
    def get_value_vehicle_detection(cls):
        return cls._vehicle_detection

    @classmethod
    def set_value_plate_detection(cls, new_value):
        if isinstance(new_value, bool):
            cls._plate_detection = new_value
        else:
            raise TypeError("Değer bir boolean olmalıdır.")

    @classmethod
    def get_value_plate_detection(cls):
        return cls._plate_detection

    @classmethod
    def set_value_speed_detection(cls, new_value):
        if isinstance(new_value, bool):
            cls._speed_detection = new_value
        else:
            raise TypeError("Değer bir boolean olmalıdır.")

    @classmethod
    def get_value_speed_detection(cls):
        return cls._speed_detection