import json

BLACK = 0
WHITE = 255

BLACK_RGB = color(0, 0, 0)
WHITE_RGB = color(255, 255, 255)

GREYSCALE_THRESHOLD = 127

RED_COLOR_SCHEME = ['#ff0000']
GREYSCALE_COLOR_SCHEME = ['#b4b4b4', '#646464', '#d4d4d4', '#4c4c4c']

class GBIPG_CONST:
    config = open('config.json')
    config_json = json.load(config)
    config.close()

    MODE = config_json['gbipg_config']['run']['mode']
    BENCHMARK_ITERATIONS = config_json['gbipg_config']['run']['benchmark_iterations']
    SAVE_STATES = config_json['gbipg_config']['run']['save_states']

    FILE_NAME = config_json['gbipg_config']['image']['file_name']
    PREPROCESS_IMG = config_json['gbipg_config']['image']['preprocess']

    WIDTH = config_json['gbipg_config']['plate']['width']
    HEIGHT = config_json['gbipg_config']['plate']['height']
    WALL_RADIUS = config_json['gbipg_config']['plate']['wall_radius']

    MIN_CIRCLE_RADIUS = config_json['gbipg_config']['plate']['circles']['min_radius']
    BOX_SIZE = config_json['gbipg_config']['plate']['circles']['box_size']
    
    FIG_COLOR_SCHEME = config_json['gbipg_config']['plate']['circles']['color_scheme']['figure']
    BG_COLOR_SCHEME = config_json['gbipg_config']['plate']['circles']['color_scheme']['background']

class MC_CONST:
    config = open('config.json')
    config_json = json.load(config)
    config.close()

    MODE = config_json['mc_config']['run']['mode']
    BENCHMARK_ITERATIONS = config_json['mc_config']['run']['benchmark_iterations']

    FILE_NAME = config_json['mc_config']['image']['file_name']
    PREPROCESS_IMG = config_json['mc_config']['image']['preprocess']

    WIDTH = config_json['mc_config']['plate']['width']
    HEIGHT = config_json['mc_config']['plate']['height']
    WALL_RADIUS = config_json['mc_config']['plate']['wall_radius']
    MIN_UNFILLED_CANVAS_RATIO = config_json['mc_config']['plate']['min_unfilled_canvas_ratio']

    MIN_CIRCLE_RADIUS = config_json['mc_config']['plate']['circles']['min_radius']
    MAX_CIRCLE_RADIUS = config_json['mc_config']['plate']['circles']['max_radius']
    
    FIG_COLOR_SCHEME = config_json['mc_config']['plate']['circles']['color_scheme']['figure']
    BG_COLOR_SCHEME = config_json['mc_config']['plate']['circles']['color_scheme']['background']