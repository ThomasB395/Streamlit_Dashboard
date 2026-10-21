import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from matplotlib.colors import LinearSegmentedColormap
from utils.preps import route_label
from utils.i18n import tr

contienent = ["Métropole", "Outre-mer", "Europe", "Hors Europe"]
metropole_domtom = {"France métropolitaine", "La Réunion", "Guadeloupe", "Martinique", "Guyane", "Mayotte", "Polynésie française", "Nouvelle-Calédonie", "Saint-Barthélemy", "Saint-Martin", "Saint-Pierre-et-Miquelon", "Wallis-et-Futuna"}
month = ["January","February","March","April","May","June","July","August","September","October","November","December",]
colors = dict(zip(contienent, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]))
SEQ = ["#e6f0fc", "#b7d3f6", "#6da7ec", "#2a78d6", "#1c5cab", "#0d366b"]
important_element, secondary_element, title1, title2, grid = "#2a78d6", "#c9c7bf", "#0b0b0b", "#52514e", "#ebeae6"


def style(fig, title, xtitle=None, ytitle=None) :
    title, xtitle, ytitle = tr(title), tr(xtitle), tr(ytitle)   # Translation if the user selected English.
    for t in fig.data :
        if getattr(t, "name", None) : t.name = tr(t.name)
    for a in fig.layout.annotations : a.text = tr(a.text)  # The purpose of this function is to have a common style for all the visualisation without rewrite the code for each visualisation.
    fig.update_layout(
        template="plotly_white",
        separators = ", ",  # For mathématical expression. The delimitor between the number an dthe decimal is a coma
        font =dict(family="Arial", size=12, color=title2),
        title = dict(text=title,x=0.5, xanchor ="center", font=dict(size=18, color=title1) ),
        margin = dict(l=10, r=20, t=110, b=90),
        hoverlabel = dict(bgcolor="white", bordercolor=grid, font=dict(size=12, color=title1)),  # For the little box that appears when you hover on a point of the graph.
        legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None)
    )
    fig.update_xaxes(title=xtitle,showgrid=False , gridcolor=grid, linecolor=grid)
    fig.update_yaxes(title=ytitle, gridcolor=grid, linecolor=grid)
    return fig



########################################################################################################################
# PART 1 : Covid & reprise

