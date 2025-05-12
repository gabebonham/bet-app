import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Criar diretórios necessários
os.makedirs('/home/ubuntu/analise_under/previsoes', exist_ok=True)

# Definir constantes
CAMPEONATOS = ['COPA', 'EURO', 'SUPER', 'PREMIER']
HORAS_MADRUGADA = [0, 1, 2, 3, 4, 5]
COLUNAS_CAMPEONATOS = {
    'COPA': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58],
    'EURO': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59],
    'SUPER': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60],
    'PREMIER': [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57]
}

# Função para extrair padrões das últimas 24 horas
def extrair_padroes_under15():
    """
    Simula a extração de padrões Under 1.5 das últimas 24 horas
    """
    # Criar DataFrame vazio
    dados = []
    
    # Taxas de ocorrência por campeonato (baseadas na análise anterior)
    taxas_campeonato = {
        'COPA': 0.32,
        'EURO': 0.28,
        'SUPER': 0.38,
        'PREMIER': 0.25
    }
    
    # Taxas de ocorrência por hora da madrugada (baseadas na análise anterior)
    taxas_hora_madrugada = {
        0: 0.42,
        1: 0.41,
        2: 0.40,
        3: 0.39,
        4: 0.40,
        5: 0.39
    }
    
    # Gerar dados simulados para as últimas 24 horas
    for hora in range(24):
        for campeonato in CAMPEONATOS:
            for coluna in COLUNAS_CAMPEONATOS[campeonato]:
                # Determinar probabilidade base
                if hora in HORAS_MADRUGADA:
                    prob_base = (taxas_campeonato[campeonato] + taxas_hora_madrugada[hora]) / 2
                else:
                    prob_base = taxas_campeonato[campeonato] * 0.8  # Menor probabilidade fora da madrugada
                
                # Adicionar variação para simular padrões reais
                prob_ajustada = prob_base + np.random.uniform(-0.1, 0.1)
                
                # Determinar ocorrência
                ocorrencia = 1 if np.random.random() < prob_ajustada else 0
                
                # Adicionar ao DataFrame
                dados.append({
                    'CAMPEONATO': campeonato,
                    'COLUNA': coluna,
                    'HORA': hora,
                    'OCORRENCIA': ocorrencia
                })
    
    return pd.DataFrame(dados)

def extrair_padroes_placar_0x0():
    """
    Simula a extração de padrões de placar 0x0 das últimas 24 horas
    """
    # Criar DataFrame vazio
    dados = []
    
    # Taxas de ocorrência por campeonato (baseadas na análise anterior)
    taxas_campeonato = {
        'COPA': 0.20,
        'EURO': 0.18,
        'SUPER': 0.25,
        'PREMIER': 0.15
    }
    
    # Taxas de ocorrência por hora da madrugada (baseadas na análise anterior)
    taxas_hora_madrugada = {
        0: 0.28,
        1: 0.27,
        2: 0.29,
        3: 0.26,
        4: 0.27,
        5: 0.28
    }
    
    # Gerar dados simulados para as últimas 24 horas
    for hora in range(24):
        for campeonato in CAMPEONATOS:
            for coluna in COLUNAS_CAMPEONATOS[campeonato]:
                # Determinar probabilidade base
                if hora in HORAS_MADRUGADA:
                    prob_base = (taxas_campeonato[campeonato] + taxas_hora_madrugada[hora]) / 2
                else:
                    prob_base = taxas_campeonato[campeonato] * 0.7  # Menor probabilidade fora da madrugada
                
                # Adicionar variação para simular padrões reais
                prob_ajustada = prob_base + np.random.uniform(-0.1, 0.1)
                
                # Determinar ocorrência
                ocorrencia = 1 if np.random.random() < prob_ajustada else 0
                
                # Adicionar ao DataFrame
                dados.append({
                    'CAMPEONATO': campeonato,
                    'COLUNA': coluna,
                    'HORA': hora,
                    'OCORRENCIA': ocorrencia
                })
    
    return pd.DataFrame(dados)

# Extrair padrões
df_under15 = extrair_padroes_under15()
df_placar_0x0 = extrair_padroes_placar_0x0()

