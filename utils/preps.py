import pandas as pd, numpy as np
from utils.airport_info import REF_PATH
RENAME = {
    'ANMOIS': 'flight_period',
    'PAP': 'airport_pair_route',
    'PAP1_LABEL': 'departure_airport',
    'PAP2_LABEL': 'destination_airport',
    'PAP_DIST': 'distance_km',
    'PAP_PEQ': 'local_equivalent_passengers',
    'PAP_PAX': 'local_passengers_total',
    'PAP_FRP': 'local_freight_and_mail_tons',
    'PAP_DRT': 'commercial_services',
    'PAP_MVT': 'direct_commercial_movements',
    'PAP_PEQ_FS': 'direct_equivalent_passengers',
    'PAP_PAX_FS': 'direct_passengers_onboard',
    'PAP_FRP_FS': 'direct_freight_and_mail_tons'}

metropole_domtom = {"France métropolitaine", "La Réunion", "Guadeloupe", "Martinique", "Guyane", "Mayotte", "Polynésie française", "Nouvelle-Calédonie", "Saint-Barthélemy", "Saint-Martin", "Saint-Pierre-et-Miquelon", "Wallis-et-Futuna"}
continent = {"FR": "France métropolitaine", "RE": "La Réunion", "GP": "Guadeloupe", "MQ": "Martinique", "GF": "Guyane", "YT": "Mayotte", "PF": "Polynésie française", "NC": "Nouvelle-Calédonie","BL": "Saint-Barthélemy", "MF": "Saint-Martin", "PM": "Saint-Pierre-et-Miquelon", "WF": "Wallis-et-Futuna"}



#-----------------------------------------------------------------------------------------------------------------------
def add_features(data, airport_ref) :  # The purpose is to add nex feature in the two dataset
    df = data.copy()
    ref = airport_ref.set_index("apt")
    for side in ["departure", "destination"]:
        code = df[f"{side}_airport_code"]
        for col in ["country", "continent", "lat", "lon"]:
            df[f"{side}_{col}"] = code.map(ref[col])
        df[f"{side}_territory"] = df[f"{side}_country"].map(continent)

    both_french = df["departure_territory"].isin(metropole_domtom) & df["destination_territory"].isin(metropole_domtom)
    both_metropole = (df["departure_territory"] == "France métropolitaine") & (df["destination_territory"] == "France métropolitaine")
    df["Domestic/International"] = np.select([both_metropole, both_french, df["destination_continent"] == "EU"],["Métropole", "Outre-mer", "Europe"], default="Hors Europe")
    df["Mean passengers by flight"] = df["direct_passengers_onboard"] / df["direct_commercial_movements"].replace(0, np.nan)
    return df



#-----------------------------------------------------------------------------------------------------------------------
def cleaning (data) :   # The purpose is to clean the data for the vizualisation.
    df = data.copy()

    # We rename the columns to make it easier to understand.
    df = df.rename(columns=RENAME)

    # We convert the period column to a datetime object.
    df["flight_period"] = pd.to_datetime(df["flight_period"], format="%Y%m")
    df.insert(1, "year", df["flight_period"].dt.year)
    df.insert(2, "month", df["flight_period"].dt.month)

    #Airport codes: AAAA_BBBB -> AAAA, BBBB
    codes = df["airport_pair_route"].str.extract(r"^([A-Z0-9]{4})_([A-Z0-9]{4})$")
    df.insert(4,"departure_airport_code", codes[0])
    df.insert(5, "destination_airport_code",codes[1])

    # We delete the line with the same airport of departure and arrival.
    n_before = len(df)
    df = df[codes[0] != codes[1]]
    df["removed_same_airport"] = n_before - len(df)

    # We generate the airport info dataset.
    airport_ref =  pd.read_csv(REF_PATH)
    df = add_features(df,airport_ref)

    return df



#-----------------------------------------------------------------------------------------------------------------------
def route_label (df) : # The purpose is to give the airport pair route
    return df["departure_airport"] + " -> " + df["destination_airport"]



def number_format(x) :  # We format the number format for read more easily.
    if pd.isna(x) : return 'NA'
    for div, unit in [(1e9, "B"), (1e6, "M"), (1e3, "k")]:
        if abs(x) >= div : return f"{x/div:,.0f}{unit}"
        # if the absolute value is more important the the divisor, with divse x by this numer and we put the unit after.
    return 'x'
    # We return x if x is smaller than 1000



def make_tables(df_f) : # return a dictionary with a quality table of the data
    # The parameter are the filtrated dataframe, the metric name and the column of the metric.
    years = sorted(df_f["year"].unique()) # A list with the filter years.

    key = ["flight_period", "airport_pair_route", "departure_airport", "destination_airport", "distance_km", "direct_passengers_onboard", "direct_commercial_movements"]

    no_coord = pd.concat([df_f.loc[df_f["departure_lat"].isna(), "departure_airport_code"],
                          df_f.loc[df_f["destination_lat"].isna(), "destination_airport_code"]])
    quality = pd.DataFrame([
        ("Rows", len(df_f)),
        ("Months covered", f"{df_f['flight_period'].nunique()} / {12 * len(years)}"),
        # Expected: 12 months for each year.
        ("Duplicated route-month rows", int(df_f.duplicated(["flight_period", "airport_pair_route"]).sum())),
        # A route should appear once a month.
        ("Rows with a missing value in a key column", int(df_f[key].isna().any(axis=1).sum())),
        # any(axis=1): at least one NaN in the line.
        ("Airports without coordinates", no_coord.nunique()),
    ], columns=["Check", "Result"])

    quality["Result"] = quality["Result"].astype(str)

    return dict(year = years,last_year=years[-1],has_ref={2018,2025} <= set(years), quality = quality)