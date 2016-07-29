import unittest
import sys
import math

from .helpers import generate_random_points, get_aggregated_convex_hull_area
from ..routing.van_points.grouped_van_points import GroupedVanPoints
from ..routing.van_points.distributed_van_points import DistributedVanPoints


class TestBase(unittest.TestCase):
    DEFAULT_NUM_POINTS = 50

    def setUp(self):
        self.points = generate_random_points(self.DEFAULT_NUM_POINTS)

    def tearDown(self):
        self.points = None


class GroupingTest(TestBase):

    def test_num_groups(self):
        # Assert we have exactly one point group per van
        for num_vans in range(1, 30):
            van_points = GroupedVanPoints(num_vans, self.points)
            num_groups = len(van_points.van_points)
            self.assertEqual(num_groups, num_vans)

    def test_group_sizes(self):
        # Assert point groups consist of at least one point
        for num_vans in range(1, 30):
            van_points = GroupedVanPoints(num_vans, self.points)
            for point_group in van_points.van_points.itervalues():
                self.assertGreaterEqual(len(point_group), 1)
                self.assertLessEqual(len(point_group), self.DEFAULT_NUM_POINTS - num_vans + 1)

    def test_total_number_of_points_in_groups(self):
        # Assert total number of points in point groups is correct
        for num_vans in range(1, 30):
            van_points = GroupedVanPoints(num_vans, self.points)
            found_points = sum([len(point_group) for point_group in van_points.van_points.itervalues()])
            self.assertEqual(found_points, len(self.points))


class DistributionTest(TestBase):

    def test_group_size(self):
        points = generate_random_points(self.DEFAULT_NUM_POINTS)
        for num_vans in range(1, 11):
            min_num_vans = math.floor(float(len(points)) / num_vans)
            max_num_vans = math.ceil(float(len(points)) / num_vans)
            distributed_van_points = DistributedVanPoints(num_vans, points)

            # Assert points are evenly distributed
            for van_points in distributed_van_points.van_points.itervalues():
                self.assertIn(len(van_points), [min_num_vans, max_num_vans])


if __name__ == '__main__':
    unittest.main()