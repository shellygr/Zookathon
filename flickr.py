def _get_gps_index(exif_list):
    for i in xrange(0, len(exif_list)):
        if u'tag' in exif_list[i] and exif_list[i][u'tag'] == u'GPSLatitude':
            return i - 1
    return None

def _flickr_to_degrees(f_coor):
    coor = f_coor
    coor = coor.replace(" deg", " ")
    coor = coor.replace("' ", " ")
    coor = coor.replace("\"", " ")
    split_coor = coor.split()
    d = float(split_coor[0])
    m = float(split_coor[1])
    s = float(split_coor[2])
    return d + (m / 60.0) + (s / 3600.0)


def get_gps_data_from_exif(output):
    exif = output["photo"]["exif"]
    gps_index = _get_gps_index(exif)
    if not gps_index:
        return None
    lat = _flickr_to_degrees(str(exif[gps_index + 1][u'raw'][u'_content']))
    if exif[gps_index][u'raw'][u'_content'] == u'South':
        lat = -lat
    lon = _flickr_to_degrees(str(exif[gps_index + 3][u'raw'][u'_content']))
    if exif[gps_index + 2][u'raw'][u'_content'] == u'South':
        lon = -lon
    return lat, lon

import flickrapi
import flickrapi.shorturl

api_key = u'bcf1f89686c3135e7b61b884acbb060b'
api_secret = u'0d265afcea544a3b'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
#
# photos = flickr.photos.search(privacy_filter=1, has_geo=1, per_page='3', lat=32.113332, lon=34.803250)
#
# print photos

output_dict = {u'photos': {u'total': u'75784', u'photo': [{u'isfamily': 0, u'title': u'Hotel Galileo', u'farm': 9, u'ispublic': 1, u'server': u'8668', u'isfriend': 0, u'secret': u'4071d0bf09', u'owner': u'59243894@N00', u'id': u'28760597723'}, {u'isfamily': 0, u'title': u'\u05d0\u05e0\u05e8\u05d2\u05d9\u05d5\u05ea \u05d8\u05d5\u05d1\u05d5\u05ea \u05e2\u05dd \u05d8\u05dc\u05d9\u05d4 \u05d0\u05dc\u05d3\u05d5\u05e8 \u05d0\u05e9\u05e4\u05d9\u05ea  \u05d4\u05d0\u05df.\u05d0\u05dc.\u05e4\u05d9 #nlp #taliaeldor #yossibehar', u'farm': 9, u'ispublic': 1, u'server': u'8273', u'isfriend': 0, u'secret': u'95081f7c61', u'owner': u'43475674@N04', u'id': u'29270728832'}, {u'isfamily': 0, u'title': u'Since this picture was taken my grandson became whiter and I am totally black. \u0422\u0430\u043a \u043a\u0430\u043a \u044d\u0442\u0430 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f \u0431\u044b\u043b\u0430 \u0441\u0434\u0435\u043b\u0430\u043d\u0430 \u043c\u043e\u0439 \u0432\u043d\u0443\u043a \u0441\u0442\u0430\u043b \u0431\u0435\u043b\u044b\u043c, \u0438 \u044f \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u0447\u0435\u0440\u043d\u044b\u043c.', u'farm': 9, u'ispublic': 1, u'server': u'8553', u'isfriend': 0, u'secret': u'3c196da1aa', u'owner': u'104303998@N06', u'id': u'29263684952'}], u'perpage': 3, u'page': 1, u'pages': 25262}, u'stat': u'ok'}


# for key in output_dict:
#     print key

# for key in output_dict["photos"]["photo"]:
#     print key

# for key in output_dict["photos"].keys():
#     print key
#     print output_dict["photos"][key]
#
# photo_dict = output_dict["photos"]["photo"]
#
# for i in xrange(0, len(photo_dict)):
#     print photo_dict[i]
#
import urllib
from dbconnection import *
from classify_image import *
from wikipediaApi import *
from random import *

def getPhotos():
    output = flickr.photos.search(privacy_filter=1, has_geo=1, per_page='5', group_id=u'49502993915@N01',extras= 'url_z')
    i=0
    for row in output[u'photos'][u'photo']:
        print row
        exif = flickr.photos.getExif(photo_id = row['id'])
        gpsCoord = get_gps_data_from_exif(exif)
        if gpsCoord != None:
            lat,lon = gpsCoord
        else:
            continue
        flickrapi.shorturl.url(row['id'])
        urllib.urlretrieve(row['url_z'], r"flickr/flickrAuto{0}.jpg".format(i))
        relativePath = "flickrAuto{0}.jpg".format(i)
        lables = classify('flickr/'+relativePath)
        date = '%d Aug 2016, %d:%d' % (randint(1, 29) + 1, randint(1, 12) + 8, randint(1, 50) + 1)
        insertLine(relativePath,lat,lon,lables,date,getEndangeredStatus(lables))
        i+=1


getPhotos()
