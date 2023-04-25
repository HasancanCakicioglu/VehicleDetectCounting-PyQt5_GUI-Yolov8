from PyQt5.QtChart import QPieSeries, QChartView, QChart
from PyQt5.QtGui import QPainter


class pie_Chart():
    def __init__(self,ui):
        self.ui=ui


    def createPieCharts(self,layout):


        series1 = QPieSeries()
        series1.append("Motorbike", 15)
        series1.append("Car", 40)
        series1.append("Bus", 25)
        series1.append("Truck", 20)

        chartView1 = QChartView()
        chartView1c = chartView1.chart()
        chart1 = QChart()
        chartView1c.addSeries(series1)
        chartView1.setRenderHint(QPainter.Antialiasing)
        chartView1c.setTitle("Vehicle Counts")
        chartView1c.setAnimationOptions(QChart.SeriesAnimations)

        chartView1.setFixedSize(self.ui.frame_static_page.width() / 1.1, self.ui.frame_static_page.height() / 1.1)

        layout.addWidget(chartView1)



