from random import uniform

from ..routing.graph.point import Point


def generate_random_points(num):
    return [Point("id-" + str(i), uniform(-90, 90), uniform(-90, 90)) for i in range(num)]

def get_aggregated_convex_hull_area(van_points):
    return sum([van_points._get_van_area(van) for van in van_points._vans])
