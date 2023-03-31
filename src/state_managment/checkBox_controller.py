

class CheckBoxController:
    _vehicle_detection = False

    @classmethod
    def set_value(cls, new_value):
        if isinstance(new_value, bool):
            cls._vehicle_detection = new_value
        else:
            raise TypeError("Değer bir boolean olmalıdır.")

    @classmethod
    def get_value(cls):
        return cls._vehicle_detection