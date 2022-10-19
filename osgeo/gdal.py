


from osgeo import gdal

# from osgeo import osr
# proj = osr.SpatialReference()
# proj.ImportFromEPSG(3857)
# output.SetProjection(proj)

def print_tif_info(tifPath):
# def lambda_handler(event, context):
#     print(event)
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     s3Key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
#     print('bucket= ', bucket)
#     print('key=', s3Key)
#     print('event=', event)
    
    gTif = gdal.Open(tifPath)
    # gTif = gdal.Open("/vsis3/{0}/{1}".format(bucket, s3Key))
    print(gTif.GetMetadata())

def translate_jpeg(inPath):

    ds = gdal.Open(inPath)
    ds = gdal.Translate('C:/job/igo/API/output.jpeg', ds)
    # ds = gdal.Translate('output.jpeg', ds, projWin = [-75.3, 5.5, -73.5, 3.7])
    ds = None

def translate_pdf(inPath):

    ds = gdal.Open(inPath)
    ds = gdal.Translate('C:/job/PDF/doc/gdalCallWMS/output.pdf', ds)
    # ds = gdal.Translate('output.jpeg', ds, projWin = [-75.3, 5.5, -73.5, 3.7])
    ds = None


    
WestBoundCoord = -8765186.907517731
NorthBoundCoord = 7046882.511666969
EastBoundCoord = -7317163.843683353
SouthBoundCoord = 5559723.68935058

EPSG = "-a_srs EPSG:3857" #WGS84
a_ullr = "-a_ullr -8002058.621, 5969600.050, -8000178.748, 5967433.538"
# translateOptionText = EPSG+" -a_ullr " + str(WestBoundCoord) + " " + str(NorthBoundCoord) + " " + str(EastBoundCoord) + " " + str(SouthBoundCoord)

translateOptionText = EPSG+" "+ a_ullr

translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))


outputFile = 'D:\\python\\gitProjet\\donneeTests\\osgeo\\output.pdf'
# outputFile = 'C:/job/PDF/doc/gdalCallWMS/output.pdf'
call2 = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=sh_reg_eco&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG:3857&STYLES=&WIDTH=1184&HEIGHT=1216&BBOX=-8765186.907517731%2C5559723.68935058%2C-7317163.843683353%2C7046882.511666969"
callIntervTif = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/tiff&TRANSPARENT=true&LAYERS=ca_interv_fores_close_scale&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG:3857&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"

inFile = "D:\\python\\gitProjet\\donneeTests\\osgeo\\ok_mffpecofor.tif"
# inFile = "D:\\python\\gitProjet\\donneeTests\\osgeo\\mffpecofor.pdf"

# marche pas avec la call direct
# gdal.Translate(outputFile, callIntervTif, options=translateoptions)
gdal.Translate(outputFile, inFile, options=translateoptions)
# gdal.Translate(outputFile, call2, options=translateoptions)


# pathTif = "C:/job/igo/API/ex.tif"
# pathTif = "C:/job/PDF/doc/gdalCallWMS/mffpecofor.tif"
# callWms = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=1071a701&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=pee_index_pdf&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG:3857&STYLES=&WIDTH=1067&HEIGHT=859&BBOX=-8027172.305944708%2C5714193.0143339215%2C-8016977.517297172%2C5722400.440246043"
# call2 = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=sh_reg_eco&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG:3857&STYLES=&WIDTH=1184&HEIGHT=1216&BBOX=-8765186.907517731%2C5559723.68935058%2C-7317163.843683353%2C7046882.511666969"

# print_tif_info(pathTif)
# translate_jpeg(pathTif)
# translate_pdf(pathTif)
# translate_pdf(call2)
