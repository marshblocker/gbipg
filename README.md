# gbipg
Graph-based Ishihara Plate Generation Algorithm. Implemented in Processing Python Mode.

## Table of Contents
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Usage](#usage)
    * [Quick Start](#quick-start)
    * [GBIPG and Monte Carlo](#gbipg-and-monte-carlo)
    * [Changing the Model Parameters](#changing-the-model-parameters)
    * [Adding Your Own Input Image](#adding-your-own-input-image)

## Getting Started
### Prerequisites
To run this program from the command line, you need to have Java 8 and the standalone version of Processing.py installed in your machine. 
To do so, follow the instruction in the Requirements section of this [tutorial by Processing.py](https://py.processing.org/tutorials/command-line/).
Take note of the location of `processing-py.jar` file, this will be the driver of our program.

### Installation
Clone this repo in your machine using `git clone https://github.com/marshblocker/gbipg.git`.

## Usage
### Quick Start
To get a quick insight on what the program does, run the following commands in your terminal:
```
cd path/to/gbipg/directory
java -jar path/to/processing-py.jar gbipg.py
```
After a few seconds, the following Ishihara plate should display on a new window: ![Ishihara plate of a hand](./preview/hand-gbipg.png)

### GBIPG and Monte Carlo
Within the `gbipg/` directory, there is `gbipg.py` which executes the GBIPG algorithm (the program we run in the Quick Start section) and `montecarlo.py` which executes the traditional Monte Carlo algorithm. If you want to use the Monte Carlo algorithm, just run `java -jar path/to/processing-py.jar montecarlo.py` in your terminal. Just note that the Monte Carlo algorithm is comparably slower than the GBIPG algorithm.

### Changing the Model Parameters
Within the `gbipg/data/` directory, there is `config.json` which stores the parameters of both `gbipg.py` and `montecarlo.py` as separate attributes. You can change it depending on your need. Here is a table that describes what each of the parameters do:

Parameter | Description | Data Type | Example Value
:---: | :---: | :---: | :---:
`run.mode` | Use the program normally or use it to benchmark the algorithm. | `str` | `"normal"`, `"benchmark"`
`run.benchmark_iterations` | If `benchmark` mode, this parameter determines how many times the program will be run. | `int` | `2`, `10`
`image.file_name` | The name of the PNG file used as input to the program. The file should be located in `gbipg/data` directory. | `str` | `"hand.png"`, `"circle.png"`
`image.preprocess` | Preprocess the input image before being it is used as input to the program. It is recommended that this is _always_ set to `True`. | `bool` | `true`, `false`
`plate.width` & `plate.height` | The width and height of the canvas. Their values should _always_ be equal. | `int` | `800`, `350`
`plate.wall_radius` | The radius of the circular wall that sets the boundary of the background display. | `int` | `232`, `100`
`plate.min_unfilled_canvas_ratio` | If the ratio of the remaining area over the total area of the canvas is below this parameter, then the Monte Carlo algorithm stops its execution. Its values is between `0.0` and `1.0`. _Only applicable to the Monte Carlo algorithm_. | `float` | `0.4`, `0.56`
`plate.circles.min_radius` | The smallest possible radius of a circle in the canvas. | `int` | `5`, `11`
`plate.circles.max_radius` | The largest possible radius of a circle in the canvas. _Only applicable to the Monte Carlo algorithm_. | `int` | `15`, `8`
`plate.circles.box_size` | How far the random points are distributed in the canvas. _Only applicable to the GBIPG algorithm_. | `int` | `30`, `20`
`plate.circles.color_scheme.figure` & `plate.circles.color_scheme.background` | The list of colors a circle on a figure/background can have. | `list[str]` | `["#3fac70", "#98a86d", "#c5bc6e", "#87934b"]`

### Adding Your Own Input Image
Besides the sample input images in the `gbipg/data/` directory, you could also use your own image as input to the program by placing it in the `gbipg/data/` directory and replacing the `image.file_name` parameter with the file name of your image. Just make sure that your image is in .png format and that it is a [grayscale](https://en.wikipedia.org/wiki/Grayscale) image. You could use [this website](https://pinetools.com/grayscale-image) to convert your image to grayscale. It is discouraged to use heavily-detailed images as it can lead to poorly-rendered Ishihara plates.
