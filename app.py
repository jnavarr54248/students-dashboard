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
app = dash.Dash(__name__, external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"])
app.title = "Dashboard Educativo - Profesional"
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

# Layout principal
app.layout = html.Div([
    html.Img(src='/assets/logo_universidad.png', style={
        'height': '80px',
        'margin': '20px auto',
        'display': 'block'
    }),

    html.H1("📊 Dashboard Educativo - Rendimiento de Estudiantes", style={'textAlign': 'center', 'fontFamily': 'Inter, sans-serif'}),
    html.P("Explora cómo el género, el entorno socioeconómico y la preparación previa influyen en el desempeño académico.",
           style={'textAlign': 'center', 'padding': '0 50px', 'fontFamily': 'Inter, sans-serif'}),

    html.Div([
        html.Div([
            html.Label("Curso de preparación"),
            dcc.Dropdown(
                id='prep-course',
                options=[{'label': val.capitalize(), 'value': val} for val in df['test_preparation_course'].unique()],
                value='none', clearable=False
            )
        ], style={'width': '30%', 'padding': '10px'}),

        html.Div([
            html.Label("Género"),
            dcc.RadioItems(
                id='gender-radio',
                options=[{'label': i.capitalize(), 'value': i} for i in df['gender'].unique()],
                value='female',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            )
        ], style={'width': '30%', 'padding': '10px'}),

        html.Div([
            html.Label("Grupo socioeconómico (anónimo)"),
            dcc.Dropdown(
                id='ethnicity-dropdown',
                options=[{'label': val, 'value': val} for val in sorted(df['race/ethnicity'].unique())],
                value='Grupo 1 - Condiciones limitadas',
                clearable=False
            )
        ], style={'width': '40%', 'padding': '10px'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.Div(id='kpis', style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='scatter-graph'),
        dcc.Graph(id='box-plot')
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),

    html.Div([
        dcc.Graph(id='bar-graph')
    ]),

    html.Div([
        dcc.Graph(id='histogram-graph'),
        dcc.Graph(id='heatmap-graph')
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),

    html.Div([
        dcc.Graph(id='radar-graph'),
        dcc.Graph(id='pie-graph')
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),

    html.Div([
        dcc.Graph(id='violin-graph'),
        dcc.Graph(id='line-graph')
    ], style={'display': 'flex', 'flexWrap': 'wrap'})
])

if __name__ == '__main__':
    app.run(debug=True)
