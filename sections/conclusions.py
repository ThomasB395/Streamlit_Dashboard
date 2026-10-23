import streamlit as st
from utils.i18n import tr
import pandas as pd

# Measure columns of the DGAC file (used for the validation checks).
MEASURES = ["distance_km", "local_equivalent_passengers", "local_passengers_total", "local_freight_and_mail_tons",
            "commercial_services", "direct_commercial_movements",
            "direct_equivalent_passengers", "direct_passengers_onboard", "direct_freight_and_mail_tons"]

# Definitions and units, taken from Info_Data.pdf (DGAC, series ASP_PAP).
# Peq = equivalent passenger: 1 Peq = 1 passenger or 0.1 tonne of freight/mail.
# All the counts are departures and arrivals combined.
DEFINITIONS = pd.DataFrame([
    ("flight_period", "ANMOIS", "Mois (AAAA-MM)", "Période de l'observation"),
    ("airport_pair_route", "PAP", "Codes OACI AAAA_BBBB", "Liaison entre deux aéroports"),
    ("departure_airport", "PAP1_LABEL", "Texte", "Nom du premier aéroport de la liaison"),
    ("destination_airport", "PAP2_LABEL", "Texte", "Nom du second aéroport de la liaison"),
    ("distance_km", "PAP_DIST", "km", "Distance orthodromique entre les deux aéroports"),
    ("local_equivalent_passengers", "PAP_PEQ", "Peq", "Passagers équivalents locaux sur la liaison"),
    ("local_passengers_total", "PAP_PAX", "Passagers", "Passagers locaux sur la liaison"),
    ("local_freight_and_mail_tons", "PAP_FRP", "Tonnes", "Fret et poste locaux sur la liaison"),
    ("commercial_services", "PAP_DRT", "Nombre", "Dessertes commerciales, avec ou sans escale intermédiaire"),
    ("direct_commercial_movements", "PAP_MVT", "Nombre", "Mouvements commerciaux directs (sans escale intermédiaire)"),
    ("direct_equivalent_passengers", "PAP_PEQ_FS", "Peq", "Passagers équivalents à bord des vols directs"),
    ("direct_passengers_onboard", "PAP_PAX_FS", "Passagers", "Passagers à bord des vols directs"),
    ("direct_freight_and_mail_tons", "PAP_FRP_FS", "Tonnes", "Fret et poste à bord des vols directs"),
    ("Mean passengers by flight", "(calculée)", "Passagers / mouvement", "direct_passengers_onboard / direct_commercial_movements"),
    ("Domestic/International", "(calculée)", "Catégorie", "Métropole, Outre-mer, Europe ou Hors Europe, d'après le fichier de référence des aéroports"),
], columns=["Variable", "Colonne source", "Unité", "Définition"])


def _tr_table(d, cols=()):  # Translate the column names and the text cells of the given columns.
    d = d.copy()
    for c in cols:
        d[c] = d[c].map(tr)
    return d.rename(columns=tr)

