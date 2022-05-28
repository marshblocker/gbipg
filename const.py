import json

config = open('config.json')
config_json = json.load(config)
config.close()

# Canvas dimensions.
WIDTH = config_json['plate']['width']
HEIGHT = config_json['plate']['height']

BLACK = 0
WHITE = 255

BLACK_RGB = color(0, 0, 0)
WHITE_RGB = color(255, 255, 255)

GREYSCALE_THRESHOLD = 127

FIG_COLOR_SCHEME = config_json['plate']['circles']['color_scheme']['figure']
BG_COLOR_SCHEME = config_json['plate']['circles']['color_scheme']['background']
RED_COLOR_SCHEME = ['#ff0000']
GREYSCALE_COLOR_SCHEME = ['#b4b4b4', '#646464', '#d4d4d4', '#4c4c4c']

MIN_CIRCLE_RADIUS = config_json['plate']['circles']['min_radius']
MAX_CIRCLE_RADIUS = config_json['plate']['circles']['mc_max_radius']
WALL_RADIUS = config_json['plate']['wall_radius']
BOX_SIZE = config_json['plate']['circles']['box_size']