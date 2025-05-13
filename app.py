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

# Layout
app.layout = html.Div([
    html.Div([
        html.Img(src='/assets/logo_universidad.png', style={
            'height': '80px',
            'margin': '20px auto',
            'display': 'block'
        })
    ]),
    html.H1("📊 Dashboard Educativo - Rendimiento de Estudiantes - Semillero de Investigación ONTARE", style={'textAlign': 'center', 'fontFamily': 'Inter, sans-serif'}),
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

# Callback para KPIs
@app.callback(
    Output('kpis', 'children'),
    [Input('prep-course', 'value'),
     Input('gender-radio', 'value'),
     Input('ethnicity-dropdown', 'value')]
)
def actualizar_kpis(prep, gender, eth):
    filtro = df[
        (df['test_preparation_course'] == prep) &
        (df['gender'] == gender) &
        (df['race/ethnicity'] == eth)
    ]
    return [
        tarjeta_kpi("Puntaje Promedio en Matemáticas", filtro['math_score'].mean(), '#1f77b4'),
        tarjeta_kpi("Puntaje Promedio en Lectura", filtro['reading_score'].mean(), '#2ca02c'),
        tarjeta_kpi("Puntaje Promedio en Escritura", filtro['writing_score'].mean(), '#d62728')
    ]

# Callback para los gráficos
@app.callback(
    [Output('scatter-graph', 'figure'),
     Output('box-plot', 'figure'),
     Output('bar-graph', 'figure'),
     Output('histogram-graph', 'figure'),
     Output('heatmap-graph', 'figure'),
     Output('radar-graph', 'figure'),
     Output('pie-graph', 'figure'),
     Output('violin-graph', 'figure'),
     Output('line-graph', 'figure')],
    [Input('prep-course', 'value'),
     Input('gender-radio', 'value'),
     Input('ethnicity-dropdown', 'value')]
)
def actualizar_graficos(prep, gender, eth):
    filtro = df[
        (df['test_preparation_course'] == prep) & 
        (df['gender'] == gender) & 
        (df['race/ethnicity'] == eth)
    ]

    fig1 = px.scatter(filtro, x="math_score", y="reading_score", color="parental_level_of_education", size="writing_score",
                      hover_data=['lunch'], title="📐 Matemáticas vs Lectura", template="plotly_white",
                      color_discrete_sequence=px.colors.qualitative.Prism)

    fig2 = px.box(filtro, x="parental_level_of_education", y="writing_score", color="parental_level_of_education",
                  title="✍️ Escritura por Nivel Educativo de Padres", template="plotly_white",
                  color_discrete_sequence=px.colors.qualitative.Safe)

    barras = df[(df['gender'] == gender) & (df['test_preparation_course'] == prep)]
    fig3 = px.bar(barras.groupby('race/ethnicity')[['math_score', 'reading_score', 'writing_score']].mean().reset_index(),
                  x='race/ethnicity', y=['math_score', 'reading_score', 'writing_score'], barmode='group',
                  title="📊 Promedio de Puntajes por Grupo Socioeconómico", template="plotly_white",
                  labels={"value": "Promedio Puntaje", "race/ethnicity": "Grupo"},
                  color_discrete_sequence=px.colors.qualitative.Bold)

    fig4 = px.histogram(filtro, x="math_score", nbins=20, color="parental_level_of_education",
                        title="📊 Distribución de Puntajes en Matemáticas", template="plotly_white",
                        color_discrete_sequence=px.colors.qualitative.Pastel)

    fig5 = px.imshow(df[["math_score", "reading_score", "writing_score"]].corr(), text_auto=True,
                     color_continuous_scale='Viridis', title="🔍 Correlación entre Puntajes Académicos",
                     template="plotly_white")

    radar_df = filtro[['math_score', 'reading_score', 'writing_score']].mean()
    fig6 = go.Figure()
    fig6.add_trace(go.Scatterpolar(r=radar_df.values, theta=radar_df.index, fill='toself', name='Promedios'))
    fig6.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False,
                       title="📈 Comparación Radar de Puntajes")

    pie_df = filtro['parental_level_of_education'].value_counts().reset_index()
    pie_df.columns = ['Nivel educativo', 'Cantidad']
    fig7 = px.pie(pie_df, values='Cantidad', names='Nivel educativo', title="🧠 Nivel Educativo de Padres",
                  color_discrete_sequence=px.colors.qualitative.Set3)

    fig8 = px.violin(df[df['test_preparation_course'] == prep], x="gender", y="reading_score", color="gender",
                     box=True, points="all", title="📚 Distribución de Lectura por Género", template="plotly_white")

    linea_df = df[df['test_preparation_course'] == prep].groupby("parental_level_of_education")[
        ["math_score", "reading_score", "writing_score"]
    ].mean().reset_index()
    fig9 = px.line(linea_df, x="parental_level_of_education",
                   y=["math_score", "reading_score", "writing_score"], markers=True,
                   title="📉 Tendencias por Educación Parental",
                   labels={"value": "Promedio", "variable": "Materia"}, template="plotly_white")

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
