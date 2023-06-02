import sys
from PyQt5.QtWidgets import QApplication

from src.Initialize.model_initialize import initialize
from src.constants.assets.assets_constants import AssetsConstants
from src.constants.assets.assets_enums import assetsEnum
from src.screen.main.controller.sidebar_main_controller import MainWindow



if __name__=="__main__":
    initialize()
    app = QApplication(sys.argv)

    with open(AssetsConstants.get_theme_path(assetsEnum.style_qss.value),"r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)



    window = MainWindow()
    window.show()


    sys.exit(app.exec())


