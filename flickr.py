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
# print flickrapi.shorturl.url(u'28760597723')
print flickr.photos.getExif(photo_id = u'28760597723')