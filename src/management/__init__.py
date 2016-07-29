import argparse
import sys
import json

from routing.graph.point import Point
from routing.van_points.grouped_van_points import GroupedVanPoints
from routing.van_points.distributed_van_points import DistributedVanPoints


def _build_default_parser():
    parser = argparse.ArgumentParser(description="Give each MakeSpace van a group of lon / lat points to visit.")
    parser.add_argument("num_vans", type=int, help="number of vans")
    parser.add_argument("points_file", nargs='?', type=argparse.FileType("r"), default=sys.stdin,
        help='file with list of points on format [ {"lat": <float>, "lon": <float>, "id": <string>}, ... ] (default: sys.stdin)')
    parser.add_argument("--plot", "-p", nargs='?', type=bool, default=False, help="Plot groups")
    parser.add_argument("--filename", "-f", nargs='?', type=str, default="groups.json", help="Filename of output file")
    return parser


def _parse_args():
    parser = _build_default_parser()
    args = parser.parse_args()
    return {
        "num_vans": args.num_vans,
        "point_dicts": json.load(args.points_file),
        "plot": args.plot,
        "filename": args.filename
    }


def _execute_from_command_line(grouping_class):
    args = _parse_args()
    num_vans = args["num_vans"]
    plot = args["plot"]
    filename = args["filename"]
    points = [Point(**point_dict) for point_dict in args["point_dicts"]]
    route_plan = grouping_class(num_vans, points)
    if plot:
        route_plan.plot()
    if filename:
        route_plan.save(filename)


def execute_group_from_command_line():
    """
    Execute the group van points algorithm from command line.
    """
    _execute_from_command_line(GroupedVanPoints)


def execute_distribute_from_command_line():
    """
    Execute the distribute van points algorithm from command line.
    """
    _execute_from_command_line(DistributedVanPoints)
