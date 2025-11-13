import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from app.ui.layout import apply_css, header, sidebar_inputs
from app.core.calculator import calculate_all
from app.ui.charts import plot_breakdown, plot_sankey
from app.data.exporter import make_report_bytes

st.set_page_config(page_title="Calculadora de Carbono — Avançada", page_icon="🌿", layout="wide")

apply_css()  # injects CSS for selected theme

# Header
header()

# Sidebar inputs (returns a dict of inputs and config)
inputs = sidebar_inputs()

if st.sidebar.button('Calcular pegada'):
    results = calculate_all(inputs)
    total = results['total_after']
    st.header(inputs['i18n']['results_header'])
    c1, c2, c3 = st.columns(3)
    c1.metric(inputs['i18n']['metric_total'], f"{total:,.1f} kg CO₂e")
    c2.metric(inputs['i18n']['metric_trees'], f"{int(total/21)} {inputs['i18n']['trees']}")
    c3.metric(inputs['i18n']['metric_note'], inputs['i18n']['reference'])
    st.plotly_chart(plot_breakdown(results['breakdown']), use_container_width=True)
    st.plotly_chart(plot_sankey(results['breakdown']), use_container_width=True)

    st.subheader(inputs['i18n']['details'])
    st.dataframe(results['details_df'])

    # export
    csv_bytes = make_report_bytes(results['details_df'])
    st.download_button(inputs['i18n']['download_csv'], csv_bytes, file_name='relatorio_carbono.csv', mime='text/csv')
