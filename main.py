from utils import *
import matplotlib.pyplot
import matplotlib
cmap = matplotlib.colors.LinearSegmentedColormap
COLORS = {"Union": "#585858",
          "AfD": "#11a1ee",
          "SPD": "#e11e29",
          "Grüne": "#47c639",
          "BSW": "#cd3275",
          "FDP": "#ffb800"}

def make_cmap(color: str) -> cmap:
    return cmap.from_list("", ["white", color])


def get_color(colormap: cmap, value: float, max_value: float) -> str:
    value = int(round(255/max_value*value))
    return tuple_to_hex(colormap(value))


def main():
    df = get_wiki_tables("https://en.wikipedia.org/wiki"
                         "/2024_European_Parliament_election_in_Germany",
                         "State")[0]
    df = df.dropna()
    df["State"] = df["State"].apply(lambda x: remove_in_parens(x))
    for column in df.columns:
        try:
            print(column)
            cmap = make_cmap(COLORS[column])
            for value in df[column]:
                print(get_color(cmap, value, max(df[column])))
        except KeyError:
            pass


if __name__ == "__main__":
    main()