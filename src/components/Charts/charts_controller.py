from src.components.Charts.pie_chart import pie_Chart



class charts_Controller(pie_Chart):
    def __init__(self):
        super().__init__(self.ui)
        self.frame = self.ui.frame_static_page

        if self.frame.layout() is not None:
            for i in reversed(range(self.frame.layout().count())):
                widgetToRemove = self.frame.layout().itemAt(i).widget()
                self.frame.layout().removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)

