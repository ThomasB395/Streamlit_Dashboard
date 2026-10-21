import streamlit as st
from utils.i18n import tr
import utils.viz as viz


def render (df, tables) :

    st.header(tr("Partie 2 : Le réseau français"))
    st.markdown(tr("""Dans cette section, nous allons essayer de voir d'où partent la plupart des vols, où ils vont et quelle est leur popularité. 
    Pour cette section, nous utiliserons l'année la plus récente sélectionnée dans les filtres. Les analyses affiché ci dessous sont faites a partir des chiffres de 2025 
    """), unsafe_allow_html=True)


    last_year = tables['last_year']

    # Visualisation 1 :
    st.plotly_chart(viz.map_airports(df, last_year), use_container_width=True)
    st.markdown(tr("""
    - On peut voir que presque tous les vols partent de Paris (CDG > ORY).
    - Le réseau français suit le modèle du hub, avec notamment AirFrance basée à CDG, puis assure les correspondances vers le reste du pays et du monde.
    </br></br></br>
    """), unsafe_allow_html=True)

    # Visualisation 2 :
    st.plotly_chart(viz.bar_top_routes(df, last_year), use_container_width=True)
    st.markdown(tr("""
    - Nous allons maintenant essayer d'identifier les liaisons qui porte le réseau français.
    - Il est clair que certaines liaisons dominent largement le classement. On retrouve en tête de liste New York, Madrid, Lisbonne, Nice et Montréal.
    - Parmi ces liaisons, il y a des vols long-courriers qui répondent aux besoins des voyages d'affaires comme de tourism. C'est le cas de New York et Montréal.
    - Le même objectif vaut aussi pour les vols en direction de Londres bien que la distance soit plus courte
    - Les liaisons intérieures comme CDG–NCE sont aussi la plupart du temps des trajets professionnels. 
    - Les liaisons court et moyen-courrier (Madrid, Lisbonne) sont fréquentes et portées par le tourisme, d'où leur bon classement.
    - En conclusion, il est clair que certaines liaisons représentent une grande partie du réseau, soutenues par de nombreuses connexions plus petites. 
    - L'affirmation précédente selon laquelle Paris est le hub du réseau est confirmée. Il faut regarder les 36 liaisons les plus fréquentées pour trouver un vol qui ne passe pas par Paris et cette liaison transporte moins d'un million de passagers par an.
    </br></br></br>
    """), unsafe_allow_html=True)

    # Visualisation 3 :
    st.plotly_chart(viz.concentration_curve(df,last_year), use_container_width=True)
    st.markdown(tr("""
    - La courbe monte très fortement au début, puis s'aplatit. Seulement 38 des 289 liaisons 13% du total représentent 50 % du trafic.
    - Une petite minorité de liaisons représente la moitié de tous les passagers, tandis que la grande majorité des liaisons se partage le reste.
    - Le réseau de transport aérien français repose donc sur un petit nombre de liaisons, ce qui signifie que si l'une ou plusieurs d'entre elles venaient à fermer, pour divers raison, cela pourrait avoir un impact important sur le secteur.

    </br></br></br>
    """), unsafe_allow_html=True)

    # Visualisation 4 :
    st.plotly_chart(viz.box_passengers_by_distance(df,last_year), use_container_width=True)
    st.markdown(tr("""
    - Il y a environ 130 passagers par vol sur les liaisons court-courrier et environ 248 sur les liaisons long-courrier. Les vols long-courriers sont donc environ 1,9 fois plus chargés. 
    - Le premier quart des vols long-courriers (219) est supérieur à la limite haute des vols court-courriers (environ 190). Trois vols long-courriers sur quatre transportent donc plus de passagers que presque tous les vols court-courriers
    - L'intervalle des vols long-courriers va de 219 à 307, contre environ 40 pour les vols court-courriers. Les vols long-courriers sont à la fois plus grands et beaucoup plus variables. Les vols court-courriers comptent environ 190 passagers, alors que les vols long-courriers en comptent jusqu'à 422. 
    - Les vols long-courriers transportent environ deux fois plus de passagers par vol que les vols court-courriers, les deux catégories se chevauchant à peine. La distanceest un facteur important. Les gens prennent davantage l'avion pour de longues distances que pour des plus courtes. 
    </br></br></br>
    """), unsafe_allow_html=True)



    st.header(tr("Conclusion : "))
    st.markdown(tr("""
    Le réseau de transport aérien français est un hub centré sur Paris. Quelques liaisons concentrent l'essentiel de l'activité.   
    Cette dépendance est quantifiable : 13 % des liaisons représentent 50 % du trafic. Cela est dû non seulement à la taille des avions mais aussi à l'évolution des mentalités liée à des enjeux de société comme l'écologie'. Les vols long-courriers transportent environ deux fois plus de passagers par vol.  
    Le fait que le réseau repose principalement sur un petit nombre de liaisons pourrait avoir un impact négatif important sur le secteur si une ou plusieurs de ces liaisons aériennes venaient à fermer pour diverses raisons. Un exemple qui vient à l'esprit est la fermeture de nombreuses liaisons e direction du Moyen-Orient en raison de la guerre.
    </br></br></br>
    """), unsafe_allow_html=True)