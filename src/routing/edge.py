from math import radians, cos, sin, asin, sqrt


class Edge(object):
    """
    Edge base class.
    """

    @classmethod
    def connect_edge_pairs(cls, edge_pairs):
        """
        Return a new list with edges (pairs of point_a, point_b) ordered as they're connected in the graph.

        Eg:
        > connect_edge_pairs([[1,2], [3,1], [2,3]])
        < [[1,2], [2,3], [3,1]]
        """
        connected_edges = [edge_pairs[0]]
        for i in range(len(edge_pairs) - 1):
            current_edge = connected_edges[i]
            next_edge = [edge for edge in edge_pairs if current_edge[1] == edge[0]][0]
            connected_edges.append(next_edge)
        return connected_edges


class Distance(Edge):
    """
    Geographic edge.
    """

    def __init__(self, point_a, point_b, haversine=None):
        """
        Initiate distance and calculate its haversine (great circle distance).
        """
        self.point_a = point_a
        self.point_b = point_b
        self.haversine = haversine or self.haversine(
            point_a.lon,
            point_a.lat,
            point_b.lon,
            point_b.lat
        )

    @classmethod
    def haversine(cls, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth in kilometers (specified in decimal degrees)
        """
        # Radius of earth in kilometers.
        r = 6371
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return c * r


class DistanceTable(object):
    """
    Distance table for fast lookups of distances between geographic two points.

    Structured on the following format
    {
        "a": {
            "b": distance_a_b,
            "c": distance_a_c,
            ...
        },
        "b": {
            "a": distance_b_a,
            "c": distance_b_c
        },
        ...
    }
    """

    def __init__(self):
        """
        Initiate table
        """
        self.table = {}

    @classmethod
    def generate_from_points(cls, points):
        """
        Create a DistanceTable instance with distances between all points.
        """
        dt = DistanceTable()
        for i, point_a in enumerate(points):
            dt.table.setdefault(point_a, {})
            for point_b in points[i + 1:]:
                dt.table.setdefault(point_b, {})
                distance_a_b = Distance(point_a, point_b)
                distance_b_a = Distance(point_b, point_a, distance_a_b.haversine)
                dt.table[point_a][point_b] = distance_a_b
                dt.table[point_b][point_a] = distance_b_a
        return dt

    def get_nearest_distances(self, origin_point):
        """
        Get a list of Distances connected to the given Point, ordered by distance.
        """
        return sorted(self.table[origin_point].values(), key=lambda d: d.haversine)

    def get_nearest_distance(self, origin_point, exclude_points=None):
        """
        Get the nearest Distance to a given Point. Points in `exclude_points` are excluded.
        """
        exclude_points = exclude_points or []
        return [d for d in self.get_nearest_distances(origin_point) if d.point_b not in exclude_points][0]

    def get_nearest_point(self, origin_point, exclude_points=None):
        """
        The the nearest Point to a given Point. Points in `exclude_points` are excluded.
        """
        return self.get_nearest_distance(origin_point, exclude_points=exclude_points).point_b