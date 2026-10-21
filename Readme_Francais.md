# Etude du traffic aérien français entre 2018 et 2025. 

Projet : Streamlit Dashboard - Data Storytelling  
Cours : EFREI Paris -  Data Analysis & Visualization - ST2DVZ-2627PSA01  
Auteur : **Bottalico Thomas** [Mail](mailto:thomas.bottalico@efrei.net) | [LinkedIn](https://www.linkedin.com/in/thomas-bottalico/) |  [Github](https://github.com/ThomasB395)  
Référent : **M Mano Mathew Joseph** [Mail](mailto:mano.mathew@efrei.fr) | [LinkedIn](https://www.linkedin.com/in/manomathew/)


## 1. Problématique
1. Quel a été l'impact du Covid-19 sur le traffic aérien francais et le secteur s'est il redressé ? 
2. La reprise est elle la même pour tous les types de liasons (Métropole, Outre-mer, Europe, Hors Europe) ?
3. A quoi ressemble le réseau français aujourd'hui ? Quelles sont les aéroports clé ? Quelle liaisons le portent et a quel points est il concentrè ?


## 2. Données 
| Jeu de données | Source | Licence |
|---|---|---|
| Trafic aérien commercial mensuel français par paire d'aéroports, par sens, depuis 1990 (fichiers `ASP_PAP_2018.csv` à `ASP_PAP_2025.csv`) | DGAC, [data.gouv.fr](https://www.data.gouv.fr/datasets/trafic-aerien-commercial-mensuel-francais-par-paire-daeroports-par-sens-depuis-1990) | Licence Ouverte / Etalab 2.0 |
| Référentiel des aéroports (`airports_ref.csv` : pays, continent, coordonnées) | [OurAirports](https://ourairports.com/data/) | Domaine public |

- La documentation des variables (unités, définitions) est dans `data/Info_Data.pdf`. Elle est reprise dans la section « Variables, unités et définitions » de l'application.
- Le dossier `data/` fait environ 2 Mo : les fichiers sont fournis directement avec le projet.


## 3. Préparation des données
Code : 'utils/load.py', 'utils/preps.py', 'utils/airport_info.py'
- Chargement et concaténation de tous les fichiers `ASP_PAP_*.csv` (séparateur `;`, décimale `,`).
- Renommage des colonnes en noms explicites (ex. `PAP_PAX_FS` → `direct_passengers_onboard`).
- Conversion de `ANMOIS` en date, puis création des colonnes `year` et `month`.
- Extraction des codes OACI de départ et de destination depuis la paire `AAAA_BBBB`.
- Suppression des lignes dont l'aéroport de départ est aussi l'aéroport d'arrivée.
- Jointure avec le référentiel OurAirports : pays, continent, latitude, longitude et territoire français.
- Variables créées :
  - `Domestic/International` : Métropole, Outre-mer, Europe ou Hors Europe.
  - `Mean passengers by flight` = passagers à bord / mouvements commerciaux directs.


## 4. Contenu de l'application
| Section | Contenu |
|---|---|
| Introduction | Contexte, objectifs, KPIs liés aux filtres (période, liaisons, aéroports, régions, passagers) |
| Partie 1 : Covid et aviation | Trafic mensuel avec bande de référence 2018 et événements annotés, heatmap de saisonnalité, trafic par type de liaison, indice de reprise (base 100 = 2018), liaisons gagnantes et perdantes entre 2018 et 2025 |
| Partie 2 : Le réseau français | Carte des aéroports et des principales liaisons, top des liaisons, courbe de concentration, passagers par vol selon la distance |
| Conclusions | Qualité des données (lignes, mois couverts, doublons, valeurs manquantes, contrôles de validation), dictionnaire des variables, limites, points clés et implications |


**Filtres (barre latérale) :** langue (FR/EN), plage d'années, type de liaison, région, aéroport. Ils s'appliquent à toutes les sections.

**Remarques :**
- 2018 est l'année de référence (dernière année complète avant le Covid). Les graphiques comparatifs ont besoin de 2018 et de 2025 dans la plage sélectionnée, sinon un message s'affiche.
- La partie 2 utilise la dernière année sélectionnée.
- Les commentaires sont rédigés à partir des filtres par défaut (2018 à 2025, tous les types de liaisons).

Prérequis : Python version 3.14.

```bash

python -m venv .venv
source .venv/bin/activate       
pip install -r requirements.txt
streamlit run app.py
```

Pour regénérer le référentiel des aéroports à partir d'OurAirports (facultatif, le fichier est déjà fourni) :

```bash

python -m utils.airport_info
```

**Traduction anglaise :** elle passe par Argos Translate. Les traductions déjà faites sont enregistrées dans `utils/translations.json`. Si un texte n'y est pas encore, le modèle français → anglais (environ 100 Mo) est téléchargé une seule fois.

## 6. Structure du projet

```
Streamlit_Dashboard/
├── app.py                 # Page principale : configuration, cache, filtres, enchaînement des sections
├── sections/
│   ├── intro.py           # Contexte, objectifs, KPIs
│   ├── Story1.py          # Partie 1 : Covid et reprise
│   ├── Story2.py          # Partie 2 : structure du réseau
│   └── conclusions.py     # Qualité des données, limites, points clés
├── utils/
│   ├── load.py            # Chargement des CSV
│   ├── preps.py           # Nettoyage, variables créées, tables de qualité
│   ├── viz.py             # Fonctions graphiques Plotly avec un style commun
│   ├── airport_info.py    # Construction du référentiel aéroports (OurAirports)
│   ├── i18n.py            # Traduction FR → EN
│   └── translations.json  # Cache des traductions
├── data/                  # Données DGAC, référentiel aéroports, Info_Data.pdf
├── assets/                # Logo EFREI
└── requirements.txt       # Dépendances avec versions fixées
```

**Performance :** les données nettoyées et les listes des filtres sont mises en cache avec `st.cache_data`. La traduction utilise `st.cache_resource` et un cache sur disque.

## 7. Limites et éthique

- La DGAC ne publie que les liaisons d'au moins 10 000 passagers équivalents par mois, avec au moins 3 opérateurs et aucun opérateur au-dessus de 85 % de l'activité. Les petites liaisons sont donc absentes.
- Les comptages cumulent départs et arrivées.
- La catégorie « Europe » correspond au continent européen (Royaume-Uni et Suisse compris), pas à l'Union européenne.
- Le jeu de données ne donne aucune cause aux variations. Les explications (Covid, grèves, concurrence du TGV, écologie) sont des interprétations, pas des liens de causalité démontrés.
- Les données sont agrégées par liaison et par mois : aucune donnée personnelle, aucun risque de réidentification.