import pandas as pd
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


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


def svg_to_png(svg_name: str) -> None:
    png_name = f"{svg_name.split('.')[0]}.png"
    drawing = svg2rlg(svg_name)
    renderPM.drawToFile(drawing, png_name, fmt="PNG")