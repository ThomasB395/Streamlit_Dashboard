import streamlit as st
from utils.i18n import tr
import pandas as pd
from utils.preps import number_format



def render (df, tables) :
    st.header(tr("Introduction : "))

    st.markdown(tr("""
    En 2020, la pandémie de COVID-19 a frappé le monde entier. Avec les différents confinements, le secteur de l'aviation a été profondément touché par cette crise.  
    À partir des données rendues publiques par le gouvernement, nous tenterons d'évaluer l'impact du COVID-19 sur le secteur de l'aviation commerciale française et la manière dont celui-ci s'est redressé.  
    Nous examinerons ensuite la structure du réseau français.  
    Il est important de noter que les analyses suivantes sont réalisé avec les valeurs des filtres par défault. Pour les visualisations qui ne contienne qu'une année, c'est la derniére année séléctioné qui est pris en compte.  
    """))

    airports = pd.concat([df["departure_airport_code"], df["destination_airport_code"]]).nunique()
    regions = pd.concat([df["departure_territory"], df["destination_territory"]]).nunique()
    c1, c2, c3,c4, c5 = st.columns(5)
    c1.metric(tr("Période"), f"{tables['year'][0]} - {tables['year'][-1]}")
    c2.metric(tr("Liaisons"), df["airport_pair_route"].nunique())
    c3.metric(tr("Aéroports"), airports)
    c4.metric(tr("Régions"), regions)
    c5.metric(tr("Passagers"), number_format(df["direct_passengers_onboard"].sum()))


