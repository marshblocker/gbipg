import math
import random
import time

from const import MC_CONST
from img import getImage
from classes import Point
import const
import utils

def settings():
    size(MC_CONST.WIDTH, MC_CONST.HEIGHT)

def setup():
    if is_MC_parameters_valid():
        img = getImage(MC_CONST.FILE_NAME, MC_CONST, MC_CONST.PREPROCESS_IMG)
        if img:
            if MC_CONST.MODE == 'normal':
                normal_mode(img)
            elif MC_CONST.MODE == 'benchmark':
                benchmark_mode(img, MC_CONST.BENCHMARK_ITERATIONS)
            else:
                print('Error: Invalid mode.')
                exit()
        else:
            print('Failed.')
            exit()
    else:
        print('Failed.')
        exit()

def normal_mode(img):
    print('Program start.')
    if run(img):
        print('Success.')
    else:
        print('Failed.')

def benchmark_mode(img, iterations):
    print('Program start.')
    avg_time = 0.0
    variance = 0.0
    duration_list = []

    success = True
    for i in range(1, iterations+1):
        start_time = time.time()

        success = run(img)

        duration = round(time.time() - start_time, 3)
        duration_list.append(duration)
        avg_time += duration
        print('Iteration {} of {}: {} seconds.'
              .format(i, iterations, duration))

        if not success:
            print('Failed at iteration {} of {}'.format(i, iterations))
            avg_time = avg_time / i
            variance = sum([(duration - avg_time)**2 for duration in duration_list]) / (iterations - 1)
            break

    if success:
        print('Success.')
        avg_time = round(avg_time / iterations, 3)
        variance = round(sum([(duration - avg_time)**2 for duration in duration_list]) / (iterations - 1), 3)
    
    print('Average runtime: {} seconds'.format(avg_time))
    print('Variance: {}'.format(variance))

def run(img):
    background(const.WHITE)
    if img:
        img.loadPixels()
        monte_carlo(img.pixels)
        return True
    else:
        return False

def monte_carlo(img_pxls):
    remaining_canvas_area = math.pi * MC_CONST.WALL_RADIUS**2
    MIN_UNFILLED_AREA = remaining_canvas_area * MC_CONST.MIN_UNFILLED_CANVAS_RATIO
    noStroke()
    while remaining_canvas_area > MIN_UNFILLED_AREA:
        loadPixels()
        x, y = random.randint(0, MC_CONST.WIDTH-1), random.randint(0, MC_CONST.HEIGHT-1)
        r = random.randint(MC_CONST.MIN_CIRCLE_RADIUS, MC_CONST.MAX_CIRCLE_RADIUS)
        p = Point(x, y, img_pxls, MC_CONST)
        
        overlap = False

        if p.will_overlap_wall():
            overlap = True
        
        if p.will_overlap_something(r, pixels):
            overlap = True

        if not overlap:
            color_scheme = MC_CONST.FIG_COLOR_SCHEME if p.in_fig() else MC_CONST.BG_COLOR_SCHEME
            fill(random.choice(color_scheme))
            ellipse(x, y, 2*r, 2*r)

            circle_area = math.pi * r**2
            remaining_canvas_area -= circle_area

def is_MC_parameters_valid():
    positive_int_parameters = {
        MC_CONST.BENCHMARK_ITERATIONS: 'benchmark iterations',
        MC_CONST.WIDTH: 'width',
        MC_CONST.HEIGHT: 'height',
        MC_CONST.WALL_RADIUS: 'wall radius',
        MC_CONST.MIN_CIRCLE_RADIUS: 'minimum circle radius',
        MC_CONST.MAX_CIRCLE_RADIUS: 'maximum circle radius',
    }

    for param in positive_int_parameters:
        if type(param) != int or param <= 0:
            print("Error: Invalid {} parameter value. Must be a non-zero, positive integer.".format(positive_int_parameters[param]))
            return False

    if MC_CONST.MODE not in ['normal', 'benchmark']:
        print("Error: Invalid mode parameter value. Must be 'normal' or 'benchmark'.")
        return False

    if type(MC_CONST.PREPROCESS_IMG) != bool:
        print("Error: Invalid preprocess image parameter value. Must be a boolean type.")
        return False

    if not MC_CONST.FILE_NAME.endswith('.png'):
        print("Error: Supplied image is not in PNG format.")
        return False

    if MC_CONST.WIDTH != MC_CONST.HEIGHT:
        print("Error: Canvas' width and height parameters are not equal.")
        return False

    if MC_CONST.WALL_RADIUS >= MC_CONST.WIDTH / 2:
        print("Error: Canvas' wall radius parameter is too large for the canvas' width/height parameter.")
        print("Make sure that it is less than half of the canvas' width/height parameter.")
        return False

    if MC_CONST.MIN_CIRCLE_RADIUS >= MC_CONST.MAX_CIRCLE_RADIUS:
        print("Error: Circles' minimum radius parameter is larger than its maximum radius parameter.")
        return False

    if MC_CONST.MAX_CIRCLE_RADIUS >= MC_CONST.WALL_RADIUS / 2:
        print("Error: Circles' maximum radius parameter is too large.")
        return False

    if MC_CONST.MIN_UNFILLED_CANVAS_RATIO > 1.0:
        print("Error: Invalid value for the minimum unfilled canvas ratio parameter. Should be less than 1.0.")
        return False

    for color_hex in MC_CONST.BG_COLOR_SCHEME:
        if not utils.is_color_hex(color_hex):
            print("Error: Invalid background color scheme parameter value.")
            return False

    for color_hex in MC_CONST.FIG_COLOR_SCHEME:
        if not utils.is_color_hex(color_hex):
            print("Error: Invalid figure color scheme parameter value.")
            return False

    return True


