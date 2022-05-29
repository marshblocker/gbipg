import time
import random as rand
import json

from img import getImage
from classes import Point, CirclesAdjacencyGraph
from const import GBIPG_CONST, WHITE_RGB
import utils
import const

def settings():
    size(GBIPG_CONST.WIDTH, GBIPG_CONST.HEIGHT)

def setup():
    if is_GBIPG_parameters_valid():
        img = getImage(GBIPG_CONST.FILE_NAME, GBIPG_CONST, GBIPG_CONST.PREPROCESS_IMG)
        if img:
            if GBIPG_CONST.MODE == 'normal':
                normal_mode(img)
            elif GBIPG_CONST.MODE == 'benchmark':
                benchmark_mode(img, GBIPG_CONST.BENCHMARK_ITERATIONS)
        else:
            print('Failed.')
            exit()
    else:
        print('Failed.')
        exit()

def normal_mode(img):
    print('Program start.')
    run(img)
    print('Success.')

def benchmark_mode(img, iterations):
    print('Program start.')
    avg_time = 0.0
    variance = 0.0
    duration_list = []

    for i in range(1, iterations+1):
        start_time = time.time()

        run(img)

        duration = round(time.time() - start_time, 3)
        duration_list.append(duration)
        avg_time += duration
        print('Iteration {} of {}: {} seconds.'.format(i, iterations, duration))

    print('Success.')
    avg_time = round(avg_time / iterations, 3)
    variance = round(sum([(duration - avg_time)**2 for duration in duration_list]) / (iterations - 1), 3)
    
    print('Average runtime: {} seconds'.format(avg_time))
    print('Variance: {}'.format(variance))

def run(img):
    background(const.WHITE)
    GBIPG(img)

def GBIPG(img):
    ''' 
    Generate compactly-filled, randomized circles on the background and the 
    figure using the Graph-based Ishihara Plate Generation (GBIPG) Algorithm.

    Parameters:
        img_pxls: list[color] := The pixels of the image reference.

    Return Value:
        None
    '''
    img.loadPixels
    fig_random_points, bg_random_points = generate_random_points(img.pixels)

    fig_cag = build_circles_adjacency_graph(fig_random_points, img.pixels, False)
    bg_cag = build_circles_adjacency_graph(bg_random_points, img.pixels, True)

    image(img, 0, 0)
    solved_fig_cag = solve_csp_of_cag(fig_cag, GBIPG_CONST.FIG_COLOR_SCHEME)
    solved_bg_cag = solve_csp_of_cag(bg_cag, GBIPG_CONST.BG_COLOR_SCHEME)
    display_final_nodes(solved_fig_cag.nodes, solved_bg_cag.nodes)

    fill_up_crevices(img.pixels)
    

def generate_random_points(img_pxls):
    '''
    Return a list of random points in the background and a list of random points in the figure. 
    The random points are generated such that they do not overlap with other points, 
    figure boundary, and the canvas wall.

    Parameters:
        img_pxls: list[color]

    Return Value:
        (fig_random_points, bg_random_points): tuple[list[Point], list[Point]]
    '''
    bg_random_points = []
    fig_random_points = []

    stroke(const.BLACK)

    start = GBIPG_CONST.WIDTH/2 - GBIPG_CONST.WALL_RADIUS
    end = GBIPG_CONST.WIDTH/2 + GBIPG_CONST.WALL_RADIUS
    
    # How distributed the points are in the canvas.
    box_size = GBIPG_CONST.BOX_SIZE

    for i in range(start, end, box_size):
        for j in range(start, end, box_size):
            x = int(rand.uniform(
                    min(end, i + GBIPG_CONST.MIN_CIRCLE_RADIUS), 
                    min(end, i + box_size - GBIPG_CONST.MIN_CIRCLE_RADIUS)
                ))
            y = int(rand.uniform(
                    min(end, j + GBIPG_CONST.MIN_CIRCLE_RADIUS), 
                    min(end, j + box_size - GBIPG_CONST.MIN_CIRCLE_RADIUS)
                ))
            p = Point(x, y, img_pxls, GBIPG_CONST)
            overlap = False

            if p.will_overlap_wall() or p.will_overlap_fig_boundary(img_pxls):
                overlap = True

            if not overlap:
                if p.in_fig():
                    fig_random_points.append(p)
                else:
                    bg_random_points.append(p)

    if GBIPG_CONST.SAVE_STATES:
        noStroke()
        r = GBIPG_CONST.MIN_CIRCLE_RADIUS

        fill(rand.choice(GBIPG_CONST.FIG_COLOR_SCHEME))
        for p in fig_random_points:
            x, y = p.get_coord()
            ellipse(x, y, 2*r, 2*r)

        fill(rand.choice(GBIPG_CONST.BG_COLOR_SCHEME))
        for p in bg_random_points:
            x, y = p.get_coord()
            ellipse(x, y, 2*r, 2*r)

        img_name = GBIPG_CONST.FILE_NAME.rstrip(".png") + "-step1.png"
        saveFrame(img_name)
        background(WHITE_RGB)

    return (fig_random_points, bg_random_points)


