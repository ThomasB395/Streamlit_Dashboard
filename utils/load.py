# Load of the data

from pathlib import Path
import pandas as pd, glob


def load_data() :
    data_dir = Path(__file__).resolve().parents[1] / 'data'
    files = sorted(glob.glob(str(data_dir/"ASP_PAP_*.csv")))
    frames = []
    for i in files :
        df = pd.read_csv(
            i, sep=";", decimal=",", encoding="utf-8-sig")
            # We convert an object column to a date column for easier manipulation

        frames.append(df)
    return pd.concat(frames, ignore_index=True)
    # The function return a unique dataframe with all the data of all the csv.