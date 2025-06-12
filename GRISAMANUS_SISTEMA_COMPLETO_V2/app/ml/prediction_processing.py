from sktime.datasets import load_airline
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.theta import ThetaForecaster
from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
import pandas as pd
from sktime.utils.plotting import plot_series
import sys
from sklearn.metrics import mean_absolute_error, r2_score
from sktime.forecasting.arima import AutoARIMA
from sktime.forecasting.fbprophet import Prophet
import glob
import os
import sys
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sktime.forecasting.compose import make_reduction
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
import itertools
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from datetime import datetime,timedelta
def get_base_path():
    import os

    # get the current working directory
    current_working_directory = os.getcwd()
    return current_working_directory

def get_generated_path():
    if getattr(sys, 'frozen', False):
        # Running as executable - use _MEIPASS if available
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        generated_path = os.path.join(base_path, '..','app','generated')
    else:
        # Running in development
        base_path = os.path.dirname(os.path.abspath(__file__))
        generated_path = os.path.join(base_path, '..', 'generated')
    
    # Create directory if it doesn't exist
    os.makedirs(generated_path, exist_ok=True)
    return generated_path
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
def create_dated_filename(name, extension):
    """
    Creates a filename with the format: name_DD-MM-YYYY_HH-MM-SS.ext
    """
    directory = get_generated_path()
    
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{name}_{timestamp}.{extension}"
    full_path = os.path.join(directory, filename)
    
    return full_path
def get_adaptive_params(X_train, y_train):
    """
    Returns LightGBM parameters dynamically adjusted based on dataset characteristics
    """
    n_samples = len(X_train)
    n_features = X_train.shape[1]
    target_stats = y_train.describe() if hasattr(y_train, 'describe') else pd.Series(y_train).describe()
    
    # Base parameters (good defaults)
    params = {
        'objective': 'regression',
        'metric': 'mae',
        'seed': 42,
        'force_row_wise': True
    }
    
    # Dynamic adjustments based on sample size
    if n_samples < 300:
        # Tiny dataset settings
        params.update({
            'boosting_type': 'dart',  # Better for small data
            'num_leaves': min(8, 2**3),
            'min_child_samples': max(3, int(n_samples*0.1)),
            'learning_rate': 0.05,
            'n_estimators': 50,
            'max_depth': 3,
            'feature_fraction': 0.8
        })
    elif n_samples < 1000:
        # Small dataset settings
        params.update({
            'num_leaves': min(16, 2**4),
            'min_child_samples': max(5, int(n_samples*0.05)),
            'learning_rate': 0.1,
            'n_estimators': 100,
            'max_depth': 4,
            'feature_fraction': 0.9
        })
    elif n_samples < 5000:
        # Medium dataset settings
        params.update({
            'num_leaves': min(31, 2**5),
            'min_child_samples': max(10, int(n_samples*0.03)),
            'learning_rate': 0.07,
            'n_estimators': 200,
            'max_depth': 5
        })
    else:
        # Large dataset settings
        params.update({
            'num_leaves': min(63, 2**6),
            'min_child_samples': max(20, int(n_samples*0.01)),
            'learning_rate': 0.05,
            'n_estimators': 300,
            'max_depth': 6
        })
    
    # Adjust for target variable characteristics
    if target_stats['std'] < 0.5:  # Very low variance
        params['learning_rate'] *= 0.5  # Slower learning
        params['lambda_l1'] = 0.1  # Add regularization
    
    # Feature-dependent adjustments
    if n_features < 5:
        params['feature_fraction'] = 1.0  # Use all features
    elif n_features > 20:
        params['feature_fraction'] = 0.7  # Stronger feature sampling
    
    return params
