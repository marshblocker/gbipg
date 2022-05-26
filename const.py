import json

config = open('config.json')
config_json = json.load(config)
config.close()

# Canvas dimensions.
WIDTH = 800
HEIGHT = 800

BLACK = 0
WHITE = 255

BLACK_RGB = color(0, 0, 0)
WHITE_RGB = color(255, 255, 255)

GREYSCALE_THRESHOLD = 127

FIG_COLOR_SCHEME = config_json['color_scheme']['figure']
BG_COLOR_SCHEME = config_json['color_scheme']['background']
RED_COLOR_SCHEME = ['#ff0000']

MIN_CIRCLE_RADIUS = config_json['circles']['min_radius']
MAX_NUM_CIRCLES = config_json['circles']['max_num']