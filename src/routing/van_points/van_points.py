import json

from ..van import Van
from ..graph.map import Map
from ..graph.edge import DistanceTable


class VanPoints(object):
    """
    Base class for van point algorithms.
    """

    name = "Route plan"

    def __init__(self, num_vans, points):
        """
        Constructor runs `set_van_points` which must be implmented by sub class.
        """
        self._points = points
        self._map = Map(points)
        # Generate distance table
        self._dt = DistanceTable.generate_from_points(points)
        # Give vans initial positions
        # Initiate van points by mapping each van to an empty list
        # Structure:
        # {
        #     <Van>: []   # point added in `set_van_points()`
        # }
        # Create vans
        self._vans = [Van("Van " + str(i)) for i in xrange(num_vans)]
        self.van_points = dict(zip(self._vans, [[] for i in range(len(self._vans))]))
        self.set_van_points()

    def distirbute_vans_on_convex_hull(self, vans, convex_hull):
        """
        Place vans evenly on convex hull.
        """
        num_vans_on_convex_hull = min(len(vans), len(convex_hull))
        step_size = int(round(float(
            len(convex_hull)) / num_vans_on_convex_hull
        ))
        distributed_points = [point_index for i, point_index in enumerate(convex_hull) if not i % step_size]
        # Remove any points extra points
        distributed_points = distributed_points[:len(vans)]
        return distributed_points

    @property
    def _visited_points(self):
        return reduce(lambda a, b: a + b, self.van_points.itervalues())
    
    def _get_initial_van_point(self, van):
        return self.van_points[van][0]

    def _register_van_at_point(self, van, point):
        self.van_points[van].append(point)

    def _get_nearest_not_visisted_point(self, point):
        return self._dt.get_nearest_point(point, exclude_points=self._visited_points)

    def _list_van_points_as_dicts(self):
        return [[dict(point) for point in points] for points in self.van_points.itervalues()]

    def save(self, filename="points.json"):
        """
        Save van points as json to file.
        """
        with open(filename, 'wb') as f:
            json.dump(self._list_van_points_as_dicts(), f, indent=2)

    def plot(self):
        """
        Plot van points on a local web page. The required dependencies can be installed by `pip install -r requirements_inc_plot.txt`
        """
        import numpy as np
        import plotly
        from plotly.graph_objs import Scatter, Layout, Data

        vans_points_dicts = self._list_van_points_as_dicts()
        colors = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 280, len(vans_points_dicts))]
        traces = []
        for i, van_points in enumerate(vans_points_dicts):
            points = [(point['lat'], point['lon']) for point in van_points]
            x, y = zip(*points)
            marker = dict(
                color=colors[i],
                size=20
            )
            traces.append(
                Scatter(
                    x=x,
                    y=y,
                    mode='markers',
                    marker=marker,
                    name="Van " + str(i + 1)
                )
            )
        data = Data(traces)
        
        plotly.offline.plot({
            "data": data,
            "layout": Layout(title=self.name)
        })

    def set_van_points(self):
        """
        Algorithm which sets van points (must be sub classed).
        """
        raise NotImplementedError()

