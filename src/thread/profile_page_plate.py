from PyQt5.QtCore import QThread, pyqtSignal


class UpdateProfileThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, plate_dict, table_widget):
        super().__init__()
        self.plate_dict = plate_dict
        self.table_widget = table_widget

    def run(self):
        for dictionary in self.plate_dict:
            plate_text = dictionary['plate_text'][0]
            self.result_signal.emit(plate_text)