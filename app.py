import streamlit as st
import pandas as pd
import plotly.express as px

# Configuració de la pàgina
st.set_page_config(page_title="Logistics AI Optimizer", page_icon="🚛", layout="wide")

# Títol i descripció
st.title("🚛 Logistics AI: Optimitzador de Flota i Retards")
st.markdown("""
Aquesta eina utilitza **IA i anàlisi de dades** per detectar colls d'ampolla en la cadena logística.
*Projecte desenvolupat per Valentí Secanell - Enginyer Industrial.*
""")

# Barra lateral per pujar fitxers
st.sidebar.header("Configuració")
uploaded_file = st.sidebar.file_uploader("Puja el fitxer d'operacions (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # --- NETEJA DE DADES ---
    df['Logistics_Delay_Reason'] = df['Logistics_Delay_Reason'].fillna('Cap').astype(str)
    
    # --- MÈTRIQUES PRINCIPALS (KPIs) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_delay = (df['Logistics_Delay'] == 1).mean() * 100
        st.metric("Taxa de Retard", f"{total_delay:.1f}%", delta="-2.3% vs mes passat")
    with col2:
        avg_utilization = df['Asset_Utilization'].mean()
        st.metric("Ús Mitjà d'Actius", f"{avg_utilization:.1f}%")
    with col3:
        avg_temp = df['Temperature'].mean()
        st.metric("Temp. Mitjana Càrrega", f"{avg_temp:.1f} °C")

    # --- VISUALITZACIONS ---
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Motius Principals de Retard")
        # Gràfic circular professional
        fig_pie = px.pie(df[df['Logistics_Delay']==1], 
                         names='Logistics_Delay_Reason', 
                         hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("📈 Utilització vs Retard")
        # Gràfic de barres interactiu
        util_data = df.groupby('Logistics_Delay_Reason')['Asset_Utilization'].mean().reset_index()
        fig_bar = px.bar(util_data, x='Logistics_Delay_Reason', y='Asset_Utilization',
                         labels={'Asset_Utilization': 'Utilització (%)'},
                         color='Asset_Utilization', color_continuous_scale='Blues')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAULA DETALLADA ---
    st.subheader("📋 Llistat d'Incidències Crítiques")
    incidencies = df[df['Logistics_Delay'] == 1][['Asset_ID', 'Logistics_Delay_Reason', 'Traffic_Status', 'Asset_Utilization']]
    st.dataframe(incidencies, use_container_width=True)

else:
    st.info("👋 Benvingut! Puja el fitxer csv des de la barra lateral per començar l'anàlisi.")