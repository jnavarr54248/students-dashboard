import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Cargar dataset
url = "https://raw.githubusercontent.com/jnavarr54248/students-performance-dashboard/main/StudentsPerformance.csv"
df = pd.read_csv(url)
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Renombrar valores para mayor interpretabilidad
df['race/ethnicity'] = df['race/ethnicity'].replace({
    'group A': 'Grupo 1 - Condiciones limitadas',
    'group B': 'Grupo 2 - Acceso limitado',
    'group C': 'Grupo 3 - Promedio',
    'group D': 'Grupo 4 - Buen acceso',
    'group E': 'Grupo 5 - Óptimas condiciones'
})

# Inicializar app
app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
])
app.title = "Dashboard Educativo - Profesional"

# Exponer el servidor Flask para Gunicorn
server = app.server

# Estilo para tarjetas KPI
def tarjeta_kpi(titulo, valor, color):
    return html.Div([
        html.H4(titulo, style={'margin': '0', 'fontWeight': '600'}),
        html.H2(f"{valor:.1f}", style={'marginTop': '10px'})
    ], style={
        'background': color,
        'padding': '20px',
        'border-radius': '15px',
        'color': 'white',
        'textAlign': 'center',
        'width': '30%',
        'boxShadow': '2px 2px 15px rgba(0,0,0,0.2)',
        'fontFamily': 'Inter, sans-serif'
    })

# Layout
app.layout = html.Div([
    html.H1("Dashboard Educativo - Semillero ONTARE", style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='prep-course',
            options=[{'label': val.capitalize(), 'value': val} for val in df['test_preparation_course'].unique()],
            value='none'
        ),
        dcc.RadioItems(
            id='gender-radio',
            options=[{'label': val.capitalize(), 'value': val} for val in df['gender'].unique()],
            value='female',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='ethnicity-dropdown',
            options=[{'label': val, 'value': val} for val in df['race/ethnicity'].unique()],
            value='Grupo 1 - Condiciones limitadas'
        )
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),
    html.Div(id='kpis', style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}),
    dcc.Graph(id='scatter-graph')
])

# Callbacks
@app.callback(
    Output('kpis', 'children'),
    [Input('prep-course', 'value'),
     Input('gender-radio', 'value'),
     Input('ethnicity-dropdown', 'value')]
)
def update_kpis(prep, gender, eth):
    filtro = df[
        (df['test_preparation_course'] == prep) &
        (df['gender'] == gender) &
        (df['race/ethnicity'] == eth)
    ]
    return [
        tarjeta_kpi("Matemáticas", filtro['math_score'].mean(), '#1f77b4'),
        tarjeta_kpi("Lectura", filtro['reading_score'].mean(), '#2ca02c'),
        tarjeta_kpi("Escritura", filtro['writing_score'].mean(), '#d62728')
    ]

@app.callback(
    Output('scatter-graph', 'figure'),
    [Input('prep-course', 'value'),
     Input('gender-radio', 'value'),
     Input('ethnicity-dropdown', 'value')]
)
def update_scatter(prep, gender, eth):
    filtro = df[
        (df['test_preparation_course'] == prep) &
        (df['gender'] == gender) &
        (df['race/ethnicity'] == eth)
    ]
    fig = px.scatter(filtro, x='math_score', y='reading_score', color='parental_level_of_education',
                     size='writing_score', hover_data=['lunch'], template='plotly_white')
    return fig

# Ejecutar localmente
if __name__ == '__main__':
    app.run(debug=True)