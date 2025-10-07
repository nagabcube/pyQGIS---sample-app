# -*- coding: utf-8 -*-
import os, sys

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsApplication

from splash import NewSplashScreen
from widgets.mainWindow import MainWindow
from qt_material import apply_stylesheet

def setup_qgis(app):
    """ Set QGIS paths based on whether running as a bundled application or not """
    if getattr(sys, "frozen", False):
        print("Running In An Application Bundle")
        bundle_dir = sys._MEIPASS
        os.environ["PROJ_LIB"] = bundle_dir + "/proj_db"
        os.environ["GDAL_DRIVER_PATH"] = bundle_dir + "/qgis/plugins"
    else:
        print("Running In A Normal Python Environment")
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
qgs = QgsApplication([], True)
qgs.setPrefixPath('qgis', True)
setup_qgis(qgs)
qgs.initQgis()

splash = NewSplashScreen()
splash.show()
qgs.initQgis()
apply_stylesheet(qgs, theme='dark_lightgreen.xml')

mainWindow = MainWindow()
mainWindow.setWindowIcon(QIcon('./icons/pyqgis.ico'))
mainWindow.showMaximized()
mainWindow.show()
splash.finish(mainWindow)
qgs.exec_()
qgs.exitQgis()
