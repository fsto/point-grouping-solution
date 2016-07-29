import math

from pyhull.delaunay import DelaunayTri


def _distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def triangle_area(a, b, c):
    """
    Calculate the area of a triangle.
    """
    side_a = _distance(a, b)
    side_b = _distance(b, c)
    side_c = _distance(c, a)
    s = 0.5 * (side_a + side_b + side_c)
    return math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

def points_area(points):
    """
    Calcualte the area of a graph using Delaunay triangulation.
    """
    if len(points) < 3:
        # Area = 0 when we have < 3 points
        return 0
    elif len(points) == 3:
        return triangle_area(*points)
    else: 
        triangles_indexes = DelaunayTri(points).vertices
        triangles_points = [(points[a], points[b], points[c]) for a, b, c in triangles_indexes]
        area = sum([triangle_area(*triangle_points) for triangle_points in triangles_points])
        return area
