from pyhull.convex_hull import ConvexHull

from .edge import Edge


class Map(object):
    """
    Map class / a graph.
    """

    def __init__(self, points):
        """
        Set points and calculate convex hull.
        """
        self._points = points
        self.convex_hull = self.get_convex_hull()

    def _get_point_by_lat_lon(self, lat, lon):
        """
        Get the first Point that has the given `lat` and `lon`.
        Optimization: use and index instead of a O(n) search.
        """
        for point in self._points:
            if (point.lat, point.lon) == (lat, lon):
                return point
        return None

    def get_convex_hull(self):
        """
        Get instance's convex hull Ponits.
        """
        # Extract lat lon pairs from our points
        lat_lons = [(point.lat, point.lon) for point in self._points]
        hull_edges = ConvexHull(lat_lons).vertices
        sorted_hull_edges = Edge.connect_edge_pairs(hull_edges)
        hull_points = [self._points[edge[0]] for edge in sorted_hull_edges]
        # Convert our lat lon pair convex hull to a Point convex hull
        # point_hull = [self._get_point_by_lat_lon(*lat_lon_pair) for lat_lon_pair in lat_lon_hull.points]
        return hull_points

    def get_convex_hull_by_resolution(cls, resolution):
        """
        Get `resolution` number of points of the convex hull.
        """
        if not 1 <= resolution <= len(self._points):
            raise ValueError("`resolution` must be 1 <= resolution <= len(points)")