def process_for_cup(team_df, start_cup_df, name):
    team_df['Time da casa'] = pd.Categorical(team_df['Time da casa'])
    team_df['Time contra'] = pd.Categorical(team_df['Time contra'])
    # team_df.info()
    X = team_df[['Time_Casa', 'Time_Contra', 'Data_ano', 'Data_mes', 'Data_dia', 'HORA', 'COLUNA']]
    y_home = team_df['Gols_Casa']
    y_away = team_df['Gols_Visitante']
    # print('X')
    # print(X.info())
    # print('y_home')
    # print(y_home.info())
    # print('y_away')
    # print(y_away.info())
    start_cup_df = start_cup_df.copy()
    start_cup_df['Time_Casa'] = pd.Categorical(
        start_cup_df['Time_Casa'],
        categories=team_df['Time da casa'].cat.categories
    )
    start_cup_df['Time_Contra'] = pd.Categorical(
        start_cup_df['Time_Contra'],
        categories=team_df['Time contra'].cat.categories
    )

    start_cup_df['Data_ano'] = datetime.now().year
    start_cup_df['Data_mes'] = datetime.now().month
    start_cup_df['Data_dia'] = datetime.now().day
    X_pred = start_cup_df[['Time_Casa', 'Time_Contra', 'Data_ano', 'Data_mes', 'Data_dia', 'HORA', 'COLUNA']]
    # print('Xpred')
    # print(X_pred.info())
    X_pred.columns = X.columns  

    X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
    _, _, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)
    
    # model_home = lgb.LGBMRegressor(**get_adaptive_params(X_train,y_train_home))
    # model_away = lgb.LGBMRegressor(**get_adaptive_params(X_train,y_train_away))
    model_home = lgb.LGBMRegressor()
    model_away = lgb.LGBMRegressor()
    
    model_home.fit(X_train, y_train_home, categorical_feature=['Time_Casa', 'Time_Contra'])
    model_away.fit(X_train, y_train_away, categorical_feature=['Time_Casa', 'Time_Contra'])

    y_pred_home = model_home.predict(X_test)
    y_pred_away = model_away.predict(X_test)

    mae_home = mean_absolute_error(y_test_home, y_pred_home)
    r2_home = r2_score(y_test_home, y_pred_home)

    mae_away = mean_absolute_error(y_test_away, y_pred_away)
    r2_away = r2_score(y_test_away, y_pred_away)

    model_home.fit(X, y_home, categorical_feature=['Time_Casa', 'Time_Contra'])
    model_away.fit(X, y_away, categorical_feature=['Time_Casa', 'Time_Contra'])

    prediction_home = model_home.predict(X_pred, predict_disable_shape_check=True)
    prediction_away = model_away.predict(X_pred, predict_disable_shape_check=True)

    metrics_data = {
        'MAE_Casa': [mae_home],
        'R2_Casa': [r2_home],
        'MAE_Visitante': [mae_away],
        'R2_Visitante': [r2_away]
    }
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.to_csv('app\\generated\\metrics.csv', index=False)
    start_cup_df['Casa Gols Previsão'] = prediction_home
    start_cup_df['Visitante Gols Previsão'] = prediction_away
    start_cup_df = start_cup_df.drop(['Data_ano','Data_mes','Data_dia'], axis=1)
    start_cup_df.to_csv(f'app\\generated\\{name}_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv', index=False)

