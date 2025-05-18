import argparse
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
import pathlib
from tkinter import messagebox
from pathlib import Path
from app.ml.betting_config import BettingConfig
from app.bet.main import execute_api_call
from sklearn.preprocessing import LabelEncoder
def get_base_path():
    import os

    # get the current working directory
    current_working_directory = os.getcwd()
    return current_working_directory

def get_generated_path():
    """Get the correct path to generated files"""
    base = get_base_path()
    path = os.path.join(base,'app','generated')
    return path
BASE_DIR = get_base_path()
GENERATED_PATH = get_generated_path()
# from app.file_util import get_most_recent_file
# Parâmetros de confiança e stake (mantém lógica original)
def get_script_relative_path(relative_path):
    """Convert relative path to be based on this script's location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(GENERATED_PATH, relative_path))

import os
import glob
import sys
from pathlib import Path
from datetime import datetime

def get_most_recent_file(base_name, extension):
    """
    Finds the most recent file in the generated directory matching the pattern:
    base_name_DD-MM-YYYY_HH-MM-SS.extension
    
    Args:
        base_name (str): The base name of the file (e.g., "predictions")
        extension (str): File extension without dot (e.g., "csv")
    
    Returns:
        str: Full path to the most recent matching file
        None: If no matching file is found
    """
    # Determine the correct generated directory path
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            # Try MEIPASS first
            gen_dir = Path(sys._MEIPASS) / 'generated'
        else:
            # Fallback to executable directory
            gen_dir = Path(sys.executable).parent / 'generated'
    else:
        # Running in development
        gen_dir = Path(__file__).parent.parent / 'generated'
    
    # Build search pattern
    pattern = os.path.join(get_generated_path(), f"{base_name}_*.{extension}")
    
    # Find all matching files
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    # Find the most recently created file
    most_recent = max(files, key=os.path.getctime)
    
    return most_recent

conf_alta = 0.80
conf_media_min = 0.70
conf_media_max = 0.79
conf_baixa_min = 0.55
conf_baixa_max = 0.69
stake_base = 20.00
stake_alta_pct = 100
stake_media_pct = 50
stake_baixa_pct = 25
def create_dated_filename(name, extension="pkl", directory="."):
    """
    Creates a filename with the format: name_DD-MM-YYYY_HH-MM-SS.ext

    Args:
        name (str): Base name of the file (e.g., 'model')
        extension (str): File extension without dot (e.g., 'pkl', 'csv')
        directory (str): Directory where the file will be placed

    Returns:
        str: Full path to the new dated file
    """
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{name}_{timestamp}.{extension}"
    directory = os.path.join('app',directory)
    full_path = os.path.join(get_generated_path(), filename)
    return full_path
# Dicionário de campeonatos e suas colunas
campeonatos = {
    "Copa":    [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58],
    "Euro":    [2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50,53,56,59],
    "Super":   [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58],
    "Premier": [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57]
}

# Funções de feature extraction e cálculo (importadas ou definidas externamente)

def extrair_features_simuladas(hora, campeonato, coluna, csv_path='historico.csv'):
    """
    Extrai features com base no CSV histórico, hora e campeonato.
    A 'coluna' é tratada como um índice válido ou ID de uma linha no dataframe.
    """
    df = pd.read_csv(csv_path)

    # Normalizar os nomes das colunas (remover espaços e deixar em maiúsculas)
    df.columns = df.columns.str.strip().str.upper()

    # Verificar se as colunas esperadas estão presentes
    required_columns = ['HORA', 'CAMPEONATO', 'COLUNA', 'PROBABILIDADE', 'OUTCOME']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Erro: As seguintes colunas estão ausentes no histórico: {', '.join(missing_columns)}")
        return None

    # Filtrar os dados com base no campeonato e hora
    df_filtrado = df[df['CAMPEONATO'].str.upper() == campeonato.upper()]
    df_filtrado = df_filtrado[df_filtrado['HORA'] == hora]

    # Verificar se o DataFrame filtrado não está vazio
    if df_filtrado.empty:
        print(f"Erro: Nenhum dado encontrado para o campeonato '{campeonato}' na hora '{hora}'")
        return None

    # Agora, buscar a linha correspondente à 'COLUNA' no dataframe filtrado
    linha = df_filtrado[df_filtrado['COLUNA'] == coluna]
    
    # Verificar se a linha foi encontrada
    if linha.empty:
        print(f"Erro: Nenhum dado encontrado para a 'COLUNA' {coluna} no campeonato '{campeonato}' na hora '{hora}'")
        return None

    # Extração das features
    features = {
        'HORA': linha['HORA'].values[0],  # Assumindo que é uma única linha
        'GOLS_TOTAIS': linha.get('GOLS TOTAIS', 'N/A'),  # Utiliza 'N/A' caso a coluna não exista
        'ODD_O25': linha.get('ODD OVER 2.5', 'N/A'),
        'ODD_U25': linha.get('ODD UNDER 2.5', 'N/A'),
        'ODD_O35': linha.get('ODD OVER 3.5', 'N/A'),
        'ODD_U35': linha.get('ODD UNDER 3.5', 'N/A')
    }

    return features

def calcular_probabilidade_ajustada(features):
    """
    Estima a probabilidade ajustada com base nas odds Over 2.5 e Under 2.5.
    """
    try:
        odd_o25 = features['ODD_O25']
        if odd_o25 <= 0:
            return 0.5  # fallback

        prob = 1 / odd_o25  # fórmula inversa da odd (simplificada)
        return round(min(max(prob, 0), 1), 3)
    except Exception as e:
        return 0.5  # fallback se erro

# --- Feedback & Learning Loop ---
def calibrar_confianca(config, prob):
    """Determine confidence level based on probability"""
    if prob >= config.conf_alta:
        return 'alta'
    elif prob >= config.conf_media_min:
        return 'média'
    elif prob >= config.conf_baixa_min:
        return 'baixa'
    else:
        return 'fraca'
def calcular_stake(config, confidence_level):
    """Calculate stake amount based on confidence level"""
    if confidence_level == 'alta':
        return config.stake_base * (config.stake_alta_pct / 100)
    elif confidence_level == 'média':
        return config.stake_base * (config.stake_media_pct / 100)
    elif confidence_level == 'baixa':
        return config.stake_base * (config.stake_baixa_pct / 100)
    return 0  # No bet for 'fraca' confidence
def filter_by_time(df, hora_atual, num_horas):
    """Filter dataframe rows where HORA is within the next num_horas from hora_atual."""
    try:
        
        hora_min = hora_atual
        hora_max = hora_atual + num_horas
        if hora_max >=24:
            hora_max = 23
        print("Filtering between", hora_min, "and", hora_max)
        print("Before filtering, df shape:", df.shape)

        df = df[(df['HORA'] >=hora_min) & (df['HORA'] <= hora_max)]
        print("after filtering, df shape:", df.shape)


        return df

    except Exception as e:
        print(f"Error in filter_by_time: {e}")
        return df
def record_results(pred_csv, actuals_csv, history_csv,horas,max):
    """
    Processes prediction and actuals files with identical structure:
    ['HORA','CAMPEONATO','COLUNA','PROBABILIDADE','OUTCOME']
    Handles COLUNA formatting inconsistencies and removes duplicates.
    """
    try:
        # Read files with standardized column names
        preds = pd.read_csv(pred_csv)
        actuals = pd.read_csv(actuals_csv)
        
        # Standardize column names
        preds.columns = preds.columns.str.upper()
        actuals.columns = actuals.columns.str.upper()
        
        # Convert COLUNA to integer to standardize formatting (e.g., "02" -> 2)
        for df in [preds, actuals]:
            df['COLUNA'] = df['COLUNA'].astype(str).str.strip().str.zfill(2).astype(int)
        
        # For historico, we'll prioritize actuals when available
        if os.path.exists(history_csv):
            historico = pd.read_csv(history_csv)
            historico['COLUNA'] = historico['COLUNA'].astype(str).str.strip().str.zfill(2).astype(int)
        else:
            historico = pd.DataFrame(columns=preds.columns)
        
        # Create composite key for comparison
        preds['KEY'] = preds['HORA'].astype(str) + '_' + preds['CAMPEONATO'] + '_' + preds['COLUNA'].astype(str)
        actuals['KEY'] = actuals['HORA'].astype(str) + '_' + actuals['CAMPEONATO'] + '_' + actuals['COLUNA'].astype(str)
        historico['KEY'] = historico['HORA'].astype(str) + '_' + historico['CAMPEONATO'] + '_' + historico['COLUNA'].astype(str)
        
        # Update historico with actuals where available
        updated_entries = []
        
        # First add all historical entries not in actuals
        mask = ~historico['KEY'].isin(actuals['KEY'])
        updated_entries.append(historico[mask])
        
        # Then add all actuals (overwriting historical entries)
        updated_entries.append(actuals.drop(columns=['KEY']))
        
        # Combine and clean
        merged = pd.concat(updated_entries, ignore_index=True)
        
        # Remove any remaining duplicates (keeping last occurrence)
        merged = merged.drop_duplicates(
            subset=['HORA', 'CAMPEONATO', 'COLUNA'],
            keep='last'
        )
        
        # Save the updated history
        merged[['HORA', 'CAMPEONATO', 'COLUNA', 'PROBABILIDADE', 'OUTCOME']].to_csv(history_csv, index=False)
        
        print(f"Histórico atualizado com {len(merged)} registros únicos")
        print(f"Novos registros adicionados: {len(actuals)}")
        
    except Exception as e:
        print(f"Erro ao processar arquivos: {str(e)}")
        


def train_model(input_csv, x_path, y_path, model_path, x_old_path=None, y_old_path=None, error_weight=0.2):
    """
    Trains a DecisionTree model with multi-output support and proper preprocessing.
    
    Returns:
        tuple: (X_test, y_test) DataFrames if successful, None if failed
    """
    try:
        model = MultiOutputRegressor(GradientBoostingRegressor())
        df = pd.read_csv(get_most_recent_file('historico','csv'))
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
        # with open(create_dated_filename('model', 'pkl'), "wb") as f:
        #     pickle.dump((model, X_train.columns.tolist()), f)
        with open(create_dated_filename('model', 'pkl'), "wb") as f:
            pickle.dump(model, f)
        return X_train, y_train, le_home, le_away, le_league, combined
    except Exception as e:
        print(f'Erro no treinamento {e}')
        return None, None
            
        

def predict(config, model_path, x_path, y_path, hora, max,X,y,create,le_home, le_away, le_league, combined):
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
            
            with open(get_most_recent_file('model','pkl'), 'rb') as f:
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

        
        
        # X_test['Time da casa'] = le_home.inverse_transform(X_test['Time da casa'])
        # X_test['Time contra'] = le_away.inverse_transform(X_test['Time contra'])
        # X_test['Campeonato'] = le_league.inverse_transform(X_test['Campeonato'])
        
        # 7. Add model performance score (same for all rows)

        # 8. Join X_test and predictions side by side
        

       # After generating pred_df and before concatenating
        df_concat = pd.concat([combined, actuals_o], axis=1)
        df_concat = pd.concat([df_concat, pred_df], axis=1)
        # 10. Save
        # result_df = result_df.drop(columns=['Data'])

        output_path = create_dated_filename(name='pred',extension='csv')
        df_concat.to_csv(output_path, index=False)
        print(f"Predictions saved successfully to {output_path}")
    
    except Exception as e:
        if str(e).startswith("Input X contains NaN."):
            messagebox.showwarning('Problemas na Previsão', 'Provavelmente alguns campos de algumas das tabelas geradas pela api estão nulas.')
            print(e)
            return 
        messagebox.showerror('Problema na Previsão',e)
        print(e)
        

def concatenate_csv_files(file_list):
    """
    Given a list of CSV file paths, returns a single concatenated DataFrame.
    
    Parameters:
        file_list (list of str): Paths to CSV files
    
    Returns:
        pd.DataFrame: Concatenated DataFrame
    """
    dfs = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            print(f"❌ Failed to read '{file}': {e}")
    
    if not dfs:
        print("⚠️ No valid CSVs were read.")
        return pd.DataFrame()  # Return empty DataFrame

    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df
def get_all_table_csv_from_generated():
    files = []
    # Specify the directory path
    directory = get_generated_path()
    
    # List all files in the directory
    for filename in os.listdir(directory):
        # Check if the file starts with 'table' and ends with '.csv'
        if filename.startswith('tabela') and filename.endswith('.csv'):
            # Get the full path of the file
            full_path = os.path.join(directory, filename)
            files.append(full_path)
    
    return files        
def generate_actuals_from_existing_data(input_file, output_file, horas, max):
    """
    Generates actuals file by appending processed columns to the original data.
    Adds: HORA, COLUNA, PROBABILIDADE, OUTCOME
    """
    df = None
    if input_file:
        df = concatenate_csv_files(input_file)
    else:
        df = concatenate_csv_files(get_all_table_csv_from_generated())
    print(get_most_recent_file('tabela','csv'))
    
    hora_list = []
    coluna_list = []
    probabilidade_list = []
    outcome_list = []
    campeonato_list = []
    for _, row in df.iterrows():
        
        # Calculate normalized probabilities
        prob_casa = 1 / row['Odd Casa Vence']
        prob_empate = 1 / row['Odd Empate']
        prob_visitante = 1 / row['Odd Visitante Vence']
        total_prob = prob_casa + prob_empate + prob_visitante

        weighted_prob = (prob_casa * 1 + prob_empate * 0.5 + prob_visitante * 0) / total_prob
        # campeonat_num = 0
        # campeonato = row['Campeonato']
        # if campeonato.lower()=='euro':
        #     campeonat_num = 0
        # elif campeonato.lower()=='copa':
        #     campeonat_num = 1
        # elif campeonato.lower()=='premier':
        #     campeonat_num = 2
        # elif campeonato.lower()=='super':
        #     campeonat_num = 3 
        # else:
        #     campeonat_num = 4
        # Determine actual outcome
        gols_casa = row['Gols time casa']
        gols_contra = row['Gols time contra']

        if gols_casa > gols_contra:
            outcome = 2  # Home win
        elif gols_casa == gols_contra:
            outcome = 1  # Draw
        else:
            outcome = 0  # Away win
        
        
        probabilidade_list.append(weighted_prob)
        outcome_list.append(outcome)
        # campeonato.append()
    # Add new columns to original DataFrame
    df['Tempo'] = pd.to_datetime(df['Tempo'], format='%H:%M', errors='coerce')

    df['HORA'] = df['Tempo'].dt.hour
    df['COLUNA'] = df['Tempo'].dt.minute
    df['PROBABILIDADE'] = probabilidade_list
    df['OUTCOME'] = outcome_list
    df['OUTCOME'] = df['OUTCOME'].astype(int)
    df['Campeonato'] = df['Campeonato'].astype(str)
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d', errors='coerce')
    df['Data das odds'] = pd.to_datetime(df['Data das odds'], format='%d-%m-%Y %H:%M', errors='coerce')
    df['PROBABILIDADE'] = df['PROBABILIDADE'].astype(float)
    df['Tempo'] = pd.to_datetime(df['Tempo'], format='%H:%M', errors='coerce')
    df['Time da casa'] = df['Time da casa'].astype(str)
    df['Time contra'] = df['Time contra'].astype(str)
    df['Odd Over 2.5'] = df['Odd Over 2.5'].astype(float)
    df['Odd Over 3.5'] = df['Odd Over 3.5'].astype(float)
    df['Odd Under 2.5'] = df['Odd Under 2.5'].astype(float)
    df['Odd Under 3.5'] = df['Odd Under 3.5'].astype(float)
    df['Odd Casa Vence'] = df['Odd Casa Vence'].astype(float)
    df['Odd Empate'] = df['Odd Empate'].astype(float)
    df['Odd Visitante Vence'] = df['Odd Visitante Vence'].astype(float)
    df['Placar Exato'] = df['Placar Exato'].astype(str)
    df['Odd Placar Exato'] = df['Odd Placar Exato'].astype(float)
    output_file = create_dated_filename(extension='csv',name='historico')
    # df = filter_by_time(df=df,hora_atual=horas,num_horas=max)
    # Save result
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} match records with calculated outcomes.")

def record_results(pred_csv, actuals_csv, history_csv):
    """
    Simplified version that just updates the history with new data
    """
    new_data = pd.read_csv(actuals_csv)
    
    if os.path.exists(history_csv):
        history = pd.read_csv(history_csv)
        # Update existing records and append new ones
        combined = pd.concat([history, new_data])
    else:
        combined = new_data
    
    combined.to_csv(history_csv, index=False)
    print(f"History updated with {len(combined)} records")

# Main block
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline Grisamanus com Feedback')
    sub = parser.add_subparsers(dest='cmd')

    # Subcommand to generate actuals.csv
    p_generate_actuals = sub.add_parser('generate_actuals', help='Gerar arquivo de resultados reais (actuals.csv)')
    p_generate_actuals.add_argument('input', help='CSV com dados históricos de jogos')
    p_generate_actuals.add_argument('output', help='CSV de saída com resultados reais (actuals.csv)')

    # Existing subcommands
    p_rec = sub.add_parser('feedback', help='Atualizar histórico com resultados')
    p_rec.add_argument('pred', help='CSV de previsões')
    p_rec.add_argument('actuals', help='CSV de resultados reais')
    p_rec.add_argument('history', help='CSV histórico acumulado')

    p_train = sub.add_parser('train', help='Treinar modelo a partir do histórico')
    p_train.add_argument('history', help='CSV histórico com outcomes')
    p_train.add_argument('model', help='Path para salvar modelo')

    p_pred = sub.add_parser('predict', help='Gerar previsões usando modelo')
    p_pred.add_argument('input', help='CSV com dados a prever')
    p_pred.add_argument('model', help='Modelo treinado (.pkl)')
    p_pred.add_argument('output', help='CSV de saída com previsões')

    args = parser.parse_args()

    # Handle the subcommands
    if args.cmd == 'generate_actuals':
        generate_actuals_from_existing_data(args.input, args.output)
    elif args.cmd == 'feedback':
        record_results(args.pred, args.actuals, args.history)
    elif args.cmd == 'train':
        train_model(args.history, args.model)
    elif args.cmd == 'predict':
        predict(args.input, args.model, args.output)
    else:
        parser.print_help()


def generate_actuals(input_csv, actuals_csv):
 
    generate_actuals_from_existing_data(input_csv, actuals_csv)

def execute( actuals_path, model_path,x_path,y_path,input_csv=None,x_old_path=None,y_old_path=None,train=True,create=True,pred_path=None,history_path=None,config=None,hora=0, max=24):
    if (not x_path) and not actuals_path:
        try:
            x_path = get_most_recent_file('x_in_novo', 'csv')
        except Exception as e:
            pass
    if input_csv == '' or input_csv==None:
        try:
            input_csv = get_most_recent_file('tabela', 'csv')
        except Exception as e:
            pass
    if (not y_path) and not actuals_path:
        try:    
            y_path = get_most_recent_file('y_out_novo', 'csv')
        except Exception as e:
            pass
    
    if config is None:
        config = BettingConfig()
    elif isinstance(config, dict):
        config = BettingConfig()
    elif not isinstance(config, BettingConfig):
        raise ValueError("config must be either BettingConfig instance or dictionary")
    conf = config.load_config()
    config.from_dict(conf)
    X,y =None,None
    # if create:
    #     if not input_csv:
    #         execute_api_call()
    #     generate_actuals_from_existing_data(input_csv, actuals_path,horas=hora,max=max)
    #     # record_results(pred_path, actuals_path, history_path)
    # else:
    #     X,y = train_model(x_path,y_path,model_path,x_old_path,y_old_path,input_csv=input_csv)
    #     predict(config,model_path,x_path,y_path,hora,max,X,y, create)
    #     return 
    # if train:
    #     X,y = train_model(actuals_path,x_path,y_path,model_path,x_old_path,y_old_path)
    try:
        if not input_csv:
             execute_api_call()
        generate_actuals_from_existing_data(input_csv, actuals_path,horas=hora,max=max)
        X,y,le_home, le_away, le_league, combined = train_model(model_path=model_path, x_old_path=None, x_path=None, y_old_path=None, y_path=None, input_csv=None)
        predict(config,model_path,x_path,y_path,hora,max,X,y,create,le_home, le_away, le_league, combined)
    except Exception as e:
        messagebox.showerror('execute_api_call', e)
    
    
    