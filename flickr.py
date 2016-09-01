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