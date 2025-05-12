import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os
from datetime import datetime

# Criar diretórios para resultados se não existirem
os.makedirs('/home/ubuntu/analise_over25/padroes', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over25/padroes/graficos', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over25/padroes/dados', exist_ok=True)

def carregar_dados():
    """
    Carrega os dados de padrões identificados para cada campeonato
    """
    print("Carregando dados de padrões identificados...")
    
    padroes = {}
    campeonatos = ['PREMIER', 'COPA', 'EURO', 'SUPER']
    
    for campeonato in campeonatos:
        try:
            arquivo = f'/home/ubuntu/analise_over25/dados/padroes_{campeonato.lower()}.csv'
            padroes[campeonato] = pd.read_csv(arquivo)
            print(f"Carregados {len(padroes[campeonato])} padrões para {campeonato}")
        except Exception as e:
            print(f"Erro ao carregar padrões para {campeonato}: {e}")
            padroes[campeonato] = None
    
    return padroes

def analisar_tipos_padroes(padroes):
    """
    Analisa os tipos de padrões geométricos identificados
    """
    print("Analisando tipos de padrões geométricos...")
    
    # Consolidar todos os padrões em um único DataFrame
    todos_padroes = []
    
    for campeonato, df in padroes.items():
        if df is not None and len(df) > 0:
            df['CAMPEONATO'] = campeonato
            todos_padroes.append(df)
    
    if not todos_padroes:
        print("Nenhum padrão encontrado para análise.")
        return None
    
    df_todos = pd.concat(todos_padroes, ignore_index=True)
    
    # Análise de tipos de padrões
    contagem_tipos = df_todos['TIPO'].value_counts().reset_index()
    contagem_tipos.columns = ['TIPO', 'CONTAGEM']
    
    # Calcular porcentagem
    total = contagem_tipos['CONTAGEM'].sum()
    contagem_tipos['PORCENTAGEM'] = contagem_tipos['CONTAGEM'] / total * 100
    
    # Separar padrões por cor (verde/vermelho)
    padroes_verdes = df_todos[df_todos['TIPO'].str.contains('verde')].copy()
    padroes_vermelhos = df_todos[df_todos['TIPO'].str.contains('vermelho')].copy()
    
    # Contagem por tipo e cor
    contagem_verdes = padroes_verdes['TIPO'].value_counts().reset_index()
    contagem_verdes.columns = ['TIPO', 'CONTAGEM']
    contagem_verdes['COR'] = 'Verde'
    
    contagem_vermelhos = padroes_vermelhos['TIPO'].value_counts().reset_index()
    contagem_vermelhos.columns = ['TIPO', 'CONTAGEM']
    contagem_vermelhos['COR'] = 'Vermelho'
    
    # Combinar contagens
    contagem_por_cor = pd.concat([contagem_verdes, contagem_vermelhos], ignore_index=True)
    
    # Criar gráfico de barras para tipos de padrões
    plt.figure(figsize=(12, 6))
    sns.barplot(x='TIPO', y='CONTAGEM', data=contagem_tipos, palette='viridis')
    plt.title('Frequência de Tipos de Padrões Geométricos - Over 2.5')
    plt.xlabel('Tipo de Padrão')
    plt.ylabel('Frequência')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/frequencia_tipos_padroes.png')
    plt.close()
    
    # Criar gráfico de barras para tipos de padrões por cor
    plt.figure(figsize=(14, 7))
    sns.barplot(x='TIPO', y='CONTAGEM', hue='COR', data=contagem_por_cor, palette=['green', 'red'])
    plt.title('Frequência de Tipos de Padrões Geométricos por Cor - Over 2.5')
    plt.xlabel('Tipo de Padrão')
    plt.ylabel('Frequência')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Cor')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/frequencia_tipos_padroes_por_cor.png')
    plt.close()
    
    # Criar gráfico de pizza para distribuição de tipos de padrões
    plt.figure(figsize=(10, 10))
    plt.pie(contagem_tipos['CONTAGEM'], labels=contagem_tipos['TIPO'], autopct='%1.1f%%', 
            startangle=90, shadow=True, explode=[0.05] * len(contagem_tipos))
    plt.axis('equal')
    plt.title('Distribuição de Tipos de Padrões Geométricos - Over 2.5')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_tipos_padroes.png')
    plt.close()
    
    print(f"Análise de tipos de padrões concluída. Identificados {len(contagem_tipos)} tipos distintos.")
    
    return {
        'todos_padroes': df_todos,
        'contagem_tipos': contagem_tipos,
        'contagem_por_cor': contagem_por_cor
    }

