import random as rand

from const import GBIPG_CONST
import const
import utils


class Point:
    ''' 
    Represents the center point of a circle to be generated on the Ishihara Plate.
    '''

    def __init__(self, x, y, canvas_pxls, ModelConst):
        self._x = x
        self._y = y
        self._ModelConst = ModelConst
        self._loc = self._ModelConst.WIDTH*self._y + self._x
        self._in_fig = (canvas_pxls[self.get_loc()] == const.BLACK_RGB)

    def get_loc(self):
        return self._loc

    def _set_loc(self):
        self._loc = self._ModelConst.WIDTH*self._y + self._x

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
        return utils.distance_squared(p_coord, p2_coord) <= (2 * self._ModelConst.MIN_CIRCLE_RADIUS)**2

    def will_overlap_wall(self):
        px, py = self.get_coord()

        if utils.distance_squared((px, py), (self._ModelConst.WIDTH/2, self._ModelConst.HEIGHT/2)) > self._ModelConst.WALL_RADIUS**2:
            return True

        return False

    def will_overlap_fig_boundary(self, canvas_pxls):
        return utils.opposite_colr_point_in_circle(self, self._ModelConst.MIN_CIRCLE_RADIUS, canvas_pxls, self._ModelConst)

    def will_overlap_something(self, r, canvas_pxls):
        return utils.other_colr_point_in_circle(self, r, canvas_pxls, self._ModelConst)


class Node():
    ''' Node of the CirclesAdjacencyGraph class.

    Attributes:
        center: Point
        radius: int := Initially set to MIN_CIRCLE_RADIUS.
        max_radius: int := Initially set to MIN_CIRCLE_RADIUS.
        adj_nodes: list[int] := list of index (in CirclesAdjacencyGraph) of nodes adjacent to this node.
    '''

    def __init__(self, center, ModelConst):
        self.center = center
        self.radius = GBIPG_CONST.MIN_CIRCLE_RADIUS
        self.max_radius = GBIPG_CONST.MIN_CIRCLE_RADIUS
        self.adj_nodes = []
        self._ModelConst = ModelConst

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

        nearest_wall_x = cx if cx < GBIPG_CONST.WIDTH - cx else GBIPG_CONST.WIDTH - cx
        nearest_wall_y = cy if cy < GBIPG_CONST.HEIGHT - cy else GBIPG_CONST.HEIGHT - cy
        return min([nearest_wall_x, nearest_wall_y])

    def _other_node_distance(self, n2):
        c1 = self.center.get_coord()
        c2 = n2.center.get_coord()
        return utils.distance(c1, c2) - GBIPG_CONST.MIN_CIRCLE_RADIUS

    def _nearest_fig_boundary_distance(self, canvas_pxls):
        nearest_dist = self.max_radius
        c = self.center
        curr_max_radius = self.max_radius
        opp_colr_points = utils.get_opposite_colr_points_in_circle(
            c, curr_max_radius, canvas_pxls, self._ModelConst)

        for p2_loc in opp_colr_points:
            p2x, p2y = utils.loc_to_coord(p2_loc, self._ModelConst)

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

    def __init__(self, center_points, canvas_pxls, ModelConst, save_frame):
        self.nodes = self._get_nodes(center_points, ModelConst)
        for i in range(len(self.nodes)):
            self.nodes[i].build_adj_nodes(i, self.nodes, canvas_pxls)

        if ModelConst == GBIPG_CONST and GBIPG_CONST.SAVE_STATES:
            noStroke()
            r = GBIPG_CONST.MIN_CIRCLE_RADIUS
            fig_colr = rand.choice(GBIPG_CONST.FIG_COLOR_SCHEME)
            bg_colr = rand.choice(GBIPG_CONST.BG_COLOR_SCHEME)
            for node in self.nodes:
                fill(fig_colr if node.center.in_fig() else bg_colr)
                cx, cy = node.center.get_coord()
                ellipse(cx, cy, 2*r, 2*r)

            for node in self.nodes:
                stroke(bg_colr if node.center.in_fig() else fig_colr)
                fill(bg_colr if node.center.in_fig() else fig_colr)
                cx, cy = node.center.get_coord()
                for indx in node.adj_nodes:
                    node2 = self.nodes[indx]
                    cx2, cy2 = node2.center.get_coord()
                    line(cx, cy, cx2, cy2)
                    ellipse(cx, cy, r, r)

            if save_frame:
                img_name = GBIPG_CONST.FILE_NAME.rstrip(".png") + "-step2.png"
                saveFrame(img_name)
                background(const.WHITE_RGB)

    def _get_nodes(self, center_points, ModelConst):
        nodes = []
        for p in center_points:
            nodes.append(Node(p, ModelConst))

        return nodes
