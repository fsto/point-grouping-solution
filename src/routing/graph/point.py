class Point(object):
    """Geographic node."""

    def __init__(self, id, lat, lon):
        self.id = id
        self.lon = lon
        self.lat = lat

    def __repr__(self):
        return "(%s, %s)" % (
            # self.id,
            self.lat,
            self.lon,
            # super(Point, self).__repr__()
        )

    def __iter__(self):
        yield 'lat', self.lat,
        yield 'lon', self.lon,
        yield 'id', self.id