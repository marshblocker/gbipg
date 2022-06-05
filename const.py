import json

import utils

BLACK = 0
WHITE = 255

BLACK_RGB = color(0, 0, 0)
WHITE_RGB = color(255, 255, 255)

GRAYSCALE_THRESHOLD = 127

RED_COLOR_SCHEME = ['#ff0000']
GRAYSCALE_COLOR_SCHEME = ['#b4b4b4', '#646464', '#d4d4d4', '#4c4c4c']


class ModelConst:
    def __init__(self, mode, benchmark_iterations, file_name, preprocess_img,
                 width, height, wall_radius, max_filled_area_ratio,
                 min_circle_radius, max_circle_radius, fig_color_scheme,
                 bg_color_scheme):
        self.MODE = mode
        self.BENCHMARK_ITERATIONS = benchmark_iterations
        self.FILE_NAME = file_name
        self.PREPROCESS_IMG = preprocess_img
        self.WIDTH = width
        self.HEIGHT = height
        self.WALL_RADIUS = wall_radius
        self.MAX_FILLED_AREA_RATIO = max_filled_area_ratio
        self.MIN_CIRCLE_RADIUS = min_circle_radius
        self.MAX_CIRCLE_RADIUS = max_circle_radius
        self.FIG_COLOR_SCHEME = fig_color_scheme
        self.BG_COLOR_SCHEME = bg_color_scheme

    def is_parameters_valid(self):
        positive_int_parameters = {
            self.BENCHMARK_ITERATIONS: 'benchmark_iterations',
            self.WIDTH: 'width',
            self.HEIGHT: 'height',
            self.WALL_RADIUS: 'wall_radius',
            self.MIN_CIRCLE_RADIUS: 'minimum_circle_radius',
            self.MAX_CIRCLE_RADIUS: 'maximum_circle_radius',
        }

        for param in positive_int_parameters:
            if type(param) != int or param <= 0:
                print("Error: Invalid {} parameter value. Must be a non-zero, positive integer.".format(
                    positive_int_parameters[param]))
                return False

        if self.MODE not in ['normal', 'benchmark']:
            print("Error: Invalid mode parameter value. Must be 'normal' or 'benchmark'.")
            return False

        if type(self.PREPROCESS_IMG) != bool:
            print(
                "Error: Invalid preprocess_img parameter value type. Must be a boolean type.")
            return False

        if not self.FILE_NAME.endswith('.png'):
            print("Error: Supplied image is not in PNG format.")
            return False

        if self.WIDTH != self.HEIGHT:
            print("Error: Canvas' width and height parameters are not equal.")
            return False

        if self.WALL_RADIUS >= self.WIDTH / 2:
            print(
                "Error: Canvas' wall_radius parameter is too large for the canvas' width/height parameter.")
            print(
                "Make sure that it is less than half of the canvas' width/height parameter.")
            return False

        if self.MIN_CIRCLE_RADIUS >= self.MAX_CIRCLE_RADIUS:
            print(
                "Error: min_circle_radius parameter is larger than max_circle_radius parameter.")
            return False

        if self.MAX_CIRCLE_RADIUS >= self.WALL_RADIUS / 2:
            print("Error: max_circle_radius parameter is too large.")
            return False

        if self.MAX_FILLED_AREA_RATIO > 1.0 or self.MAX_FILLED_AREA_RATIO < 0.0:
            print(
                "Error: Invalid value for max_filled_area_ratio parameter. Should be between 0.0 and 1.0.")
            return False

        for color_hex in self.BG_COLOR_SCHEME:
            if not utils.is_color_hex(color_hex):
                print(
                    "Error: Invalid bg_color_scheme parameter value. Must be of the form '#xxxxxx'.")
                return False

            if color_hex.upper() in ['#000000', '#FFFFFF']:
                print(
                    "Error: Invalid bg_color_scheme parameter value. Cannot use black or white as background color.")

        for color_hex in self.FIG_COLOR_SCHEME:
            if not utils.is_color_hex(color_hex):
                print(
                    "Error: Invalid fig_color_scheme parameter value. Must be of the form '#xxxxxx'.")
                return False

            if color_hex in ['#000000', '#FFFFFF']:
                print(
                    "Error: Invalid fig_color_scheme parameter value. Cannot use black or white as figure color.")

        return True


