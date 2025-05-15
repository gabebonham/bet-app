import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, mean_squared_error
import joblib
from sklearn.base import clone

import os
import pickle
from datetime import datetime
from sklearn.model_selection import train_test_split
from ml.betting_config import BettingConfig

BASE_DIR = os.path.join(os.path.dirname(__file__))
GENERATED_PATH = os.path.join(BASE_DIR, '../generated')
# from app.file_util import get_most_recent_file
# Parâmetros de confiança e stake (mantém lógica original)
def get_script_relative_path(relative_path):
    """Convert relative path to be based on this script's location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(GENERATED_PATH, relative_path))

def get_most_recent_file(name, directory="."):
    """Find most recent file with pattern name_*.csv"""
    abs_dir = get_script_relative_path(directory)
    pattern = os.path.join(GENERATED_PATH, f"{name}_*.csv")
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    dated_files = []
    for f in files:
        try:
            # Extract date from filename (pattern: name_DD-MM-YYYY_HH-MM-SS.csv)
            date_str = os.path.basename(f)[len(name)+1:-4]
            dt = datetime.strptime(date_str, "%d-%m-%Y_%H-%M-%S")
            dated_files.append((dt, f))
        except ValueError:
            continue
    
    if not dated_files:
        return None
    
    return max(dated_files, key=lambda x: x[0])[1]
def get_most_recent_file_pkl(name, directory="."):
    """Find most recent file with pattern name_*.pkl"""
    abs_dir = get_script_relative_path(name)
    pattern = os.path.join(GENERATED_PATH, f"{name}_*.pkl")
    files = glob.glob(pattern)
    
    if not files:
        return None
    dated_files = []
    for f in files:
        try:
            # Extract date from filename (pattern: name_DD-MM-YYYY_HH-MM-SS.csv)
            date_str = os.path.basename(f)[len(name)+1:-4]
            dt = datetime.strptime(date_str, "%d-%m-%Y_%H-%M-%S")
            dated_files.append((dt, f))
        except ValueError:
            continue
    
    if not dated_files:
        return None
    
    return max(dated_files, key=lambda x: x[0])[1]

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
    full_path = os.path.join(directory, filename)
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

        df = df[(df['HORA'] >=hora_max) & (df['HORA'] <= hora_max)]
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
        


def train_model(input_csv, x_path, y_path,model_path,x_old_path=None,y_old_path=None,error_weight=0.2):
    """
    Trains a DecisionTree model with multi-output support and proper preprocessing.
    """
    try:
        
        print(model_path)
        model = None
        # 1. Load and convert data
        try:
            df = pd.read_csv(get_most_recent_file('actuals','../generated'))
        except Exception as e:
            pass
        # Load existing model if exists
        
        try:
            if model_path and os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
        except Exception as e:
            pass  # You may want to log or print e for debugging

        
            
        if not model:
            model = DecisionTreeRegressor()
        
            
        # Type conversions
       
        
        df['OUTCOME'] = df['OUTCOME'].astype(int)
        df['Campeonato'] = df['Campeonato'].astype(str)
        df['Data das odds'] = pd.to_datetime(df['Data das odds'],  errors='coerce')
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
        
        df['COLUNA'] = df['COLUNA'].astype(int)
        # Define columns
        target_columns = ['OUTCOME']
        columns_to_drop = [
            'Data das odds', 'HORA', 'COLUNA', 'Campeonato', 'Data', 'Tempo',
            'Time da casa', 'Time contra', 'Placar Exato', 'Odd Placar Exato',
            'OUTCOME', 'PROBABILIDADE'  # drop target columns too
        ]
        # Feature selection
        X = df.drop(columns=columns_to_drop)
        y = df[target_columns]

        # Drop rows where either X or y has NaNs
        combined = pd.concat([X, y], axis=1).dropna()
        X = combined[X.columns]
        y = combined[y.columns]
        print(model_path)
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        if x_path and x_path and os.path.exists(x_path) and os.path.exists(y_path) and not model_path:
            x_old = pd.read_csv(x_path)
            y_old = pd.read_csv(y_path)

            error_mask = ~y.eq(y_old).all(axis=1)
            x_errors = X[error_mask]
            y_errors = y[error_mask]

            X_augmented = pd.concat([x_old, x_errors], ignore_index=True)
            y_augmented = pd.concat([y_old, y_errors], ignore_index=True)

            sample_weight = np.ones(len(y_augmented))
            sample_weight[-len(y_errors):] = error_weight

            new_model = clone(model)
            new_model.fit(X_augmented, y_augmented, sample_weight=sample_weight)
            
            with open(create_dated_filename(name='model',directory='./app/generated',extension='pkl'), 'wb') as f:
                pickle.dump(new_model, f)
            return
        # Train the model
        if x_path and x_path and os.path.exists(x_path) and os.path.exists(y_path) and model_path:
            x_old = X
            y_old = y

            error_mask = ~y.eq(y_old).all(axis=1)
            x_errors = X[error_mask]
            y_errors = y[error_mask]

            X_augmented = pd.concat([x_old, x_errors], ignore_index=True)
            y_augmented = pd.concat([y_old, y_errors], ignore_index=True)

            sample_weight = np.ones(len(y_augmented))
            sample_weight[-len(y_errors):] = error_weight

            new_model = clone(model)
            new_model.fit(X_augmented, y_augmented, sample_weight=sample_weight)
            print('mimi')
            with open(create_dated_filename(name='model',directory='./app/generated',extension='pkl'), 'wb') as f:
                pickle.dump(new_model, f)
            return
        print('awaw')
        model.fit(X_train, y_train)
        print('uiui')
        # Save test sets and model
        X_test.to_csv(create_dated_filename(directory='./app/generated',extension='csv',name='x_in_novo'), index=False)
        y_test.to_csv(create_dated_filename(directory='./app/generated',extension='csv',name='y_out_novo'), index=False)
        df.to_csv(create_dated_filename(directory='./app/generated',extension='csv',name='actuals_from_training'), index=False)
        print('model_path')
        if model_path and os.path.exists(model_path):
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
        else:
            print('model_path2')
            with open(create_dated_filename(directory='./app/generated',extension='pkl',name='model'), 'wb') as f:
                pickle.dump(model, f)
        print("Model trained successfully.")
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        



def predict(config, model_path, x_path, y_path, hora, max):
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
            if model_path and os.path.exists(model_path): # 1. Load model
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            else:
               with open(get_most_recent_file_pkl('model','../generated'), 'rb') as f:
                model = pickle.load(f)
        except:
            with open(get_most_recent_file_pkl('model','../generated'), 'rb') as f:
                model = pickle.load(f)
        # 2. Load test data
        X_test = pd.read_csv(get_most_recent_file(name='x_in_novo',directory='../generated'))
        y_test = pd.read_csv(get_most_recent_file(name='y_out_novo',directory='../generated'))
        
        
        actuals = pd.read_csv(get_most_recent_file('actuals', '../generated'))
       

        
        # 3. Make predictions
        predictions = model.predict(X_test)
        
        # Check shape of predictions to understand the structure
        print("Shape of predictions:", predictions.shape)
        
        # 4. Create predictions DataFrame
        if len(predictions.shape) == 1:  # 1D output
            pred_df = pd.DataFrame(predictions, columns=['PREDICTION_SCORE'])
        else:  # Multi-output
            pred_df = pd.DataFrame(predictions, columns=[f'PREDICTION_SCORE_{i+1}' for i in range(predictions.shape[1])])

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

        # 6. Add confidence and stake
        pred_df['CONFIDENCE_LEVEL'] = pred_df['PROBABILIDADE'].apply(
            lambda c: config.calibrar_confianca(c) if pd.notnull(c) else None
        )

        pred_df['RECOMMENDED_STAKE'] = pred_df['CONFIDENCE_LEVEL'].apply(
            lambda c: config.calcular_stake(c) if pd.notnull(c) else None
        )

        # 7. Add model performance score (same for all rows)
        score = mean_squared_error(y_test, predictions)
        pred_df['PREDICTION_SCORE'] = score

        # 8. Join X_test and predictions side by side
        X_test = X_test.reset_index(drop=True)
        pred_df = pred_df.reset_index(drop=True)
        actuals_df = actuals.reset_index(drop=True)

        # Concatenar todos os DataFrames horizontalmente
        result_df = pd.concat([X_test, pred_df, actuals_df], axis=1)

        # 9. Ensure types
        result_df['PREDICTION_SCORE'] = result_df['PREDICTION_SCORE'].astype(float)
        result_df['PROBABILIDADE'] = result_df['PROBABILIDADE'].astype(float)
        result_df['CONFIDENCE_LEVEL'] = result_df['CONFIDENCE_LEVEL'].astype(str)
        result_df['RECOMMENDED_STAKE'] = result_df['RECOMMENDED_STAKE'].astype(float)

        # 10. Save
        result_df = result_df.drop(columns=['Data'])

        output_path = create_dated_filename(name='pred',directory='./app/generated',extension='csv')
        result_df.to_csv(output_path, index=False)
        print(f"Predictions saved successfully to {output_path}")

    
    except Exception as e:
        print(e)
        


def generate_actuals_from_existing_data(input_file, output_file, horas, max):
    """
    Generates actuals file by appending processed columns to the original data.
    Adds: HORA, COLUNA, PROBABILIDADE, OUTCOME
    """
    if input_file:
        df = pd.read_csv(os.path.join(BASE_DIR,input_file))
    else:
        df = pd.read_csv(get_most_recent_file('tabela','../generated'))
    print(get_most_recent_file('tabela','../generated'))
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
    output_file = create_dated_filename(directory='./app/generated',extension='csv',name='actuals')
    df = filter_by_time(df=df,hora_atual=horas,num_horas=max)
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

import os
from datetime import datetime
import glob

def get_script_relative_path(relative_path):
    """Convert relative path to be based on this script's location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, relative_path))