def line_trafic_mensuel (df) :
    m = df.groupby("flight_period", as_index=False)["direct_passengers_onboard"].sum()
    # as_index+False permit to have a dataframe and not a series. It's like a reset_index
    m["direct_passengers_onboard_in_million"] = m["direct_passengers_onboard"] / 1e6

    # We keep only the data from 2018 for have a referentiel of flight before the covid-19.
    ref = m[m["flight_period"].dt.year==2018]["direct_passengers_onboard_in_million"]

    fig = go.Figure()  # We create a plotly figure object.
    fig.add_hrect(y0=ref.min(), y1=ref.max(),  # Creation of the rectangle that will represent the reference of 2018 trafic.
                  fillcolor=important_element, opacity=0.08,  # Parameter of teh rectangle
                  annotation_text="2018 reference - Before Covid", annotation_position="top left",annotation_yshift=17 , # Permit to put the text on the left in the rectangle and 17 pixels up.
                  annotation_font=dict(size=11, color=title2))  # Text Police informaion

    fig.add_hline(y=ref.mean(), # Add_hline permit to add a horizontal line on the graph.The values here was compute with the mean of the 2018 trafic.
                  line=dict(color=title2, width=1, dash="dot"), # Parameter of the line
                  annotation_text=f"Mean of 2018 : {ref.mean():.1f} M", annotation_position="bottom", annotation_font=dict(size=15, color=title2))  # Text Police informaion

    fig.add_trace(go.Scatter(x=m["flight_period"], y=m["direct_passengers_onboard_in_million"],  # Add_trace add a the Scatter graph to the figure.
                             mode="lines", line=dict(color=important_element, width=2.5),name="Passengers",
                             hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.2f} Million of passengers<extra></extra>")) # Personalisation of the box with the number of passengers.

    events = {"2020-04": tr("1er Confinement"),"2020-10": tr("2éme Confinement"),"2021-04": tr("3éme Confinement"),
              "2021-07": tr("Passe Sanitaire, réouverture partielle"),"2022-02": tr("Fin des controles au frontiére"),"2022-03": tr("Fin du passe vaccinal"), "2022-08": tr("Fin de toues les mesures liées au COVID-19"),
              "2022-12":tr("Gréve des contrôleurs aérien"),"2023-09": tr("Fin de la gréve des contrôleurs aérien"),"2024-01": tr("Annulation de vol due a l'installation de 4-Flight system"), "2024-08": tr("JO de Paris")}

    for key, value in events.items() :
        y = m.loc[m["flight_period"] == key, "direct_passengers_onboard_in_million"]  # Add the number of passegeners on board to the hovertemplate box.
        if y.empty : continue
        fig.add_annotation(x=key, y=y.iloc[0], text=value, showarrow=True, arrowhead=0, arrowcolor=title2, ax=40, ay=-50, font=dict(size=11, color=title2), align="left", bgcolor="rgba(255,255,255,.8)")
        # Add the different events to the graph

    return style(fig, tr("Evolution du traffic aérien"), tr("Année"), tr("Millions de passagers"))



def heatmap_saisonalite (df) :
    table = df.pivot_table(index="year", columns="month", values="direct_passengers_onboard", aggfunc="sum") / 1e6
    # Transform the df in a table with the sum of the passengers on board for each month and each year.
    table.columns = [tr(m) for m in month]   # replace the number of month by the name of the month

    fig = px.imshow(table,text_auto=".1f",aspect="auto", labels=dict(color=tr("Million of passengers"), x=tr("Month"), y=tr("Year")),
    )
    fig.update_yaxes(type="category")  # We display one line by year

    return style(fig, tr("Heatmap du traffic saisonier"), tr("Mois"), tr("Année"))



def monthly_traffic(df, ref_year=2018):
    m = df.groupby(["Domestic/International", "flight_period"], as_index=False)["direct_passengers_onboard"].sum()
    m["M"] = m["direct_passengers_onboard"] / 1e6
    #A dataframe with the number of passenger for each month each year and each type of flight (Domestic, UE, ETC)

    fig = go.Figure()

    # One line per segment, always in the same order, so the colors never change.
    for seg in contienent:
        s = m[m["Domestic/International"] == seg]
        fig.add_trace(go.Scatter(
            x=s["flight_period"], y=s["M"], mode="lines", name=seg, line=dict(color=colors[seg], width=2),
            hovertemplate="%{y:.2f} million passengers<extra></extra>"))


    fig.update_xaxes(hoverformat="%b %Y")     # date shown at the top of the hover box
    return style(fig, tr("Traffic mensuel pour les différents types de vol"),
                 tr("Année"), tr("Millions de passagers"))



def traffic_recovery_index (df) :
    m = df.groupby(["Domestic/International", "year", "month"], as_index=False)["direct_passengers_onboard"].sum()
    #A dataframe with the number of passenger for each month each year and each type of flight (Domestic, UE, ETC)

    base = m[m["year"] == 2018][["direct_passengers_onboard", "month","Domestic/International"]].rename(columns={"direct_passengers_onboard": "base"})
    # We keep only the direct_passengers_onboard, month, Domestic/International data for the 2028 year.
    # We rename the column to have a

    m = m[m["year"] >2018].merge(base, on=["month", "Domestic/International"]).sort_values(["Domestic/International", "year", "month"])
    # We join the data when the year is superior to 2018 to the data of 2018

    roll = m.groupby("Domestic/International")[["direct_passengers_onboard", "base"]].transform(lambda s: s.rolling(3, min_periods=1).sum())
    m["index"] = 100 * roll["direct_passengers_onboard"] / roll["base"]
    m["date"] = pd.to_datetime(dict(year=m["year"], month=m["month"], day=1))
    # the ratio of the passengers on board in the different year compared to 2018

    fig = go.Figure()
    fig.add_hline(y=100, line=dict(color=title2, width=1, dash="dash"))
    for i in contienent :
        s = m[m["Domestic/International"] == i]
        fig.add_trace(go.Scatter(x=s["date"], y=s["index"], mode="lines", name=i, line=dict(color=colors[i], width=2),
                                 customdata=s[["direct_passengers_onboard"]],
                                 hovertemplate=f"<b>{i}</b> - %{{x|%b %Y}}<br>Index: %{{y:.0f}} (100 = 2018)"
                                 "<br>%{customdata[0]:,.0f} passengers on board"))

    return style(fig, "Index sur retour du traffic pour chaque type de vol", tr("Année"), tr("Indice de Traffic"))



def evolution_of_the_laison(df) :
    g = df[df["year"].isin([2018, 2025])].assign(route=route_label)
    p = g.pivot_table(index=["route", "Domestic/International"], columns="year", values="direct_passengers_onboard", aggfunc="sum").dropna().reset_index()
    p["delta"] = (p[2025] - p[2018]) / 1e3
    p["pct"] = 100 * (p[2025] - p[2018]) / p[2018]
    sel = pd.concat([p.nlargest(10,"delta"), p.nsmallest(10,"delta")]).sort_values("delta")

    fig = go.Figure()
    for i in contienent :
        s = sel[sel["Domestic/International"]==i]
        fig.add_trace(go.Bar(x=s["delta"], y=s["route"], orientation="h", name=i, marker_color=colors[i],
                             customdata=s[[2018, 2025, "pct"]],
                             hovertemplate=f"<b>%{{y}}</b> ({i})<br>{2018}: %{{customdata[0]:,.0f}} passengers"
                          f"<br>{2025}: %{{customdata[1]:,.0f}} passengers"
                          "<br>Change: %{x:+,.0f} k (%{customdata[2]:+.0f} %)<extra></extra>"))

        fig.add_vline(x=0, line=dict(color=title2, width=1))
        fig.update_yaxes(categoryorder="array", categoryarray=list(sel["route"]))
        fig.update_layout(barmode="relative", bargap=0.25, height=200 + 25 * len(sel))

    return style(fig,tr("Evolution des liasons aérienne"),tr("Changement dans le nombre de passager annuel"), tr("Liason"))



########################################################################################################################
# Part 2 : A quoi ressemble lé résaux ?

def map_airports(df, year = 2025) :
    d = df[df["year"] == year] # For this part, we keep only the data from 2025 (the latest part of the dataset)
    columns = ["airport", "airport_code", "country", "continent", "territory", "lat", "lon"]
    ends = []
    for i in ["departure", "destination"] :
        e = d[[f"{i}_{c}" for c in columns] + ["direct_passengers_onboard"]]
        ends.append(e.rename(columns=lambda c:c.replace(f"{i}_", "")))
    airports = pd.concat(ends).groupby(columns, as_index=False, dropna=False)["direct_passengers_onboard"].sum()
    airports["direct_passengers_onboard_in_million"] = airports["direct_passengers_onboard"] / 1e6

    airports["zone"] = np.select([airports["territory"]=="France métropolitaine", airports["territory"].notna(), airports["continent"] == "EU"],["Métropole", "Outre-mer", "Europe"], default="Hors Europe")

    fig = go.Figure()

    top = d.groupby(["departure_lat", "departure_lon", "destination_lat", "destination_lon"], as_index=False)["direct_passengers_onboard"].sum()
    top = top.nlargest(50, "direct_passengers_onboard" )
    lat, lon = [], []
    for x,y in top.iterrows() :
        lat +=[y["departure_lat"], y["destination_lat"], None]
        lon +=[y["departure_lon"], y["destination_lon"], None]
    fig.add_trace(go.Scattergeo(lat=lat, lon=lon, mode="lines", line=dict(width=0.8, color=secondary_element),hoverinfo="skip", name="Top 30 routes"))


    biggest_airport = airports["direct_passengers_onboard_in_million"].max()
    for i in contienent :
        s = airports[airports["zone"]==i]
        fig.add_trace(go.Scattergeo(
            lat=s["lat"],lon=s["lon"],name =i,mode="markers", customdata=s[["airport", "direct_passengers_onboard"]],
            marker=dict(size=s["direct_passengers_onboard_in_million"], sizemode="area",sizeref=2*biggest_airport/45**2, sizemin=3,
                        color=colors[i], opacity=0.8, line=dict(width=1, color="white")),
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]:.2f} million passengers<extra></extra>"))

    fig.update_geos(projection_type="natural earth", showcountries=True, countrycolor="white", landcolor="#f1f0ec",
                    showocean=True, oceancolor="#fcfcfb", coastlinecolor=grid, showframe=False,
                    lataxis_range=[-35, 65], lonaxis_range=[-90, 125], domain=dict(x=[0, 1], y=[0, 1]))

    fig = style(fig, tr("Carte des aéroports les plus important"))
    fig.update_layout(height=850, margin=dict(l=0, r=0, t=90, b=0), legend=dict(itemsizing="constant"))
    return fig



def bar_top_routes(df, year = 2025) :
    d = df[df["year"] == year].assign(route = route_label)
    t = d.groupby(["route", "Domestic/International"], as_index=False).agg(
        direct_passengers_onboard=("direct_passengers_onboard", "sum"), distance_km=("distance_km", "first"))
    t = t.nlargest(36, "direct_passengers_onboard").sort_values("direct_passengers_onboard")
    t["direct_passengers_onboard_in_million"] = t["direct_passengers_onboard"] / 1e6

    fig = go.Figure()
    for i in contienent :
        s = t[t["Domestic/International"]==i]
        fig.add_trace(go.Bar(x=s["direct_passengers_onboard_in_million"], y=s["route"], name=i, orientation="h", marker_color=colors[i],
        text=s["direct_passengers_onboard_in_million"],texttemplate="%{x:.2f}" ,textposition="outside", cliponaxis=False,
                      customdata=s[["distance_km"]],
                      hovertemplate=f"<b>%{{y}}</b> ({i})<br>%{{customdata[0]:,.0f}} km"
                                           "<br>%{x:.2f} million passengers<extra></extra>"))

    fig.update_yaxes(categoryorder="array", categoryarray=list(t["route"]))
    fig.update_layout(barmode= "relative", bargap=0.25, height=200+25*36)

    return style(fig,tr("Quel trajet a le plus grand nombre de passagers ?"))


def concentration_curve(df, year = 2025):
    r = df[df["year"] == year].assign(route=route_label).groupby("route")["direct_passengers_onboard"].sum().sort_values(ascending=False)

    c = pd.DataFrame({"route": r.index, "route_rank": range(1, len(r) + 1)})
    c["share_of_passengers"] = 100 * r.cumsum().values / r.sum()
    c["share_of_routes"] = 100 * c["route_rank"] / len(c)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=c["share_of_routes"], y=c["share_of_passengers"], mode="lines",
                             line=dict(color=important_element, width=2.5), fill="tozeroy", fillcolor="rgba(42,120,214,.08)",
                             customdata=c[["route_rank", "route"]],
                             hovertemplate="Top %{customdata[0]} flight (%{x:.0f} % of the flight)"
                                           "<br>= %{y:.1f} % of the passengers<br>Last flight added: %{customdata[1]}<extra></extra>"))
    fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", line=dict(color=secondary_element, width=1, dash="dot"), hoverinfo="skip"))

    for threshold in [50, 80]:
        p = c[c["share_of_passengers"] >= threshold].iloc[0]
        fig.add_annotation(x=p["share_of_routes"], y=p["share_of_passengers"], ax=50, ay=30, arrowhead=0, arrowcolor=title2,
                           text=f"{int(p['route_rank'])} flight ({p['share_of_routes']:.0f} %)<br>= {threshold} % of the traffic",
                           font=dict(size=11, color=title1), align="left", bgcolor="rgba(255,255,255,.8)")
    fig.add_annotation(x=60, y=52, text="Equal share", showarrow=False, textangle=-28, font=dict(size=10, color=title2))

    fig.update_xaxes(range=[0, 100], ticksuffix=" %")
    fig.update_yaxes(range=[0, 101], ticksuffix=" %")
    fig.update_layout(showlegend=False)
    return style(fig, tr(f"Courbe de Concentration "), tr("Pourcentage de vol"), tr("Pourcentage du traffic"))


def box_passengers_by_distance(df, year=2025):
    d = df[(df["year"] == year) & df["Mean passengers by flight"].notna()].assign(route=route_label)
    d["distance_class"] = pd.cut(d["distance_km"], [0, 1500, 4000, float("inf")],
                                 labels=["Short-haul flight (< 1 500 km)", "Medium-haul flight (1 500 - 4 000 km)", "Long-haul flight (> 4 000 km)"])

    fig = go.Figure()
    for i in d["distance_class"].cat.categories:
        s = d[d["distance_class"] == i]
        fig.add_trace(go.Box(y=s["Mean passengers by flight"], name=i, boxpoints="outliers", hovertext=s["route"],
                             marker=dict(color=important_element, size=5, opacity=0.5),
                             line=dict(color=important_element, width=1.5), fillcolor="rgba(42,120,214,.15)"))

    fig.update_yaxes(rangemode="tozero")
    fig.update_layout(showlegend=False)
    return style(fig, tr(f"Nombre de passager en fonction de la distance de vol"), tr("Distance du vol"), tr("Nombre de passager par vol"))

