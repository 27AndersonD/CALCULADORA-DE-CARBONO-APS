import streamlit as st, json, os
from app.core.factors import DEFAULT_FACTORS

# language dictionaries
LANG = {
    'pt': {
        'title': '🌿 Calculadora de Carbono — Avançada',
        'results_header': 'Resultado',
        'metric_total': 'Emissões (ano)',
        'metric_trees': 'Equivalente em árvores/ano',
        'metric_note': 'Observação',
        'reference': 'Use fatores locais para maior precisão',
        'details': 'Detalhamento (kg CO₂e/ano)',
        'download_csv': 'Baixar CSV',
        'sidebar_theme': 'Tema visual',
        'sidebar_scope': 'Escopo do cálculo',
        'sidebar_lang': 'Idioma / Language',
        'calc_button': 'Calcular pegada',
        'trees': 'Árvores Necessárias'
    },
    'en': {
        'title': '🌿 Advanced Carbon Calculator',
        'results_header': 'Result',
        'metric_total': 'Emissions (per year)',
        'metric_trees': 'Equivalent trees/year',
        'metric_note': 'Note',
        'reference': 'Adjust local factors for accuracy',
        'details': 'Breakdown (kg CO₂e/year)',
        'download_csv': 'Download CSV',
        'sidebar_theme': 'Visual theme',
        'sidebar_scope': 'Calculation scope',
        'sidebar_lang': 'Idioma / Language',
        'calc_button': 'Calculate footprint',
        'trees': 'trees',
    }
}

def apply_css():
    # choose theme css file (Streamlit will re-run; sidebar stores choice)
    theme = st.session_state.get('theme_choice', 'light')
    css_path = f"app/assets/style_{theme}.css"
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def header():
    # Show title using selected language
    lang = st.session_state.get('lang_choice', 'pt')
    st.markdown(f"<div class='card'><h1>{LANG[lang]['title']}</h1><p class='muted'>Interface avançada e personalizável.</p></div>", unsafe_allow_html=True)

def sidebar_inputs():
    # Theme and language + inputs for multiple scopes
    lang_default = st.session_state.get('lang_choice', 'pt')

    lang_select = st.sidebar.selectbox(
        'Idioma / Language',
        options=['pt', 'en'],
        index=0 if lang_default == 'pt' else 1,
        key='lang_choice'
    )
    i18n = LANG[st.session_state['lang_choice']]

    # Theme choices: light, dark, unip
    theme_default = st.session_state.get('theme_choice', 'light')
    theme = st.sidebar.selectbox(
        i18n['sidebar_theme'],
        options=['light', 'dark', 'unip'],
        index=['light','dark','unip'].index(theme_default),
        key='theme_choice'
    )

    apply_css()

    scope = st.sidebar.selectbox(i18n['sidebar_scope'], options=['personal','enterprise','hybrid'], index=0)

    st.sidebar.markdown('---')
    st.sidebar.subheader('Transporte (km/week)')
    car = st.sidebar.number_input('Car (km/week)', min_value=0.0, value=30.0)
    bus = st.sidebar.number_input('Bus (km/week)', min_value=0.0, value=10.0)
    train = st.sidebar.number_input('Train (km/week)', min_value=0.0, value=15.0)

    st.sidebar.subheader('Energia (mês)')
    elec = st.sidebar.number_input('Electricity (kWh/month)', min_value=0.0, value=180.0)
    gas = st.sidebar.number_input('Gas (m³/month)', min_value=0.0, value=8.0)

    st.sidebar.subheader('Alimentação (kg/week)')
    meat = st.sidebar.number_input('Red meat (kg/week)', min_value=0.0, value=0.5)
    dairy = st.sidebar.number_input('Dairy (kg/week)', min_value=0.0, value=1.0)
    veg = st.sidebar.number_input('Veg & grains (kg/week)', min_value=0.0, value=3.0)

    st.sidebar.subheader('Resíduos (kg/week)')
    waste = st.sidebar.number_input('Waste (kg/week)', min_value=0.0, value=7.0)
    recycle_rate = st.sidebar.slider('Recycling rate (%)', 0,100,30)

    st.sidebar.subheader('Voos (km/year)')
    flights = st.sidebar.number_input('Flights (km/year)', min_value=0.0, value=0.0)

    return {
        'lang': lang_select,
        'i18n': i18n,
        'theme': theme,
        'scope': scope,
        'transport': {'car': car*52, 'bus': bus*52, 'train': train*52},
        'elec_kwh_year': elec*12,
        'gas_m3_year': gas*12,
        'food': {'meat_kg': meat*52, 'dairy_kg': dairy*52, 'veg_kg': veg*52},
        'waste_kg_year': waste*52,
        'recycle_rate': recycle_rate,
        'flights_km_year': flights
    }
