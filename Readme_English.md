# French air traffic study, 2018 to 2025

Project: Streamlit Dashboard - Data Storytelling  
Course: EFREI Paris - Data Analysis & Visualization - ST2DVZ-2627PSA01  
Author: **Thomas Bottalico** [Mail](mailto:thomas.bottalico@efrei.net) | [LinkedIn](https://www.linkedin.com/in/thomas-bottalico/) | [GitHub](https://github.com/ThomasB395)  
Supervisor: **Mano Joseph Mathew** [Mail](mailto:mano.mathew@efrei.fr) | [LinkedIn](https://www.linkedin.com/in/manomathew/)

Online app: [https://thomasb395-streamlit-dashboard-app-ywvvau.streamlit.app/](https://thomasb395-streamlit-dashboard-app-ywvvau.streamlit.app/)  
Source code: [https://github.com/ThomasB395/Streamlit_Dashboard](https://github.com/ThomasB395/Streamlit_Dashboard)


## 1. Problem statement
1. What was the impact of Covid-19 on French air traffic, and has the sector recovered?
2. Is the recovery the same for every type of route (Mainland France, Overseas territories, Europe, Outside Europe)?
3. What does the French network look like today? Which airports are key? Which routes carry it, and how concentrated is it?


## 2. Data
| Dataset | Source | License |
|---|---|---|
| Monthly French commercial air traffic by airport pair and direction since 1990 (files `ASP_PAP_2018.csv` to `ASP_PAP_2025.csv`) | DGAC, [data.gouv.fr](https://www.data.gouv.fr/datasets/trafic-aerien-commercial-mensuel-francais-par-paire-daeroports-par-sens-depuis-1990) | Licence Ouverte / Etalab 2.0 |
| Airport reference table (`airports_ref.csv`: country, continent, coordinates) | [OurAirports](https://ourairports.com/data/) | Public domain |

- The variable documentation (units, definitions) is in `data/Info_Data.pdf`. It is reproduced in the "Variables, units and definitions" section of the app.
- The `data/` folder is about 2 MB: the files are shipped directly with the project.


## 3. Data preparation
Code: `utils/load.py`, `utils/preps.py`, `utils/airport_info.py`
- Loading and concatenation of all the `ASP_PAP_*.csv` files (separator `;`, decimal `,`).
- Columns renamed with explicit names (e.g. `PAP_PAX_FS` → `direct_passengers_onboard`).
- Conversion of `ANMOIS` to a date, then creation of the `year` and `month` columns.
- Extraction of the departure and destination ICAO codes from the `AAAA_BBBB` pair.
- Removal of the rows where the departure airport is also the arrival airport.
- Join with the OurAirports reference table: country, continent, latitude, longitude and French territory.
- Created variables:
  - `Domestic/International`: Mainland France, Overseas, Europe or Outside Europe.
  - `Mean passengers by flight` = passengers on board / direct commercial movements.


## 4. App content
| Section | Content |
|---|---|
| Introduction | Context, objectives, KPIs tied to the filters (period, routes, airports, regions, passengers) |
| Part 1: Covid and aviation | Monthly traffic with a 2018 reference band and annotated events, seasonality heatmap, traffic by route type, recovery index (base 100 = 2018), winning and losing routes between 2018 and 2025 |
| Part 2: The French network | Map of the airports and main routes, top routes, concentration curve, passengers per flight by distance |
| Conclusions | Data quality (rows, months covered, duplicates, missing values, validation checks), data dictionary, limitations, key insights and implications |


**Filters (sidebar):** language (FR/EN), year range, route type, region, airport. They apply to every section.

**Notes:**
- 2018 is the reference year (last full year before Covid). The comparison charts need both 2018 and 2025 in the selected range; otherwise a message is displayed.
- Part 2 uses the last selected year.
- The comments are written for the default filters (2018 to 2025, all route types).


## 5. Installation and launch
```bash

python3.14 --version
```
### 1. MacOS

MacOS (Homebrew), skip if `brew --version` already works :

  Apple Silicon Mac (M1/M2/M3...):
```bash
  
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
```

  Intel Mac: installation not supported (some translation dependencies are not available for Python 3.14 on Intel Mac). Use the online version: [https://thomasb395-streamlit-dashboard-app-ywvvau.streamlit.app/](https://thomasb395-streamlit-dashboard-app-ywvvau.streamlit.app/)

Install Python 3.14:

```bash

brew install python@3.14
```

Run the app :
```bash

python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

To regenerate the airport reference table from OurAirports (optional, the file is already provided):

```bash

python -m utils.airport_info
```

### 2. Windows

Windows (winget, already included in Windows 10/11), skip if `py -3.14 --version` already works:

Install Python 3.14:

```powershell

winget install Python.Python.3.14
```

Run the app (PowerShell):
```powershell

py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks the activation script, run this once, then activate again:
```powershell

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

To regenerate the airport reference table from OurAirports (optional, the file is already provided):

```powershell

python -m utils.airport_info
```

**English translation:** it relies on Argos Translate. Translations already done are saved in `utils/translations.json`. If a text is not there yet, the French → English model (about 100 MB) is downloaded once.


## 6. Project structure

```
Streamlit_Dashboard/
├── app.py                 # Main page: configuration, cache, filters, sections order
├── sections/
│   ├── intro.py           # Context, objectives, KPIs
│   ├── Story1.py          # Part 1: Covid and recovery
│   ├── Story2.py          # Part 2: network structure
│   └── conclusions.py     # Data quality, limitations, key insights
├── utils/
│   ├── load.py            # CSV loading
│   ├── preps.py           # Cleaning, created variables, quality tables
│   ├── viz.py             # Plotly chart functions with a shared style
│   ├── airport_info.py    # Airport reference table builder (OurAirports)
│   ├── i18n.py            # FR → EN translation
│   └── translations.json  # Translation cache
├── data/                  # DGAC data, airport reference table, Info_Data.pdf
├── assets/                # EFREI logo 
└── requirements.txt       # Pinned dependencies
```

**Performance:** the cleaned data and the filter lists are cached with `st.cache_data`. The translation uses `st.cache_resource` and an on-disk cache.


## 7. Limitations and ethics

- The DGAC only publishes routes with at least 10,000 equivalent passengers per month, at least 3 operators and no operator above 85 % of the activity. Small routes are therefore missing.
- Counts combine departures and arrivals.
- The "Europe" category is the European continent (United Kingdom and Switzerland included), not the European Union.
- The dataset gives no cause for the variations. The explanations (Covid, strikes, competition from high-speed trains, environmental concerns) are interpretations, not proven causal links.
- The data is aggregated by route and by month: no personal data, no re-identification risk.


English translation generated by AI from the French version