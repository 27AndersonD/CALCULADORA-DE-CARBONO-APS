import plotly.express as px, plotly.graph_objects as go
import pandas as pd

def plot_breakdown(breakdown: dict):
    df = pd.DataFrame({'sector': list(breakdown.keys()), 'kgCO2e': list(breakdown.values())})
    df = df[df['sector']!='Total']
    fig = px.bar(df, x='sector', y='kgCO2e', text='kgCO2e', title='Emissões por setor')
    fig.update_layout(yaxis_title='kg CO₂e')
    return fig

def plot_sankey(breakdown: dict):
    labels = [k for k in breakdown.keys() if k!='Total'] + ['Total']
    values = [v for k,v in breakdown.items() if k!='Total']
    source=[]; target=[]; val=[]
    for i,v in enumerate(values):
        source.append(i); target.append(len(labels)-1); val.append(v)
    node=dict(label=labels, pad=15, thickness=20)
    link=dict(source=source, target=target, value=val)
    fig = go.Figure(go.Sankey(node=node, link=link))
    fig.update_layout(title_text='Fluxo de emissões por setor')
    return fig
