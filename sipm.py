import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# ----------------------------
# DATOS SIMULADOS
# ----------------------------

datos = pd.DataFrame({
    "Localidad": [
        "Tiripetío",
        "Atécuaro",
        "Cuto de la Esperanza",
        "Santiago Undameo",
        "Capula",
        "Tenencia Morelos"
    ],
    "Lat": [
        19.5660,
        19.5930,
        19.7100,
        19.5300,
        19.7000,
        19.6200
    ],
    "Lon": [
        -101.2200,
        -101.2800,
        -101.1700,
        -101.1800,
        -101.2800,
        -101.1200
    ],
    "Tramites": [
        235,
        180,
        145,
        170,
        780,
        1250
    ],
    "Dias_Ultima_Visita": [
        180,
        150,
        120,
        110,
        20,
        10
    ],
    "Distancia_MAC": [
        19,
        17,
        22,
        15,
        8,
        4
    ],
    "Crecimiento": [
        15,
        12,
        18,
        10,
        2,
        1
    ]
})

# ----------------------------
# CALCULO IPA
# ----------------------------

datos["IPA"] = (
    (datos["Tramites"] / datos["Tramites"].max()) * 40 +
    (datos["Dias_Ultima_Visita"] / datos["Dias_Ultima_Visita"].max()) * 30 +
    (datos["Distancia_MAC"] / datos["Distancia_MAC"].max()) * 20 +
    (datos["Crecimiento"] / datos["Crecimiento"].max()) * 10
)

datos["IPA"] = datos["IPA"].round(0)

# ----------------------------
# COLOR PRIORIDAD
# ----------------------------

def color_prioridad(ipa):
    if ipa >= 70:
        return "red"
    elif ipa >= 50:
        return "orange"
    else:
        return "green"

# ----------------------------
# INTERFAZ
# ----------------------------

st.set_page_config(
    page_title="SIPM-IA",
    layout="wide"
)

st.title("📍 SIPM-IA")
st.subheader("Sistema Inteligente de Planeación de Módulos")

# Métricas

col1, col2, col3 = st.columns(3)

col1.metric(
    "Localidades analizadas",
    len(datos)
)

col2.metric(
    "Prioridad Alta",
    len(datos[datos["IPA"] >= 70])
)

col3.metric(
    "Prioridad Media",
    len(datos[(datos["IPA"] >= 50) & (datos["IPA"] < 70)])
)

st.divider()

# Ranking

st.subheader("🏆 Ranking de Prioridades")

ranking = datos.sort_values(
    "IPA",
    ascending=False
)

st.dataframe(
    ranking[
        [
            "Localidad",
            "IPA",
            "Tramites",
            "Dias_Ultima_Visita"
        ]
    ],
    use_container_width=True
)

st.divider()

# MAPA

st.subheader("🗺️ Mapa Inteligente")


from streamlit_folium import st_folium

m = folium.Map(
location=[19.70, -101.18],
zoom_start=10
)

st_folium(
m,
width=800,
height=500
)
#from streamlit_folium import st_folium

#for _, row in datos.iterrows():

 #color = color_prioridad(row["IPA"])

 #folium.CircleMarker(
 #location=[row["Lat"], row["Lon"]],
 #radius=max(8, row["Tramites"] / 100),
 #popup=f"""
 #<b>{row['Localidad']}</b><br>
 #IPA: {row['IPA']}<br>
 #Trámites: {row['Tramites']}
 #""",
 #color=color,
 #fill=True,
 #fill_color=color,
 #fill_opacity=0.8
#).add_to(m) 

st.write("Mapa construido correctamente")
st.write(m)

st_folium(
m,
width=900,
height=600
)

st.divider()

# RECOMENDACIONES

st.subheader("🤖 Recomendaciones Automáticas")

for _, row in ranking.iterrows():

    if row["IPA"] >= 70:

        recomendacion = (
            "Programar módulo móvil prioritario."
        )

    elif row["IPA"] >= 50:

        recomendacion = (
            "Monitorear demanda y evaluar visita."
        )

    else:

        recomendacion = (
            "Cobertura adecuada."
        )

    st.success(
        f"{row['Localidad']} | IPA {row['IPA']} | {recomendacion}"
    )

st.divider()

# SIMULADOR

st.subheader("📈 Simulador de Escenarios")

localidad = st.selectbox(
    "Seleccione localidad",
    datos["Localidad"]
)

fila = datos[
    datos["Localidad"] == localidad
].iloc[0]

st.write("### Situación Actual")

st.write(
    f"""
    Trámites Anuales: {fila['Tramites']}
    
    Última Visita: {fila['Dias_Ultima_Visita']} días
    
    IPA: {fila['IPA']}
    """
)

proyeccion = int(
    fila["Tramites"] * 1.25
)

st.write("### Escenario Propuesto")

st.info(
    f"""
    Si se aumenta la frecuencia de visitas:

    Trámites proyectados: {proyeccion}

    Incremento estimado: 25%
    """
)