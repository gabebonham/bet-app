import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os
import sys
from ml.betting_config import BettingConfig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
# from app.file_util import get_most_recent_file
# Parâmetros de confiança e stake (mantém lógica original)
conf_alta = 0.80
conf_media_min = 0.70
conf_media_max = 0.79
conf_baixa_min = 0.55
conf_baixa_max = 0.69
stake_base = 20.00
stake_alta_pct = 100
stake_media_pct = 50
stake_baixa_pct = 25

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
    except:
        return 0.5  # fallback se erro
def calibrar_confianca(prob):
    if prob >= 0.8:
        return 'alta'
    elif prob >= 0.7:
        return 'média'
    elif prob >= 0.55:
        return 'baixa'
    else:
        return 'fraca'

# --- Feedback & Learning Loop ---
def calibrar_confianca(self, prob):
    """Determine confidence level based on probability"""
    if prob >= self.conf_alta:
        return 'alta'
    elif prob >= self.conf_media_min:
        return 'média'
    elif prob >= self.conf_baixa_min:
        return 'baixa'
    else:
        return 'fraca'
def calcular_stake(self, confidence_level):
    """Calculate stake amount based on confidence level"""
    if confidence_level == 'alta':
        return self.stake_base * (self.stake_alta_pct / 100)
    elif confidence_level == 'média':
        return self.stake_base * (self.stake_media_pct / 100)
    elif confidence_level == 'baixa':
        return self.stake_base * (self.stake_baixa_pct / 100)
    return 0  # No bet for 'fraca' confidence

def record_results(pred_csv, actuals_csv, history_csv):
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
        if 'preds' in locals():
            print("Colunas no pred.csv:", preds.columns.tolist())
            print("Amostra de dados:\n", preds.head())
        if 'actuals' in locals():
            print("Colunas no actuals.csv:", actuals.columns.tolist())
            print("Amostra de dados:\n", actuals.head())
        if 'historico' in locals():
            print("Colunas no historico.csv:", historico.columns.tolist())
            print("Amostra de dados:\n", historico.head())
        raise


def train_model(history_csv, model_path):
    """
    Trains a RandomForest model with proper feature handling and metadata saving.
    """
    try:
        # 1. Load and validate data
        data = pd.read_csv(history_csv)
        
        if data.empty:
            raise ValueError("Input CSV file is empty. No data to train on.")
            
        # Check required columns
        required_cols = ['HORA', 'CAMPEONATO', 'COLUNA', 'PROBABILIDADE', 'OUTCOME']
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # 2. Preprocess data
        data['COLUNA'] = data['COLUNA'].astype(str).str.zfill(2).astype(int)
        
        # Filter out placeholder outcomes (0.5) if needed
        if 0.5 in data['OUTCOME'].unique():
            print("Warning: Found placeholder outcomes (0.5). These will be excluded from training.")
            data = data[data['OUTCOME'].isin([0, 1])]
        
        if data.empty:
            raise ValueError("No valid training data after filtering (all outcomes were 0.5).")
        
        # 3. Feature engineering
        X = pd.DataFrame()
        y = data['OUTCOME'].astype(int)
        
        # Basic features
        X['HORA'] = data['HORA'].astype(int)
        X['COLUNA'] = data['COLUNA']
        X['PROBABILIDADE'] = data['PROBABILIDADE']
        
        # Time features
        X['HORA_SIN'] = np.sin(2 * np.pi * X['HORA']/24)
        X['HORA_COS'] = np.cos(2 * np.pi * X['HORA']/24)
        X['MINUTO'] = X['COLUNA'] % 60
        
        # One-hot encode championships
        for camp in data['CAMPEONATO'].unique():
            X[f'CAMPEONATO_{camp}'] = (data['CAMPEONATO'] == camp).astype(int)
        
        # 4. Train model
        rf = RandomForestClassifier(
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [3, 5],
            'min_samples_split': [2, 5]
        }
        
        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=param_grid,
            cv=TimeSeriesSplit(n_splits=min(5, len(data)-1)),  # Fixed this line
            scoring='roc_auc',
            verbose=1,
            n_jobs=-1
        )
        grid_search.fit(X, y)
        best_rf = grid_search.best_estimator_
        
        # 5. Save model with proper metadata
        model_data = {
            'model': best_rf,
            'features': X.columns.tolist(),
            'class_names': ['loss', 'win'],
            'train_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
            'best_params': grid_search.best_params_
        }
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")
        
        return model_data
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        raise
        print(f"\nError during training: {str(e)}")
        if 'data' in locals():
            print("\nData shape:", data.shape if not data.empty else "Empty")
            print("\nAvailable columns:", data.columns.tolist())
            print("\nData sample:", data.head() if not data.empty else "No data")
        raise
