@echo off
set OSGEO4W_ROOT=C:\DevTools\QGIS
%OSGEO4W_ROOT%\bin\python-qgis.bat -m PyInstaller -w ^
--clean ^
--add-data="%OSGEO4W_ROOT%\apps\Python39\Lib\site-packages\PyQt5\*.pyd;PyQt5" ^
--add-data="%OSGEO4W_ROOT%\bin\gdalplugins;gdalplugins" ^
--add-data="%OSGEO4W_ROOT%\apps\qgis\plugins;qgis\plugins" ^
--add-data="%OSGEO4W_ROOT%\share\proj;proj_db" ^
--add-data="data;data" ^
--add-data="icons;icons" ^
--icon=icons\pyqgis.ico ^
--name="PyQGIS Demo" ^
main.py