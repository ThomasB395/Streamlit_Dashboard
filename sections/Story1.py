import streamlit as st
from utils.i18n import tr
import utils.viz as viz


def render (df, tables) :  # We display the visualisation, the text of this analysis and the conclusion of the 1er part

    st.header(tr("Partie 1 : Covid et Aviation"))
    st.markdown(tr("""En 2018, les aéroports français ont accueilli 81,2 millions de passagers, soit une moyenne de 6,76 millions par mois. Ce chiffre servira de référence pour analyser les variations pendant et après la période du Covid et tenter de voir si cette crise a eu un impact sur notre façon de voyager en avion.
    Nous avons choisi l'année 2018 comme référence car il s'agit de la dernière année complète avant que l'on entende parler du Covid."""), unsafe_allow_html=True)

    # Visualisation 1 :
    st.plotly_chart(viz.line_trafic_mensuel(df), use_container_width=True)
    st.markdown(tr("""
    - Jusqu'en février 2020, les chiffres sont restés dans la fourchette de référence de 2018, entre 4,7 et 8,4 millions de passagers. Comme on peut le voir, la baisse a commencé en mars. Le trafic a chuté de 55 % en un  mois, passant de 4,8 à 2,2 millions de passagers. La baisse a atteint son paroxysme en avril, avec une chute de 99,7 % par rapport à 2018. Pour la première fois, le trafic total sur l'ensemble du pays n'a pas dépassé un million de passagers, soit 0,02 million de passagers durant le premier mois du premier confinement.
    - L'été 2020 a connu une légère reprise des déplacements, mais le trafic global reste bien en dessous des chiffres de 2018/2019 malgré la fin du confinement. On comprend que les voyageurs ont eu peur de voyager et d'utiliser les transports en commun.
    - En octobre 2020, le deuxième confinement a été annoncé, et on a observé une nouvelle baisse suivie d'une légère hausse jusqu'au troisième confinement.
    - C'est en juillet 2021 que la courbe montre une réelle amélioration des chiffres. Grâce au pass sanitaire et à la fin de tous les confinements, le nombre de passagers est monté à 3,9 millions en août. L'été suivant, la levée de toutes les restrictions liées au Covid a fait monter le nombre de passagers à 6,35 millions. Néanmoins, on est  encore loin des niveaux précédant la pandémie. Ce n'est qu'en 2023 que le nombre de passagers revient à la normale.
    - Si le trafic ralentit à partir de 2022, ce n'est plus dû au Covid mais dû à des mouvements sociaux. 
    - À partir des Jeux olympiques de Paris, on peut considérer que le trafic est entièrement revenu à la normale. Cependant, il reste, en moyenne, 8% inférieur aux taux de 2018
                </br></br></br>                """)
                , unsafe_allow_html=True)

    # Visualisation 2 :
    st.plotly_chart(viz.heatmap_saisonalite(df), use_container_width=True)
    st.markdown(tr("""
                - Le graphique nous a montré que le trafic revenait progressivement à la normale. En revanche, il ne nous dit pas si le trafic avait retrouvé le même schéma qu'avant la pandémie.
                - Le schéma annuel de base est le suivant : il y a un creux en janvier/février, après quoi le trafic augmente progressivement jusqu'en juillet/août. Le trafic diminue légèrement en septembre/octobre puis plus fortement en décembre. On observe cette tendance en 2018/2019. 
                - En 2020, la heatmap confirme que le trafic s'est arrêté. En 2021, le trafic reprend en été mais reste assez stable vers la fin de l'année. Il n'y a aucun signe de la baisse habituelle de demande en fin d'année.
                - En 2022, bien que l'été ait connu une forte fréquentation, tout comme en 2021, les saisons distinctes ne sont pas encore revenues.
                - Si 2024 a été une année assez floue concernant les saisons de trafic, 2025 confirme un retour au schéma de 2018. On observe de nouveau un pic estival et une chute hivernale. 
                - Si le Covid a eu un impact sur notre façon de voyager, il n'a pas affecté les saisons de pointe. Les habitudes de voyage restent les mêmes qu'avant les confinements. 
                - Cette heatmap nous apprend toutefois quelque chose. On avait pu observer avec la courbe qu'une fois revenu à un trafic normal, celui-ci restait légèrement inférieur aux niveaux d'avant le COVID. Ici, on voit clairement que la baisse est répartie sur toute l'année plutôt que sur un ou deux mois précis. 
                - Il y a donc une baisse du nombre de passagers à l'année qu'il nous faut expliquer. 
                </br></br></br>""")
                ,unsafe_allow_html=True)

    # Visualisation 3 :
    st.plotly_chart(viz.monthly_traffic(df), use_container_width=True)

    # Visualisation 4 :
    if tables['has_ref'] :
        st.plotly_chart(viz.traffic_recovery_index(df), use_container_width=True)
        st.markdown(tr("""
                - Les deux visualisations suivantes visent à montrer l'évolution du trafic, mais en la décomposant en fonction du type de liaison : les vols au départ et à destination de la France métropolitaine (Corse comprise), des territoires d'outre-mer (DOM-TOM), de l'Union européenne et des destinations hors Union européenne. 
                - Le premier graphique montre l'évolution sur la période 2018–2025 (comme le montre la première courbe), mais en la décomposant par type de liaison. 
                - Le second graphique, quant à lui, montre le pourcentage du nombre de passagers retrouvé par rapport aux niveaux d'avant Covid.
                - En 2018/2019, la répartition était la suivante : UE (55%) > Hors UE (24%) > France métropolitaine (16%) > Départements et territoires d'outre-mer (5%). 
                - On remarque que les vols vers les départements et territoires d'outre-mer ne suivent pas les variations saisonnières avec la heatmap. Ces vols restent assez stables tout au long de l'année, contrairement aux autres types de liaisons.
                - Depuis le début du confinement, ce sont les vols intérieurs qui ont maintenu le secteur à flot, en particulier les vols en France métropolitaine. Les vols internationaux se sont complètement effondrés. 
                - Le second graphique montre que si les vols intérieurs en France métropolitaine ont connu la plus faible baisse, ce sont les vols vers les départements et territoires d'outre-mer (DOM-TOM) qui ont rebondi le plus rapidement, atteignant 61 % du trafic de 2018 dès février 2021, alors que le reste du secteur ne dépassait pas 16 % de celui-ci. Cela s'explique par le fait que les contrôles aux frontières restent stricts pour les vols internationaux et par l'existence de moyens de transport alternatifs à l'avion pour se déplacer dans la métropole. 
                - Il est néanmoins intéressant de noter qu'après la fin des contrôles aux frontières en mars 2022, les vols hors UE ont connu une hausse spectaculaire, au point d'être les premiers à retrouver leurs niveaux d'avant crise, dépassant ainsi ceux des départements et territoires d'outre-mer.
                - Pour répondre à la question de savoir ce qui est à l'origine de la baisse des chiffres par rapport à 2018, ce sont les vols intérieurs les fautifs. En 2025, le plus haut volume de vols intérieurs s'élève à 56 % de ceux de 2018. Les vols européens sont également en baisse atteignant 96% du trafic de 2018.
                - La baisse des vols intérieurs est suffisamment importante pour entraîner une diminution globale du trafic, alors qu'à l'international et dans les départements et territoires d'outre-mer, les chiffres n'ont jamais été aussi élevés, avec une hausse de 30 % du nombre de vols internationaux.
                </br></br></br>""")
                ,unsafe_allow_html=True)
    else : st.info(tr("Cette visualisation nécessite les années 2018 à 2025"))

    # Visualisation 5 :
    if tables['has_ref']:
        st.plotly_chart(viz.evolution_of_the_laison(df), use_container_width=True)
        st.markdown(tr("""
                - Ce dernier graphique montre l'évolution des liaisons. Il met en avant les 10 liaisons qui ont le plus profité de la crise du Covid et les 10 liaisons qui en ont le plus souffert.
                - Ce graphique confirme que les liaisons intérieures connaissent une baisse du nombre de passagers. Parmi les 10 liaisons avec les plus fortes baisses, quatre sont nationales et accessibles en TGV. La liaison Paris–Toulouse a connu la plus forte baisse (36 %). La navette Marseille–Paris a perdu 473 000 passagers (33%) en 2025.  
                - Si, en utilisant les filtres, on n'affiche que les vols intérieurs, il n'y a pratiquement aucun gain à signaler pour énormément de pertes. Seuls six vols sont en gain, et ils ne couvrent même pas les pertes de la liaison Paris–Marseille.
                - Les DOM-TOM, en revanche, n'apparaissent pas sur le graphique. Cela confirme ce que l'on peut observer sur les courbes, la demande est à l'équilibre.
                - Lorsque l'on applique le filtre des vols hors UE, il est clair que les vols internationaux vers Singapour et d'autres destinations gagnent en popularité.
                </br></br></br>""")
                , unsafe_allow_html=True)
    else: st.info(tr("Cette visualisation nécessite les années 2018 à 2025"))


    st.header(tr("Conclusion : "))
    st.markdown(tr("""Cette analyse nous a montré que le Covid n'a pas eu d'impact à très long terme sur le secteur. Les données indiquent que seuls les vols intérieurs ont connu une baisse de la demande. Le reste du secteur s'est remis assez rapidement de cette crise internationale, voire en a profité.  
            Il est également important de noter que concernant cette baisse, le Covid n'en est probablement pas le seul facteur. Le jeu de données ne fournit aucune information sur les raisons des hausses ou des baisses. Le Covid a conduit à la découverte d'autres façons de voyager à l'intérieur du pays, il a accéléré le processus, mais il n'est pas le seul responsable de cette baisse. Des facteurs tels que l'impact environnemental et d'autres, bien que non inclus dans le fichier CSV, devraient être pris en compte pour expliquer cette baisse.
    """), unsafe_allow_html=True)