def predict(input_csv, model_path, output_csv, config):
    """
    Generates predictions from raw match data.
    """
    try:
        # Initialize default config if none provided
        if config is None:
            config = BettingConfig()
        elif isinstance(config, dict):
            config = BettingConfig.from_dict(config)
        # 1. Load model
        model_data = joblib.load(model_path)
        model = model_data['model']
        expected_features = model_data['features']
        
        # 2. Load and prepare new data
        df = pd.read_csv(input_csv)
        processed_rows = []
        
        for _, row in df.iterrows():
            hora, coluna = row['Tempo'].split(':')
            
            # Calculate probability (using only home win probability for binary)
            prob = 1 / row['Odd Casa Vence']
            
            processed_rows.append({
                'HORA': hora,
                'COLUNA': coluna.zfill(2),
                'CAMPEONATO': row['Campeonato'],
                'PROBABILIDADE': prob
            })
        
        Xnew = pd.DataFrame(processed_rows)
        
        # 3. Create feature matrix
        Xfeat = pd.get_dummies(
            Xnew[['HORA','COLUNA','PROBABILIDADE','CAMPEONATO']],
            columns=['CAMPEONATO']
        )
        
        # Ensure feature alignment
        for feat in expected_features:
            if feat not in Xfeat.columns:
                Xfeat[feat] = 0
        Xfeat = Xfeat[expected_features]
        
        # 4. Make predictions
        df['PREDICTION'] = model.predict(Xfeat)
        df['PROBABILITY'] = model.predict_proba(Xfeat)[:, 1]  # Probability of class 1 (win)
        df['CONFIDENCE_LEVEL'] = df['PROBABILITY'].apply(config.calibrar_confianca)
        df['RECOMMENDED_STAKE'] = df['CONFIDENCE_LEVEL'].apply(config.calcular_stake)
        # 5. Save results
        df.to_csv(output_csv, index=False)
        print(f"Predictions saved to {output_csv}")
        
    except Exception as e:
        print(f"Prediction failed: {str(e)}")
        raise
def predict_generic(input_csv, model_path, output_csv, config=None):
    """
    Generates predictions from either raw or processed match data.
    Handles both formats:
    1. Raw format: 'Tempo' column (e.g., "15:30")
    2. Processed format: 'HORA' and 'COLUNA' columns
    """
    try:
        # Initialize config
        if config is None:
            config = BettingConfig()
        elif isinstance(config, dict):
            config = BettingConfig.from_dict(config)

        # 1. Load model
        model_data = joblib.load(model_path)
        model = model_data['model']
        expected_features = model_data['features']
        
        # 2. Load and prepare data
        df = pd.read_csv(input_csv)
        processed_rows = []
        
        # Check which format we're dealing with
        if 'Tempo' in df.columns:
            # Raw data format processing
            for _, row in df.iterrows():
                try:
                    hora, coluna = row['Tempo'].split(':')
                    prob = 1 / row['Odd Casa Vence']
                    processed_rows.append({
                        'HORA': hora,
                        'COLUNA': coluna.zfill(2),
                        'CAMPEONATO': row['Campeonato'],
                        'PROBABILIDADE': prob
                    })
                except KeyError as e:
                    print(f"Missing required column in row: {e}")
                    raise
        elif all(col in df.columns for col in ['HORA', 'COLUNA', 'CAMPEONATO']):
            # Processed data format
            for _, row in df.iterrows():
                processed_rows.append({
                    'HORA': str(row['HORA']),
                    'COLUNA': str(row['COLUNA']).zfill(2),
                    'CAMPEONATO': row['CAMPEONATO'],
                    'PROBABILIDADE': row.get('PROBABILIDADE', 0.5)  # Default if missing
                })
        else:
            raise ValueError("Input data must contain either 'Tempo' or 'HORA/COLUNA' columns")

        Xnew = pd.DataFrame(processed_rows)
        
        # 3. Create feature matrix
        Xfeat = pd.get_dummies(
            Xnew[['HORA','COLUNA','PROBABILIDADE','CAMPEONATO']],
            columns=['CAMPEONATO']
        )
        
        # Ensure feature alignment
        for feat in expected_features:
            if feat not in Xfeat.columns:
                Xfeat[feat] = 0
        Xfeat = Xfeat[expected_features]
        
        # 4. Make predictions
        df['PREDICTION'] = model.predict(Xfeat)
        df['PROBABILITY'] = model.predict_proba(Xfeat)[:, 1]
        
        # 5. Apply betting config
        df['CONFIDENCE_LEVEL'] = df['PROBABILITY'].apply(config.calibrar_confianca)
        df['RECOMMENDED_STAKE'] = df['CONFIDENCE_LEVEL'].apply(config.calcular_stake)
        
        # 6. Save results
        df.to_csv(output_csv, index=False)
        print(f"Predictions saved to {output_csv}")
        
    except Exception as e:
        print(f"Error generating predictions: {str(e)}")
        print("Available columns in input data:", pd.read_csv(input_csv).columns.tolist())
        raise
