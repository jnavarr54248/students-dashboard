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

@app.callback(
    Output('kpis', 'children'),
    Input('prep-course', 'value'),
    Input('gender-radio', 'value'),
    Input('ethnicity-dropdown', 'value')
)
def actualizar_kpis(prep, gender, eth):
    filtro = df[(df['test_preparation_course'] == prep) & (df['gender'] == gender) & (df['race/ethnicity'] == eth)]
    return [
        tarjeta_kpi("Puntaje Promedio en Matemáticas", filtro['math_score'].mean(), '#1f77b4'),
        tarjeta_kpi("Puntaje Promedio en Lectura", filtro['reading_score'].mean(), '#2ca02c'),
        tarjeta_kpi("Puntaje Promedio en Escritura", filtro['writing_score'].mean(), '#d62728')
    ]

@app.callback(
    Output('scatter-graph', 'figure'),
    Output('box-plot', 'figure'),
    Output('bar-graph', 'figure'),
    Output('histogram-graph', 'figure'),
    Output('heatmap-graph', 'figure'),
    Output('radar-graph', 'figure'),
    Output('pie-graph', 'figure'),
    Output('violin-graph', 'figure'),
    Output('line-graph', 'figure'),
    Input('prep-course', 'value'),
    Input('gender-radio', 'value'),
    Input('ethnicity-dropdown', 'value')
)
def actualizar_graficos(prep, gender, eth):
    filtro = df[(df['test_preparation_course'] == prep) & (df['gender'] == gender) & (df['race/ethnicity'] == eth)]

    fig1 = px.scatter(filtro, x="math_score", y="reading_score", color="parental_level_of_education", size="writing_score", hover_data=['lunch'], template="plotly_white", title="📐 Matemáticas vs Lectura")
    fig2 = px.box(filtro, x="parental_level_of_education", y="writing_score", color="parental_level_of_education", template="plotly_white", title="✍️ Escritura por Nivel Educativo de Padres")
    barras = df[(df['gender'] == gender) & (df['test_preparation_course'] == prep)]
    fig3 = px.bar(barras.groupby('race/ethnicity')[['math_score', 'reading_score', 'writing_score']].mean().reset_index(), x='race/ethnicity', y=['math_score', 'reading_score', 'writing_score'], barmode='group', template="plotly_white", title="📊 Puntajes por Grupo Socioeconómico")
    fig4 = px.histogram(filtro, x="math_score", nbins=20, color="parental_level_of_education", template="plotly_white", title="📊 Distribución de Matemáticas")
    fig5 = px.imshow(df[["math_score", "reading_score", "writing_score"]].corr(), text_auto=True, color_continuous_scale='Viridis', title="🔍 Correlación entre Puntajes", template="plotly_white")
    radar_df = filtro[['math_score', 'reading_score', 'writing_score']].mean()
    fig6 = go.Figure()
    fig6.add_trace(go.Scatterpolar(r=radar_df.values, theta=radar_df.index, fill='toself'))
    fig6.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False, title="📈 Comparación Radar")
    pie_df = filtro['parental_level_of_education'].value_counts().reset_index()
    pie_df.columns = ['Nivel educativo', 'Cantidad']
    fig7 = px.pie(pie_df, values='Cantidad', names='Nivel educativo', template="plotly_white", title="🧠 Nivel Educativo de Padres")
    fig8 = px.violin(df[df['test_preparation_course'] == prep], x="gender", y="reading_score", color="gender", box=True, points="all", template="plotly_white", title="📚 Lectura por Género")
    linea_df = df[df['test_preparation_course'] == prep].groupby("parental_level_of_education")[["math_score", "reading_score", "writing_score"]].mean().reset_index()
    fig9 = px.line(linea_df, x="parental_level_of_education", y=["math_score", "reading_score", "writing_score"], markers=True, template="plotly_white", title="📉 Tendencias por Educación Parental")
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9

@app.callback(
    Output('conclusiones', 'children'),
    Input('prep-course', 'value'),
    Input('gender-radio', 'value'),
    Input('ethnicity-dropdown', 'value')
)
def generar_conclusiones(prep, gender, eth):
    filtro = df[(df['test_preparation_course'] == prep) & (df['gender'] == gender) & (df['race/ethnicity'] == eth)]
    if filtro.empty:
        return "No hay datos disponibles para los filtros seleccionados."
    avg_math = filtro['math_score'].mean()
    avg_read = filtro['reading_score'].mean()
    avg_write = filtro['writing_score'].mean()
    curso = "con preparación" if prep == "completed" else "sin preparación"
    genero = "mujeres" if gender == "female" else "hombres"
    return html.Div([
        html.H4("📌 Conclusiones del análisis:", style={'fontWeight': '600'}),
        html.P(f"Los estudiantes seleccionados son {genero} del grupo '{eth}' que están {curso}.", style={'marginBottom': '10px'}),
        html.P(f"Presentan un puntaje promedio de {avg_math:.1f} en matemáticas, {avg_read:.1f} en lectura y {avg_write:.1f} en escritura."),
        html.P("Se observa una tendencia en la que el rendimiento en lectura y escritura suele ser más alto que en matemáticas, lo cual puede estar influenciado por factores socioeconómicos o el nivel educativo de los padres.")
    ])

if __name__ == '__main__':
    app.run(debug=True)
