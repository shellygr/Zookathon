from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
import math

#############  https://gist.github.com/erans/983821 MIT licence ##########


# def get_exif_data(image):
#     """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
#     exif_data = {}
#     info = image._getexif()
#     if info:
#         for tag, value in info.items():
#             decoded = TAGS.get(tag, tag)
#             if decoded == "GPSInfo":
#                 gps_data = {}
#                 for t in value:
#                     sub_decoded = GPSTAGS.get(t, t)
#                     gps_data[sub_decoded] = value[t]
#
#                 exif_data[decoded] = gps_data
#             else:
#                 exif_data[decoded] = value
#
#     return exif_data
#
#
# def _get_if_exist(data, key):
#     if key in data:
#         return data[key]
#
#     return None
#
#
# def get_lat_lon(exif_data):
#     """Returns the latitude and longitude, if available,
#     from the provided exif_data (obtained through get_exif_data above)"""
#     lat = None
#     lon = None
#
#     if "GPSInfo" in exif_data:
#         gps_info = exif_data["GPSInfo"]
#
#         gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
#         gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
#         gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
#         gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
#
#         if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
#             lat = _convert_to_degrees(gps_latitude)
#             if gps_latitude_ref != "N":
#                 lat = 0 - lat
#
#             lon = _convert_to_degrees(gps_longitude)
#             if gps_longitude_ref != "E":
#                 lon = 0 - lon
#
#     return lat, lon

############# end eran MIT licence ##########

#import PIL,PIL.Image
#import PIL.ExifTags
#img = PIL.Image.open(r'C:\facebookHackathon2016\test3.jpg')
#exif_data = img._getexif()
#exif = {
#    PIL.ExifTags.TAGS[k]: v
#    for k, v in img._getexif().items()
#    if k in PIL.ExifTags.TAGS
#}
#print(exif)


def _convert_to_degrees(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def _convert_to_exif_format(dec_deg):
    """Helper function to convert GPS coordinates from decimal degrees to EXIF format"""
    degrees = math.floor(dec_deg)
    minutes = math.floor(60*(dec_deg - degrees))
    seconds = 3600*(dec_deg - degrees) - 60*minutes

    # A note about the return value: this is only one possible configuration that might be used in EXIF.
    # Another configuration might be, for example, ((degrees,1), (minutes,100), (0,1)),
    # for a representation that only cares about minutes up to two decimal places.
    return (degrees,1), (minutes,1), (seconds,1)


def read_gps_data(filename):
    """Receives a path to an image.
    Returns the latitude and longitude coordinates.
    For example: (32.1133, 34.8044) for an image from TAU campus.
    Returns None for a file with missing or wrong EXIF or GPS data."""
    im = Image.open(filename)
    if "exif" not in im.info:
        return None
    exif_dict = piexif.load(im.info["exif"])
    if "GPS" not in exif_dict:
        return None
    gps_data = exif_dict["GPS"]
    if not all(ind in gps_data for ind in [1,2,3,4]):
        return None
    lat_ref = exif_dict["GPS"][1]
    if lat_ref not in ('N','S'):
        return None
    lat = _convert_to_degrees(exif_dict["GPS"][2])
    if lat_ref == 'S':
        lat = -lat
    lon_ref = exif_dict["GPS"][3]
    if lon_ref not in ('E', 'W'):
        return None
    lon = _convert_to_degrees(exif_dict["GPS"][4])
    if lon_ref == 'W':
        lon = -lon
    return lat, lon


def write_gps_data(filename, lat, lon):
    """Receives a path to an image, latitude and longitude coordinates.
    Writes the input values on the image's exif data.
    If the file did not originally have any exif data, or had missing GPS data,
    the function creates EXIF and GPS entries of its own in a weird way,
    that is compatible with read_gps_data. (SILLY HACK)"""
    lat_ref = 'N'
    if lat < 0:
        lat_ref = 'S'
        lat = -lat
    lat_exif = _convert_to_exif_format(lat)
    lon_ref = 'E'
    if lon < 0:
        lon_ref = 'W'
        lon = -lon
    lon_exif = _convert_to_exif_format(lat)
    im = Image.open(filename)
    exif_dict = dict()
    if "exif" in im.info:
        exif_dict = piexif.load(im.info["exif"])
    if "GPS" not in exif_dict:
        exif_dict["GPS"] = dict()
    exif_dict["GPS"][1] = lat_ref
    exif_dict["GPS"][2] = lat_exif
    exif_dict["GPS"][3] = lon_ref
    exif_dict["GPS"][4] = lon_exif
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)



# # TEST:
# test_coordinates = read_gps_data("original_thumb.jpg")
# write_gps_data("thumb.jpg", -test_coordinates[0], -test_coordinates[1])
# print test_coordinates
# print read_gps_data("thumb.jpg")