def generate_actuals_from_existing_data(input_file, output_file):
    """
    Generates actuals file with just one row per match and outcome.
    Creates only: HORA, CAMPEONATO, COLUNA, PROBABILIDADE, OUTCOME
    """
    df = pd.read_csv(input_file)
    processed_data = []
    
    for _, row in df.iterrows():
        hora = row['Tempo'].split(':')[0]  # Hour
        coluna = row['Tempo'].split(':')[1].zfill(2)  # Minute (2 digits)
        
        # Calculate normalized probabilities
        prob_casa = 1 / row['Odd Casa Vence']
        prob_empate = 1 / row['Odd Empate']
        prob_visitante = 1 / row['Odd Visitante Vence']
        total_prob = prob_casa + prob_empate + prob_visitante
        
        # Single row per match with weighted average probability
        weighted_prob = (prob_casa*1 + prob_empate*0.5 + prob_visitante*0) / total_prob
        processed_data.append((
            hora,
            row['Campeonato'],
            coluna,
            weighted_prob,  # Combined probability
            0.5  # Placeholder outcome
        ))
    
    result_df = pd.DataFrame(
        processed_data,
        columns=['HORA','CAMPEONATO','COLUNA','PROBABILIDADE','OUTCOME']
    )
    result_df.to_csv(output_file, index=False)
    print(f"Generated {len(result_df)} match records")

def record_results(pred_csv, actuals_csv, history_csv):
    """
    Simplified version that just updates the history with new data
    """
    new_data = pd.read_csv(actuals_csv)
    
    if os.path.exists(history_csv):
        history = pd.read_csv(history_csv)
        # Update existing records and append new ones
        combined = pd.concat([history, new_data]).drop_duplicates(
            subset=['HORA','CAMPEONATO','COLUNA'],
            keep='last'
        )
    else:
        combined = new_data
    
    combined.to_csv(history_csv, index=False)
    print(f"History updated with {len(combined)} records")


def generate_actuals_from_existing_data(input_file, output_file):
    """
    Generates actual outcomes from match data with REAL SCORES
    Converts "Gols time casa" and "Gols time contra" to binary outcomes
    """
    df = pd.read_csv(input_file)
    processed_data = []
    
    for _, row in df.iterrows():
        hora = row['Tempo'].split(':')[0]
        coluna = row['Tempo'].split(':')[1].zfill(2)
        
        # Calculate REAL outcome (1=home win, 0=draw/loss)
        home_goals = row['Gols time casa']
        away_goals = row['Gols time contra']
        outcome = 1 if home_goals > away_goals else 0 if home_goals < away_goals else 0.5
        
        # Calculate home win probability
        prob = 1 / row['Odd Casa Vence']
        
        processed_data.append([
            hora,
            row['Campeonato'],
            coluna,
            prob,
            outcome  # REAL outcome from the scoreline
        ])
    
    pd.DataFrame(
        processed_data,
        columns=['HORA','CAMPEONATO','COLUNA','PROBABILIDADE','OUTCOME']
    ).to_csv(output_file, index=False)
    print(f"Generated {len(processed_data)} records with REAL outcomes")

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
    
    if not files:
        raise FileNotFoundError(f"No files found matching {pattern}")
    
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

def get_script_relative_path(relative_path):
    """Convert relative path to be based on this script's location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, relative_path))

def get_most_recent_file(name, directory="."):
    """Find most recent file with pattern name_*.csv"""
    abs_dir = get_script_relative_path(directory)
    pattern = os.path.join(abs_dir, f"{name}_*.csv")
    files = glob.glob(pattern)
    
    if not files:
        raise FileNotFoundError(f"No files found matching {pattern}")
    
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

def execute(just_predict=True, config=None):
    # Initialize configuration
    if config is None:
        config = BettingConfig()  # Default values
    elif isinstance(config, dict):
        config = BettingConfig.from_dict(config)
    elif not isinstance(config, BettingConfig):
        raise ValueError("config must be either BettingConfig instance or dictionary")
    # Get paths - all files are in root or one level up
    table = get_most_recent_file('tabela', '../generated')  # Looks in parent directory
    actuals = get_script_relative_path('../generated/actuals.csv')
    pred = get_script_relative_path(f'../generated/pred_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv')
    history = get_script_relative_path('../generated/historico.csv')
    model = get_script_relative_path('../generated/model.pkl')
    
    # Ensure output directory exists (for prediction file)
    os.makedirs(os.path.dirname(pred), exist_ok=True)
    
    if not just_predict:
        from ml.implementacao_drisamanus_corrigida import generate_actuals_from_existing_data
        from ml.implementacao_drisamanus_corrigida import record_results, train_model
        generate_actuals_from_existing_data(table, actuals)
        record_results(pred, actuals, history)
        train_model(history, model)
    
    from ml.implementacao_drisamanus_corrigida import predict
    # predict(history, model, pred, config)
    predict_generic(history, model, pred, config)

def generate_actuals():
    
    # Get paths - all files are in root or one level up
    table = get_most_recent_file('tabela', '../generated')  # Looks in parent directory
    actuals = get_script_relative_path('../generated/actuals.csv')
    generate_actuals_from_existing_data(table, actuals)

