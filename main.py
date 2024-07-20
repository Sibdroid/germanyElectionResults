import utils
from utils import *
from gradient import *
import matplotlib
import re
cmap = matplotlib.colors.LinearSegmentedColormap
COLORS = {"Union": "#585858",
          "AfD": "#11a1ee",
          "SPD": "#e11e29",
          "Grüne": "#47c639",
          "BSW": "#cd3275",
          "FDP": "#ffb800"}
NAMES = {"North Rhine-Westphalia": "North_Rhine-Westphalia",
         "Lower Saxony": "Lower_Saxony",
         "Bavaria": "Bayern",
         "Baden-Württemberg": "Baden-Wuttemberg"}

def make_cmap(color: str) -> cmap:
    return cmap.from_list("", ["white", color])


def get_color(colormap: cmap, value: float, max_value: float) -> str:
    value = int(round(255/max_value*value))
    return tuple_to_hex(colormap(value))


def make_color_df(df: pd.DataFrame) -> pd.DataFrame:
    full_colors = []
    for column in df.columns:
        try:
            colors = []
            cmap = make_cmap(COLORS[column])
            for value in df[column]:
                colors += [get_color(cmap, value, max(df[column]))]
            full_colors += [colors]
        except KeyError:
            pass
    color_df = pd.DataFrame(full_colors, columns=df["State"],
                            index=[i for i in COLORS.keys()]).transpose()
    return color_df


def make_map(df: pd.DataFrame,
             color_df: pd.DataFrame,
             party: str,
             write_path: str) -> None:
    colors = [i for i in color_df[party]]
    colors.sort(key=lambda x: utils.get_brightness(x), reverse=True)
    values = df[party]
    min_value, max_value = min(values), max(values)
    if min_value < 10:
        left_x = 20.5
    else:
        left_x = 25
    with open("basemap.svg", encoding="UTF-8") as file:
        header_split = """inkscape:window-maximized="1" />"""
        header, paths, footer = split_svg(file.read(), header_split)
        new_paths = []
        for path in paths:
            fill = [i for i in path.splitlines() if "fill=" in i
                    and "style" not in i][0].strip()
            fill = re.findall('"([^"]*)"', fill)[0]
            id = [i for i in path.splitlines() if "id=" in i][0]
            id = re.findall('"([^"]*)"', id)[0]
            path = path.replace(fill, color_df[party][id].upper())
            path = "".join([i+"\n" for i in path.splitlines()
                            if """style="fill""""" not in i])
            path += " />"
            new_paths += [path]
    with open(write_path, "w", encoding="UTF-8") as file:
        contents = header + "".join(new_paths) + footer
        contents = contents.replace('   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"',
                                    '''   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:xlink="http://www.w3.org/1999/xlink"''')
        contents = contents.replace('   id="defs22"><inkscape:perspective',
                                    f'''   id="defs22"><linearGradient
     id="linearGradient1"
     inkscape:collect="always"><stop
       style="stop-color:{colors[0]};stop-opacity:1;"
       offset="0"
       id="stop1" /><stop
       style="stop-color:{colors[-1]};stop-opacity:1;"
       offset="1"
       id="stop2" /></linearGradient><inkscape:perspective''')
        contents = contents.replace('     id="perspective26" /></defs><sodipodi:namedview',
                                    '''     id="perspective26" /><linearGradient
     inkscape:collect="always"
     xlink:href="#linearGradient1"
     id="linearGradient2"
     x1="14.089786"
     y1="35.530762"
     x2="150.08684"
     y2="35.530762"
     gradientUnits="userSpaceOnUse" /></defs><sodipodi:namedview''')
        contents = contents.replace('/></svg>',
                                    f''' /&gt;<rect
   style="fill:url(#linearGradient2);stroke-width:4;stroke-dashoffset:2.92652;paint-order:fill markers stroke"
   id="rect1"
   width="135.99706"
   height="33.080364"
   x="14.089786"
   y="18.99058"
   ry="0.92131364"
   transform="matrix(1.1029651,0,0,0.4534412,-5.5405412,1.3888888)" /><text
   xml:space="preserve"
   style="font-size:16px;line-height:1;font-family:Roboto;-inkscape-font-specification:Roboto;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;stroke-width:4;stroke-dashoffset:2.92652;paint-order:fill markers stroke"
   x="{left_x}"
   y="37.368561"
   id="text2"
   transform="translate(4.7741776,3.1705017)"><tspan
     sodipodi:role="line"
     id="tspan2"
     x="{left_x}"
     y="37.368561">{min_value}%</tspan></text><text
   xml:space="preserve"
   style="font-size:16px;line-height:1;font-family:Roboto;-inkscape-font-specification:Roboto;text-align:center;text-anchor:middle;fill:#000000;fill-opacity:1;stroke-width:4;stroke-dashoffset:2.92652;paint-order:fill markers stroke"
   x="111.18678"
   y="39.20636"
   id="text3"
   transform="translate(28.067248,1.3327026)"><tspan
     sodipodi:role="line"
     id="tspan3"
     x="111.18678"
     y="39.20636">{max_value}%</tspan></text></svg>

''')
        file.write(contents)


def main():
    df = get_wiki_tables("https://en.wikipedia.org/wiki"
                         "/2024_European_Parliament_election_in_Germany",
                         "State")[0]
    df = df.dropna()
    df["State"] = df["State"].apply(lambda x: remove_in_parens(x))
    color_df = make_color_df(df)
    color_df = change_df_index(color_df, NAMES)
    print(df)
    for i in COLORS.keys():
        make_map(df, color_df, i, f"generated-maps/{i}-map.svg")
    #image_paths = []
    #for party in COLORS.keys():
    #    svg_to_png(f"ready-maps/{party}-map-grad.svg",
    #               f"ready-maps/{party}-map-grad.png")
    #    image_paths += [f"ready-maps/{party}-map-grad.png"]
    #make_image_grid(image_paths, 2, 3).save("ready-maps/grid.png")
    #name = "gradient0.png"
    #generate_gradient((195, 231, 250), (17, 161, 238), 200, 1000).save(name)


if __name__ == "__main__":
    main()