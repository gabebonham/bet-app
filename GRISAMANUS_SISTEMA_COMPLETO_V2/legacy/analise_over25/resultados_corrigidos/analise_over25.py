import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Criar diretórios para resultados se não existirem
os.makedirs('/home/ubuntu/analise_over25/resultados_corrigidos', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over25/resultados_corrigidos/graficos', exist_ok=True)

def analisar_resultados_over25():
    """
    Analisa os resultados das previsões do Over 2.5 com base nas correções enviadas pelo usuário
    """
    print("Analisando resultados das previsões do Over 2.5...")
    
    # Criar DataFrame com os dados das previsões corrigidas
    dados = []
    
    # Tabela 1 (probabilidades 0.55-0.58)
    dados_tabela1 = [
        {"CAMPEONATO": "SUPER", "COLUNA": 28, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 16, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 23, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 42, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 1, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 43, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 55, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.57, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 52, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.57, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 10, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.57, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 52, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.57, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 25, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.57, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 23, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.57, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 59, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.56, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 16, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.56, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 29, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.56, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "COPA", "COLUNA": 19, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.56, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "EURO", "COLUNA": 17, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.56, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 25, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.55, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 43, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.55, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 49, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.55, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""}
    ]
    dados.extend(dados_tabela1)
    
    # Tabela 2 (probabilidades 0.58-0.61)
    dados_tabela2 = [
        {"CAMPEONATO": "SUPER", "COLUNA": 16, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 38, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 28, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 48, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 10, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 46, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 3, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 36, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 20, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.60, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 17, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 52, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "COPA", "COLUNA": 4, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 37, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 37, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 6, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 51, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 19, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 13, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.59, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 7, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 28, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 49, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 41, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 22, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.58, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""}
    ]
    dados.extend(dados_tabela2)
    
    # Tabela 3 (probabilidades 0.61-0.64)
    dados_tabela3 = [
        {"CAMPEONATO": "EURO", "COLUNA": 50, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 45, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.63, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 46, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.63, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 13, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.63, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 42, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.63, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 2, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.63, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 25, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.63, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 7, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 36, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 26, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 40, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 10, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 26, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 55, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 29, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 31, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 13, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 39, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.62, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 34, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 52, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 57, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 21, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "SUPER", "COLUNA": 1, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.61, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""}
    ]
    dados.extend(dados_tabela3)
    
    # Tabela 4 (probabilidades 0.64-0.66)
    dados_tabela4 = [
        {"CAMPEONATO": "SUPER", "COLUNA": 4, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 50, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 18, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 48, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 3, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 54, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 55, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 11, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 31, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 34, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 40, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 9, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 9, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.65, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 37, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 1, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 33, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 44, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 16, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 20, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 8, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "SUPER", "COLUNA": 13, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 21, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "SUPER", "COLUNA": 7, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.64, "CONFIANCA": "BAIXA", "STAKE": "R$5.00", "RESULTADO": "VERDE", "GALE": ""}
    ]
    dados.extend(dados_tabela4)
    
    # Tabela 5 (probabilidades 0.66-0.69)
    dados_tabela5 = [
        {"CAMPEONATO": "PREMIER", "COLUNA": 45, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.69, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 0, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.69, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 43, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.69, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 25, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.69, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 6, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.68, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 43, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.68, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 52, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.68, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 34, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "EURO", "COLUNA": 41, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 32, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 46, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 48, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 40, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 54, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 0, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.67, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 40, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 33, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 30, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 22, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 21, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 33, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 15, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 46, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.66, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""}
    ]
    dados.extend(dados_tabela5)
    
    # Tabela 6 (probabilidades 0.70-0.78)
    dados_tabela6 = [
        {"CAMPEONATO": "SUPER", "COLUNA": 4, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.78, "CONFIANCA": "ALTA", "STAKE": "R$20.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 27, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.76, "CONFIANCA": "ALTA", "STAKE": "R$20.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 31, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.75, "CONFIANCA": "ALTA", "STAKE": "R$20.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 31, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.74, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 0, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.74, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 45, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.73, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "3"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 12, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.73, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "SUPER", "COLUNA": 49, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.73, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "EURO", "COLUNA": 11, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.72, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 51, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.72, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 24, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.72, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 49, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.72, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "SUPER", "COLUNA": 55, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.72, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "COPA", "COLUNA": 43, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.71, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 39, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.71, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "COPA", "COLUNA": 28, "HORA": 14, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.70, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERMELHO", "GALE": ""},
        {"CAMPEONATO": "PREMIER", "COLUNA": 24, "HORA": 13, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.70, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "1"},
        {"CAMPEONATO": "PREMIER", "COLUNA": 57, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.70, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "2"},
        {"CAMPEONATO": "SUPER", "COLUNA": 37, "HORA": 12, "MERCADO": "OVER 2.5", "PROBABILIDADE": 0.70, "CONFIANCA": "MEDIA", "STAKE": "R$10.00", "RESULTADO": "VERDE", "GALE": "2"}
    ]
    dados.extend(dados_tabela6)
    
    # Converter para DataFrame
    df = pd.DataFrame(dados)
    
    # Converter colunas para tipos apropriados
    df['PROBABILIDADE'] = df['PROBABILIDADE'].astype(float)
    df['RESULTADO'] = df['RESULTADO'].apply(lambda x: 1 if x == 'VERDE' else 0)
    df['GALE'] = df['GALE'].fillna('0').astype(str)
    df['GALE'] = df['GALE'].apply(lambda x: int(x) if x.isdigit() else 0)
    
    # Salvar DataFrame em CSV
    arquivo_csv = '/home/ubuntu/analise_over25/resultados_corrigidos/previsoes_over25_corrigidas.csv'
    df.to_csv(arquivo_csv, index=False)
    print(f"Dados salvos em: {arquivo_csv}")
    
    # Análise geral
    total_previsoes = len(df)
    acertos = df['RESULTADO'].sum()
    taxa_acerto = acertos / total_previsoes
    
    print(f"\nAnálise Geral:")
    print(f"Total de previsões: {total_previsoes}")
    print(f"Total de acertos: {acertos}")
    print(f"Taxa de acerto: {taxa_acerto:.2%}")
    
    # Análise por nível de confiança
    print("\nAnálise por Nível de Confiança:")
    for confianca in ['ALTA', 'MEDIA', 'BAIXA']:
        df_conf = df[df['CONFIANCA'] == confianca]
        total_conf = len(df_conf)
        acertos_conf = df_conf['RESULTADO'].sum()
        taxa_conf = acertos_conf / total_conf if total_conf > 0 else 0
        print(f"{confianca}: {acertos_conf}/{total_conf} = {taxa_conf:.2%}")
    
    # Análise por campeonato
    print("\nAnálise por Campeonato:")
    for campeonato in ['PREMIER', 'SUPER', 'COPA', 'EURO']:
        df_camp = df[df['CAMPEONATO'] == campeonato]
        total_camp = len(df_camp)
        acertos_camp = df_camp['RESULTADO'].sum()
        taxa_camp = acertos_camp / total_camp if total_camp > 0 else 0
        print(f"{campeonato}: {acertos_camp}/{total_camp} = {taxa_camp:.2%}")
    
    # Análise por hora
    print("\nAnálise por Hora:")
    for hora in sorted(df['HORA'].unique()):
        df_hora = df[df['HORA'] == hora]
        total_hora = len(df_hora)
        acertos_hora = df_hora['RESULTADO'].sum()
        taxa_hora = acertos_hora / total_hora if total_hora > 0 else 0
        print(f"Hora {hora}: {acertos_hora}/{total_hora} = {taxa_hora:.2%}")
    
    # Análise por faixa de probabilidade
    print("\nAnálise por Faixa de Probabilidade:")
    faixas = [(0.55, 0.60), (0.60, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80)]
    for min_prob, max_prob in faixas:
        df_prob = df[(df['PROBABILIDADE'] >= min_prob) & (df['PROBABILIDADE'] < max_prob)]
        total_prob = len(df_prob)
        acertos_prob = df_prob['RESULTADO'].sum()
        taxa_prob = acertos_prob / total_prob if total_prob > 0 else 0
        print(f"Probabilidade {min_prob:.2f}-{max_prob:.2f}: {acertos_prob}/{total_prob} = {taxa_prob:.2%}")
    
    # Análise de gales
    print("\nAnálise de Gales:")
    sem_gale = len(df[df['GALE'] == 0])
    com_gale_1 = len(df[df['GALE'] == 1])
    com_gale_2 = len(df[df['GALE'] == 2])
    com_gale_3 = len(df[df['GALE'] == 3])
    
    print(f"Acertos sem gale: {sem_gale}/{acertos} = {sem_gale/acertos:.2%}")
    print(f"Acertos com 1 gale: {com_gale_1}/{acertos} = {com_gale_1/acertos:.2%}")
    print(f"Acertos com 2 gales: {com_gale_2}/{acertos} = {com_gale_2/acertos:.2%}")
    print(f"Acertos com 3 gales: {com_gale_3}/{acertos} = {com_gale_3/acertos:.2%}")
    
    # Identificar pontos fora da curva
    print("\nPontos Fora da Curva:")
    
    # 1. Previsões de ALTA confiança que falharam
    alta_falhas = df[(df['CONFIANCA'] == 'ALTA') & (df['RESULTADO'] == 0)]
    if len(alta_falhas) > 0:
        print(f"Previsões de ALTA confiança que falharam: {len(alta_falhas)}")
        for _, falha in alta_falhas.iterrows():
            print(f"  - {falha['CAMPEONATO']} {falha['COLUNA']} Hora {falha['HORA']} (Prob: {falha['PROBABILIDADE']:.2f})")
    
    # 2. Previsões de BAIXA confiança com alta taxa de acerto
    baixa_acertos = df[(df['CONFIANCA'] == 'BAIXA') & (df['RESULTADO'] == 1) & (df['GALE'] == 0)]
    if len(baixa_acertos) > 0:
        print(f"Previsões de BAIXA confiança com acerto direto (sem gale): {len(baixa_acertos)}")
    
    # 3. Campeonatos com desempenho muito diferente da média
    for campeonato in ['PREMIER', 'SUPER', 'COPA', 'EURO']:
        df_camp = df[df['CAMPEONATO'] == campeonato]
        taxa_camp = df_camp['RESULTADO'].mean()
        if abs(taxa_camp - taxa_acerto) > 0.1:  # Mais de 10% de diferença da média
            print(f"Campeonato {campeonato} tem desempenho muito diferente da média: {taxa_camp:.2%} vs {taxa_acerto:.2%}")
    
    # 4. Horas com desempenho muito diferente da média
    for hora in sorted(df['HORA'].unique()):
        df_hora = df[df['HORA'] == hora]
        taxa_hora = df_hora['RESULTADO'].mean()
        if abs(taxa_hora - taxa_acerto) > 0.1:  # Mais de 10% de diferença da média
            print(f"Hora {hora} tem desempenho muito diferente da média: {taxa_hora:.2%} vs {taxa_acerto:.2%}")
    
    # Criar visualizações
    criar_visualizacoes(df)
    
    return df

def criar_visualizacoes(df):
    """
    Cria visualizações para análise dos resultados
    """
    print("Criando visualizações para análise dos resultados...")
    
    # 1. Taxa de acerto por nível de confiança
    plt.figure(figsize=(10, 6))
    confiancas = ['ALTA', 'MEDIA', 'BAIXA']
    taxas = []
    
    for confianca in confiancas:
        df_conf = df[df['CONFIANCA'] == confianca]
        taxa = df_conf['RESULTADO'].mean() if len(df_conf) > 0 else 0
        taxas.append(taxa)
    
    cores = ['lightgreen', 'lightblue', 'lightcoral']
    bars = plt.bar(confiancas, taxas, color=cores)
    
    plt.title('Taxa de Acerto por Nível de Confiança - Over 2.5')
    plt.xlabel('Nível de Confiança')
    plt.ylabel('Taxa de Acerto')
    plt.ylim(0, 1)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}',
                ha='center', va='bottom')
    
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('/home/ubuntu/analise_over25/resultados_corrigidos/graficos/taxa_acerto_confianca.png')
    plt.close()
    
    # 2. Taxa de acerto por campeonato
    plt.figure(figsize=(10, 6))
    campeonatos = ['PREMIER', 'SUPER', 'COPA', 'EURO']
    taxas = []
    
    for campeonato in campeonatos:
        df_camp = df[df['CAMPEONATO'] == campeonato]
        taxa = df_camp['RESULTADO'].mean() if len(df_camp) > 0 else 0
        taxas.append(taxa)
    
    cores = ['blue', 'green', 'red', 'purple']
    bars = plt.bar(campeonatos, taxas, color=cores)
    
    plt.title('Taxa de Acerto por Campeonato - Over 2.5')
    plt.xlabel('Campeonato')
    plt.ylabel('Taxa de Acerto')
    plt.ylim(0, 1)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}',
                ha='center', va='bottom')
    
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('/home/ubuntu/analise_over25/resultados_corrigidos/graficos/taxa_acerto_campeonato.png')
    plt.close()
    
    # 3. Taxa de acerto por hora
    plt.figure(figsize=(12, 6))
    horas = sorted(df['HORA'].unique())
    taxas = []
    
    for hora in horas:
        df_hora = df[df['HORA'] == hora]
        taxa = df_hora['RESULTADO'].mean() if len(df_hora) > 0 else 0
        taxas.append(taxa)
    
    # Colorir por ciclo de 6 horas
    cores = []
    for hora in horas:
        if 0 <= hora < 6:
            cores.append('lightcoral')
        elif 6 <= hora < 12:
            cores.append('lightsalmon')
        elif 12 <= hora < 18:
            cores.append('lightgreen')
        else:
            cores.append('lightblue')
    
    bars = plt.bar(horas, taxas, color=cores)
    
    plt.title('Taxa de Acerto por Hora - Over 2.5')
    plt.xlabel('Hora')
    plt.ylabel('Taxa de Acerto')
    plt.ylim(0, 1)
    plt.xticks(horas)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}',
                ha='center', va='bottom')
    
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('/home/ubuntu/analise_over25/resultados_corrigidos/graficos/taxa_acerto_hora.png')
    plt.close()
    
    # 4. Taxa de acerto por faixa de probabilidade
    plt.figure(figsize=(12, 6))
    faixas = [(0.55, 0.60), (0.60, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80)]
    labels = [f'{min_prob:.2f}-{max_prob:.2f}' for min_prob, max_prob in faixas]
    taxas = []
    
    for min_prob, max_prob in faixas:
        df_prob = df[(df['PROBABILIDADE'] >= min_prob) & (df['PROBABILIDADE'] < max_prob)]
        taxa = df_prob['RESULTADO'].mean() if len(df_prob) > 0 else 0
        taxas.append(taxa)
    
    # Gradiente de cores baseado na probabilidade
    cores = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(faixas)))
    bars = plt.bar(labels, taxas, color=cores)
    
    plt.title('Taxa de Acerto por Faixa de Probabilidade - Over 2.5')
    plt.xlabel('Faixa de Probabilidade')
    plt.ylabel('Taxa de Acerto')
    plt.ylim(0, 1)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}',
                ha='center', va='bottom')
    
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('/home/ubuntu/analise_over25/resultados_corrigidos/graficos/taxa_acerto_probabilidade.png')
    plt.close()
    
    # 5. Distribuição de gales
    plt.figure(figsize=(10, 6))
    gales = [0, 1, 2, 3]
    contagem = []
    
    for gale in gales:
        count = len(df[(df['RESULTADO'] == 1) & (df['GALE'] == gale)])
        contagem.append(count)
    
    cores = ['lightgreen', 'lightyellow', 'orange', 'red']
    bars = plt.bar([f'Sem Gale', '1 Gale', '2 Gales', '3 Gales'], contagem, color=cores)
    
    plt.title('Distribuição de Acertos por Número de Gales - Over 2.5')
    plt.xlabel('Número de Gales')
    plt.ylabel('Número de Acertos')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom')
    
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('/home/ubuntu/analise_over25/resultados_corrigidos/graficos/distribuicao_gales.png')
    plt.close()
    
    # 6. Heatmap de taxa de acerto por campeonato e hora
    plt.figure(figsize=(12, 8))
    
    # Criar pivot table
    pivot = pd.pivot_table(df, values='RESULTADO', index='CAMPEONATO', columns='HORA', aggfunc='mean')
    
    # Criar heatmap
    sns.heatmap(pivot, annot=True, cmap='RdYlGn', vmin=0, vmax=1, fmt='.2f')
    
    plt.title('Taxa de Acerto por Campeonato e Hora - Over 2.5')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/resultados_corrigidos/graficos/heatmap_campeonato_hora.png')
    plt.close()
    
    print("Visualizações criadas com sucesso!")

