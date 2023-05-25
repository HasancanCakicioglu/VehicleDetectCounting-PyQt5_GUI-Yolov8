import time

class VideoController:
    playing = False

    @staticmethod
    def control():
        while VideoController.playing:
            time.sleep(1)
            print("Video is playing...")

    @staticmethod
    def stop():
        VideoController.playing = True

    @staticmethod
    def run():
        VideoController.playing = False

    @staticmethod
    def toggle():
        if VideoController.playing:
            VideoController.playing = False
        else:
            VideoController.playing = True
