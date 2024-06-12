from utils import *
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


def main():
    df = get_wiki_tables("https://en.wikipedia.org/wiki"
                         "/2024_European_Parliament_election_in_Germany",
                         "State")[0]
    df = df.dropna()
    df["State"] = df["State"].apply(lambda x: remove_in_parens(x))
    color_df = make_color_df(df)
    color_df = change_df_index(color_df, NAMES)
    #print(color_df.to_string())
    party = "Union"
    with open("basemap.svg", encoding="UTF-8") as file:
        header_split = """inkscape:window-maximized="1" />"""
        header, paths, footer = split_svg(file.read(), header_split)
        for path in paths:
            fill = [i for i in path.splitlines() if "fill=" in i
                    and "style" not in i][0]
            id = [i for i in path.splitlines() if "id=" in i][0]
            id = re.findall('"([^"]*)"', id)[0]
            print(color_df[party][id])



if __name__ == "__main__":
    main()