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
app = dash.Dash(__name__, external_stylesheets=["https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"])
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
        'border-radius': '20px',
        'color': 'white',
        'textAlign': 'center',
        'width': '30%',
        'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
        'fontFamily': 'Poppins, sans-serif'
    })

# Layout
app.layout = html.Div([
    html.Img(src='/assets/logo_universidad.png', style={
        'height': '80px',
        'margin': '20px auto',
        'display': 'block'
    }),

    html.H1("📊 Semillero de Investigación ONTARE - Dashboard Educativo - Rendimiento de Estudiantes", style={'textAlign': 'center', 'fontFamily': 'Poppins, sans-serif', 'color': '#1a202c'}),
    html.P("Explora cómo el género, el entorno socioeconómico y la preparación previa influyen en el desempeño académico.",
           style={'textAlign': 'center', 'padding': '0 50px', 'fontFamily': 'Poppins, sans-serif', 'color': '#4a5568'}),

    html.Div([
        html.Div([
            html.Label("Curso de preparación", style={'fontFamily': 'Poppins, sans-serif'}),
            dcc.Dropdown(
                id='prep-course',
                options=[{'label': val.capitalize(), 'value': val} for val in df['test_preparation_course'].unique()],
                value='none', clearable=False,
                style={'fontFamily': 'Poppins, sans-serif'}
            )
        ], style={'width': '30%', 'padding': '10px'}),

        html.Div([
            html.Label("Género", style={'fontFamily': 'Poppins, sans-serif'}),
            dcc.RadioItems(
                id='gender-radio',
                options=[{'label': i.capitalize(), 'value': i} for i in df['gender'].unique()],
                value='female',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                style={'fontFamily': 'Poppins, sans-serif'}
            )
        ], style={'width': '30%', 'padding': '10px'}),

        html.Div([
            html.Label("Grupo socioeconómico (anónimo)", style={'fontFamily': 'Poppins, sans-serif'}),
            dcc.Dropdown(
                id='ethnicity-dropdown',
                options=[{'label': val, 'value': val} for val in sorted(df['race/ethnicity'].unique())],
                value='Grupo 1 - Condiciones limitadas',
                clearable=False,
                style={'fontFamily': 'Poppins, sans-serif'}
            )
        ], style={'width': '40%', 'padding': '10px'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.Div(id='kpis', style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='scatter-graph', config={'displayModeBar': False}),
        dcc.Graph(id='box-plot', config={'displayModeBar': False}),
        dcc.Graph(id='bar-graph', config={'displayModeBar': False}),
        dcc.Graph(id='histogram-graph', config={'displayModeBar': False}),
        dcc.Graph(id='heatmap-graph', config={'displayModeBar': False}),
        dcc.Graph(id='radar-graph', config={'displayModeBar': False}),
        dcc.Graph(id='pie-graph', config={'displayModeBar': False}),
        dcc.Graph(id='violin-graph', config={'displayModeBar': False}),
        dcc.Graph(id='line-graph', config={'displayModeBar': False})
    ]),

    html.Div(id='conclusiones', style={
        'padding': '30px',
        'fontFamily': 'Poppins, sans-serif',
        'fontSize': '16px',
        'color': '#2d3748',
        'backgroundColor': '#edf2f7',
        'borderTop': '1px solid #cbd5e0',
        'marginTop': '30px'
    }),

    html.Footer("Juan Camilo Navarro Herrera - Estudiante de Maestría en Ciencia de Datos", style={
        'textAlign': 'center',
        'padding': '20px',
        'fontFamily': 'Poppins, sans-serif',
        'color': '#718096',
        'fontSize': '14px'
    })
])