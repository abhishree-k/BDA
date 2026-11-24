from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR = Path(__file__).parent / "output"


def read_result(filename, columns):
    path = OUTPUT_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Required result file not found: {path}. Run process.py first.")
    return pd.read_csv(path).reindex(columns=columns)


def save_bar(dataframe, category, chart_title, x_label, y_label, filename, horizontal=False):
    figure, axis = plt.subplots(figsize=(10, 5))
    if horizontal:
        axis.barh(dataframe[category], dataframe["count"])
        axis.invert_yaxis()
    else:
        axis.bar(dataframe[category].astype(str), dataframe["count"])
        axis.tick_params(axis="x", labelrotation=35)
    axis.set_title(chart_title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close(figure)


def main():
    type_counts = read_result("type_counts.csv", ["type", "count"])
    countries = read_result("top_countries.csv", ["country", "count"])
    release_years = read_result(
        "titles_by_release_year.csv", ["release_year", "count"]
    ).sort_values("release_year")
    genres = read_result("top_genres.csv", ["genre", "count"])

    save_bar(type_counts, "type", "Netflix Titles by Type", "Type", "Title count", "type_counts.png")
    save_bar(
        countries,
        "country",
        "Top 10 Countries by Netflix Title Count",
        "Title count",
        "Country",
        "top_countries.png",
        horizontal=True,
    )

    figure, axis = plt.subplots(figsize=(10, 5))
    axis.plot(release_years["release_year"], release_years["count"], marker="o")
    axis.set_title("Netflix Titles by Release Year (Last 20 Years)")
    axis.set_xlabel("Release year")
    axis.set_ylabel("Title count")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "titles_by_release_year.png", dpi=150)
    plt.close(figure)

    save_bar(
        genres,
        "genre",
        "Top 10 Netflix Genres",
        "Title count",
        "Genre",
        "top_genres.png",
        horizontal=True,
    )

    total_titles = int(type_counts["count"].sum())
    leading_type = (
        f"{type_counts.loc[type_counts['count'].idxmax(), 'type']} "
        f"({int(type_counts['count'].max())})"
        if not type_counts.empty
        else "no data"
    )
    top_country = (
        f"{countries.iloc[0]['country']} ({int(countries.iloc[0]['count'])})"
        if not countries.empty
        else "no data"
    )
    top_genre = (
        f"{genres.iloc[0]['genre']} ({int(genres.iloc[0]['count'])})"
        if not genres.empty
        else "no data"
    )
    peak_year = (
        f"{int(release_years.loc[release_years['count'].idxmax(), 'release_year'])} "
        f"({int(release_years['count'].max())})"
        if not release_years.empty
        else "no data"
    )
    print(
        "\n".join(
            [
                f"Total titles by type: {total_titles}.",
                f"Most common type: {leading_type}.",
                f"Top country: {top_country}.",
                f"Top genre: {top_genre}.",
                f"Peak release year in the selected range: {peak_year}.",
            ]
        )
    )


if __name__ == "__main__":
    main()
