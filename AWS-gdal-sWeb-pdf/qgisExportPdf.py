

# trouve ici:   https://gis.stackexchange.com/questions/416035/it-does-not-render-the-project-layers-in-the-qgis-canvas-nor-in-the-layout-expor


import os
import qgis.core

# from qgis.core import *

QgsApplication.setPrefixPath("C:/OSGeo4W/apps/qgis", True)

qgs = QgsApplication([], False)

qgs.initQgis()

file_dir = 'C:\\Users\\Ben\\Desktop\\Project_folder'

layer_paths = [os.path.join(file_dir, f) for f in os.scandir(file_dir)
                if f.name.endswith('.gpkg')
                or f.name.endswith('shp')]
#print(layer_paths)

style_paths = [os.path.join(file_dir, f) for f in os.scandir(file_dir)
                if f.name.endswith('.qml')]
#print(style_paths)

layer_names = ['3.Protected_areas', '2.Water', '1.Rivers']
layers_to_add = []

for i, n in enumerate(layer_names):
    for p in layer_paths:
        if n[3:] in p:
            layers_to_add.insert(i, p)

project = QgsProject.instance()
proj_file_path = os.path.join(file_dir, 'Standalone_Project.qgs')
project.setFileName(proj_file_path)

project.setCrs(QgsCoordinateReferenceSystem('epsg:3857'))

osm_url = 'type=xyz&url=https://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0'
osm_lyr = QgsRasterLayer(osm_url, '4.OpenStreetMap', 'wms')
project.addMapLayer(osm_lyr)

# Store maximum and minimum values of layer bounding boxes
x_maxs = []
x_mins = []
y_maxs = []
y_mins = []

for index, path in enumerate(layers_to_add):
    lyr = QgsVectorLayer(path, layer_names[index], 'ogr')
    if lyr.isValid():
        # Transform layer extents to project crs
        transformed_extent = QgsCoordinateTransform(lyr.crs(), project.crs(), project).transform(lyr.extent())
        x_maxs.append(transformed_extent.xMaximum())
        x_mins.append(transformed_extent.xMinimum())
        y_maxs.append(transformed_extent.yMaximum())
        y_mins.append(transformed_extent.yMinimum())
        project.addMapLayer(lyr)
        lyr.loadNamedStyle([pth for pth in style_paths if layer_names[index][3:] in pth][0])

# Calculate collective extent of vector layers in project and...
# ...construct a QgsRectangle from x and y extremes
extent = QgsRectangle(min(x_mins), min(y_mins), max(x_maxs), max(y_maxs))
# Slightly increase extent outside of project vector layers
extent.grow(1000)#extent crs map units (project crs which is meters)
project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))

# Create layout
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName('Test Layout')
project.layoutManager().addLayout(layout)
map = QgsLayoutItemMap(layout)
map.attemptMove(QgsLayoutPoint(5,5, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(200,150, QgsUnitTypes.LayoutMillimeters))
map.setFrameEnabled(True)
map.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
# Provide a meaningful extent to render
map.setExtent(extent)
layout.addLayoutItem(map)

legend = QgsLayoutItemLegend(layout)
legend.attemptMove(QgsLayoutPoint(210, 50, QgsUnitTypes.LayoutMillimeters))
legend.setFrameEnabled(True)
legend.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
legend.setFixedSize(QgsLayoutSize(50,40, QgsUnitTypes.LayoutMillimeters))
legend.refresh()
layout.addLayoutItem(legend)

project.write()

pdfPath = os.path.join(file_dir, 'Test Layout.pdf')
exporter = QgsLayoutExporter(layout)
exporter.exportToPdf(pdfPath, QgsLayoutExporter.PdfExportSettings())

qgs.exitQgis()