import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import joblib

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Page d'accueil
home_layout = html.Div([
    html.H1("Bienvenue à l'application de prédiction de crédit", className="text-center mt-4"),
    html.Div([
        dcc.Link(html.Button("Accéder au formulaire", className="btn btn-primary"), href="/formulaire")
    ], className="text-center mt-4")
])

# Formulaire de prédiction de crédit
prediction_layout = dbc.Container([
     dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Link(html.Button("Retour", className="btn btn-secondary"), href="/"),
            ]),
        ], width=12, className="mb-3"),
    ]),
    html.H1("Prédiction de crédit", className="text-center mt-4"),
    dbc.Row([
        dbc.Col([
            html.Label("Mode de la surface totale", className="font-weight-bold"),
            dcc.Input(id="total_area_mode", type="number", placeholder="Ex : 0.0085", className="form-control"),
        ], width=6, className="mb-3"),
          dbc.Col([
            html.Label("Observations à 30 jours du cercle social", className="font-weight-bold"),
            dcc.Input(id="social_circle_observations", type="number", placeholder="Ex : 10.0", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Âge de la voiture", className="font-weight-bold"),
            dcc.Input(id="car_age", type="number", placeholder="Ex : 17.0", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Montant demandé à l'agence de crédit (année)", className="font-weight-bold"),
            dcc.Input(id="credit_amount_year", type="number", placeholder="Ex : 6.0", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Heure de début du processus", className="font-weight-bold"),
            dcc.Input(id="process_start_time", type="number", placeholder="Ex : 12", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Population relative de la région", className="font-weight-bold"),
            dcc.Input(id="region_population", type="number", placeholder="Ex : 0.018801", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Revenu total", className="font-weight-bold"),
            dcc.Input(id="total_income", type="number", placeholder="Ex : 180000.0", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Montant du crédit", className="font-weight-bold"),
            dcc.Input(id="credit_amount", type="number", placeholder="Ex : 781920.0", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Jours depuis le dernier changement de téléphone", className="font-weight-bold"),
            dcc.Input(id="days_since_last_phone_change", type="number", placeholder="Ex : -22471", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Jours d'enregistrement", className="font-weight-bold"),
            dcc.Input(id="registration_days", type="number", placeholder="Ex : -22471", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Jours depuis la publication de l'identité", className="font-weight-bold"),
            dcc.Input(id="days_since_identity_published", type="number", placeholder="Ex : -1166.0", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Jours depuis la naissance", className="font-weight-bold"),
            dcc.Input(id="days_since_birth", type="number", placeholder="Ex : -22471", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Source externe 2", className="font-weight-bold"),
            dcc.Input(id="external_source_2", type="number", placeholder="Ex : 0.2820694905045227", className="form-control"),
        ], width=6, className="mb-3"),
        dbc.Col([
            html.Label("Source externe 3", className="font-weight-bold"),
            dcc.Input(id="external_source_3", type="number", placeholder="Ex : 0.7713615919194317", className="form-control"),
        ], width=6, className="mb-3"),
    ], className="mb-3"),
    
    dbc.Row([
        dbc.Col(html.Button("Prédire", id="predict-button", className="btn btn-success btn-block"), width=6),
    ], className="mb-4"),
    html.Div(id="output", className="text-center mb-4 font-weight-bold", style={"font-size": "18px"}),
])

# Callback pour gérer la navigation entre les pages
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/formulaire':
        return prediction_layout
    else:
        return home_layout

# Votre logique de prédiction
@app.callback(
    Output("output", "children"),
    [Input("predict-button", "n_clicks")],
    [State("total_area_mode", "value"),
     State("social_circle_observations", "value"),
     State("car_age", "value"),
     State("credit_amount_year", "value"),
     State("process_start_time", "value"),
     State("region_population", "value"),
     State("total_income", "value"),
     State("credit_amount", "value"),
     State("days_since_last_phone_change", "value"),
     State("registration_days", "value"),
     State("days_since_identity_published", "value"),
     State("days_since_birth", "value"),
     State("external_source_2", "value"),
     State("external_source_3", "value")])

def predict_credit(n_clicks, total_area_mode, social_circle_observations, car_age, credit_amount_year, process_start_time, region_population, total_income, credit_amount, days_since_last_phone_change, registration_days, days_since_identity_published, days_since_birth, external_source_2, external_source_3):
    if n_clicks is not None:
        # Prétraitement des données et prédiction
        data = np.array([total_area_mode, social_circle_observations,
                         car_age, credit_amount_year,
                         process_start_time, region_population,
                         total_income, credit_amount,
                         days_since_last_phone_change,
                         registration_days,
                         days_since_identity_published,
                         days_since_birth, external_source_2,
                         external_source_3]).reshape(1, -1)
        
        columns = ['Mode de la surface totale',
                   'Observations à 30 jours du cercle social',
                   'Âge de la voiture', "Montant demandé à l'agence de crédit (année)", 
                   'Heure de début du processus', 'Population relative de la région', 'Revenu total',
                   'Montant du crédit', 'Jours depuis le dernier changement de téléphone',
                   "Jours d'enregistrement", "Jours depuis la publication de l'identité", 
                   'Jours depuis la naissance', 'Source externe 2', 'Source externe 3']
        
        X = pd.DataFrame(data, columns=columns)
        
        # Chargement du modèle
        loaded_rf_model = joblib.load('random_forest_model.pkl')
        
        # Prédiction
        prediction_credit = loaded_rf_model.predict(X)
        
        # Retour de la prédiction
        return f"Prédiction de crédit : {prediction_credit[0]}"
        
    else:
        return ""


# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



if __name__ == '__main__':
    app.run_server(debug=True)

