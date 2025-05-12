import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Criar diretórios necessários
os.makedirs('/home/ubuntu/tabelas_operacionais', exist_ok=True)

def criar_tabela_operacional_over35():
    """
    Cria uma tabela operacional para o mercado Over 3.5 com base nas análises realizadas
    """
    # Dados das taxas de ocorrência por campeonato
    campeonatos = ['PREMIER', 'EURO', 'COPA', 'SUPER']
    taxas_campeonato = [28.0, 22.0, 23.0, 20.0]  # Porcentagens
    
    # Dados das taxas de ocorrência por ciclo
    ciclos = ['00h-05h', '06h-11h', '12h-17h', '18h-23h']
    taxas_ciclo = [16.0, 20.0, 33.0, 26.0]  # Porcentagens
    
    # Criar DataFrame para a tabela operacional
    horas = list(range(24))
    dados = []
    
    for hora in horas:
        # Determinar o ciclo da hora
        if 0 <= hora <= 5:
            ciclo = '00h-05h'
            taxa_ciclo = 16.0
        elif 6 <= hora <= 11:
            ciclo = '06h-11h'
            taxa_ciclo = 20.0
        elif 12 <= hora <= 17:
            ciclo = '12h-17h'
            taxa_ciclo = 33.0
        else:
            ciclo = '18h-23h'
            taxa_ciclo = 26.0
        
        # Determinar a recomendação com base na taxa do ciclo
        if taxa_ciclo >= 30:
            recomendacao = 'ALTA'
            stake = 'R$25.00'
            confianca = '⭐⭐⭐'
        elif taxa_ciclo >= 25:
            recomendacao = 'MÉDIA'
            stake = 'R$15.00'
            confianca = '⭐⭐'
        elif taxa_ciclo >= 20:
            recomendacao = 'BAIXA'
            stake = 'R$5.00'
            confianca = '⭐'
        else:
            recomendacao = 'NÃO OPERAR'
            stake = '-'
            confianca = '❌'
        
        # Adicionar combinações específicas de alta ocorrência
        combinacoes_especiais = {
            13: {'campeonato': 'PREMIER', 'taxa': 50.0, 'recomendacao': 'MUITO ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐⭐'},
            14: {'campeonato': 'PREMIER', 'taxa': 50.0, 'recomendacao': 'MUITO ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐⭐'},
            16: {'campeonato': 'PREMIER', 'taxa': 45.0, 'recomendacao': 'MUITO ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐⭐'},
            17: {'campeonato': 'PREMIER', 'taxa': 45.0, 'recomendacao': 'MUITO ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐⭐'},
            21: {'campeonato': 'PREMIER', 'taxa': 45.0, 'recomendacao': 'MUITO ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐⭐'},
            8: {'campeonato': 'EURO', 'taxa': 40.0, 'recomendacao': 'ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐'},
            22: {'campeonato': 'EURO', 'taxa': 40.0, 'recomendacao': 'ALTA', 'stake': 'R$25.00', 'confianca': '⭐⭐⭐'}
        }
        
        if hora in combinacoes_especiais:
            combo = combinacoes_especiais[hora]
            campeonato_recomendado = combo['campeonato']
            taxa_especifica = combo['taxa']
            recomendacao = combo['recomendacao']
            stake = combo['stake']
            confianca = combo['confianca']
        else:
            # Para horas sem combinações especiais, recomendar o campeonato com maior taxa
            campeonato_recomendado = 'PREMIER'  # Campeonato com maior taxa geral
            taxa_especifica = taxa_ciclo  # Usar a taxa do ciclo
        
        dados.append({
            'HORA': hora,
            'CICLO': ciclo,
            'TAXA_CICLO': taxa_ciclo,
            'CAMPEONATO_RECOMENDADO': campeonato_recomendado,
            'TAXA_ESPECIFICA': taxa_especifica,
            'RECOMENDACAO': recomendacao,
            'STAKE': stake,
            'CONFIANCA': confianca
        })
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Salvar tabela em CSV
    arquivo_csv = '/home/ubuntu/tabelas_operacionais/tabela_operacional_over35.csv'
    df.to_csv(arquivo_csv, index=False)
    
    # Criar visualização da tabela
    plt.figure(figsize=(14, 10))
    
    # Criar uma tabela colorida
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
    # Definir cores para as recomendações
    cores = {
        'MUITO ALTA': '#1a9850',  # Verde escuro
        'ALTA': '#66bd63',        # Verde
        'MÉDIA': '#fdae61',       # Laranja
        'BAIXA': '#f46d43',       # Vermelho claro
        'NÃO OPERAR': '#d73027'   # Vermelho escuro
    }
    
    # Criar lista de cores para cada linha
    cell_colors = []
    for _, row in df.iterrows():
        recomendacao = row['RECOMENDACAO']
        cor = cores.get(recomendacao, '#ffffff')  # Branco para valores não mapeados
        cell_colors.append([cor] * len(df.columns))
    
    # Criar tabela
    tabela = plt.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        cellColours=cell_colors
    )
    
    # Ajustar tamanho da fonte
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1.2, 1.5)
    
    # Título
    plt.title('Tabela Operacional - Over 3.5', fontsize=16, pad=20)
    
    # Salvar imagem
    plt.savefig('/home/ubuntu/tabelas_operacionais/tabela_operacional_over35.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Tabela operacional para Over 3.5 criada com sucesso!")
    print(f"CSV: {arquivo_csv}")
    print(f"Imagem: /home/ubuntu/tabelas_operacionais/tabela_operacional_over35.png")
    
    return df

def atualizar_tabela_consolidada():
    """
    Atualiza a tabela operacional consolidada incluindo o mercado Over 3.5
    """
    # Verificar se as tabelas individuais existem
    tabelas = {
        'BTTS': '/home/ubuntu/tabelas_operacionais/tabela_operacional_btts.csv',
        'OVER 2.5': '/home/ubuntu/tabelas_operacionais/tabela_operacional_over25.csv',
        'OVER 3.5': '/home/ubuntu/tabelas_operacionais/tabela_operacional_over35.csv'
    }
    
    dados_consolidados = []
    
    # Para cada hora, consolidar as recomendações dos três mercados
    for hora in range(24):
        registro = {'HORA': hora}
        
        for mercado, arquivo in tabelas.items():
            if os.path.exists(arquivo):
                try:
                    df = pd.read_csv(arquivo)
                    linha = df[df['HORA'] == hora]
                    
                    if not linha.empty:
                        registro[f'{mercado}_RECOMENDACAO'] = linha['RECOMENDACAO'].values[0]
                        registro[f'{mercado}_CAMPEONATO'] = linha['CAMPEONATO_RECOMENDADO'].values[0]
                        registro[f'{mercado}_STAKE'] = linha['STAKE'].values[0]
                        registro[f'{mercado}_CONFIANCA'] = linha['CONFIANCA'].values[0]
                    else:
                        registro[f'{mercado}_RECOMENDACAO'] = 'N/A'
                        registro[f'{mercado}_CAMPEONATO'] = 'N/A'
                        registro[f'{mercado}_STAKE'] = 'N/A'
                        registro[f'{mercado}_CONFIANCA'] = 'N/A'
                except Exception as e:
                    print(f"Erro ao ler {arquivo}: {e}")
                    registro[f'{mercado}_RECOMENDACAO'] = 'ERRO'
                    registro[f'{mercado}_CAMPEONATO'] = 'ERRO'
                    registro[f'{mercado}_STAKE'] = 'ERRO'
                    registro[f'{mercado}_CONFIANCA'] = 'ERRO'
            else:
                registro[f'{mercado}_RECOMENDACAO'] = 'N/A'
                registro[f'{mercado}_CAMPEONATO'] = 'N/A'
                registro[f'{mercado}_STAKE'] = 'N/A'
                registro[f'{mercado}_CONFIANCA'] = 'N/A'
        
        dados_consolidados.append(registro)
    
    # Criar DataFrame consolidado
    df_consolidado = pd.DataFrame(dados_consolidados)
    
    # Salvar tabela consolidada em CSV
    arquivo_csv = '/home/ubuntu/tabelas_operacionais/tabela_operacional_consolidada.csv'
    df_consolidado.to_csv(arquivo_csv, index=False)
    
    print(f"Tabela operacional consolidada atualizada com sucesso!")
    print(f"CSV: {arquivo_csv}")
    
    return df_consolidado

if __name__ == "__main__":
    # Criar tabela operacional para Over 3.5
    df_over35 = criar_tabela_operacional_over35()
    
    # Atualizar tabela consolidada
    df_consolidado = atualizar_tabela_consolidada()
    
    print("\nProcesso concluído com sucesso!")
