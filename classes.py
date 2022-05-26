import random as rand

from const import *
import utils


class Point:
    ''' 
    Represents the center point of a circle to be generated on the Ishihara Plate.
    '''

    def __init__(self, x, y, canvas_pxls):
        self._x = x
        self._y = y
        self._loc = WIDTH*self._y + self._x
        self._in_fig = (canvas_pxls[self.get_loc()] == BLACK_RGB)

    def get_loc(self):
        return self._loc

    def _set_loc(self):
        self._loc = WIDTH*self._y + self._x

    def get_coord(self):
        return (self._x, self._y)

    def set_coord(self, new_coord):
        self._x, self._y = new_coord
        self._set_loc()

    def in_fig(self):
        return self._in_fig

    def will_overlap_point(self, p2):
        p_coord = self.get_coord()
        p2_coord = p2.get_coord()
        return utils.distance_squared(p_coord, p2_coord) <= (2 * MIN_CIRCLE_RADIUS)**2

    def will_overlap_wall(self):
        px, py = self.get_coord()

        if px <= MIN_CIRCLE_RADIUS or WIDTH - px <= MIN_CIRCLE_RADIUS:
            return True

        if py <= MIN_CIRCLE_RADIUS or HEIGHT - py <= MIN_CIRCLE_RADIUS:
            return True

        return False

    def will_overlap_fig_boundary(self, canvas_pxls):
        return utils.opposite_colr_point_in_circle(self, MIN_CIRCLE_RADIUS, canvas_pxls)


class Node():
    ''' Node of the CirclesAdjacencyGraph class.

    Attributes:
        center: Point
        radius: int := Initially set to MIN_CIRCLE_RADIUS.
        max_radius: int := Initially set to MIN_CIRCLE_RADIUS.
        adj_nodes: list[int] := list of index (in CirclesAdjacencyGraph) of nodes adjacent to this node.
    '''

    def __init__(self, center):
        self.center = center
        self.radius = MIN_CIRCLE_RADIUS
        self.max_radius = MIN_CIRCLE_RADIUS
        self.adj_nodes = []

    def build_adj_nodes(self, indx, node_list, canvas_pxls):
        ''' 
        Get all adjacent nodes of this node and adjust max_radius 
        accordingly.

        Parameters:
            indx: int := Index of this node in the node_list.
            node_list: list[Node]
            canvas_pxls: list[color]

        Return Value:
            None
        '''
        max_radius = max(self.max_radius, self._nearest_wall_distance())

        adj_nodes = []
        for i, node in enumerate(node_list):
            if i != indx:
                distance = self._other_node_distance(node)
                if distance < max_radius:
                    max_radius = distance
                    adj_nodes = [i]
                elif distance == max_radius:
                    adj_nodes.append(i)

        self.max_radius = max_radius

        new_max_radius = self._nearest_fig_boundary_distance(canvas_pxls)
        if new_max_radius < self.max_radius:
            self.max_radius = new_max_radius
            adj_nodes = []

        for index in adj_nodes:
            if index not in self.adj_nodes:
                self.adj_nodes.append(index)
                if indx not in node_list[index].adj_nodes:
                    node_list[index].adj_nodes.append(indx)

    def _nearest_wall_distance(self):
        cx, cy = self.center.get_coord()

        nearest_wall_x = cx if cx < WIDTH - cx else WIDTH - cx
        nearest_wall_y = cy if cy < HEIGHT - cy else HEIGHT - cy
        return min([nearest_wall_x, nearest_wall_y])

    def _other_node_distance(self, n2):
        c1 = self.center.get_coord()
        c2 = n2.center.get_coord()
        return utils.distance(c1, c2) - MIN_CIRCLE_RADIUS

    def _nearest_fig_boundary_distance(self, canvas_pxls):
        nearest_dist = self.max_radius
        c = self.center
        curr_max_radius = self.max_radius
        opp_colr_points = utils.get_opposite_colr_points_in_circle(
            c, curr_max_radius, canvas_pxls)

        for p2_loc in opp_colr_points:
            p2x, p2y = utils.loc_to_coord(p2_loc)

            distance = utils.distance(c.get_coord(), (p2x, p2y))
            nearest_dist = min(nearest_dist, distance)

        return nearest_dist


class CirclesAdjacencyGraph:
    ''' 
    A graph with nodes representing the circles of the Ishihara Plate. Two nodes are adjacent with
    each other when at least one of them has their max_radius bounded by the other node.

    Attributes:
        nodes: list[Node]
    '''

    def __init__(self, center_points, canvas_pxls):
        self.nodes = self._get_nodes(center_points)
        for i in range(len(self.nodes)):
            self.nodes[i].build_adj_nodes(i, self.nodes, canvas_pxls)

    def visualize(self, color_scheme):
        noStroke()
        r = MIN_CIRCLE_RADIUS
        for node in self.nodes:
            fill(rand.choice(color_scheme))
            cx, cy = node.center.get_coord()
            ellipse(cx, cy, 2*r, 2*r)

        for node in self.nodes:
            colr = color(rand.uniform(0, 255), rand.uniform(
                0, 255), rand.uniform(0, 255))
            stroke(colr)
            fill(colr)
            cx, cy = node.center.get_coord()
            for indx in node.adj_nodes:
                node2 = self.nodes[indx]
                cx2, cy2 = node2.center.get_coord()
                line(cx, cy, cx2, cy2)
                ellipse(cx, cy, r, r)

    def _get_nodes(self, center_points):
        nodes = []
        for p in center_points:
            nodes.append(Node(p))

        return nodes
