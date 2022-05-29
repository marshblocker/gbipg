import math

from const import *


def distance(p1, p2):
    ''' Euclidean distance between p1 and p2.

    Parameters:
        p1: tuple[int, int]
        p2: tuple[int, int]

    Return Value:
        float
    '''
    p1x, p1y = p1
    p2x, p2y = p2

    dx = p2x - p1x
    dy = p2y - p1y

    dx_squared = dx * dx
    dy_squared = dy * dy

    res = math.sqrt(dx_squared + dy_squared)
    return res


def distance_squared(p1, p2):
    ''' Squared Euclidean distance between p1 and p2.

    Parameters:
        p1: tuple[int, int]
        p2: tuple[int, int]

    Return Value:
        float
    '''
    p1x, p1y = p1
    p2x, p2y = p2

    dx = p2x - p1x
    dy = p2y - p1y

    dx_squared = dx * dx
    dy_squared = dy * dy

    return dx_squared + dy_squared


def loc_to_coord(loc, ModelConst):
    '''
    Paremeter:
        loc: int
        ModelConst: GBIPG_CONST | MC_CONST

    Return Value:
        (x, y): tuple[int, int]
    '''
    x = loc % ModelConst.WIDTH
    y = (loc - x) / ModelConst.WIDTH
    return (x, y)

def nearest_other_colored_pixel(node, pxls):
    nearest_dist = node.max_radius
    c = node.center
    cx, cy = c.get_coord()
    curr_max_radius = node.max_radius
    opp_colr_points = get_opposite_colr_points_in_circle(
        c, curr_max_radius, pxls, node._ModelConst)

    for p2_loc in opp_colr_points:
        p2x, p2y = loc_to_coord(p2_loc, node._ModelConst)

        dist = distance((cx, cy), (p2x, p2y))
        nearest_dist = min(nearest_dist, dist)

    return nearest_dist


def get_opposite_colr_points_in_circle(p, r, canvas_pxls, ModelConst):
    '''
    Get all points that are opposite the color of point p within the
    circle with center point p and radius r.

    Parameters:
        p: Point := center point of the circle.
        r: int := radius of the circle.
        canvas_pxls: list[color] := color of each pixel in the canvas.
        ModelConst: GBIPG_CONST | MC_CONST

    Return Value:
        opp_colr_points: list[int] := list of indices (in canvas_pxls) of points
                                      that have their color opposite to point p.
    '''
    opp_colr_points = []
    px, py = p.get_coord()
    p_colr = BLACK_RGB if p.in_fig() else WHITE_RGB
    r_squared = r*r
    i = 0

    y_start = ceil(max(0, py - r))
    x_start = ceil(max(0, px - r))
    y_end = ceil(min(ModelConst.HEIGHT, py + r + 1))
    x_end = ceil(min(ModelConst.WIDTH, px + r + 1))

    for p2y in range(y_start, y_end):
        for p2x in range(x_start, x_end):
            p2_loc = ModelConst.WIDTH*p2y + p2x
            if distance_squared((px, py), (p2x, p2y)) <= r_squared and canvas_pxls[p2_loc] != p_colr:
                opp_colr_points.append(p2_loc)

    return opp_colr_points


def opposite_colr_point_in_circle(p, r, canvas_pxls, ModelConst):
    '''
    Checks if a point that has its color opposite to point p is 
    within the circle with center point p and radius r.

    Parameters:
        p: Point := center point of the circle.
        r: int := radius of the circle.
        canvas_pxls: list[color] := color of each pixel in the canvas.
        ModelConst: GBIPG_CONST | MC_CONST

    Return Value:
        boolean := Returns True if a point with opposite color to point p 
                   is within the circle.
    '''
    px, py = p.get_coord()
    p_colr = BLACK_RGB if p.in_fig() else WHITE_RGB
    r_squared = r*r

    y_start = ceil(max(0, py - r))
    x_start = ceil(max(0, px - r))
    y_end = ceil(min(ModelConst.HEIGHT, py + r + 1))
    x_end = ceil(min(ModelConst.WIDTH, px + r + 1))

    for p2y in range(y_start, y_end):
        for p2x in range(x_start, x_end):
            p2_loc = ModelConst.WIDTH*p2y + p2x
            if distance_squared((px, py), (p2x, p2y)) <= r_squared and canvas_pxls[p2_loc] != p_colr:
                return True

    return False

def other_colr_point_in_circle(p, r, canvas_pxls, ModelConst):
    px, py = p.get_coord()
    p_colr = BLACK_RGB if p.in_fig() else WHITE_RGB
    r_squared = r*r

    y_start = ceil(max(0, py - r))
    x_start = ceil(max(0, px - r))
    y_end = ceil(min(ModelConst.HEIGHT, py + r + 1))
    x_end = ceil(min(ModelConst.WIDTH, px + r + 1))

    for p2y in range(y_start, y_end):
        for p2x in range(x_start, x_end):
            p2_loc = ModelConst.WIDTH*p2y + p2x
            if distance_squared((px, py), (p2x, p2y)) <= r_squared and canvas_pxls[p2_loc] not in [BLACK_RGB, WHITE_RGB]:
                return True

    return False


def get_rgb(colr):
    return (red(colr), green(colr), blue(colr))


def print_rgb(colr):
    r, g, b = get_rgb(colr)
    print(r, g, b)


def is_greyscale(colr):
    '''
    Returns True if the pixel's color is greyscale.
    '''
    r = red(colr)
    g = green(colr)
    b = blue(colr)

    if r != g or g != b:
        return False

    return True

def is_color_hex(inp):
    valid_chars = [str(num) for num in range(10)] + [chr(x) for x in range(ord('A'), ord('F') + 1)]
    if len(inp) != 7 or inp[0] != '#':
        return False

    for char in inp[1:].upper():
        if char not in valid_chars:
            return False
    
    return True