def build_circles_adjacency_graph(center_points, img_pxls, save_frame):
    ''' Build the CirclesAdjacencyGraph from the given center_points.

    Parameters:
        center_points: list[Point]
        img_pxls: list[color]
        saveFrame: bool

    Return Value:
        cag: CirclesAdjacencyGraph
    '''
    cag = CirclesAdjacencyGraph(center_points, img_pxls, GBIPG_CONST)

    if GBIPG_CONST.SAVE_STATES:
        noStroke()
        r = GBIPG_CONST.MIN_CIRCLE_RADIUS
        fig_colr = rand.choice(GBIPG_CONST.FIG_COLOR_SCHEME)
        bg_colr = rand.choice(GBIPG_CONST.BG_COLOR_SCHEME)
        for node in cag.nodes:
            fill(fig_colr if node.center.in_fig() else bg_colr)
            cx, cy = node.center.get_coord()
            ellipse(cx, cy, 2*r, 2*r)

        for node in cag.nodes:
            stroke(bg_colr if node.center.in_fig() else fig_colr)
            fill(bg_colr if node.center.in_fig() else fig_colr)
            cx, cy = node.center.get_coord()
            for indx in node.adj_nodes:
                node2 = cag.nodes[indx]
                cx2, cy2 = node2.center.get_coord()
                line(cx, cy, cx2, cy2)
                ellipse(cx, cy, r, r)

        if save_frame:
            img_name = GBIPG_CONST.FILE_NAME.rstrip(".png") + "-step2.png"
            saveFrame(img_name)
            background(const.WHITE_RGB)

    return cag


def solve_csp_of_cag(cag, color_scheme):
    ''' Solve the Constraint Satisfaction Problem of the Circles Adjacency Graph cag.

    Params:
        cag: CirclesAdjacencyGraph
        color_scheme: list[str] := list of color hex strings that will be used as argument to fill().

    Return Value:
        solved_cag: CirclesAdjacencyGraph := This is cag but with the radius of each of its node
                                             satisfying the CSP of cag.
    '''
    noStroke()
    for i in range(len(cag.nodes)):
        loadPixels()
        cag.nodes[i].radius = utils.nearest_other_colored_pixel(cag.nodes[i], pixels)
        cx, cy = cag.nodes[i].center.get_coord()
        for indx in cag.nodes[i].adj_nodes:
            cx2, cy2 = cag.nodes[indx].center.get_coord()
            other_node_new_max_radius = utils.distance(
                (cx, cy), (cx2, cy2)) - cag.nodes[i].radius
            if other_node_new_max_radius < cag.nodes[indx].max_radius:
                cag.nodes[indx].max_radius = other_node_new_max_radius
                cag.nodes[indx].adj_nodes.remove(i)

        fill(rand.choice(color_scheme))
        r = cag.nodes[i].radius
        ellipse(cx, cy, 2*r, 2*r)

    solved_cag = cag

    return solved_cag

def display_final_nodes(fig_nodes, bg_nodes):
    background(const.WHITE_RGB)
    noStroke()

    for node in fig_nodes:
        fill(rand.choice(GBIPG_CONST.FIG_COLOR_SCHEME))
        cx, cy = node.center.get_coord()
        r = node.radius
        ellipse(cx, cy, 2*r, 2*r)

    for node in bg_nodes:
        fill(rand.choice(GBIPG_CONST.BG_COLOR_SCHEME))
        cx, cy = node.center.get_coord()
        r = node.radius
        ellipse(cx, cy, 2*r, 2*r)

    if GBIPG_CONST.SAVE_STATES:
        img_name = GBIPG_CONST.FILE_NAME.rstrip(".png") + "-step3.png"
        saveFrame(img_name)