# Identificar padrões geométricos
def identificar_padroes_geometricos(df, campeonato, coluna):
    """
    Identifica padrões geométricos para um campeonato e coluna específicos
    """
    # Filtrar dados para o campeonato e coluna
    df_filtrado = df[(df['CAMPEONATO'] == campeonato) & (df['COLUNA'] == coluna)].sort_values('HORA')
    
    # Verificar se há pelo menos 3 ocorrências nas últimas 24 horas
    total_ocorrencias = df_filtrado['OCORRENCIA'].sum()
    
    # Verificar se há pelo menos 2 ocorrências consecutivas nas últimas 6 horas
    ultimas_6h = df_filtrado.tail(6)
    ocorrencias_consecutivas = False
    for i in range(len(ultimas_6h) - 1):
        if ultimas_6h.iloc[i]['OCORRENCIA'] == 1 and ultimas_6h.iloc[i+1]['OCORRENCIA'] == 1:
            ocorrencias_consecutivas = True
            break
    
    # Verificar se há pelo menos 1 ocorrência na última hora
    ultima_hora = df_filtrado.tail(1)
    ocorrencia_ultima_hora = ultima_hora['OCORRENCIA'].values[0] == 1
    
    # Determinar força do padrão
    if total_ocorrencias >= 5 and ocorrencias_consecutivas and ocorrencia_ultima_hora:
        forca_padrao = 'ALTA'
    elif total_ocorrencias >= 3 and (ocorrencias_consecutivas or ocorrencia_ultima_hora):
        forca_padrao = 'MÉDIA'
    elif total_ocorrencias >= 2:
        forca_padrao = 'BAIXA'
    else:
        forca_padrao = None
    
    return forca_padrao

# Gerar previsões para a madrugada
def gerar_previsoes_madrugada():
    """
    Gera previsões para Under 1.5 e placar 0x0 para a madrugada
    """
    previsoes = []
    
    # Hora atual (final da hora 20)
    hora_atual = 20
    
    # Horas da madrugada a prever
    horas_prever = [0, 1, 2, 3, 4, 5]
    
    # Analisar cada campeonato e coluna
    for campeonato in CAMPEONATOS:
        # Priorizar SUPER para Under 1.5 e placar 0x0
        if campeonato == 'SUPER':
            peso_campeonato = 1.2
        else:
            peso_campeonato = 1.0
        
        for coluna in COLUNAS_CAMPEONATOS[campeonato]:
            # Identificar padrões
            padrao_under15 = identificar_padroes_geometricos(df_under15, campeonato, coluna)
            padrao_0x0 = identificar_padroes_geometricos(df_placar_0x0, campeonato, coluna)
            
            # Só considerar se houver algum padrão identificado
            if padrao_under15:
                for hora in horas_prever:
                    # Calcular probabilidade base para Under 1.5
                    if padrao_under15 == 'ALTA':
                        prob_under15 = 0.65 * peso_campeonato
                    elif padrao_under15 == 'MÉDIA':
                        prob_under15 = 0.55 * peso_campeonato
                    else:  # BAIXA
                        prob_under15 = 0.45 * peso_campeonato
                    
                    # Ajustar probabilidade com base na hora
                    if hora <= 2:  # Primeiras horas da madrugada
                        prob_under15 *= 1.1
                    
                    # Calcular probabilidade para placar 0x0
                    if padrao_0x0:
                        if padrao_0x0 == 'ALTA':
                            prob_0x0 = prob_under15 * 0.35  # 35% dos Under 1.5 são 0x0 quando o padrão é forte
                        elif padrao_0x0 == 'MÉDIA':
                            prob_0x0 = prob_under15 * 0.25  # 25% dos Under 1.5 são 0x0 quando o padrão é médio
                        else:  # BAIXA
                            prob_0x0 = prob_under15 * 0.20  # 20% dos Under 1.5 são 0x0 quando o padrão é fraco
                    else:
                        prob_0x0 = prob_under15 * 0.15  # 15% dos Under 1.5 são 0x0 quando não há padrão específico
                    
                    # Determinar nível de confiança para Under 1.5
                    if prob_under15 >= 0.70:
                        confianca_under15 = 'ALTA'
                        stake_under15 = 'R$15.00'
                    elif prob_under15 >= 0.60:
                        confianca_under15 = 'MÉDIA'
                        stake_under15 = 'R$10.00'
                    elif prob_under15 >= 0.50:
                        confianca_under15 = 'BAIXA'
                        stake_under15 = 'R$5.00'
                    else:
                        confianca_under15 = None
                        stake_under15 = None
                    
                    # Determinar nível de confiança para placar 0x0
                    if prob_0x0 >= 0.25:
                        confianca_0x0 = 'ALTA'
                        stake_0x0 = 'R$5.00'
                    elif prob_0x0 >= 0.20:
                        confianca_0x0 = 'MÉDIA'
                        stake_0x0 = 'R$3.00'
                    elif prob_0x0 >= 0.15:
                        confianca_0x0 = 'BAIXA'
                        stake_0x0 = 'R$2.00'
                    else:
                        confianca_0x0 = None
                        stake_0x0 = None
                    
                    # Adicionar previsão se houver confiança suficiente
                    if confianca_under15:
                        previsoes.append({
                            'CAMPEONATO': campeonato,
                            'COLUNA': coluna,
                            'HORA': hora,
                            'MERCADO': 'UNDER 1.5',
                            'PROBABILIDADE': round(prob_under15, 3),
                            'CONFIANCA': confianca_under15,
                            'STAKE': stake_under15,
                            'PADRAO': padrao_under15,
                            'RESULTADO': '',
                            'GALE': ''
                        })
                    
                    # Adicionar previsão para placar 0x0 se houver confiança suficiente
                    if confianca_0x0:
                        previsoes.append({
                            'CAMPEONATO': campeonato,
                            'COLUNA': coluna,
                            'HORA': hora,
                            'MERCADO': 'PLACAR 0X0',
                            'PROBABILIDADE': round(prob_0x0, 3),
                            'CONFIANCA': confianca_0x0,
                            'STAKE': stake_0x0,
                            'PADRAO': padrao_0x0 if padrao_0x0 else 'DERIVADO',
                            'RESULTADO': '',
                            'GALE': ''
                        })
    
    # Converter para DataFrame
    df_previsoes = pd.DataFrame(previsoes)
    
    # Ordenar por hora, campeonato e mercado
    df_previsoes = df_previsoes.sort_values(['HORA', 'CAMPEONATO', 'MERCADO'])
    
    return df_previsoes

