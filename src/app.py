import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import os
import datetime as dt
import pathlib

bollette = ['BUPA_2022','Cagliari_3piano', 'Cagliari_5piano', 'Villasimius_Serre_Morus']

def get_pandas_data(xlsx_filename: str, xlsx_sheet: str ) -> pd.DataFrame:
   '''
   Load data from /data directory as a pandas DataFrame
   using relative paths. Relative paths are necessary for
   data loading to work in Render.
   '''
   PATH = pathlib.Path('src').parent
   DATA_PATH = PATH.joinpath("data").resolve()
   return pd.read_excel(DATA_PATH.joinpath(xlsx_filename),sheet_name=xlsx_sheet)
consumi1 = get_pandas_data("Bollette.xlsx", bollette)
#creiamo un applicazione web con stile bootstrap
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

server = app.server


app.layout = html.Div([
    dbc.Container([
        dbc.Row([ #definiamo una riga
            dbc.Col([  #definiamo una colonna
                html.H1('Analisi Consumi e Copertura fotovoltaico', #titolo
                    className='text-center', #classe che contiene uno stile
                    style={'color':'white', 'font-family':'--tds-font-family--combined','font-weight': '--tds-heading--font-weight'}
                ), # colore del titolo e font
            ])
        ]),
        dbc.Row([ 
            dbc.Col([  
                html.H4("Seleziona l'abitazione",style={'color':'white','font-family':'--tds-font-family--combined','font-weight': '--tds-heading--font-weight'}),
                dcc.Dropdown(options = [{'label': i, 'value': i} for i in bollette],value='BUPA_2022', id = 'bollette', style ={'width' :'400px','font-family':'--tds-font-family--combined','font-weight': '--tds-heading--font-weight'}),
            ])
        ]),
        dbc.Row([ 
            dbc.Col([ 
                dcc.Graph(id='Consumi')
            ])
        ]),
    ])
    ],style={'background-color':'#000000',
         'background-size': '50%',
         'height':'1130px'
         }
)

@app.callback(
    Output('Consumi', 'figure'),
    Input("bollette", "value"),
)
def mappa(bollette):
    mesi = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
    consumi = consumi1
    fig2 = go.Figure(
            data=[
            go.Bar(name='F1', x=mesi, y=consumi['F1'], hovertemplate= "consumo: %{y}"),
            go.Bar(name='F2', x=mesi, y=consumi['F2'], hovertemplate= "consumo: %{y}"),
            go.Bar(name='F3', x=mesi, y=consumi['F3'], hovertemplate= "consumo: %{y}")
            ])
    
    fig2.update_layout(
        xaxis_title="Mesi",
        yaxis_title="Consumi",
        yaxis_ticksuffix = ' kWh ',
        hoverlabel_font =dict(
            color="#ffffff",
            size=15
        ),
        margin = dict(t=0, l=0, r=0, b=0),
        paper_bgcolor  = '#000000',
        plot_bgcolor  = '#000000',
        legend=dict(
            title="Fasce",
            y=0.5,
            x=1,
            font=dict(

                color="#ffffff"
            )
        ),        
    )
    
    fig2.update_xaxes(color='#ffffff',
                      mirror=True,
                      gridcolor='#000000'
    )
    
    fig2.update_yaxes(color='#ffffff', 
                      gridcolor='#ffffff'
    )
    
    return fig2

    
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False)