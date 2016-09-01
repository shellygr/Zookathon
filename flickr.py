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
    lat = _flickr_to_degrees(str(exif[31][u'raw'][u'_content']))
    if exif[30][u'raw'][u'_content'] == u'South':
        lat = -lat
    lon = _flickr_to_degrees(str(exif[33][u'raw'][u'_content']))
    if exif[32][u'raw'][u'_content'] == u'South':
        lon = -lon
    return lat, lon