from pathlib import Path

import pandas as pd
from pymongo import MongoClient


MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "bigdata_db"
COLLECTION_NAME = "netflix"
CSV_PATH = Path(__file__).parent / "data" / "netflix_titles.csv"
CHUNK_SIZE = 1000


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {CSV_PATH}. Download and unzip it into ./data first."
        )

    dataframe = pd.read_csv(CSV_PATH)
    records = dataframe.astype(object).where(pd.notna(dataframe), None).to_dict("records")

    with MongoClient(MONGODB_URI) as client:
        collection = client[DATABASE_NAME][COLLECTION_NAME]
        collection.drop()
        inserted_count = 0

        for start in range(0, len(records), CHUNK_SIZE):
            result = collection.insert_many(records[start : start + CHUNK_SIZE])
            inserted_count += len(result.inserted_ids)

    print(f"Inserted {inserted_count} documents into {DATABASE_NAME}.{COLLECTION_NAME}.")


if __name__ == "__main__":
    main()
