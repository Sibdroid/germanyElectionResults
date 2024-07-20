import pandas as pd
import re
import subprocess
from PIL import Image, ImageColor
from math import sqrt


def remove_in_parens(text: str):
    return re.sub("[\(\[].*?[\)\]]", "", text).strip()


def tuple_to_hex(tpl: tuple[float, float, float, float]) -> str:
    return "#" + "".join([hex(int(i * 255))[2:].zfill(2) for i in tpl[:-1]])


def get_wiki_tables(url: str,
                    column_match: str | list[str]) -> list[pd.DataFrame]:
    dfs = pd.read_html(url, header=0)
    dfs_to_return = []
    for df in dfs:
        columns = [i for i in df.columns]
        if isinstance(column_match, str):
            if column_match in columns:
                dfs_to_return += [df]
        else:
            if all([partial_match in columns for
                    partial_match in column_match]):
                dfs_to_return += [df]
    return dfs_to_return


def split_svg(contains: str,
              header_split: str) -> tuple[str, list[str], str]:
    header, paths = contains.split(header_split)
    header += header_split
    paths = ["<path" + i for i in paths.split("<path")
             if i.strip()]
    paths[-1] = paths[-1].replace("""</svg>""", "")
    return header, paths, """</svg>"""


def change_df_index(df: pd.DataFrame, changes: dict[str, str]):
    index = [changes.get(i, i) for i in df.index]
    df.index = index
    return df


def svg_to_png(svg_name: str, png_name: str,
               background_color: str = "white") -> None:
    args = [
        "C:/Program Files/Inkscape/bin/inkscape.com",
        svg_name,
        "-o",
        png_name,
        "-b",
        background_color
    ]
    subprocess.run(args)


def make_image_grid(png_paths: list[str], rows: int, cols: int):
    images = [Image.open(i) for i in png_paths]
    w, h = images[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    for i, img in enumerate(images):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid


def get_brightness(color: str) -> float:
    r, g, b = ImageColor.getcolor(color, "RGB")
    return sqrt(0.299 * r ** 2 + 0.587 * g ** 2 + 0.114 * b ** 2)
