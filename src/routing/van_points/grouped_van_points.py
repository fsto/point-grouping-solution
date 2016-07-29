from .van_points import VanPoints
from ..helpers import points_area


class GroupedVanPoints(VanPoints):
    """
    Grouped van points algorithm which priorites convex hull areas being small over vans getting an even number of points.
    """

    name = "Grouped Van Points"

    def _get_van_area(self, van):
        # For enhancement capabilities, see README.md
        
        van_points = [(point.lat, point.lon) for point in self.van_points[van]]
        return points_area(van_points)

    def _get_initial_van_points(self):
        """
        Get initial points by the following algorithm:
        1. initial_points = distribute vans roughly evenly along the convex hull
        2. i = 0
        3. While len(vans) > len(initial_points):
            a. next_point = initial_points[i]
            b. nearest_point = next_point's nearest point which is not in initial_points
            c. initial_points.append(nearest_point)
            d. i++
        4. Return initial_points
        """
        vans = self._vans
        points = self._points
        if len(vans) > len(points):
            raise ValueError("There are more vans than points")

        initial_points = self.distirbute_vans_on_convex_hull(vans, self._map.convex_hull)

        i = 0
        while len(vans) > len(initial_points):
            next_point = initial_points[i]
            initial_points.append(
                self._dt.get_nearest_point(next_point, exclude_points=initial_points)
            )
            i += 1
        return initial_points

    def _register_initial_van_points(self):
        _initial_vans_points = self._get_initial_van_points()
        for van, initial_point in zip(self._vans, _initial_vans_points):
            self._register_van_at_point(van, initial_point)

    def set_van_points(self):
        """
        Algorithm which assigns extends the smallest convex hull area.

        Pseudo code:

        1. while len(visited_points) < number of points:
            a. van = van with the smallest convex hull area
            b. next_point = get_nearest_not_visited_point(van.current_point)
            c. register van at current_point
        """
        self._register_initial_van_points()
        while len(self._visited_points) < len(self._points):
            van = sorted(self._vans, key=lambda van: self._get_van_area(van))[0]
            current_point = self._get_current_van_point(van)
            next_point = self._get_nearest_not_visisted_point(current_point)
            self._register_van_at_point(van, next_point)