def process_prediction(hora_atual,numero_horas):
    data_frames = []
    files = glob.glob('app\\generated\\tabela*.csv')
    for file in files:
        df_file = pd.read_csv(file)
        data_frames.append(df_file)
    # print(files)
    # print(get_generated_path())
    result_df = pd.concat(data_frames)
    result_df.to_csv(create_dated_filename('pred', 'csv'), index=False)
    df = result_df
    # print(259)
    # 
    # 
    hora_min = datetime.now()
    hora_max = hora_min + timedelta(hours=6)

    # Get total minutes (int)
    total_minutes = int((hora_max - hora_min).total_seconds() / 60)

    # Generate a list of datetimes at 1-minute intervals
    time_list = [hora_min + timedelta(minutes=i) for i in range(total_minutes + 1)]
    horas_reais = []
    for i in time_list:
        horas_reais.append(i.hour)
    time_period = {}
    for hora in horas_reais:
        time_period[hora] = []
        for minute in range(2,60,3):
            time_period[hora].append(minute)
    time_period_copa_super = {}
    for hora in horas_reais:
        time_period_copa_super[hora] = []
        for minute in range(1,60,3):
            time_period_copa_super[hora].append(minute)
    time_period_premier = {}
    for hora in horas_reais:
        time_period_premier[hora] = []
        for minute in range(0,60,3):
            time_period_premier[hora].append(minute)





    # print('time_period')
    # print(time_period)
    #   
    # 
    all_teams_dfs = {}
    all_teams_dfs['Euro'] = df[df['Campeonato']=='Euro']
    all_teams_dfs['Super'] = df[df['Campeonato']=='Super']
    all_teams_dfs['Copa'] = df[df['Campeonato']=='Copa']
    all_teams_dfs['Premier'] = df[df['Campeonato']=='Premier']
    # print(all_teams_dfs)

    all_teams = {}
    for name, cup_df in all_teams_dfs.items():
        away_team = cup_df.rename(columns={'Time contra':'Time'})['Time']
        home_team = cup_df.rename(columns={'Time da casa':'Time'})['Time']
        all_teams[name] = pd.concat([away_team, home_team]).drop_duplicates().to_list()
    # 
    # 
    # print(all_teams)
    
    column_euro = {'HORA':[],'COLUNA':[], 'Time_Casa':[], 'Time_Contra':[]}
    column_premier = {'HORA':[],'COLUNA':[], 'Time_Casa':[], 'Time_Contra':[]}
    column_super = {'HORA':[],'COLUNA':[], 'Time_Casa':[], 'Time_Contra':[]}
    column_copa = {'HORA':[],'COLUNA':[], 'Time_Casa':[], 'Time_Contra':[]}
    for hour, minutes in time_period.items():
        for minute in minutes:
            for cup, teams in all_teams.items():
                team_pairs = [f"{x}-{y}" for x, y in itertools.combinations(teams, 2)]
                time_str = f"{hour:02d}:{minute:02d}"
                for team_pair in team_pairs:
                    if cup == 'Euro':
                        team_x, team_y = team_pair.split('-')
                        column_euro['HORA'].append(hour)
                        column_euro['COLUNA'].append(minute)
                        column_euro['Time_Contra'].append(team_y)
                        column_euro['Time_Casa'].append(team_x)
                        
                        column_euro['HORA'].append(hour)
                        column_euro['COLUNA'].append(minute)
                        column_euro['Time_Contra'].append(team_x)
                        column_euro['Time_Casa'].append(team_y)
    for hour, minutes in time_period_copa_super.items():
        for minute in minutes:
            for cup, teams in all_teams.items():
                team_pairs = [f"{x}-{y}" for x, y in itertools.combinations(teams, 2)]
                time_str = f"{hour:02d}:{minute:02d}"
                for team_pair in team_pairs:
                    if cup == 'Super':
                        team_x, team_y = team_pair.split('-')
                        column_super['HORA'].append(hour)
                        column_super['COLUNA'].append(minute)
                        column_super['Time_Contra'].append(team_y)
                        column_super['Time_Casa'].append(team_x)
                        
                        column_super['HORA'].append(hour)
                        column_super['COLUNA'].append(minute)
                        column_super['Time_Contra'].append(team_x)
                        column_super['Time_Casa'].append(team_y)
                    elif cup == 'Copa':
                        team_x, team_y = team_pair.split('-')
                        column_copa['HORA'].append(hour)
                        column_copa['COLUNA'].append(minute)
                        column_copa['Time_Contra'].append(team_y)
                        column_copa['Time_Casa'].append(team_x)
                        
                        column_copa['HORA'].append(hour)
                        column_copa['COLUNA'].append(minute)
                        column_copa['Time_Contra'].append(team_x)
                        column_copa['Time_Casa'].append(team_y)
    for hour, minutes in time_period_premier.items():
        for minute in minutes:
            for cup, teams in all_teams.items():
                team_pairs = [f"{x}-{y}" for x, y in itertools.combinations(teams, 2)]
                time_str = f"{hour:02d}:{minute:02d}"
                for team_pair in team_pairs:
                    if cup == 'Premier':
                        team_x, team_y = team_pair.split('-')
                        column_premier['HORA'].append(hour)
                        column_premier['COLUNA'].append(minute)
                        column_premier['Time_Contra'].append(team_y)
                        column_premier['Time_Casa'].append(team_x)
                        
                        column_premier['HORA'].append(hour)
                        column_premier['COLUNA'].append(minute)
                        column_premier['Time_Contra'].append(team_x)
                        column_premier['Time_Casa'].append(team_y)
    # print(column_euro)
    start_euro_df = pd.DataFrame(column_euro)
    start_premier_df = pd.DataFrame(column_premier)
    start_super_df = pd.DataFrame(column_super)
    start_copa_df = pd.DataFrame(column_copa)
    start_euro_df.to_csv(create_dated_filename('start_euro_df', 'csv'), index=False)
    start_premier_df.to_csv(create_dated_filename('start_premier_df', 'csv'), index=False)
    start_super_df.to_csv(create_dated_filename('start_super_df', 'csv'), index=False)
    start_copa_df.to_csv(create_dated_filename('start_copa_df', 'csv'), index=False)
    # 
    # 
    # print(333)
    
    for team_name, team_df in all_teams_dfs.items():
        team_df = team_df.copy()
        
        
        team_df['Data das odds_Y'] = pd.to_datetime(team_df['Data das odds'], format='mixed').dt.year.astype(int)
        team_df['Data das odds_m'] = pd.to_datetime(team_df['Data das odds'], format='mixed').dt.month.astype(int)
        team_df['Data das odds_d'] = pd.to_datetime(team_df['Data das odds'], format='mixed').dt.day.astype(int)
        team_df['Data das odds_H'] = pd.to_datetime(team_df['Data das odds'], format='mixed').dt.hour.astype(int)
        team_df['Data das odds_M'] = pd.to_datetime(team_df['Data das odds'], format='mixed').dt.minute.astype(int)
        team_df['Data_ano'] = pd.to_datetime(team_df['Data'], format='%Y-%m-%d').dt.year.astype(int)
        team_df['Data_mes'] = pd.to_datetime(team_df['Data'], format='%Y-%m-%d').dt.month.astype(int)
        team_df['Data_dia'] = pd.to_datetime(team_df['Data'], format='%Y-%m-%d').dt.day.astype(int)
        team_df['HORA'] = pd.to_datetime(team_df['Tempo'], format='%H:%M').dt.hour.astype(int)
        team_df['COLUNA'] = pd.to_datetime(team_df['Tempo'], format='%H:%M').dt.minute.astype(int)
        team_df['Time_Casa'] = pd.Categorical(team_df['Time da casa'])
        team_df['Time da casa'] = pd.Categorical(team_df['Time da casa'])
        team_df['Time_Contra'] = pd.Categorical(team_df['Time contra'])
        team_df['Time contra'] = pd.Categorical(team_df['Time contra'])
        
        home_goals = []
        away_goals = []
        for i, row in team_df.iterrows():
            exact_score = row['Placar Exato'].replace('+', '')
            score_home, score_away = exact_score.split('-')
            away_goals.append(int(score_away))
            home_goals.append(int(score_home))

        team_df['Gols_Casa'] = home_goals
        team_df['Gols_Visitante'] = away_goals
        team_df = team_df.drop(columns=['Placar Exato'])
        
        if team_name == 'Euro':    
            process_for_cup(team_df,start_euro_df,team_name)
        if team_name == 'Copa':    
            process_for_cup(team_df,start_copa_df,team_name)
        if team_name == 'Premier':    
            process_for_cup(team_df,start_premier_df,team_name)
        if team_name == 'Super':    
            process_for_cup(team_df,start_super_df,team_name)
