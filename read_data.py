import pandas as pd
import re


def remove_in_parens(text: str):
    return re.sub("[\(\[].*?[\)\]]", "", text).strip()


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


def main():
    df = get_wiki_tables("https://en.wikipedia.org/wiki"
                          "/2024_European_Parliament_election_in_Germany",
                           "State")[0]
    print(df.to_string())


if __name__ == "__main__":
    main()