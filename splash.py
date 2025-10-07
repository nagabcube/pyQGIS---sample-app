# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QSplashScreen

class NewSplashScreen(QSplashScreen):
    def __init__(self):
        super(NewSplashScreen, self).__init__()
        self.setPixmap(QPixmap('./icons/splash.png'))

    def mousePressEvent(self, event):
        pass
