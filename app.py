import streamlit as st
import pandas as pd
from utils.load import load_data
from utils.preps import cleaning, make_tables
from utils.i18n import tr
from sections import intro, Story1, Story2, conclusions


#----------------
st.set_page_config(page_title="Tableau de bord de data storytelling", layout="wide")


st.title(tr("Etude du traffic aérien francais entre 2018 et 2025"))
st.caption("""Source : ASP_APT_1990_2025.zip  
           https://www.data.gouv.fr/datasets/trafic-aerien-commercial-mensuel-francais-par-paire-daeroports-par-sens-depuis-1990  
           Licence Libre""")

contienent = ["Métropole", "Outre-mer", "Europe", "Hors Europe"]

@st.cache_data(show_spinner=False) # We keep the result of the function in memory, so that it is not recomputed every time the function is called. It's mandatory because Streamit rerun teh script every time the user change something.
def get_data():
    return cleaning(load_data())  # Return the cleaned dataset



@st.cache_data(show_spinner=False)
def get_options():
    d = get_data()
    territories = pd.concat([d["departure_territory"], d["destination_territory"]]).dropna().unique()   # We create a unique list of all the territories.
    airports = pd.concat([                                               # We use concat for an unique columns for the 2 lines result of the mask.
        d.loc[d["departure_territory"].notna(), "departure_airport"],    # The values of departure_territory are a type of french territory or Nan for other country. notna() keep only the values that are not Nan. Loc keep only the name of the airport for the lines passe this mask.
        d.loc[d["destination_territory"].notna(), "destination_airport"] # Same thing for the destination_territory.
    ]).unique() # Keep only one times each airport.
    return sorted(territories),sorted(airports)        # Return the territories and airports list for the filter list.




def apply_filters(df, years, contienent, territories, airports) :
    # Year in paramete is a tuple with the min and max year of the filter.
    # .between(*years) take the year in th df between the 2 part of the year filter.
    # For Domestic/International, we chek if the value of the line is in the contiennt list of the filter.
    out = df[df['year'].between(*years) & df["Domestic/International"].isin(contienent)]
    if territories : # if they are no territories selected, the filter is not applied.
        out = out[out["departure_territory"].isin(territories) | out["destination_territory"].isin(territories)]
        # We keep the line if the departure and the
    if airports : # Same thing for the airports.
        out = out[out["departure_airport"].isin(airports) | out["destination_airport"].isin(airports)]

    return out



df = get_data()
all_territories, all_airports = get_options()



with st.sidebar:    # This part is for the sidebar of the streamlit.
    st.header("Bottalico Thomas")
    st.markdown("thomas.bottalico@efrei.net")
    st.markdown("Ingénieur Data")
    st.markdown("Année : 2026-2027")



    st.header(tr("Filtres"))

    if "lang" not in st.session_state:
        st.session_state.lang = "fr"  # Français par défaut
    st.sidebar.radio("Langue / Language", ["fr", "en"],
                     format_func=lambda x: {"fr": "Français", "en": "English"}[x],
                     horizontal=True, key="lang")

    y_min, y_max = int(df["year"].min()), int(df["year"].max())
    years = st.slider(tr("Années"), y_min, y_max, (y_min, y_max), key="f_years")
    # We define a slider with the min and the max year of the dateset and the default value of the slider (2028-2025)
    contienent = st.multiselect(tr("Localisation"), contienent, default=contienent, key="f_loc")
    # We define a multiselect with all the localisation in default parameter.
    territories = st.multiselect(tr("Région"), all_territories, key="f_reg")
    # We define a multiselect with all the region. This time we don't have a default value.
    airports = st.multiselect(tr("Aéroport"), all_airports, key="f_apt")
    # Same things for the airport.

    st.markdown(tr("<br>Nom du cours : Data Analysis & Visualization"), unsafe_allow_html=True)
    st.markdown("Code du module : ST2DVZ-2627PSA01", unsafe_allow_html=True)
    st.markdown("Référent : [Mathew Mano Joseph](https://www.linkedin.com/in/manomathew/)")
    st.markdown("[Linkedin](https://www.linkedin.com/in/thomas-bottalico/)", unsafe_allow_html=True)
    st.markdown("[Github](https://github.com/ThomasB395) <br><br>", unsafe_allow_html=True)
    st.image("assets/logo_efrei_paris.png", width=300)





# Return the name of the dataset columns for the metric selected.
df_f = apply_filters(df, years, contienent, territories, airports)
# We stock the result of the filter in this dataframe.



if df_f.empty :         # If the dataframe of the filter is empty, we stop the script and display a warning.
    st.warning(tr("Aucune donnée trouvée"))
    st.stop()




has_ref = {2018, 2025} <= set(df_f["year"])
# Is True if the 2 value are in the set of the year of the filter dataset
# We nedd this because some visualisation need this year for a good functioning.
if not has_ref :       #If the 2 years are not in the filter dataset, we display a warning.
    st.info(tr("Certains graphiques doivent inclure les années 2018 et 2025 dans la plage d'années (année de référence et année finale)."))


tables = make_tables(df_f)

intro.render(df_f, tables)
st.divider()
Story1.render(df_f, tables)
st.divider()
Story2.render(df_f, tables)
st.divider()
conclusions.render(df_f, tables)
st.divider()
