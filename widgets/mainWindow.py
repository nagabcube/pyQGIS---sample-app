# -*- coding: utf-8 -*-
import os

from qgis.PyQt.QtWidgets import QMainWindow, QFileDialog, QHBoxLayout, QVBoxLayout, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject, QgsLayerTreeModel, QgsRasterLayer, QgsCoordinateReferenceSystem
from qgis.gui import QgsMapCanvas, QgsMapToolZoom, QgsMapToolPan, QgsMapToolIdentifyFeature, QgsLayerTreeView, QgsLayerTreeMapCanvasBridge
from qgis.PyQt.QtCore import Qt

from ui.main_ui import Ui_MainWindow
from utils.customMenu import CustomMenuProvider
from widgets.custom_maptool import RectangleMapTool, PolygonMapTool, PointMapTool, LineMapTool

PROJECT = QgsProject.instance()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.first_flag = True
        self.setWindowTitle('PyQGIS - Demo alkalmazás')

        vl = QVBoxLayout(self.dockWidgetContents)
        self.layerTreeView = QgsLayerTreeView(self)
        vl.addWidget(self.layerTreeView)
        self.mapCanvas = QgsMapCanvas(self)
        self.mapCanvas.setCanvasColor(Qt.black)
        crs = QgsCoordinateReferenceSystem('EPSG:3857')
        self.mapCanvas.setDestinationCrs(crs)
        hl = QHBoxLayout(self.frame)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.addWidget(self.mapCanvas)

        self.model = QgsLayerTreeModel(PROJECT.layerTreeRoot(), self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.model.setAutoCollapseLegendNodes(10)
        self.layerTreeView.setModel(self.model)
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(PROJECT.layerTreeRoot(), self.mapCanvas, self)

        self.mapCanvas.xyCoordinates.connect(self.showLngLat)

        self.actionOpen.triggered.connect(self.actionOpenTriggered)
        self.actionQuit.triggered.connect(self.close)

        self.actionPanTriggered()
        self.actionPan.triggered.connect(self.actionPanTriggered)
        self.actionZoomin.triggered.connect(self.actionZoomInTriggered)
        self.actionZoomout.triggered.connect(self.actionZoomOutTriggered)
        self.actionIdentity.triggered.connect(self.actionIdentifyTriggered)

        self.actionShapefile.triggered.connect(self.actionShapefileTriggered)
        self.actionCsv.triggered.connect(self.actionCsvTriggered)
        self.actionXYZ.triggered.connect(self.actionXYZTriggered)

        self.actionPoint.triggered.connect(self.actionPointTriggered)
        self.actionLine.triggered.connect(self.actionLineTriggered)
        self.actionRectangle.triggered.connect(self.actionRectangleTriggered)
        self.actionPolygon.triggered.connect(self.actionPolygonTriggered)

        self.actionAboutQt.triggered.connect(lambda: QMessageBox.aboutQt(self, 'Qt'))
        self.actionAbout.triggered.connect(lambda: QMessageBox.about(self, 'Névjegy', 'PyQGIS kisérleti applikáció v.0.2'))

        self.customMenuProvider = CustomMenuProvider(self.layerTreeView, self.mapCanvas)
        self.layerTreeView.setMenuProvider(self.customMenuProvider)

    def actionOpenTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '', '', 'projekt fájl(*.qgs , *.qgz)')
        if data_file:
            PROJECT.read(data_file)

    def actionPanTriggered(self):
        self.mapTool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionZoomInTriggered(self):
        self.mapTool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionZoomOutTriggered(self):
        self.mapTool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.mapTool)

    def actionIdentifyTriggered(self):
        self.identifyTool = QgsMapToolIdentifyFeature(self.mapCanvas)
        self.identifyTool.featureIdentified.connect(self.showFeatures)
        self.mapCanvas.setMapTool(self.identifyTool)

        layers = self.mapCanvas.layers()
        if layers:
            self.identifyTool.setLayer(layers[0])

    def showFeatures(self, feature):

        QMessageBox.information(self, 'Az objektum adatai', ''.join(feature.attributes()))

    def actionAddGroupTriggered(self):
        PROJECT.layerTreeRoot().addGroup('group1')

    def actionShapefileTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, 'ESRI Shape', '', '*.shp')
        if data_file:
            layer = QgsVectorLayer(data_file, os.path.splitext(os.path.basename(data_file))[0], "ogr")
            self.addLayer(layer)

    def actionCsvTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, 'Szöveg (CSV)', '', '*.csv')
        if data_file:
            data_file = os.path.splitdrive(data_file)[1]
            uri = f"file://{data_file}?delimiter=,&xField=x&yField=y"
            layer = QgsVectorLayer(uri, "point", "delimitedtext")
            self.addLayer(layer)

    def actionXYZTriggered(self):
        uri = 'type=xyz&' \
              'url=https://www.google.cn/maps/vt?lyrs=s@804%26gl=cn%26x={x}%26y={y}%26z={z}&' \
              'zmax=19&' \
              'zmin=0&' \
              'crs=EPSG3857'
        layer = QgsRasterLayer(uri, 'google', 'wms')
        self.addLayer(layer)

    def addLayer(self, layer):
        if layer.isValid():
            if self.first_flag:
                self.mapCanvas.setDestinationCrs(layer.crs())
                self.mapCanvas.setExtent(layer.extent())
                self.first_flag = False
            PROJECT.addMapLayer(layer)
            layers = [layer] + [PROJECT.mapLayer(i) for i in PROJECT.mapLayers()]
            self.mapCanvas.setLayers(layers)
            self.mapCanvas.refresh()
        else:
            print('valami gond van...')

    def actionPointTriggered(self):
        self.pointTool = PointMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.pointTool)

    def actionLineTriggered(self):
        self.lineTool = LineMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.lineTool)

    def actionRectangleTriggered(self):
        self.rectangleTool = RectangleMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.rectangleTool)

    def actionPolygonTriggered(self):
        self.polygonTool = PolygonMapTool(self.mapCanvas)
        self.mapCanvas.setMapTool(self.polygonTool)

    def showLngLat(self, point):
        x = point.x()
        y = point.y()
        self.statusbar.showMessage(f'X:{x}, Y:{y}')
