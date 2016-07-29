## MakeSpace grouping & distribution challenge

### Prerequisites

* Python 2.7

### Installation

* If you use virtualenv
  * Create a new virtualenv
  * Activate the virtualenv
* Install python libraries with `pip install -r requirements.txt`
  * If you'd like to plot your results, run `pip install -r requirements_for_plot.txt`

### Run

#### Grouping algorithm

`python src/group.py <number_of_vans> <relative_path_to_file_with_points or stdin>`

#### Distribution algorithm

`python src/distribute.py <number_of_vans> <relative_path_to_file_with_points or stdin>`

#### Plot

To plot your result use the flag `--plot`

#### Set output filename

Use flag `--filename=<filename>`

#### Help

For a full description of the commands use the `--help` flag

### Run tests

To run the very small test suite, run `python -m src.tests.test_grouping`

### Algorithms

#### Challenge

We want to give `n` vans one group of points each. Each point is a (latitude, longitude) pair which a van should visit. A few things we want to accomplish are:

* The smallest total effort for our vans
* Spread the effort somewhat fairly between the vans

The challenge is pretty much TPS on steroids and since we don't know the number of vans or points, we'll have to assume that trying each possible solution is not an option.

##### Warehouse

During this challenge, we don't know where the warehouse is or where each van starts from, so we'll ignore the distance to the first point.

##### Roads / distances / time between points

We don't know about the roads between points, so we'll assume the travel time between two points maps exactly to the distance between the two points. We'll also assume that all points are connected to all other points, forming a complete graph.

#### Grouping algorithm

To limit the "total effort for our vans this algorithm focuses on creating a [clique](https://en.wikipedia.org/wiki/Clique_(graph_theory)) of points for each van where the sum of all [convex hulls](https://en.wikipedia.org/wiki/Clique_(graph_theory)) areas is as small as possible. Since we can't try every convex hull area combination, we'll split the problem into two parts:

* finding initial positions for the vans
* assigning the rest of the points to the vans

##### Pseudo code

1. Build matrix of distances between all points
2. initial_points = distribute vans roughly evenly along the convex hull
3. i = 0
4. while len(vans) > len(initial_points):
    a. next_point = initial_points[i]
    b. nearest_point = next_point's nearest point which is not in initial_points
    c. initial_points.append(nearest_point)
    d. i++        
5. while len(visited_points) < number of points:
    a. van = van with the smallest convex hull area
    b. next_point = get_nearest_not_visited_point(van.initial_point)
    c. register van at next_point

##### Time complexity

Time complexity for the steps above

1. O(n^2)
2. O(n^2)
3. O(1)
4. O(n)
    a. O(1)
    b. O(n)
    c. O(n)
    d. O(1)
5. O(n)
    a. O(n^2)
    b. O(n)
    c. O(1)

Which results in O(n^2) for our grouping algorithm

#### Distribution algorithm

Our goal here is very similar to the grouping algorithm with the difference that we want to distribute the points evenly on the vans. Ie. 25 points with 4 vans would result in 6 vans with 4 points and 1 van with 5 points.

##### Pseudo code

1. Build matrix of distances between all points
2. initial_points = distribute vans roughly evenly along the convex hull
3. i = 0
4. while len(vans) > len(initial_points):
    a. next_point = initial_points[i]
    b. nearest_point = next_point's nearest point which is not in initial_points
    c. initial_points.append(nearest_point)
    d. i++
5. counter = 0
6. while len(visited_points) < number of points:
    a. van = vans[counter % (number of vans)]
    b. next_point = get_nearest_not_visited_point(van.initial_point)
    c. register van at next_point
    d. counter++

##### Time complexity

1. O(n^2)
2. O(n^2)
3. O(1)
4. O(n)
    a. O(1)
    b. O(n)
    c. O(n)
    d. O(1)
5. O(1)
6. O(n)
    a. O(1)
    b. O(n)
    c. O(1)

Which results in O(n^2) for our distribution algorithm

#### Enhancements

##### Overlapping cliques

The algorithms have an obvious weakness which occurs when there are unassigned points and the current van (V1) has to "stop over" other points to get to the nearest point. This happens especially often for the distribution algorithm.

I would modify the grouping algorithm by assigning the point (P1) to another van (Vx) if and only if Vx's convex hull area grows less than van V1 convex hull area would grow.

I would modify the distribution algorithm by extending the grouping algorithm modification. I would check if Vx has any point to "give" N1 where the convex hull area growths combined are smaller than than N1's area would grow with point P1.

##### Convex hull

To give each van an initial position I've chosen to distribute the vans (rougly) evenly on the convex hull of our points. `scipy.spatial.ConvexHull` makes a good job here with spatial convex hulls and convex hull areas, but to avoid heavy dependencies for anyone who'll run this code, I've chosen to use `pyhull` which currently only supports 2D points. I consider this good enough for a non production environment such as this. Hence an obvious enhancement a library that supports spatial hulls.

##### Testing

The current level of test coverage is very low. To verify the expected functionality a much more rigid testing is needed.

##### Other enhancements

There are a bunch of smaller obvious optimizations which could be solved with caching, memoization, etc. But since I'm sure the core of the algorithms have fundamental improvement possibilities, I've prioritized readablitiy over smaller optimizations to open up for discussions and bigger modifications.
