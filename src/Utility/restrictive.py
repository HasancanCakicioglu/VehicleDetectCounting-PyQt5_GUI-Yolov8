


class restrictive:

    @staticmethod
    def plate_detection_restrictive(cy,h):
        if (h * 85 / 100) > cy > (h * 45 / 100):
            return True
        else:
            return False

    @staticmethod
    def speed_detection_restrictive(cy, h):
        if (h * 80 / 100) > cy > (h * 15 / 100):
            return True
        else:
            return False