def render(df, tables) :  # Display the text and the quality metrics of the analysis.
    q = tables["quality"].set_index("Check")["Result"]
    removed = df.attrs.get("removed_same_airport", 0)

    st.header(tr("Conclusions : "))
    st.subheader(tr("Qualité des données et limites"))

    c1, c2, c3 = st.columns(3)
    c1.metric(tr("Lignes"), q["Rows"])
    c2.metric(tr("Mois couverts"), q["Months covered"])
    c3.metric(tr("Lignes dupliquées"), q["Duplicated route-month rows"])

    c4, c5, c6 = st.columns(3)
    c4.metric(tr("Lignes avec une valeur clé manquante"), q["Rows with a missing value in a key column"])
    c5.metric(tr("Aéroports sans coordonnées"), q["Airports without coordinates"])
    c6.metric(tr("Lignes supprimées"), removed)

    # Missing values by column
    st.markdown(tr("**Valeurs manquantes par colonne**"))
    miss = df.isna().sum()
    missing = pd.DataFrame({
        "Colonne": miss.index,
        "Valeurs manquantes": miss.values,
        "Part (%)": (miss.values / len(df) * 100).round(2),
    }).sort_values("Valeurs manquantes", ascending=False)
    st.dataframe(_tr_table(missing), hide_index=True, width="stretch", height=250)
    st.caption(tr("destination_territory posséde de nombreuse valeurs manquantes mais cela n'a aucun impact. La colonne n'est pas utulisé pour les visualisations."))
    st.caption(tr("Les valeurs NaN dans destination_continent et departure_continent concernent tous les aéroports américains. Cela n'a aucun impact non plus sur les visualisations puisqu'un aéroport aux États-Unis n'est pas en Europe et est donc toujours classé « Hors UE »."))

    # Validation checks
    st.markdown(tr("**Contrôles de validation**"))
    ok = lambda n: "OK" if n == 0 else "À vérifier"
    n_neg = int((df[MEASURES] < 0).sum().sum())
    n_dist = int((df["distance_km"] <= 0).sum())
    n_pax_no_mvt = int(((df["direct_passengers_onboard"] > 0) & (df["direct_commercial_movements"] == 0)).sum())
    n_mvt_no_pax = int(((df["direct_passengers_onboard"] == 0) & (df["direct_commercial_movements"] > 0)).sum())
    checks = pd.DataFrame([
        ("Valeurs négatives dans les colonnes de mesure", n_neg, "0", ok(n_neg)),
        ("Distance égale à 0 km (ou moins)", n_dist, "0", ok(n_dist)),
        ("Passagers à bord mais aucun mouvement", n_pax_no_mvt, "0", ok(n_pax_no_mvt)),
        ("Mouvements mais aucun passager", n_mvt_no_pax, "Des vols uniquement cargo sont possibles", "Info"),
    ], columns=["Contrôle", "Lignes / cellules", "Attendu", "Statut"])
    st.dataframe(_tr_table(checks, ["Contrôle", "Attendu", "Statut"]), hide_index=True, width="stretch")

    # Variables, units and definitions
    with st.expander(tr("Variables, unités et définitions (source : Info_Data.pdf)")):
        st.dataframe(_tr_table(DEFINITIONS, ["Unité", "Définition"]), hide_index=True, width="stretch")

    st.info(tr(f"""
    **Limites**
    - Les données sont filtrées par la barre latérale, les contrôles ci-dessus ne concernent que les données sélectionnées.
    - Les lignes avec le même aéroport de départ et de destination ont été supprimées lors du nettoyage.
    - Seules les liaisons avec au moins 10 000 passagers équivalents par mois, au moins 3 opérateurs et aucun opérateur au-dessus de 85 % de l'activité sont publiées. Les petites liaisons sont absentes de ce jeu de données publié par le gouvernement.
    """))

    st.subheader(tr("Points clés et prochaines étapes"))
    st.success(tr("""
    **Points clés** (filtres par défaut, 2018 à 2025)
    - Le choc du Covid a été important mais court. Le trafic a chuté de 99,7 % en avril 2020 par rapport à 2018, et est revenu à des niveaux normaux à partir de 2023.
    - La reprise est inégale. Les vols dans la métropole culminent à 56 % de leur niveau de 2018, alors que les liaisons internationales et d'outre-mer le dépassent.
    - Le réseau est un hub centré sur les aéroports parisiens et en particulier sur CDG.  13 % des liaisons transportent 50 % des passagers, et les vols long-courriers transportent environ 1,9 fois plus de passagers par vol que les court-courriers.

    **Implications**
    - La dépendance à quelques liaisons et à Paris rend le secteur vulnérable à un nouveau choc (sanitaire, guerre, fermeture de l'espace aérien).
    - Les baisses observé sur la reprise ne peuvent pas s'expliquer uniquement par la crise du covid. Kes données ne donnent aucune cause, il s'agit ici d'interprétation. """))