from .grouped_van_points import GroupedVanPoints


class DistributedVanPoints(GroupedVanPoints):
    """
    Grouped van points algorithm which priorites vans getting an even number of points over convex hull areas being small.
    """

    name = "Distributed Van Points"

    def set_van_points(self):
        """
        Algorithms which assigns the next van the nearest (to clique's origin) non assigned point.
        """
        self._register_initial_van_points()
        i = 0
        while len(self._visited_points) < len(self._points):
            van = self._vans[i % len(self._vans)]
            current_point = self._get_current_van_point(van)
            next_point = self._get_nearest_not_visisted_point(current_point)
            self._register_van_at_point(van, next_point)
            i += 1
