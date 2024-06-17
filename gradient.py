import numpy as np
from PIL import Image
RGB = tuple[int, int, int]


def generate_gradient(starting_color: RGB,
                      ending_color: RGB,
                      height: int,
                      width: int) -> Image:
    gradient = np.zeros((height, width, 3), np.uint8)
    gradient[:, :, 0] = np.linspace(starting_color[0], ending_color[0],
                                    width, dtype=np.uint8)
    gradient[:, :, 1] = np.linspace(starting_color[1], ending_color[1],
                                    width, dtype=np.uint8)
    gradient[:, :, 2] = np.linspace(starting_color[2], starting_color[2],
                                    width, dtype=np.uint8)
    return Image.fromarray(gradient)