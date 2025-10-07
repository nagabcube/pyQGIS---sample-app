# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QMenu, QAction
from qgis.core import QgsLayerTreeNode, QgsLayerTree, QgsMapLayerType
from qgis.gui import QgsLayerTreeViewMenuProvider, QgsLayerTreeView, QgsLayerTreeViewDefaultActions, QgsMapCanvas

from widgets.attributeDialog import AttributeDialog

class CustomMenuProvider(QgsLayerTreeViewMenuProvider):
    def __init__(self, layerTreeView: QgsLayerTreeView, mapCanvas: QgsMapCanvas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layerTreeView = layerTreeView
        self.mapCanvas = mapCanvas

    def createContextMenu(self):
        menu = QMenu()
        actions: QgsLayerTreeViewDefaultActions = self.layerTreeView.defaultActions()
        if not self.layerTreeView.currentIndex().isValid():
            self.actionAddGroup = actions.actionAddGroup(menu)
            menu.addAction(self.actionAddGroup)
            menu.addAction('Expand All', self.layerTreeView.expandAll)
            menu.addAction('Collapse All', self.layerTreeView.collapseAll)
            return menu

        node: QgsLayerTreeNode = self.layerTreeView.currentNode()

        if QgsLayerTree.isGroup(node):
            pass
        elif QgsLayerTree.isLayer(node):
            self.actionZoomToLayer = actions.actionZoomToLayer(self.mapCanvas, menu)
            menu.addAction(self.actionZoomToLayer)
            layer = self.layerTreeView.currentLayer()
            if layer.type() == QgsMapLayerType.VectorLayer:
                actionOpenAttributeDialog = QAction('A réteg adatai', menu)
                actionOpenAttributeDialog.triggered.connect(lambda: self.openAttributeDialog(layer))
                menu.addAction(actionOpenAttributeDialog)
            else:
                pass
            menu.addSeparator()
            actionRemoveLayer = QAction('Réteg eltávolítása', menu)
            #actionRemoveLayer.triggered.connect(node.onRemoveLayers)
            menu.addAction(actionRemoveLayer)
        else:
            print('node type is none')

        return menu

    def openAttributeDialog(self, layer):
        self.attributeDialog = AttributeDialog(self.mapCanvas, parent=self.mapCanvas.parent())
        self.attributeDialog.openAttributeDialog(layer)
        self.attributeDialog.show()