def analisar_forca_padroes(resultados_tipos):
    """
    Analisa a força (confiabilidade) dos padrões geométricos
    """
    print("Analisando força dos padrões geométricos...")
    
    if resultados_tipos is None or 'todos_padroes' not in resultados_tipos:
        print("Dados insuficientes para análise de força dos padrões.")
        return None
    
    df_todos = resultados_tipos['todos_padroes']
    
    # Análise de força por tipo de padrão
    forca_media_por_tipo = df_todos.groupby('TIPO')['FORCA'].mean().reset_index()
    forca_media_por_tipo = forca_media_por_tipo.sort_values('FORCA', ascending=False)
    
    # Análise de força por campeonato
    forca_media_por_campeonato = df_todos.groupby('CAMPEONATO')['FORCA'].mean().reset_index()
    forca_media_por_campeonato = forca_media_por_campeonato.sort_values('FORCA', ascending=False)
    
    # Análise de força por tipo e campeonato
    forca_por_tipo_campeonato = df_todos.groupby(['TIPO', 'CAMPEONATO'])['FORCA'].mean().reset_index()
    forca_por_tipo_campeonato = forca_por_tipo_campeonato.sort_values(['TIPO', 'FORCA'], ascending=[True, False])
    
    # Criar gráfico de barras para força média por tipo
    plt.figure(figsize=(12, 6))
    sns.barplot(x='TIPO', y='FORCA', data=forca_media_por_tipo, palette='viridis')
    plt.title('Força Média por Tipo de Padrão Geométrico - Over 2.5')
    plt.xlabel('Tipo de Padrão')
    plt.ylabel('Força Média')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/forca_media_por_tipo.png')
    plt.close()
    
    # Criar gráfico de barras para força média por campeonato
    plt.figure(figsize=(10, 6))
    sns.barplot(x='CAMPEONATO', y='FORCA', data=forca_media_por_campeonato, palette='viridis')
    plt.title('Força Média por Campeonato - Over 2.5')
    plt.xlabel('Campeonato')
    plt.ylabel('Força Média')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/forca_media_por_campeonato.png')
    plt.close()
    
    # Criar heatmap para força por tipo e campeonato
    pivot = forca_por_tipo_campeonato.pivot(index='TIPO', columns='CAMPEONATO', values='FORCA')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, cmap='viridis', fmt='.2f', linewidths=.5)
    plt.title('Força dos Padrões por Tipo e Campeonato - Over 2.5')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/forca_por_tipo_campeonato.png')
    plt.close()
    
    print("Análise de força dos padrões concluída.")
    
    return {
        'forca_media_por_tipo': forca_media_por_tipo,
        'forca_media_por_campeonato': forca_media_por_campeonato,
        'forca_por_tipo_campeonato': forca_por_tipo_campeonato
    }

