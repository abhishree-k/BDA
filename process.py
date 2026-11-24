from datetime import datetime
from pathlib import Path

import pandas as pd
from pymongo import MongoClient


MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "bigdata_db"
COLLECTION_NAME = "netflix"
OUTPUT_DIR = Path(__file__).parent / "output"
CURRENT_YEAR = datetime.now().year
RELEASE_YEAR_CUTOFF = CURRENT_YEAR - 19


def save_result(collection, name, pipeline, columns):
    results = list(collection.aggregate(pipeline))
    dataframe = pd.DataFrame(results, columns=columns)
    dataframe.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    print(f"\n{name}:")
    print(dataframe.to_string(index=False) if not dataframe.empty else "(no results)")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with MongoClient(MONGODB_URI) as client:
        collection = client[DATABASE_NAME][COLLECTION_NAME]

        save_result(
            collection,
            "type_counts",
            [
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "type": "$_id", "count": 1}},
                {"$sort": {"type": 1}},
            ],
            ["type", "count"],
        )

        save_result(
            collection,
            "top_countries",
            [
                {"$match": {"country": {"$type": "string", "$ne": ""}}},
                {"$project": {"countries": {"$split": ["$country", ","]}}},
                {"$unwind": "$countries"},
                {"$project": {"country": {"$trim": {"input": "$countries"}}}},
                {"$match": {"country": {"$ne": ""}}},
                {"$group": {"_id": "$country", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
                {"$limit": 10},
                {"$project": {"_id": 0, "country": "$_id", "count": 1}},
            ],
            ["country", "count"],
        )

        save_result(
            collection,
            "titles_by_release_year",
            [
                {
                    "$match": {
                        "release_year": {
                            "$gte": RELEASE_YEAR_CUTOFF,
                            "$lte": CURRENT_YEAR,
                            "$type": "number",
                        }
                    }
                },
                {"$group": {"_id": "$release_year", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}},
                {"$project": {"_id": 0, "release_year": "$_id", "count": 1}},
            ],
            ["release_year", "count"],
        )

        save_result(
            collection,
            "top_genres",
            [
                {"$match": {"listed_in": {"$type": "string", "$ne": ""}}},
                {"$project": {"genres": {"$split": ["$listed_in", ","]}}},
                {"$unwind": "$genres"},
                {"$project": {"genre": {"$trim": {"input": "$genres"}}}},
                {"$match": {"genre": {"$ne": ""}}},
                {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
                {"$limit": 10},
                {"$project": {"_id": 0, "genre": "$_id", "count": 1}},
            ],
            ["genre", "count"],
        )


if __name__ == "__main__":
    main()