def identificar_pontos_fora_da_curva(df):
    """
    Identifica pontos fora da curva nos resultados
    """
    print("\nIdentificando pontos fora da curva nos resultados...")
    
    # Taxa de acerto geral
    taxa_acerto_geral = df['RESULTADO'].mean()
    
    # 1. Previsões de ALTA confiança que falharam
    alta_falhas = df[(df['CONFIANCA'] == 'ALTA') & (df['RESULTADO'] == 0)]
    if len(alta_falhas) > 0:
        print(f"\n1. Previsões de ALTA confiança que falharam ({len(alta_falhas)}):")
        for _, falha in alta_falhas.iterrows():
            print(f"  - {falha['CAMPEONATO']} {falha['COLUNA']} Hora {falha['HORA']} (Prob: {falha['PROBABILIDADE']:.2f})")
    
    # 2. Previsões de BAIXA confiança com alta taxa de acerto
    baixa_acertos = df[(df['CONFIANCA'] == 'BAIXA') & (df['RESULTADO'] == 1) & (df['GALE'] == 0)]
    if len(baixa_acertos) > 0:
        print(f"\n2. Previsões de BAIXA confiança com acerto direto (sem gale): {len(baixa_acertos)}/{len(df[df['CONFIANCA'] == 'BAIXA'])}")
        taxa_baixa_acerto = len(baixa_acertos) / len(df[df['CONFIANCA'] == 'BAIXA'])
        print(f"   Taxa de acerto direto em BAIXA confiança: {taxa_baixa_acerto:.2%}")
    
    # 3. Campeonatos com desempenho muito diferente da média
    print("\n3. Campeonatos com desempenho diferente da média:")
    for campeonato in ['PREMIER', 'SUPER', 'COPA', 'EURO']:
        df_camp = df[df['CAMPEONATO'] == campeonato]
        taxa_camp = df_camp['RESULTADO'].mean()
        diferenca = taxa_camp - taxa_acerto_geral
        print(f"  - {campeonato}: {taxa_camp:.2%} ({diferenca:+.2%} da média)")
        
        if abs(diferenca) > 0.1:  # Mais de 10% de diferença da média
            print(f"    ** PONTO FORA DA CURVA **")
    
    # 4. Horas com desempenho muito diferente da média
    print("\n4. Horas com desempenho diferente da média:")
    for hora in sorted(df['HORA'].unique()):
        df_hora = df[df['HORA'] == hora]
        taxa_hora = df_hora['RESULTADO'].mean()
        diferenca = taxa_hora - taxa_acerto_geral
        print(f"  - Hora {hora}: {taxa_hora:.2%} ({diferenca:+.2%} da média)")
        
        if abs(diferenca) > 0.1:  # Mais de 10% de diferença da média
            print(f"    ** PONTO FORA DA CURVA **")
    
    # 5. Faixas de probabilidade com desempenho muito diferente do esperado
    print("\n5. Faixas de probabilidade com desempenho diferente do esperado:")
    faixas = [(0.55, 0.60), (0.60, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80)]
    for min_prob, max_prob in faixas:
        df_prob = df[(df['PROBABILIDADE'] >= min_prob) & (df['PROBABILIDADE'] < max_prob)]
        if len(df_prob) > 0:
            taxa_prob = df_prob['RESULTADO'].mean()
            prob_media = (min_prob + max_prob) / 2
            diferenca = taxa_prob - prob_media
            print(f"  - Probabilidade {min_prob:.2f}-{max_prob:.2f}: Taxa de acerto {taxa_prob:.2%} vs Probabilidade média {prob_media:.2%} ({diferenca:+.2%})")
            
            if abs(diferenca) > 0.1:  # Mais de 10% de diferença do esperado
                print(f"    ** PONTO FORA DA CURVA **")
    
    # 6. Combinações específicas com desempenho anômalo
    print("\n6. Combinações específicas com desempenho anômalo:")
    
    # Campeonato + Hora
    for campeonato in ['PREMIER', 'SUPER', 'COPA', 'EURO']:
        for hora in sorted(df['HORA'].unique()):
            df_combo = df[(df['CAMPEONATO'] == campeonato) & (df['HORA'] == hora)]
            if len(df_combo) >= 3:  # Pelo menos 3 previsões para ser estatisticamente relevante
                taxa_combo = df_combo['RESULTADO'].mean()
                diferenca = taxa_combo - taxa_acerto_geral
                if abs(diferenca) > 0.2:  # Mais de 20% de diferença da média
                    print(f"  - {campeonato} na Hora {hora}: {taxa_combo:.2%} ({diferenca:+.2%} da média) - {len(df_combo)} previsões")
    
    # 7. Necessidade de gales por faixa de probabilidade
    print("\n7. Necessidade de gales por faixa de probabilidade:")
    for min_prob, max_prob in faixas:
        df_prob = df[(df['PROBABILIDADE'] >= min_prob) & (df['PROBABILIDADE'] < max_prob) & (df['RESULTADO'] == 1)]
        if len(df_prob) > 0:
            sem_gale = len(df_prob[df_prob['GALE'] == 0]) / len(df_prob)
            com_gale = 1 - sem_gale
            print(f"  - Probabilidade {min_prob:.2f}-{max_prob:.2f}: Acertos diretos {sem_gale:.2%}, Com gale {com_gale:.2%}")
            
            if com_gale > 0.5:  # Mais de 50% precisou de gale
                print(f"    ** PONTO FORA DA CURVA **")
    
    return {
        'alta_falhas': alta_falhas,
        'baixa_acertos': baixa_acertos
    }

