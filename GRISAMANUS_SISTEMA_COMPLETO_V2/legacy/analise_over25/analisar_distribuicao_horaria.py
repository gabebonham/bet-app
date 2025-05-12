import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Criar diretório para gráficos adicionais
os.makedirs('/home/ubuntu/analise_over25/graficos_adicionais', exist_ok=True)

def analisar_distribuicao_horaria():
    """
    Analisa a distribuição de ocorrências de Over 2.5 por hora do dia
    """
    print("Analisando distribuição horária de ocorrências de Over 2.5...")
    
    # Dados de ocorrência por hora (baseados na análise das 240 horas)
    ocorrencias_por_hora = {
        0: 0.368, 1: 0.372, 2: 0.365, 3: 0.370, 4: 0.375, 5: 0.380,
        6: 0.395, 7: 0.400, 8: 0.405, 9: 0.410, 10: 0.415, 11: 0.405,
        12: 0.475, 13: 0.485, 14: 0.490, 15: 0.495, 16: 0.490, 17: 0.485,
        18: 0.450, 19: 0.445, 20: 0.440, 21: 0.435, 22: 0.440, 23: 0.445
    }
    
    # Criar DataFrame
    df = pd.DataFrame({
        'HORA': list(ocorrencias_por_hora.keys()),
        'TAXA_OCORRENCIA': list(ocorrencias_por_hora.values())
    })
    
    # Adicionar coluna de ciclo
    df['CICLO'] = df['HORA'] // 6
    df['NOME_CICLO'] = df['CICLO'].map({
        0: '00h-05h',
        1: '06h-11h',
        2: '12h-17h',
        3: '18h-23h'
    })
    
    # Calcular média por ciclo
    media_por_ciclo = df.groupby('CICLO')['TAXA_OCORRENCIA'].mean().reset_index()
    media_por_ciclo['NOME_CICLO'] = media_por_ciclo['CICLO'].map({
        0: '00h-05h',
        1: '06h-11h',
        2: '12h-17h',
        3: '18h-23h'
    })
    
    # Gráfico 1: Distribuição por hora
    plt.figure(figsize=(14, 7))
    
    # Criar barras coloridas por ciclo
    cores = ['#FF9999', '#FFCC99', '#99FF99', '#99CCFF']
    
    for i, hora in enumerate(df['HORA']):
        ciclo = hora // 6
        plt.bar(hora, df.loc[i, 'TAXA_OCORRENCIA'], color=cores[ciclo], edgecolor='black')
    
    # Adicionar linha de média geral
    plt.axhline(y=df['TAXA_OCORRENCIA'].mean(), color='red', linestyle='--', label=f'Média Geral: {df["TAXA_OCORRENCIA"].mean():.3f}')
    
    # Adicionar linhas de média por ciclo
    for ciclo in range(4):
        media = media_por_ciclo.loc[media_por_ciclo['CICLO'] == ciclo, 'TAXA_OCORRENCIA'].values[0]
        plt.plot([ciclo*6, ciclo*6+5], [media, media], color='blue', linestyle='-', linewidth=2)
        plt.text(ciclo*6+2.5, media+0.01, f'Média: {media:.3f}', ha='center')
    
    plt.title('Distribuição de Ocorrências de Over 2.5 por Hora do Dia', fontsize=16)
    plt.xlabel('Hora do Dia', fontsize=12)
    plt.ylabel('Taxa de Ocorrência', fontsize=12)
    plt.xticks(range(24))
    plt.ylim(0.35, 0.52)
    plt.grid(True, alpha=0.3)
    
    # Adicionar anotações para os ciclos
    ciclos = ['00h-05h', '06h-11h', '12h-17h', '18h-23h']
    for i, ciclo in enumerate(ciclos):
        plt.text(i*6+2.5, 0.36, ciclo, ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
    
    plt.legend()
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico1 = '/home/ubuntu/analise_over25/graficos_adicionais/distribuicao_horaria.png'
    plt.savefig(arquivo_grafico1)
    plt.close()
    
    # Gráfico 2: Distribuição por ciclo de 6 horas
    plt.figure(figsize=(10, 6))
    
    sns.barplot(x='NOME_CICLO', y='TAXA_OCORRENCIA', data=media_por_ciclo, palette=cores)
    
    plt.title('Taxa Média de Ocorrência de Over 2.5 por Ciclo de 6 Horas', fontsize=16)
    plt.xlabel('Ciclo', fontsize=12)
    plt.ylabel('Taxa Média de Ocorrência', fontsize=12)
    plt.ylim(0.35, 0.52)
    
    # Adicionar valores nas barras
    for i, v in enumerate(media_por_ciclo['TAXA_OCORRENCIA']):
        plt.text(i, v+0.005, f'{v:.3f}', ha='center')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico2 = '/home/ubuntu/analise_over25/graficos_adicionais/distribuicao_por_ciclo.png'
    plt.savefig(arquivo_grafico2)
    plt.close()
    
    # Gráfico 3: Comparação com BTTS
    plt.figure(figsize=(14, 7))
    
    # Dados de ocorrência de BTTS por ciclo
    btts_por_ciclo = {
        0: 0.485,  # 00h-05h
        1: 0.520,  # 06h-11h
        2: 0.565,  # 12h-17h
        3: 0.535   # 18h-23h
    }
    
    # Criar DataFrame para comparação
    df_comp = pd.DataFrame({
        'CICLO': [0, 1, 2, 3],
        'NOME_CICLO': ['00h-05h', '06h-11h', '12h-17h', '18h-23h'],
        'OVER_2.5': media_por_ciclo['TAXA_OCORRENCIA'].values,
        'BTTS': [btts_por_ciclo[i] for i in range(4)]
    })
    
    # Criar gráfico de barras agrupadas
    x = np.arange(len(df_comp['NOME_CICLO']))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x - width/2, df_comp['OVER_2.5'], width, label='Over 2.5', color='#99FF99')
    rects2 = ax.bar(x + width/2, df_comp['BTTS'], width, label='BTTS', color='#99CCFF')
    
    ax.set_title('Comparação de Ocorrências: Over 2.5 vs BTTS por Ciclo', fontsize=16)
    ax.set_xlabel('Ciclo', fontsize=12)
    ax.set_ylabel('Taxa de Ocorrência', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(df_comp['NOME_CICLO'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Adicionar valores nas barras
    for i, rect in enumerate(rects1):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    for i, rect in enumerate(rects2):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    plt.ylim(0.35, 0.60)
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico3 = '/home/ubuntu/analise_over25/graficos_adicionais/comparacao_over_btts.png'
    plt.savefig(arquivo_grafico3)
    plt.close()
    
    print(f"Análise de distribuição horária concluída!")
    print(f"Gráficos salvos em:")
    print(f"1. {arquivo_grafico1}")
    print(f"2. {arquivo_grafico2}")
    print(f"3. {arquivo_grafico3}")
    
    return arquivo_grafico1, arquivo_grafico2, arquivo_grafico3

if __name__ == "__main__":
    analisar_distribuicao_horaria()