class GBIPGConst(ModelConst):
    def __init__(self, mode, benchmark_iterations, file_name, preprocess_img,
                 width, height, wall_radius, max_filled_area_ratio,
                 min_circle_radius, max_circle_radius, fig_color_scheme,
                 bg_color_scheme, save_states, box_size):
        ModelConst.__init__(
            self, mode, benchmark_iterations, file_name, preprocess_img, width,
            height, wall_radius, max_filled_area_ratio, min_circle_radius,
            max_circle_radius, fig_color_scheme, bg_color_scheme
        )
        self.SAVE_STATES = save_states
        self.BOX_SIZE = box_size

    def is_parameters_valid(self):
        if not ModelConst.is_parameters_valid(self):
            return False

        if type(self.SAVE_STATES) != bool:
            print(
                "Error: Invalid save_states parameter value type. Must be a boolean type.")
            return False

        if self.BOX_SIZE >= self.WALL_RADIUS / 2:
            print("Error: box_size parameter is too large.")
            print("Make sure that it is less than half of the wall_radius parameter.")
            return False

        if 2*self.MIN_CIRCLE_RADIUS >= self.BOX_SIZE:
            print(
                "Error: min_circle_radius parameter is too large for the box_size parameter.")
            return False

        return True


class MCConst(ModelConst):
    def __init__(self, mode, benchmark_iterations, file_name, preprocess_img,
                 width, height, wall_radius, max_filled_area_ratio,
                 min_circle_radius, max_circle_radius, fig_color_scheme,
                 bg_color_scheme):
        ModelConst.__init__(
            self, mode, benchmark_iterations, file_name, preprocess_img, width,
            height, wall_radius, max_filled_area_ratio, min_circle_radius,
            max_circle_radius, fig_color_scheme, bg_color_scheme
        )


config = open('config.json')
config_json = json.load(config)
config.close()

gbipg_mode = config_json['gbipg_config']['run']['mode']
gbipg_benchmark_iterations = config_json['gbipg_config']['run']['benchmark_iterations']
gbipg_save_states = config_json['gbipg_config']['run']['save_states']

gbipg_file_name = config_json['gbipg_config']['image']['file_name']
gbipg_preprocess_img = config_json['gbipg_config']['image']['preprocess']

gbipg_width = config_json['gbipg_config']['plate']['width']
gbipg_height = config_json['gbipg_config']['plate']['height']
gbipg_wall_radius = config_json['gbipg_config']['plate']['wall_radius']
gbipg_max_filled_area_ratio = config_json['gbipg_config']['plate']['max_filled_area_ratio']

gbipg_min_circle_radius = config_json['gbipg_config']['plate']['circles']['min_radius']
gbipg_max_circle_radius = config_json['gbipg_config']['plate']['circles']['max_radius']
gbipg_box_size = config_json['gbipg_config']['plate']['circles']['box_size']

gbipg_fig_color_scheme = config_json['gbipg_config']['plate']['circles']['color_scheme']['figure']
gbipg_bg_color_scheme = config_json['gbipg_config']['plate']['circles']['color_scheme']['background']

GBIPG_CONST = GBIPGConst(
    gbipg_mode, gbipg_benchmark_iterations, gbipg_file_name, gbipg_preprocess_img,
    gbipg_width, gbipg_height, gbipg_wall_radius, gbipg_max_filled_area_ratio,
    gbipg_min_circle_radius, gbipg_max_circle_radius, gbipg_fig_color_scheme,
    gbipg_bg_color_scheme, gbipg_save_states, gbipg_box_size
)

mc_mode = config_json['mc_config']['run']['mode']
mc_benchmark_iterations = config_json['mc_config']['run']['benchmark_iterations']

mc_file_name = config_json['mc_config']['image']['file_name']
mc_preprocess_img = config_json['mc_config']['image']['preprocess']

mc_width = config_json['mc_config']['plate']['width']
mc_height = config_json['mc_config']['plate']['height']
mc_wall_radius = config_json['mc_config']['plate']['wall_radius']
mc_max_filled_area_ratio = config_json['mc_config']['plate']['max_filled_area_ratio']

mc_min_circle_radius = config_json['mc_config']['plate']['circles']['min_radius']
mc_max_circle_radius = config_json['mc_config']['plate']['circles']['max_radius']

mc_fig_color_scheme = config_json['mc_config']['plate']['circles']['color_scheme']['figure']
mc_bg_color_scheme = config_json['mc_config']['plate']['circles']['color_scheme']['background']

MC_CONST = MCConst(
    mc_mode, mc_benchmark_iterations, mc_file_name, mc_preprocess_img, mc_width,
    mc_height, mc_wall_radius, mc_max_filled_area_ratio, mc_min_circle_radius,
    mc_max_circle_radius, mc_fig_color_scheme, mc_bg_color_scheme
)