def fill_up_crevices(img_pxls):
    '''Fill up remaining crevices using Monte Carlo algorithm.
    
    Parameter:
        img_pxls: list[color]

    Return Value:
        None
    '''
    smallest_r = 2
    largest_r = 10

    start = GBIPG_CONST.WIDTH/2 - GBIPG_CONST.WALL_RADIUS
    end = GBIPG_CONST.WIDTH/2 + GBIPG_CONST.WALL_RADIUS
    for i in range(30000):
        loadPixels()
        x, y = int(rand.uniform(start, end-1)), int(rand.uniform(start, end-1))
        p = Point(x, y, img_pxls, GBIPG_CONST)
        r = rand.randint(smallest_r, largest_r)
        overlap = False

        if p.will_overlap_wall():
            overlap = True
        
        if p.will_overlap_something(r, pixels):
            overlap = True

        if not overlap:
            color_scheme = GBIPG_CONST.FIG_COLOR_SCHEME if p.in_fig() else GBIPG_CONST.BG_COLOR_SCHEME
            fill(rand.choice(color_scheme))
            ellipse(x, y, 2*r, 2*r)

def is_GBIPG_parameters_valid():
    positive_int_parameters = {
        GBIPG_CONST.BENCHMARK_ITERATIONS: 'benchmark iterations',
        GBIPG_CONST.WIDTH: 'width',
        GBIPG_CONST.HEIGHT: 'height',
        GBIPG_CONST.WALL_RADIUS: 'wall radius',
        GBIPG_CONST.MIN_CIRCLE_RADIUS: 'minimum circle radius',
        GBIPG_CONST.BOX_SIZE: 'box size'
    }

    for param in positive_int_parameters:
        if type(param) != int or param <= 0:
            print("Error: Invalid {} parameter value. Must be a non-zero, positive integer.".format(positive_int_parameters[param]))
            return False

    if GBIPG_CONST.MODE not in ['normal', 'benchmark']:
        print("Error: Invalid mode parameter value. Must be 'normal' or 'benchmark'.")
        return False

    if type(GBIPG_CONST.PREPROCESS_IMG) != bool:
        print("Error: Invalid preprocess image parameter value. Must be a boolean type.")
        return False

    if not GBIPG_CONST.FILE_NAME.endswith('.png'):
        print("Error: Supplied image is not in PNG format.")
        return False

    if GBIPG_CONST.WIDTH != GBIPG_CONST.HEIGHT:
        print("Error: Canvas' width and height parameters are not equal.")
        return False

    if GBIPG_CONST.WALL_RADIUS >= GBIPG_CONST.WIDTH / 2:
        print("Error: Canvas' wall radius parameter is too large for the canvas' width/height parameter.")
        print("Make sure that it is less than half of the canvas' width/height parameter.")
        return False

    if GBIPG_CONST.MIN_CIRCLE_RADIUS >= GBIPG_CONST.WALL_RADIUS / 2:
        print("Error: Circles' minimum radius parameter is too large.")
        return False

    if GBIPG_CONST.BOX_SIZE >= GBIPG_CONST.WALL_RADIUS / 2:
        print("Error: Box size parameter is too large.")
        print("Make sure that it is less than half of the canvas' wall radius parameter.")
        return False

    if 2*GBIPG_CONST.MIN_CIRCLE_RADIUS >= GBIPG_CONST.BOX_SIZE:
        print("Error: Circles' minimum radius parameter is too large for the box size parameter.")
        return False

    for color_hex in GBIPG_CONST.BG_COLOR_SCHEME:
        if not utils.is_color_hex(color_hex):
            print("Error: Invalid background color scheme parameter value. Must be of the form '#xxxxxx'.")
            return False

        if color_hex in ['#000000', '#FFFFFF']:
            print("Error: Invalid background color scheme parameter value. Cannot use black or white as background color.")

    for color_hex in GBIPG_CONST.FIG_COLOR_SCHEME:
        if not utils.is_color_hex(color_hex):
            print("Error: Invalid figure color scheme parameter value. Must be of the form '#xxxxxx'.")
            return False

        if color_hex in ['#000000', '#FFFFFF']:
            print("Error: Invalid figure color scheme parameter value. Cannot use black or white as figure color.")

    return True

