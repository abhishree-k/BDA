# Netflix Titles Big-Data Project

## What it does

Loads the Netflix Movies and TV Shows CSV into local MongoDB.
Uses MongoDB aggregation to summarize types, countries, release years, and genres.
Exports CSV results, charts, and a short text summary.

## Run

1. Create a virtual environment and install dependencies: `python -m venv .venv`, then `.venv\Scripts\activate` and `pip install -r requirements.txt`.
2. Set up Kaggle API credentials at `~/.kaggle/kaggle.json` (on Windows: `%USERPROFILE%\.kaggle\kaggle.json`).
3. Download and unzip the dataset into `./data`:
   `kaggle datasets download -d shivamb/netflix-shows -p ./data --unzip`
4. Start local MongoDB, then run `python load.py`, `python process.py`, and `python analyse.py` in order.

`load.py` replaces the collection contents on each run. Aggregation CSVs and four PNG charts are saved in `./output`.