def calibrar_modelo_over25(df):
    """
    Propõe calibrações para o modelo Over 2.5 com base nos resultados
    """
    print("\nPropondo calibrações para o modelo Over 2.5...")
    
    # Taxa de acerto geral
    taxa_acerto_geral = df['RESULTADO'].mean()
    print(f"Taxa de acerto geral: {taxa_acerto_geral:.2%}")
    
    # Análise por nível de confiança
    print("\nAnálise por Nível de Confiança:")
    for confianca in ['ALTA', 'MEDIA', 'BAIXA']:
        df_conf = df[df['CONFIANCA'] == confianca]
        total_conf = len(df_conf)
        acertos_conf = df_conf['RESULTADO'].sum()
        taxa_conf = acertos_conf / total_conf if total_conf > 0 else 0
        print(f"{confianca}: {acertos_conf}/{total_conf} = {taxa_conf:.2%}")
    
    # Análise por faixa de probabilidade
    print("\nAnálise por Faixa de Probabilidade:")
    faixas = [(0.55, 0.60), (0.60, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80)]
    for min_prob, max_prob in faixas:
        df_prob = df[(df['PROBABILIDADE'] >= min_prob) & (df['PROBABILIDADE'] < max_prob)]
        total_prob = len(df_prob)
        acertos_prob = df_prob['RESULTADO'].sum()
        taxa_prob = acertos_prob / total_prob if total_prob > 0 else 0
        print(f"Probabilidade {min_prob:.2f}-{max_prob:.2f}: {acertos_prob}/{total_prob} = {taxa_prob:.2%}")
    
    # Propor calibrações
    print("\nCalibrações Propostas:")
    
    # 1. Calibração dos níveis de confiança
    print("\n1. Calibração dos níveis de confiança:")
    
    # Analisar cada faixa de probabilidade para determinar os melhores pontos de corte
    faixas_detalhadas = [(0.55, 0.58), (0.58, 0.61), (0.61, 0.64), (0.64, 0.67), (0.67, 0.70), (0.70, 0.73), (0.73, 0.76), (0.76, 0.80)]
    resultados_faixas = []
    
    for min_prob, max_prob in faixas_detalhadas:
        df_prob = df[(df['PROBABILIDADE'] >= min_prob) & (df['PROBABILIDADE'] < max_prob)]
        total_prob = len(df_prob)
        acertos_prob = df_prob['RESULTADO'].sum()
        taxa_prob = acertos_prob / total_prob if total_prob > 0 else 0
        resultados_faixas.append((min_prob, max_prob, taxa_prob, total_prob))
    
    # Ordenar por taxa de acerto
    resultados_faixas.sort(key=lambda x: x[2], reverse=True)
    
    # Propor novos pontos de corte
    alta_min = 0.0
    media_min = 0.0
    baixa_min = 0.0
    
    for min_prob, max_prob, taxa, total in resultados_faixas:
        if taxa >= 0.75 and total >= 5 and alta_min == 0.0:
            alta_min = min_prob
        elif taxa >= 0.65 and total >= 5 and media_min == 0.0:
            media_min = min_prob
        elif taxa >= 0.55 and total >= 5 and baixa_min == 0.0:
            baixa_min = min_prob
    
    # Ajustar se não encontrou valores adequados
    if alta_min == 0.0:
        alta_min = 0.75
    if media_min == 0.0:
        media_min = 0.65
    if baixa_min == 0.0:
        baixa_min = 0.55
    
    print(f"Níveis de confiança atuais:")
    print(f"  - ALTA: probabilidade > 0.75")
    print(f"  - MÉDIA: probabilidade entre 0.65 e 0.74")
    print(f"  - BAIXA: probabilidade entre 0.55 e 0.64")
    
    print(f"\nNíveis de confiança propostos:")
    print(f"  - ALTA: probabilidade > {alta_min:.2f}")
    print(f"  - MÉDIA: probabilidade entre {media_min:.2f} e {alta_min-0.01:.2f}")
    print(f"  - BAIXA: probabilidade entre {baixa_min:.2f} e {media_min-0.01:.2f}")
    
    # 2. Ajustes de pesos por campeonato
    print("\n2. Ajustes de pesos por campeonato:")
    
    campeonatos = ['PREMIER', 'SUPER', 'COPA', 'EURO']
    taxas_campeonatos = []
    
    for campeonato in campeonatos:
        df_camp = df[df['CAMPEONATO'] == campeonato]
        taxa_camp = df_camp['RESULTADO'].mean() if len(df_camp) > 0 else 0
        diferenca = taxa_camp - taxa_acerto_geral
        taxas_campeonatos.append((campeonato, taxa_camp, diferenca))
    
    # Ordenar por taxa de acerto
    taxas_campeonatos.sort(key=lambda x: x[1], reverse=True)
    
    print("Pesos atuais por campeonato:")
    print("  - PREMIER: +0.03")
    print("  - SUPER: +0.02")
    print("  - COPA: +0.01")
    print("  - EURO: -0.01")
    
    print("\nPesos propostos por campeonato:")
    for campeonato, taxa, diferenca in taxas_campeonatos:
        # Converter diferença para um ajuste de peso
        ajuste = round(diferenca * 2, 2)  # Multiplicar por 2 para amplificar o efeito
        print(f"  - {campeonato}: {ajuste:+.2f}")
    
    # 3. Ajustes de pesos por hora
    print("\n3. Ajustes de pesos por hora:")
    
    horas = sorted(df['HORA'].unique())
    taxas_horas = []
    
    for hora in horas:
        df_hora = df[df['HORA'] == hora]
        taxa_hora = df_hora['RESULTADO'].mean() if len(df_hora) > 0 else 0
        diferenca = taxa_hora - taxa_acerto_geral
        taxas_horas.append((hora, taxa_hora, diferenca))
    
    # Agrupar por ciclo de 6 horas
    ciclos = {
        "00-05h": [],
        "06-11h": [],
        "12-17h": [],
        "18-23h": []
    }
    
    for hora, taxa, diferenca in taxas_horas:
        if 0 <= hora < 6:
            ciclos["00-05h"].append((hora, taxa, diferenca))
        elif 6 <= hora < 12:
            ciclos["06-11h"].append((hora, taxa, diferenca))
        elif 12 <= hora < 18:
            ciclos["12-17h"].append((hora, taxa, diferenca))
        else:
            ciclos["18-23h"].append((hora, taxa, diferenca))
    
    print("Pesos atuais por ciclo de 6 horas:")
    print("  - 00-05h: -0.02")
    print("  - 06-11h: 0.00")
    print("  - 12-17h: +0.04")
    print("  - 18-23h: +0.02")
    
    print("\nPesos propostos por ciclo de 6 horas:")
    for ciclo, horas_ciclo in ciclos.items():
        if horas_ciclo:
            taxa_media = sum(taxa for _, taxa, _ in horas_ciclo) / len(horas_ciclo)
            diferenca_media = sum(diferenca for _, _, diferenca in horas_ciclo) / len(horas_ciclo)
            ajuste = round(diferenca_media * 2, 2)  # Multiplicar por 2 para amplificar o efeito
            print(f"  - {ciclo}: {ajuste:+.2f} (Taxa média: {taxa_media:.2%})")
    
    # 4. Ajustes na estratégia de Martingale
    print("\n4. Ajustes na estratégia de Martingale:")
    
    # Analisar necessidade de gales por nível de confiança
    for confianca in ['ALTA', 'MEDIA', 'BAIXA']:
        df_conf = df[(df['CONFIANCA'] == confianca) & (df['RESULTADO'] == 1)]
        if len(df_conf) > 0:
            sem_gale = len(df_conf[df_conf['GALE'] == 0])
            com_gale_1 = len(df_conf[df_conf['GALE'] == 1])
            com_gale_2 = len(df_conf[df_conf['GALE'] == 2])
            com_gale_3 = len(df_conf[df_conf['GALE'] == 3])
            
            total = len(df_conf)
            print(f"{confianca}:")
            print(f"  - Sem gale: {sem_gale}/{total} = {sem_gale/total:.2%}")
            print(f"  - 1 gale: {com_gale_1}/{total} = {com_gale_1/total:.2%}")
            print(f"  - 2 gales: {com_gale_2}/{total} = {com_gale_2/total:.2%}")
            print(f"  - 3 gales: {com_gale_3}/{total} = {com_gale_3/total:.2%}")
    
    print("\nEstratégia de Martingale proposta:")
    print("  - ALTA: Até 1 gale")
    print("  - MÉDIA: Até 2 gales")
    print("  - BAIXA: Até 3 gales")
    
    # 5. Ajustes nos valores de stake
    print("\n5. Ajustes nos valores de stake:")
    
    print("Valores de stake atuais:")
    print("  - ALTA: R$20.00")
    print("  - MÉDIA: R$10.00")
    print("  - BAIXA: R$5.00")
    
    # Calcular ROI por nível de confiança
    for confianca in ['ALTA', 'MEDIA', 'BAIXA']:
        df_conf = df[df['CONFIANCA'] == confianca]
        if len(df_conf) > 0:
            stake = 20.00 if confianca == 'ALTA' else (10.00 if confianca == 'MEDIA' else 5.00)
            
            # Calcular ganhos e perdas
            ganhos = 0
            perdas = 0
            
            for _, row in df_conf.iterrows():
                if row['RESULTADO'] == 1:  # Acerto
                    if row['GALE'] == 0:
                        ganhos += stake * 0.9  # Lucro de 90% da stake
                    elif row['GALE'] == 1:
                        ganhos += stake * 0.9 - stake  # Lucro de 90% da stake - stake perdida
                    elif row['GALE'] == 2:
                        ganhos += stake * 0.9 - stake * 3  # Lucro de 90% da stake - 3x stake perdida
                    elif row['GALE'] == 3:
                        ganhos += stake * 0.9 - stake * 7  # Lucro de 90% da stake - 7x stake perdida
                else:  # Erro
                    perdas += stake * 7  # Perda de 7x stake (considerando 3 gales)
            
            roi = (ganhos - perdas) / (stake * len(df_conf))
            print(f"{confianca}: ROI = {roi:.2%}")
    
    print("\nValores de stake propostos:")
    print("  - ALTA: R$25.00")
    print("  - MÉDIA: R$15.00")
    print("  - BAIXA: R$5.00")
    
    # Resumo das calibrações
    print("\nResumo das Calibrações Propostas:")
    print("1. Níveis de confiança:")
    print(f"  - ALTA: probabilidade > {alta_min:.2f}")
    print(f"  - MÉDIA: probabilidade entre {media_min:.2f} e {alta_min-0.01:.2f}")
    print(f"  - BAIXA: probabilidade entre {baixa_min:.2f} e {media_min-0.01:.2f}")
    
    print("\n2. Pesos por campeonato:")
    for campeonato, _, diferenca in taxas_campeonatos:
        ajuste = round(diferenca * 2, 2)
        print(f"  - {campeonato}: {ajuste:+.2f}")
    
    print("\n3. Pesos por ciclo de 6 horas:")
    for ciclo, horas_ciclo in ciclos.items():
        if horas_ciclo:
            diferenca_media = sum(diferenca for _, _, diferenca in horas_ciclo) / len(horas_ciclo)
            ajuste = round(diferenca_media * 2, 2)
            print(f"  - {ciclo}: {ajuste:+.2f}")
    
    print("\n4. Estratégia de Martingale:")
    print("  - ALTA: Até 1 gale")
    print("  - MÉDIA: Até 2 gales")
    print("  - BAIXA: Até 3 gales")
    
    print("\n5. Valores de stake:")
    print("  - ALTA: R$25.00")
    print("  - MÉDIA: R$15.00")
    print("  - BAIXA: R$5.00")
    
    # Salvar calibrações em arquivo
    calibracoes = {
        'niveis_confianca': {
            'ALTA': alta_min,
            'MEDIA': media_min,
            'BAIXA': baixa_min
        },
        'pesos_campeonatos': {campeonato: round(diferenca * 2, 2) for campeonato, _, diferenca in taxas_campeonatos},
        'pesos_ciclos': {ciclo: round(sum(diferenca for _, _, diferenca in horas_ciclo) / len(horas_ciclo) * 2, 2) if horas_ciclo else 0 for ciclo, horas_ciclo in ciclos.items()},
        'estrategia_martingale': {
            'ALTA': 1,
            'MEDIA': 2,
            'BAIXA': 3
        },
        'valores_stake': {
            'ALTA': 25.00,
            'MEDIA': 15.00,
            'BAIXA': 5.00
        }
    }
    
    return calibracoes

if __name__ == "__main__":
    # Analisar resultados
    df = analisar_resultados_over25()
    
    # Identificar pontos fora da curva
    pontos_fora_curva = identificar_pontos_fora_da_curva(df)
    
    # Calibrar modelo
    calibracoes = calibrar_modelo_over25(df)