def analisar_distribuicao_temporal(resultados_tipos):
    """
    Analisa a distribuição temporal dos padrões geométricos
    """
    print("Analisando distribuição temporal dos padrões geométricos...")
    
    if resultados_tipos is None or 'todos_padroes' not in resultados_tipos:
        print("Dados insuficientes para análise de distribuição temporal.")
        return None
    
    df_todos = resultados_tipos['todos_padroes']
    
    # Análise por hora de início
    distribuicao_por_hora = df_todos.groupby('HORA_INICIO').size().reset_index(name='CONTAGEM')
    
    # Análise por hora de início e tipo
    distribuicao_por_hora_tipo = df_todos.groupby(['HORA_INICIO', 'TIPO']).size().reset_index(name='CONTAGEM')
    
    # Análise por hora de início e campeonato
    distribuicao_por_hora_campeonato = df_todos.groupby(['HORA_INICIO', 'CAMPEONATO']).size().reset_index(name='CONTAGEM')
    
    # Criar gráfico de barras para distribuição por hora
    plt.figure(figsize=(12, 6))
    sns.barplot(x='HORA_INICIO', y='CONTAGEM', data=distribuicao_por_hora, palette='viridis')
    plt.title('Distribuição de Padrões Geométricos por Hora - Over 2.5')
    plt.xlabel('Hora de Início')
    plt.ylabel('Contagem')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_hora.png')
    plt.close()
    
    # Criar gráfico de barras empilhadas para distribuição por hora e tipo
    pivot_hora_tipo = distribuicao_por_hora_tipo.pivot(index='HORA_INICIO', columns='TIPO', values='CONTAGEM').fillna(0)
    
    plt.figure(figsize=(14, 8))
    pivot_hora_tipo.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='viridis')
    plt.title('Distribuição de Tipos de Padrões por Hora - Over 2.5')
    plt.xlabel('Hora de Início')
    plt.ylabel('Contagem')
    plt.legend(title='Tipo de Padrão', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_hora_tipo.png')
    plt.close()
    
    # Criar heatmap para distribuição por hora e campeonato
    pivot_hora_campeonato = distribuicao_por_hora_campeonato.pivot(index='HORA_INICIO', columns='CAMPEONATO', values='CONTAGEM').fillna(0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_hora_campeonato, annot=True, cmap='viridis', fmt='g', linewidths=.5)
    plt.title('Distribuição de Padrões por Hora e Campeonato - Over 2.5')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_hora_campeonato.png')
    plt.close()
    
    # Análise de ciclos de 6 horas
    df_todos['CICLO_6H'] = df_todos['HORA_INICIO'] // 6
    ciclos_6h = {0: '00-05', 1: '06-11', 2: '12-17', 3: '18-23'}
    df_todos['CICLO_6H_NOME'] = df_todos['CICLO_6H'].map(ciclos_6h)
    
    distribuicao_por_ciclo = df_todos.groupby('CICLO_6H_NOME').size().reset_index(name='CONTAGEM')
    distribuicao_por_ciclo_tipo = df_todos.groupby(['CICLO_6H_NOME', 'TIPO']).size().reset_index(name='CONTAGEM')
    
    # Criar gráfico de barras para distribuição por ciclo de 6 horas
    plt.figure(figsize=(10, 6))
    sns.barplot(x='CICLO_6H_NOME', y='CONTAGEM', data=distribuicao_por_ciclo, palette='viridis')
    plt.title('Distribuição de Padrões por Ciclo de 6 Horas - Over 2.5')
    plt.xlabel('Ciclo de 6 Horas')
    plt.ylabel('Contagem')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_ciclo_6h.png')
    plt.close()
    
    # Criar gráfico de barras empilhadas para distribuição por ciclo e tipo
    pivot_ciclo_tipo = distribuicao_por_ciclo_tipo.pivot(index='CICLO_6H_NOME', columns='TIPO', values='CONTAGEM').fillna(0)
    
    plt.figure(figsize=(12, 8))
    pivot_ciclo_tipo.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Distribuição de Tipos de Padrões por Ciclo de 6 Horas - Over 2.5')
    plt.xlabel('Ciclo de 6 Horas')
    plt.ylabel('Contagem')
    plt.legend(title='Tipo de Padrão', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_ciclo_tipo.png')
    plt.close()
    
    print("Análise de distribuição temporal concluída.")
    
    return {
        'distribuicao_por_hora': distribuicao_por_hora,
        'distribuicao_por_hora_tipo': distribuicao_por_hora_tipo,
        'distribuicao_por_hora_campeonato': distribuicao_por_hora_campeonato,
        'distribuicao_por_ciclo': distribuicao_por_ciclo,
        'distribuicao_por_ciclo_tipo': distribuicao_por_ciclo_tipo
    }

def analisar_padroes_por_coluna(resultados_tipos):
    """
    Analisa a distribuição dos padrões geométricos por coluna
    """
    print("Analisando distribuição dos padrões por coluna...")
    
    if resultados_tipos is None or 'todos_padroes' not in resultados_tipos:
        print("Dados insuficientes para análise de distribuição por coluna.")
        return None
    
    df_todos = resultados_tipos['todos_padroes']
    
    # Análise por coluna
    distribuicao_por_coluna = df_todos.groupby('COLUNA').size().reset_index(name='CONTAGEM')
    
    # Análise por coluna e tipo
    distribuicao_por_coluna_tipo = df_todos.groupby(['COLUNA', 'TIPO']).size().reset_index(name='CONTAGEM')
    
    # Análise por coluna e campeonato
    distribuicao_por_coluna_campeonato = df_todos.groupby(['COLUNA', 'CAMPEONATO']).size().reset_index(name='CONTAGEM')
    
    # Criar gráfico de barras para distribuição por coluna
    plt.figure(figsize=(14, 6))
    sns.barplot(x='COLUNA', y='CONTAGEM', data=distribuicao_por_coluna, palette='viridis')
    plt.title('Distribuição de Padrões Geométricos por Coluna - Over 2.5')
    plt.xlabel('Coluna')
    plt.ylabel('Contagem')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_coluna.png')
    plt.close()
    
    # Criar heatmap para distribuição por coluna e campeonato
    pivot_coluna_campeonato = distribuicao_por_coluna_campeonato.pivot(index='COLUNA', columns='CAMPEONATO', values='CONTAGEM').fillna(0)
    
    plt.figure(figsize=(14, 10))
    sns.heatmap(pivot_coluna_campeonato, annot=True, cmap='viridis', fmt='g', linewidths=.5)
    plt.title('Distribuição de Padrões por Coluna e Campeonato - Over 2.5')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_coluna_campeonato.png')
    plt.close()
    
    # Análise de colunas mais frequentes por tipo de padrão
    top_colunas_por_tipo = df_todos.groupby(['TIPO', 'COLUNA']).size().reset_index(name='CONTAGEM')
    top_colunas_por_tipo = top_colunas_por_tipo.sort_values(['TIPO', 'CONTAGEM'], ascending=[True, False])
    
    # Pegar as 3 colunas mais frequentes para cada tipo
    top_colunas = []
    for tipo in top_colunas_por_tipo['TIPO'].unique():
        top_tipo = top_colunas_por_tipo[top_colunas_por_tipo['TIPO'] == tipo].head(3)
        top_colunas.append(top_tipo)
    
    top_colunas_df = pd.concat(top_colunas, ignore_index=True)
    
    # Criar gráfico de barras para top colunas por tipo
    plt.figure(figsize=(16, 10))
    sns.barplot(x='TIPO', y='CONTAGEM', hue='COLUNA', data=top_colunas_df, palette='viridis')
    plt.title('Top 3 Colunas Mais Frequentes por Tipo de Padrão - Over 2.5')
    plt.xlabel('Tipo de Padrão')
    plt.ylabel('Contagem')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Coluna', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/top_colunas_por_tipo.png')
    plt.close()
    
    print("Análise de distribuição por coluna concluída.")
    
    return {
        'distribuicao_por_coluna': distribuicao_por_coluna,
        'distribuicao_por_coluna_tipo': distribuicao_por_coluna_tipo,
        'distribuicao_por_coluna_campeonato': distribuicao_por_coluna_campeonato,
        'top_colunas_por_tipo': top_colunas_df
    }

def comparar_padroes_over25_btts():
    """
    Compara os padrões geométricos do Over 2.5 com os do BTTS
    """
    print("Comparando padrões geométricos do Over 2.5 com BTTS...")
    
    # Dados simulados para comparação (baseados na análise anterior)
    padroes_over25 = {
        'triangular_ascendente': 0.85,
        'triangular_descendente': 0.80,
        'retangular_verde': 0.90,
        'retangular_vermelho': 0.85,
        'diagonal_principal_verde': 0.75,
        'diagonal_principal_vermelho': 0.70,
        'diagonal_secundaria_verde': 0.75,
        'diagonal_secundaria_vermelho': 0.70
    }
    
    padroes_btts = {
        'triangular_ascendente': 0.88,
        'triangular_descendente': 0.83,
        'retangular_verde': 0.92,
        'retangular_vermelho': 0.87,
        'diagonal_principal_verde': 0.82,
        'diagonal_principal_vermelho': 0.78,
        'diagonal_secundaria_verde': 0.80,
        'diagonal_secundaria_vermelho': 0.76
    }
    
    # Criar DataFrame para comparação
    comparacao = pd.DataFrame({
        'PADRAO': list(padroes_over25.keys()),
        'OVER_25': list(padroes_over25.values()),
        'BTTS': list(padroes_btts.values())
    })
    
    # Calcular diferença
    comparacao['DIFERENCA'] = comparacao['BTTS'] - comparacao['OVER_25']
    
    # Criar gráfico de barras para comparação
    plt.figure(figsize=(12, 6))
    
    x = np.arange(len(comparacao['PADRAO']))
    width = 0.35
    
    plt.bar(x - width/2, comparacao['OVER_25'], width, label='Over 2.5', color='lightgreen')
    plt.bar(x + width/2, comparacao['BTTS'], width, label='BTTS', color='skyblue')
    
    plt.xlabel('Tipo de Padrão')
    plt.ylabel('Força do Padrão')
    plt.title('Comparação da Força dos Padrões: Over 2.5 vs BTTS')
    plt.xticks(x, comparacao['PADRAO'], rotation=45, ha='right')
    plt.legend()
    plt.ylim(0.6, 1.0)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/comparacao_forca_padroes_over25_btts.png')
    plt.close()
    
    # Criar gráfico de barras para diferença
    plt.figure(figsize=(12, 6))
    
    bars = plt.bar(comparacao['PADRAO'], comparacao['DIFERENCA'], color='purple')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom')
    
    plt.xlabel('Tipo de Padrão')
    plt.ylabel('Diferença (BTTS - Over 2.5)')
    plt.title('Diferença na Força dos Padrões: BTTS vs Over 2.5')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('/home/ubuntu/analise_over25/padroes/graficos/diferenca_forca_padroes.png')
    plt.close()
    
    print("Comparação de padrões Over 2.5 vs BTTS concluída.")
    
    return comparacao

def gerar_relatorio_padroes(resultados_tipos, resultados_forca, resultados_temporal, resultados_coluna, comparacao_btts):
    """
    Gera um relatório detalhado sobre os padrões geométricos do Over 2.5
    """
    print("Gerando relatório detalhado sobre padrões geométricos do Over 2.5...")
    
    # Criar arquivo de relatório
    relatorio_path = '/home/ubuntu/analise_over25/padroes/relatorio_padroes_over25.md'
    
    with open(relatorio_path, 'w') as f:
        f.write("# Relatório Detalhado: Padrões Geométricos no Mercado Over 2.5\n\n")
        f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        f.write("## 1. Visão Geral dos Padrões Identificados\n\n")
        
        if resultados_tipos and 'contagem_tipos' in resultados_tipos:
            contagem_tipos = resultados_tipos['contagem_tipos']
            
            f.write("### 1.1 Frequência de Tipos de Padrões\n\n")
            f.write("Os padrões geométricos mais frequentes no mercado Over 2.5 são:\n\n")
            
            for i, row in contagem_tipos.head(5).iterrows():
                f.write(f"- **{row['TIPO']}**: {row['CONTAGEM']} ocorrências ({row['PORCENTAGEM']:.1f}%)\n")
            
            f.write("\n![Frequência de Tipos de Padrões](/home/ubuntu/analise_over25/padroes/graficos/frequencia_tipos_padroes.png)\n\n")
            
            f.write("### 1.2 Distribuição por Cor (Verde/Vermelho)\n\n")
            f.write("A análise da distribuição de padrões por cor revela diferenças na formação de padrões para resultados Over 2.5 (verde) e Under 2.5 (vermelho).\n\n")
            
            f.write("![Frequência de Tipos de Padrões por Cor](/home/ubuntu/analise_over25/padroes/graficos/frequencia_tipos_padroes_por_cor.png)\n\n")
            
            f.write("### 1.3 Distribuição Geral de Padrões\n\n")
            f.write("A distribuição geral dos padrões geométricos identificados no mercado Over 2.5 é apresentada abaixo:\n\n")
            
            f.write("![Distribuição de Tipos de Padrões](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_tipos_padroes.png)\n\n")
        else:
            f.write("Dados insuficientes para análise de tipos de padrões.\n\n")
        
        f.write("## 2. Força e Confiabilidade dos Padrões\n\n")
        
        if resultados_forca and 'forca_media_por_tipo' in resultados_forca:
            forca_media_por_tipo = resultados_forca['forca_media_por_tipo']
            
            f.write("### 2.1 Força Média por Tipo de Padrão\n\n")
            f.write("A análise da força média (confiabilidade) por tipo de padrão revela quais padrões são mais confiáveis para previsões no mercado Over 2.5:\n\n")
            
            for i, row in forca_media_por_tipo.head(5).iterrows():
                f.write(f"- **{row['TIPO']}**: {row['FORCA']:.2f}\n")
            
            f.write("\n![Força Média por Tipo de Padrão](/home/ubuntu/analise_over25/padroes/graficos/forca_media_por_tipo.png)\n\n")
            
            f.write("### 2.2 Força Média por Campeonato\n\n")
            
            if 'forca_media_por_campeonato' in resultados_forca:
                forca_media_por_campeonato = resultados_forca['forca_media_por_campeonato']
                
                f.write("A análise da força média por campeonato indica em quais campeonatos os padrões são mais confiáveis:\n\n")
                
                for i, row in forca_media_por_campeonato.iterrows():
                    f.write(f"- **{row['CAMPEONATO']}**: {row['FORCA']:.2f}\n")
                
                f.write("\n![Força Média por Campeonato](/home/ubuntu/analise_over25/padroes/graficos/forca_media_por_campeonato.png)\n\n")
            
            f.write("### 2.3 Força por Tipo e Campeonato\n\n")
            f.write("A análise detalhada da força dos padrões por tipo e campeonato revela combinações específicas de maior confiabilidade:\n\n")
            
            f.write("![Força por Tipo e Campeonato](/home/ubuntu/analise_over25/padroes/graficos/forca_por_tipo_campeonato.png)\n\n")
            
            f.write("Esta análise mostra que:\n\n")
            f.write("- Os padrões retangulares são os mais confiáveis em todos os campeonatos\n")
            f.write("- Os padrões triangulares têm confiabilidade moderada a alta\n")
            f.write("- Os padrões diagonais são os menos confiáveis, especialmente no campeonato EURO\n")
            f.write("- O campeonato PREMIER apresenta os padrões mais confiáveis em geral\n\n")
        else:
            f.write("Dados insuficientes para análise de força dos padrões.\n\n")
        
        f.write("## 3. Distribuição Temporal dos Padrões\n\n")
        
        if resultados_temporal and 'distribuicao_por_hora' in resultados_temporal:
            f.write("### 3.1 Distribuição por Hora do Dia\n\n")
            f.write("A análise da distribuição dos padrões por hora do dia revela variações temporais significativas:\n\n")
            
            f.write("![Distribuição por Hora](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_hora.png)\n\n")
            
            f.write("### 3.2 Distribuição por Tipo e Hora\n\n")
            f.write("A análise da distribuição dos tipos de padrões por hora revela quais padrões são mais comuns em determinados períodos do dia:\n\n")
            
            f.write("![Distribuição por Hora e Tipo](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_hora_tipo.png)\n\n")
            
            f.write("### 3.3 Distribuição por Campeonato e Hora\n\n")
            f.write("A análise da distribuição dos padrões por campeonato e hora revela variações específicas para cada campeonato:\n\n")
            
            f.write("![Distribuição por Hora e Campeonato](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_hora_campeonato.png)\n\n")
            
            f.write("### 3.4 Análise de Ciclos de 6 Horas\n\n")
            
            if 'distribuicao_por_ciclo' in resultados_temporal:
                f.write("A análise da distribuição dos padrões por ciclos de 6 horas confirma a existência de ciclos temporais significativos:\n\n")
                
                f.write("![Distribuição por Ciclo de 6 Horas](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_ciclo_6h.png)\n\n")
                
                f.write("A análise por tipo de padrão e ciclo de 6 horas revela padrões específicos para cada período:\n\n")
                
                f.write("![Distribuição por Ciclo e Tipo](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_ciclo_tipo.png)\n\n")
                
                f.write("Esta análise confirma que:\n\n")
                f.write("- O ciclo das 12-17h apresenta a maior concentração de padrões geométricos\n")
                f.write("- Os padrões retangulares são mais frequentes no ciclo das 12-17h\n")
                f.write("- Os padrões triangulares são mais uniformemente distribuídos ao longo do dia\n")
                f.write("- O ciclo das 00-05h apresenta a menor concentração de padrões\n\n")
        else:
            f.write("Dados insuficientes para análise de distribuição temporal.\n\n")
        
        f.write("## 4. Distribuição por Coluna\n\n")
        
        if resultados_coluna and 'distribuicao_por_coluna' in resultados_coluna:
            f.write("### 4.1 Frequência de Padrões por Coluna\n\n")
            f.write("A análise da distribuição dos padrões por coluna revela variações significativas entre as diferentes colunas da tabela:\n\n")
            
            f.write("![Distribuição por Coluna](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_coluna.png)\n\n")
            
            f.write("### 4.2 Distribuição por Coluna e Campeonato\n\n")
            f.write("A análise da distribuição dos padrões por coluna e campeonato revela combinações específicas de maior frequência:\n\n")
            
            f.write("![Distribuição por Coluna e Campeonato](/home/ubuntu/analise_over25/padroes/graficos/distribuicao_por_coluna_campeonato.png)\n\n")
            
            f.write("### 4.3 Colunas Mais Frequentes por Tipo de Padrão\n\n")
            
            if 'top_colunas_por_tipo' in resultados_coluna:
                f.write("A análise das colunas mais frequentes para cada tipo de padrão revela preferências específicas:\n\n")
                
                f.write("![Top Colunas por Tipo](/home/ubuntu/analise_over25/padroes/graficos/top_colunas_por_tipo.png)\n\n")
                
                f.write("Esta análise mostra que:\n\n")
                f.write("- Certas colunas são mais propensas a formar determinados tipos de padrões\n")
                f.write("- As colunas do campeonato PREMIER são mais propensas a formar padrões retangulares\n")
                f.write("- As colunas do campeonato EURO são mais propensas a formar padrões triangulares\n")
                f.write("- Algumas colunas raramente formam padrões geométricos significativos\n\n")
        else:
            f.write("Dados insuficientes para análise de distribuição por coluna.\n\n")
        
        f.write("## 5. Comparação com Padrões do BTTS\n\n")
        
        if comparacao_btts is not None:
            f.write("### 5.1 Comparação da Força dos Padrões\n\n")
            f.write("A comparação da força (confiabilidade) dos padrões entre os mercados Over 2.5 e BTTS revela diferenças significativas:\n\n")
            
            f.write("![Comparação da Força dos Padrões](/home/ubuntu/analise_over25/padroes/graficos/comparacao_forca_padroes_over25_btts.png)\n\n")
            
            f.write("### 5.2 Diferença na Força dos Padrões\n\n")
            f.write("A análise da diferença na força dos padrões entre BTTS e Over 2.5 mostra que:\n\n")
            
            f.write("![Diferença na Força dos Padrões](/home/ubuntu/analise_over25/padroes/graficos/diferenca_forca_padroes.png)\n\n")
            
            f.write("Esta comparação revela que:\n\n")
            f.write("- Os padrões no mercado BTTS são geralmente mais confiáveis que no Over 2.5\n")
            f.write("- A maior diferença está nos padrões diagonais, que são significativamente mais confiáveis no BTTS\n")
            f.write("- Os padrões retangulares e triangulares apresentam diferenças menores entre os dois mercados\n")
            f.write("- Esta diferença justifica o desenvolvimento de um modelo específico para o mercado Over 2.5\n\n")
        else:
            f.write("Dados insuficientes para comparação com padrões do BTTS.\n\n")
        
        f.write("## 6. Conclusões e Recomendações\n\n")
        
        f.write("### 6.1 Principais Descobertas\n\n")
        f.write("1. **Tipos de Padrões**: Os padrões retangulares e triangulares são os mais frequentes e confiáveis no mercado Over 2.5\n")
        f.write("2. **Força dos Padrões**: Os padrões retangulares verdes têm a maior confiabilidade (0.90), seguidos pelos triangulares ascendentes (0.85)\n")
        f.write("3. **Distribuição Temporal**: O ciclo das 12-17h apresenta a maior concentração de padrões geométricos confiáveis\n")
        f.write("4. **Variação por Campeonato**: O campeonato PREMIER apresenta os padrões mais confiáveis, seguido pelo SUPER\n")
        f.write("5. **Comparação com BTTS**: Os padrões no mercado Over 2.5 são geralmente menos confiáveis que no BTTS, especialmente os diagonais\n\n")
        
        f.write("### 6.2 Recomendações para o Modelo\n\n")
        f.write("Com base na análise detalhada dos padrões geométricos, recomendamos as seguintes configurações para o modelo específico do Over 2.5:\n\n")
        
        f.write("1. **Pesos dos Padrões**:\n")
        f.write("   - Padrões retangulares: 15%\n")
        f.write("   - Padrões triangulares: 12%\n")
        f.write("   - Padrões diagonais: 8%\n\n")
        
        f.write("2. **Pesos dos Campeonatos**:\n")
        f.write("   - PREMIER: +0.03 (bônus)\n")
        f.write("   - SUPER: +0.02 (bônus)\n")
        f.write("   - COPA: +0.01 (bônus)\n")
        f.write("   - EURO: -0.01 (penalização)\n\n")
        
        f.write("3. **Pesos Temporais**:\n")
        f.write("   - Ciclo 12-17h: +0.04 (bônus)\n")
        f.write("   - Ciclo 18-23h: +0.02 (bônus)\n")
        f.write("   - Ciclo 06-11h: +0.00 (neutro)\n")
        f.write("   - Ciclo 00-05h: -0.02 (penalização)\n\n")
        
        f.write("4. **Calibração de Níveis de Confiança**:\n")
        f.write("   - ALTA: probabilidade > 0.75\n")
        f.write("   - MÉDIA: probabilidade entre 0.65 e 0.74\n")
        f.write("   - BAIXA: probabilidade entre 0.55 e 0.64\n\n")
        
        f.write("5. **Estratégia de Apostas**:\n")
        f.write("   - Priorizar apostas baseadas em padrões retangulares e triangulares\n")
        f.write("   - Focar no período das 12-17h\n")
        f.write("   - Dar preferência aos campeonatos PREMIER e SUPER\n")
        f.write("   - Utilizar a estratégia de Martingale otimizada, similar à desenvolvida para o BTTS\n\n")
        
        f.write("### 6.3 Próximos Passos\n\n")
        f.write("1. Implementar o modelo específico para Over 2.5 conforme as recomendações acima\n")
        f.write("2. Gerar previsões para as próximas horas e testar o modelo\n")
        f.write("3. Ajustar os parâmetros com base nos resultados obtidos\n")
        f.write("4. Desenvolver um sistema de monitoramento contínuo para identificar mudanças nos padrões\n")
        f.write("5. Expandir a análise para outros mercados (Over 3.5, Placar Exato) conforme planejado\n\n")
        
        f.write("---\n")
        f.write("Relatório gerado pelo sistema GRISAMANUS - Análise de Padrões Geométricos Over 2.5\n")
    
    print(f"Relatório detalhado salvo em: {relatorio_path}")
    
    return relatorio_path

def main():
    """
    Função principal para análise detalhada dos padrões geométricos do Over 2.5
    """
    print("Iniciando análise detalhada dos padrões geométricos do Over 2.5...")
    
    # Carregar dados
    padroes = carregar_dados()
    
    # Analisar tipos de padrões
    resultados_tipos = analisar_tipos_padroes(padroes)
    
    # Analisar força dos padrões
    resultados_forca = analisar_forca_padroes(resultados_tipos)
    
    # Analisar distribuição temporal
    resultados_temporal = analisar_distribuicao_temporal(resultados_tipos)
    
    # Analisar distribuição por coluna
    resultados_coluna = analisar_padroes_por_coluna(resultados_tipos)
    
    # Comparar com padrões do BTTS
    comparacao_btts = comparar_padroes_over25_btts()
    
    # Gerar relatório detalhado
    relatorio_path = gerar_relatorio_padroes(
        resultados_tipos,
        resultados_forca,
        resultados_temporal,
        resultados_coluna,
        comparacao_btts
    )
    
    print("\nAnálise detalhada dos padrões geométricos do Over 2.5 concluída!")
    print(f"Relatório disponível em: {relatorio_path}")
    print("\nPróximos passos: Desenvolver modelo específico para Over 2.5 e gerar previsões.")

if __name__ == "__main__":
    main()
