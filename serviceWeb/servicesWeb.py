

from owslib.wms import WebMapService


wms = WebMapService('https://geoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?', version='1.1.1')
wmsGiin = WebMapService('https://servicesvectoriels.atlas.gouv.qc.ca/IDS_INVENTAIRE_ECOFORESTIER_WMS/service.svc/get?', version='1.1.1')
# wms = WebMapService('http://wms.jpl.nasa.gov/wms.cgi', version='1.1.1')
type = wms.identification.type
# 'OGC:WMS'
titre = wms.identification.title

# wms['sh_zone_veg'].title

# img = wms.getOperationByName('GetFeatureInfo')
# img = wms.getfeatureinfo()

# GetFeatureInfo (text/html)

# OK
# response = wms.getfeatureinfo(
#     layers=['sh_zone_veg'],
#     srs='EPSG:3857',
#     bbox=(-8485786.628423,5603924.852643,-7504946.681604,7546036.867042),
#     size=(500,500),
#     format='image/jpeg',
#     query_layers=['sh_zone_veg'],
#     info_format="text/html",
#     xy=(250,250))

response = wms.getfeatureinfo(
    layers=['sh_zone_veg'],
    srs='EPSG:3857',
    bbox=(-8062540.000868,6140794.422066,-8059506.406308,6144587.609594),
    # bbox=(-8485786.628423,5603924.852643,-7504946.681604,7546036.867042),
    size=(500,500),
    format='text',
    query_layers=['sh_zone_veg'],
    info_format="text",
    xy=(250,250))

responseGiin = wmsGiin.getfeatureinfo(
    layers=['imagerie_inventaire_ecoforestier'],
    srs='EPSG:3857',
    bbox=(-8062540.000868,6140794.422066,-8059506.406308,6144587.609594),
    # bbox=(-8485786.628423,5603924.852643,-7504946.681604,7546036.867042),
    size=(500,500),
    format='text/html"',
    query_layers=['imagerie_inventaire_ecoforestier'],
    info_format="text/html",
    xy=(250,250))


print('pis')