def get_most_recent_file(name, directory="."):
    """Find most recent file with pattern name_*.csv"""
    abs_dir = get_script_relative_path(directory)
    pattern = os.path.join(abs_dir, f"{name}_*.csv")
    files = glob.glob(pattern)
    print(pattern)
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado para o padrão: {pattern}")
    
    dated_files = []
    for f in files:
        try:
            # Extract date from filename (pattern: name_DD-MM-YYYY_HH-MM-SS.csv)
            date_str = os.path.basename(f)[len(name)+1:-4]
            dt = datetime.strptime(date_str, "%d-%m-%Y_%H-%M-%S")
            dated_files.append((dt, f))
        except ValueError:
            continue
    
    if not dated_files:
        raise FileNotFoundError("No valid dated files found")
    
    return max(dated_files, key=lambda x: x[0])[1]

import os
from datetime import datetime
import glob


def generate_actuals(input_csv, actuals_csv):
 
    generate_actuals_from_existing_data(input_csv, actuals_csv)

def execute( actuals_path, model_path,x_path,y_path,input_csv=None,x_old_path=None,y_old_path=None,train=True,create=True,pred_path=None,history_path=None,config=None,hora=0, max=24):
    if (x_path == '' or x_path==None) and not actuals_path:
        try:
            x_path = get_most_recent_file('x_in_novo', '../generated')
        except Exception as e:
            pass
    if input_csv == '' or input_csv==None:
        try:
            input_csv = get_most_recent_file('tabela', '../generated')
        except Exception as e:
            pass
    if (y_path =='' or y_path==None) and not actuals_path:
        try:    
            y_path = get_most_recent_file('y_out_novo', '../generated')
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
    if create:
        generate_actuals_from_existing_data(input_csv, actuals_path,horas=hora,max=max)
        # record_results(pred_path, actuals_path, history_path)
    if train:
        train_model(actuals_path,x_path,y_path,model_path,x_old_path,y_old_path)
    predict(config,model_path,x_path,y_path,hora,max)
    