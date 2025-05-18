import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import classification_report, roc_auc_score, mean_squared_error
import joblib
from sklearn.base import clone
import sys
import os
import pickle
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from ml.betting_config import BettingConfig
def predict(config,X,y,create,combined):
    """
    Generates predictions from raw match data.
    """
    try:
        model = None
        if config is None:
            config = BettingConfig()
        elif isinstance(config, dict):
            config = BettingConfig()
        conf = config.load_config()
        config.from_dict(conf)
        try:
            
            with open('app/generated/model_17-05-2025_19-17-05.pkl', 'rb') as f:
                model = pickle.load(f)
        except:
            raise Exception('Modelo não encontrada.')
        # 2. Load test data
        
        # if X is None or y is None:
        #     X_test = pd.read_csv(get_most_recent_file('x_in_novo','csv'))
        #     y_test = pd.read_csv(get_most_recent_file('y_out_novo','csv'))
        
        actuals_o = pd.read_csv('app/generated/historico_17-05-2025_19-17-00.csv')
        actuals = actuals_o.copy()
        # if create:
        #     actuals = pd.read_csv(get_most_recent_file('actuals', 'csv'))
        # else:
        #     actuals = pd.read_csv(get_most_recent_file('pred', 'csv'))
        pred_df = None
        actuals['Data'] = pd.to_datetime(actuals['Data'], errors='coerce')
        actuals['Data das odds'] = pd.to_datetime(actuals['Data das odds'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        le_placar_1= LabelEncoder()
        le_placar_2 = LabelEncoder()
        actuals['Data_ano'] = actuals['Data'].dt.year
        actuals['Data_dia'] = actuals['Data'].dt.day
        actuals['Data_mes'] = actuals['Data'].dt.month
        actuals['Data das odds_ano'] = actuals['Data das odds'].dt.year
        actuals['Data das odds_dia'] = actuals['Data das odds'].dt.day
        actuals['Data das odds_mes'] = actuals['Data das odds'].dt.month
        actuals['Data das odds_hr'] = actuals['Data das odds'].dt.hour
        actuals['Data das odds_min'] = actuals['Data das odds'].dt.minute
        
        actuals[['Placar Exato_time_1', 'Placar Exato_time_2']] = actuals['Placar Exato'].str.split('-', expand=True)
        
        actuals['Campeonato'] = X['Campeonato']
        actuals['Time da casa'] = X['Time da casa']
        actuals['Time contra'] = X['Time contra']
        # Define columns
        pred_cols = ['Id da partida','Gols time casa','Gols time contra','Gols totais',
                    'Odd Casa Vence','Odd Empate','Odd Visitante Vence','PRED_0','PRED_1',
                    'PRED_2','PRED_3','PRED_4','PROBABILIDADE','CONFIDENCE_LEVEL',
                    'RECOMMENDED_STAKE','Id da partida','Campeonato','Data','Tempo',
                    'Time da casa','Time contra','Gols time casa','Gols time contra',
                    'Gols totais','Odd Over 2.5','Odd Under 2.5','Odd Over 3.5',
                    'Odd Under 3.5','Odd Casa Vence','Odd Empate','Odd Visitante Vence',
                    'Placar Exato','Odd Placar Exato','Data das odds','HORA','COLUNA',
                    'PROBABILIDADE','OUTCOME']
        
    
        target_columns = ['OUTCOME','Odd Over 2.5','Odd Under 2.5','Odd Over 3.5','Odd Under 3.5']
        columns_to_drop = [
            'Data das odds', 'HORA', 'COLUNA', 'Campeonato', 'Data', 'Tempo',
            'Time da casa', 'Time contra', 'Placar Exato', 'Odd Placar Exato',
            'OUTCOME', 'PROBABILIDADE','Odd Over 2.5','Odd Under 2.5','Odd Over 3.5','Odd Under 3.5'
        ]
        for_x = ['Time da casa','Time contra','Campeonato','Gols time casa',
            'Gols time contra','Gols totais','Odd Placar Exato','Data_ano','Data_dia','Data_mes',
            'Data das odds_ano','Data das odds_dia','Data das odds_mes',
            'Data das odds_hr','Data das odds_min','Placar Exato_time_1',
            'Placar Exato_time_2']
        
        X = combined[for_x]
        y = combined[target_columns]
        
        # 3. Make predictions
        predictions = model.predict(X)
        
        if len(predictions.shape) == 1:
            pred_df = pd.DataFrame(predictions, columns=['PREDICTION_SCORE'])
        else:
            pred_df = pd.DataFrame(predictions, columns=[f'PRED_{i}' for i in range(predictions.shape[1])])

        if not create:

        # 5. Add probabilities
            probabilidade_list = []
            for _, row in X_test.iterrows():
                prob_casa = 1 / row['Odd Casa Vence']
                prob_empate = 1 / row['Odd Empate']
                prob_visitante = 1 / row['Odd Visitante Vence']
                total_prob = prob_casa + prob_empate + prob_visitante
                weighted_prob = (prob_casa * 1 + prob_empate * 0.5 + prob_visitante * 0) / total_prob
                probabilidade_list.append(weighted_prob)
            
            pred_df['PROBABILIDADE'] = probabilidade_list
            pred_df['PROBABILIDADE'] = pred_df['PROBABILIDADE']
        
            # 6. Add confidence and stake
            pred_df['CONFIDENCE_LEVEL'] = pred_df['PROBABILIDADE'].apply(
                lambda c: config.calibrar_confianca(c) if pd.notnull(c) else None
            )

            pred_df['RECOMMENDED_STAKE'] = pred_df['CONFIDENCE_LEVEL'].apply(
                lambda c: config.calcular_stake(c) if pd.notnull(c) else None
            )
        # X_test['Time da casa'] = le_home.inverse_transform(X_test['Time da casa'])
        # X_test['Time contra'] = le_away.inverse_transform(X_test['Time contra'])
        # X_test['Campeonato'] = le_league.inverse_transform(X_test['Campeonato'])
        
        # 7. Add model performance score (same for all rows)

        # 8. Join X_test and predictions side by side
        

       # After generating pred_df and before concatenating
        df_concat = pd.concat([combined, X_train], axis=1)
        # 10. Save
        # result_df = result_df.drop(columns=['Data'])
        print(df_concat.columns)
    
    except Exception as e:
        
        print(e)
        
try:
    model = MultiOutputRegressor(GradientBoostingRegressor())
    df = pd.read_csv("app/generated/historico_17-05-2025_19-17-00.csv")
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df['Data das odds'] = pd.to_datetime(df['Data das odds'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    le_home = LabelEncoder()
    le_away = LabelEncoder()
    le_league = LabelEncoder()
    le_placar_1= LabelEncoder()
    le_placar_2 = LabelEncoder()
    df['Data_ano'] = df['Data'].dt.year
    df['Data_dia'] = df['Data'].dt.day
    df['Data_mes'] = df['Data'].dt.month
    df['Data das odds_ano'] = df['Data das odds'].dt.year
    df['Data das odds_dia'] = df['Data das odds'].dt.day
    df['Data das odds_mes'] = df['Data das odds'].dt.month
    df['Data das odds_hr'] = df['Data das odds'].dt.hour
    df['Data das odds_min'] = df['Data das odds'].dt.minute
    
    df[['Placar Exato_time_1', 'Placar Exato_time_2']] = df['Placar Exato'].str.split('-', expand=True)
    
    df['Campeonato'] = le_league.fit_transform(df['Campeonato'])
    df['Time da casa'] = le_home.fit_transform(df['Time da casa'])
    df['Time contra'] = le_away.fit_transform(df['Time contra'])
    # Define columns
    pred_cols = ['Id da partida','Gols time casa','Gols time contra','Gols totais',
                'Odd Casa Vence','Odd Empate','Odd Visitante Vence','PRED_0','PRED_1',
                'PRED_2','PRED_3','PRED_4','PROBABILIDADE','CONFIDENCE_LEVEL',
                'RECOMMENDED_STAKE','Id da partida','Campeonato','Data','Tempo',
                'Time da casa','Time contra','Gols time casa','Gols time contra',
                'Gols totais','Odd Over 2.5','Odd Under 2.5','Odd Over 3.5',
                'Odd Under 3.5','Odd Casa Vence','Odd Empate','Odd Visitante Vence',
                'Placar Exato','Odd Placar Exato','Data das odds','HORA','COLUNA',
                'PROBABILIDADE','OUTCOME']
    
   
    target_columns = ['OUTCOME','Odd Over 2.5','Odd Under 2.5','Odd Over 3.5','Odd Under 3.5']
    columns_to_drop = [
        'Data das odds', 'HORA', 'COLUNA', 'Campeonato', 'Data', 'Tempo',
        'Time da casa', 'Time contra', 'Placar Exato', 'Odd Placar Exato',
        'OUTCOME', 'PROBABILIDADE','Odd Over 2.5','Odd Under 2.5','Odd Over 3.5','Odd Under 3.5'
    ]
    for_x = ['Time da casa','Time contra','Campeonato','Gols time casa',
   'Gols time contra','Gols totais','Odd Placar Exato','Data_ano','Data_dia','Data_mes',
    'Data das odds_ano','Data das odds_dia','Data das odds_mes',
    'Data das odds_hr','Data das odds_min','Placar Exato_time_1',
    'Placar Exato_time_2']

    print(df['Data_ano'])
    X = df[for_x].copy()
    y = df[target_columns].copy()
    print(X.describe())
    print(y.describe())
    
    # Drop rows with missing values
    combined = pd.concat([X, y], axis=1).dropna()
    X = combined[X.columns]
    y = combined[y.columns]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    
    print("Model trained successfully.")
    predict(config=BettingConfig(), combined=combined, create=True,X=X_train,y=y_train)
except Exception as e:
    print(e)
        
    