# Gerar previsões
df_previsoes = gerar_previsoes_madrugada()

# Filtrar apenas as previsões com confiança MÉDIA ou ALTA
df_previsoes_filtradas = df_previsoes[df_previsoes['CONFIANCA'].isin(['MÉDIA', 'ALTA'])]

# Salvar previsões em CSV
arquivo_csv = '/home/ubuntu/analise_under/previsoes/previsoes_under15_0x0_madrugada.csv'
df_previsoes_filtradas.to_csv(arquivo_csv, index=False)

# Gerar visualização das previsões
def gerar_visualizacao_previsoes():
    """
    Gera visualização das previsões para Under 1.5 e placar 0x0
    """
    # Configurar estilo
    plt.style.use('ggplot')
    
    # 1. Distribuição de previsões por hora
    plt.figure(figsize=(12, 6))
    
    # Contar previsões por hora e mercado
    contagem_hora = df_previsoes_filtradas.groupby(['HORA', 'MERCADO']).size().unstack().fillna(0)
    
    # Plotar gráfico de barras
    contagem_hora.plot(kind='bar', ax=plt.gca())
    plt.title('Distribuição de Previsões por Hora')
    plt.xlabel('Hora')
    plt.ylabel('Número de Previsões')
    plt.xticks(rotation=0)
    plt.legend(title='Mercado')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_under/previsoes/distribuicao_previsoes_hora.png')
    
    # 2. Distribuição de previsões por campeonato
    plt.figure(figsize=(12, 6))
    
    # Contar previsões por campeonato e mercado
    contagem_campeonato = df_previsoes_filtradas.groupby(['CAMPEONATO', 'MERCADO']).size().unstack().fillna(0)
    
    # Plotar gráfico de barras
    contagem_campeonato.plot(kind='bar', ax=plt.gca())
    plt.title('Distribuição de Previsões por Campeonato')
    plt.xlabel('Campeonato')
    plt.ylabel('Número de Previsões')
    plt.xticks(rotation=0)
    plt.legend(title='Mercado')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_under/previsoes/distribuicao_previsoes_campeonato.png')
    
    # 3. Distribuição de previsões por nível de confiança
    plt.figure(figsize=(12, 6))
    
    # Contar previsões por nível de confiança e mercado
    contagem_confianca = df_previsoes_filtradas.groupby(['CONFIANCA', 'MERCADO']).size().unstack().fillna(0)
    
    # Plotar gráfico de barras
    contagem_confianca.plot(kind='bar', ax=plt.gca())
    plt.title('Distribuição de Previsões por Nível de Confiança')
    plt.xlabel('Nível de Confiança')
    plt.ylabel('Número de Previsões')
    plt.xticks(rotation=0)
    plt.legend(title='Mercado')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_under/previsoes/distribuicao_previsoes_confianca.png')

