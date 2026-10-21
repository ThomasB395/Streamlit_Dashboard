# Source of the used data: OurAirports (public domain), https://ourairports.com/data/

import argparse
import glob
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REF_PATH = DATA_DIR / "airports_ref.csv"
OURAIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"


REGION_NAMES = {
    "FR-ARA": "Auvergne-Rhône-Alpes", "FR-BRE": "Bretagne", "FR-COR": "Corse",
    "FR-GES": "Grand Est", "FR-HDF": "Hauts-de-France", "FR-IDF": "Île-de-France",
    "FR-NAQ": "Nouvelle-Aquitaine", "FR-OCC": "Occitanie", "FR-PAC": "Provence-Alpes-Côte d'Azur",
    "FR-PDL": "Pays de la Loire", "GF-CY": "Guyane", "GP-U-A": "Guadeloupe",
    "MQ-U-A": "Martinique", "RE-SD": "La Réunion", "YT-U-A": "Mayotte",
    "PF-U-A": "Polynésie française", "MF-U-A": "Saint-Martin", "BL-U-A": "Saint-Barthélemy",
}

# Airports absent from OurAirports (closed). Added by hand, flagged source="manual".
MANUAL_ROWS = [
    {"apt": "EDDT", "name": "Berlin Tegel Airport", "municipality": "Berlin", "country": "DE",
     "region": "DE-BE", "continent": "EU", "lat": 52.5597, "lon": 13.2877, "source": "manual"},
]


def pair_codes(pattern: str = str(DATA_DIR / "ASP_PAP_*.csv")) -> list[str]:
    pairs = pd.concat([pd.read_csv(f, sep=";", usecols=["PAP"], encoding="utf-8-sig") for f in sorted(glob.glob(pattern))])["PAP"]
    return sorted(set(pairs.str.strip().str.upper().str.split("_").explode()))


def build_ref(codes: list[str], source: str = OURAIRPORTS_URL, out: Path = REF_PATH) -> pd.DataFrame:
    oa = pd.read_csv(
        source, keep_default_na=False, na_values=[""],usecols=["ident", "name", "municipality", "iso_country", "iso_region","continent", "latitude_deg", "longitude_deg"],)
    ref = (oa[oa["ident"].isin(codes)].rename(columns={"ident": "apt", "iso_country": "country", "iso_region": "region","latitude_deg": "lat", "longitude_deg": "lon"}).assign(source="OurAirports"))
    ref = pd.concat([ref, pd.DataFrame(MANUAL_ROWS)], ignore_index=True)
    ref = ref[ref["apt"].isin(codes)].drop_duplicates("apt", keep="first")
    ref["region_name"] = ref["region"].map(REGION_NAMES)
    ref[["lat", "lon"]] = ref[["lat", "lon"]].round(5)
    ref = ref[["apt", "name", "municipality", "country", "region", "region_name","continent", "lat", "lon", "source"]].sort_values("apt")
    ref.to_csv(out, index=False)
    print(f"{len(ref)} airports written to {out} ({len(set(codes) - set(ref['apt']))} codes not found)")
    return ref


def load_airports_ref() :
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=OURAIRPORTS_URL, help="OurAirports airports.csv (url or path)")
    args = parser.parse_args()
    build_ref(pair_codes(), source=args.source)
    airports_ref = pd.read_csv(REF_PATH)
    return airports_ref


if __name__ == "__main__":
    load_airports_ref()