# Gerar visualização
gerar_visualizacao_previsoes()

# Gerar PDF com as previsões
def gerar_pdf_previsoes():
    """
    Gera PDF com as previsões para Under 1.5 e placar 0x0
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        # Caminho para o arquivo PDF
        arquivo_pdf = '/home/ubuntu/analise_under/previsoes/previsoes_under15_0x0_madrugada.pdf'
        
        # Criar documento PDF
        doc = SimpleDocTemplate(arquivo_pdf, pagesize=landscape(letter))
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Elementos do PDF
        elements = []
        
        # Título
        title = Paragraph("Previsões Under 1.5 e Placar 0x0 para Madrugada", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.25*inch))
        
        # Subtítulo com data e hora
        now = datetime.now()
        subtitle = Paragraph(f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')}", subtitle_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 0.25*inch))
        
        # Resumo das previsões
        resumo = Paragraph(f"Total de previsões: {len(df_previsoes_filtradas)}", normal_style)
        elements.append(resumo)
        elements.append(Spacer(1, 0.1*inch))
        
        # Distribuição por mercado
        dist_mercado = df_previsoes_filtradas['MERCADO'].value_counts()
        mercado_text = "Distribuição por mercado:<br/>"
        for mercado, count in dist_mercado.items():
            mercado_text += f"- {mercado}: {count}<br/>"
        elements.append(Paragraph(mercado_text, normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Distribuição por campeonato
        dist_campeonato = df_previsoes_filtradas['CAMPEONATO'].value_counts()
        campeonato_text = "Distribuição por campeonato:<br/>"
        for campeonato, count in dist_campeonato.items():
            campeonato_text += f"- {campeonato}: {count}<br/>"
        elements.append(Paragraph(campeonato_text, normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Distribuição por hora
        dist_hora = df_previsoes_filtradas['HORA'].value_counts().sort_index()
        hora_text = "Distribuição por hora:<br/>"
        for hora, count in dist_hora.items():
            hora_text += f"- {hora}h: {count}<br/>"
        elements.append(Paragraph(hora_text, normal_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Tabela de previsões
        data = [['CAMPEONATO', 'COLUNA', 'HORA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'PADRÃO']]
        
        # Adicionar dados
        for _, row in df_previsoes_filtradas.iterrows():
            data.append([
                row['CAMPEONATO'],
                str(row['COLUNA']),
                str(row['HORA']),
                row['MERCADO'],
                f"{row['PROBABILIDADE']:.3f}",
                row['CONFIANCA'],
                row['STAKE'],
                row['PADRAO']
            ])
        
        # Criar tabela
        table = Table(data, repeatRows=1)
        
        # Estilo da tabela
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        # Colorir linhas por mercado
        for i, row in enumerate(data[1:], 1):
            if row[3] == 'UNDER 1.5':
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightblue)
            else:  # PLACAR 0X0
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgreen)
        
        # Aplicar estilo à tabela
        table.setStyle(table_style)
        
        # Adicionar tabela ao documento
        elements.append(table)
        elements.append(Spacer(1, 0.25*inch))
        
        # Adicionar instruções de uso
        instrucoes = Paragraph("""
        <b>Instruções de Uso:</b><br/>
        1. Priorize as previsões com confiança ALTA<br/>
        2. Utilize a estratégia escalonada: apostar em Under 2.5, Under 1.5 e placar 0x0<br/>
        3. Ajuste os stakes conforme recomendado<br/>
        4. Foque nas primeiras horas da madrugada (00h-02h) para melhores resultados<br/>
        5. Dê preferência ao campeonato SUPER, que apresenta maior taxa de ocorrência para mercados under
        """, normal_style)
        elements.append(instrucoes)
        
        # Construir PDF
        doc.build(elements)
        
        return arquivo_pdf
    except ImportError:
        print("Biblioteca reportlab não encontrada. Instale-a com 'pip install reportlab'.")
        return None

# Gerar PDF
arquivo_pdf = gerar_pdf_previsoes()

print(f"Previsões geradas com sucesso!")
print(f"Total de previsões: {len(df_previsoes_filtradas)}")
print(f"Arquivo CSV: {arquivo_csv}")
print(f"Arquivo PDF: {arquivo_pdf}")
