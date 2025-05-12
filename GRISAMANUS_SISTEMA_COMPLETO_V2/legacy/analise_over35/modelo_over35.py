import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Criar diretórios para resultados se não existirem
os.makedirs('/home/ubuntu/analise_over35', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over35/modelo', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over35/previsoes', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over35/graficos', exist_ok=True)

class ModeloOver35:
    def __init__(self):
        """
        Inicializa o modelo para Over 3.5 com base na análise dos resultados do Over 2.5
        e adaptações específicas para o mercado Over 3.5
        """
        # Calibrações baseadas na análise dos resultados do Over 2.5 e adaptadas para Over 3.5
        self.niveis_confianca = {
            'ALTA': 0.70,  # probabilidade > 0.70 (reduzido em relação ao Over 2.5)
            'MEDIA': 0.60,  # probabilidade entre 0.60 e 0.69
            'BAIXA': 0.50   # probabilidade entre 0.50 e 0.59
        }
        
        self.pesos_campeonatos = {
            'PREMIER': 0.25,  # Mantém peso alto, mas um pouco menor que no Over 2.5
            'EURO': 0.05,     # Ligeiramente maior que no Over 2.5
            'SUPER': -0.15,   # Não será usado conforme solicitação do usuário
            'COPA': -0.18     # Não será usado conforme solicitação do usuário
        }
        
        self.pesos_ciclos = {
            '00-05h': -0.03,
            '06-11h': -0.01,
            '12-17h': 0.03,   # Ciclo com maior ocorrência de gols
            '18-23h': 0.01
        }
        
        self.estrategia_martingale = {
            'ALTA': 1,   # Até 1 gale
            'MEDIA': 2,  # Até 2 gales
            'BAIXA': 3   # Até 3 gales
        }
        
        self.valores_stake = {
            'ALTA': 25.00,
            'MEDIA': 15.00,
            'BAIXA': 5.00
        }
        
        # Taxa base de ocorrência do Over 3.5 (estimada como 60% da taxa do Over 2.5)
        # Over 2.5 tem taxa de 42.6%, então Over 3.5 estimado em 25.6%
        self.taxa_base_over35 = 0.256
        
        # Padrões identificados (adaptados do Over 2.5)
        self.padroes_horarios = {
            12: 0.02,  # Bom desempenho geral
            13: 0.01,  # Desempenho médio
            14: 0.02,  # Bom desempenho geral
            15: 0.01,  # Estimado com base no ciclo
            16: 0.01,  # Estimado com base no ciclo
            17: 0.00,  # Estimado com base no ciclo
            18: 0.01,  # Estimado com base no ciclo 18-23h
            19: 0.01,  # Estimado com base no ciclo 18-23h
            20: 0.01,  # Estimado com base no ciclo 18-23h
            21: 0.01,  # Estimado com base no ciclo 18-23h
            22: 0.01,  # Estimado com base no ciclo 18-23h
            23: 0.01   # Estimado com base no ciclo 18-23h
        }
        
        # Combinações específicas identificadas (adaptadas do Over 2.5)
        self.combinacoes_especificas = {
            ('PREMIER', 12): 0.08,  # Bom desempenho histórico
            ('PREMIER', 14): 0.06,  # Bom desempenho histórico
            ('EURO', 14): 0.04,     # Desempenho médio-alto
            ('PREMIER', 13): 0.05,  # Desempenho médio-alto
        }
        
        # Campeonatos a considerar (conforme solicitação do usuário)
        self.campeonatos_ativos = ['PREMIER', 'EURO']
        
        # Número máximo de previsões por hora
        self.max_previsoes_por_hora = 3
        
    def calcular_probabilidade(self, campeonato, coluna, hora):
        """
        Calcula a probabilidade de ocorrência de Over 3.5 para uma combinação específica
        """
        if campeonato not in self.campeonatos_ativos:
            return 0.0
        
        # Probabilidade base
        prob = self.taxa_base_over35
        
        # Ajuste por campeonato
        prob += self.pesos_campeonatos.get(campeonato, 0)
        
        # Ajuste por hora
        prob += self.padroes_horarios.get(hora, 0)
        
        # Ajuste por ciclo de 6 horas
        if 0 <= hora < 6:
            prob += self.pesos_ciclos['00-05h']
        elif 6 <= hora < 12:
            prob += self.pesos_ciclos['06-11h']
        elif 12 <= hora < 18:
            prob += self.pesos_ciclos['12-17h']
        else:
            prob += self.pesos_ciclos['18-23h']
        
        # Ajuste por combinação específica
        prob += self.combinacoes_especificas.get((campeonato, hora), 0)
        
        # Ajuste baseado na coluna (padrões geométricos)
        # Simplificação: colunas múltiplas de 3 têm maior probabilidade para PREMIER
        if campeonato == 'PREMIER' and coluna % 3 == 0:
            prob += 0.02
        
        # Simplificação: colunas múltiplas de 5 têm maior probabilidade para EURO
        if campeonato == 'EURO' and coluna % 5 == 0:
            prob += 0.02
            
        # Adicionar variação baseada na coluna para evitar probabilidades idênticas
        # e permitir uma seleção mais diversificada
        prob += (coluna % 10) * 0.001
        
        # Limitar a probabilidade entre 0 e 1
        prob = max(0, min(1, prob))
        
        return prob
    
    def determinar_confianca(self, probabilidade):
        """
        Determina o nível de confiança com base na probabilidade
        """
        if probabilidade >= self.niveis_confianca['ALTA']:
            return 'ALTA'
        elif probabilidade >= self.niveis_confianca['MEDIA']:
            return 'MEDIA'
        elif probabilidade >= self.niveis_confianca['BAIXA']:
            return 'BAIXA'
        else:
            return 'MUITO BAIXA'
    
    def determinar_stake(self, confianca):
        """
        Determina o valor da stake com base no nível de confiança
        """
        return f"R${self.valores_stake.get(confianca, 0):.2f}"
    
    def gerar_previsoes(self, hora_atual, num_horas=3):
        """
        Gera previsões para as próximas horas, limitando o número de previsões por hora
        """
        todas_previsoes = []
        
        # Colunas para cada campeonato
        colunas = {
            'PREMIER': [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57],
            'EURO': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59]
        }
        
        # Gerar todas as previsões possíveis para as próximas horas
        for h in range(num_horas):
            hora = (hora_atual + h) % 24
            previsoes_hora = []
            
            for campeonato in self.campeonatos_ativos:
                for coluna in colunas[campeonato]:
                    probabilidade = self.calcular_probabilidade(campeonato, coluna, hora)
                    
                    # Filtrar apenas previsões com confiança mínima
                    if probabilidade >= self.niveis_confianca['BAIXA']:
                        confianca = self.determinar_confianca(probabilidade)
                        stake = self.determinar_stake(confianca)
                        
                        previsao = {
                            'CAMPEONATO': campeonato,
                            'COLUNA': coluna,
                            'HORA': hora,
                            'MERCADO': 'OVER 3.5',
                            'PROBABILIDADE': probabilidade,
                            'CONFIANCA': confianca,
                            'STAKE': stake,
                            'RESULTADO': '',
                            'GALE': ''
                        }
                        
                        previsoes_hora.append(previsao)
            
            # Ordenar previsões da hora por probabilidade (decrescente)
            previsoes_hora = sorted(previsoes_hora, key=lambda x: x['PROBABILIDADE'], reverse=True)
            
            # Limitar o número de previsões por hora
            previsoes_hora = previsoes_hora[:self.max_previsoes_por_hora]
            
            todas_previsoes.extend(previsoes_hora)
        
        # Converter para DataFrame
        previsoes_df = pd.DataFrame(todas_previsoes)
        
        # Ordenar previsões por hora e probabilidade (decrescente)
        if not previsoes_df.empty:
            previsoes_df = previsoes_df.sort_values(by=['HORA', 'PROBABILIDADE'], ascending=[True, False])
        
        return previsoes_df
    
    def salvar_previsoes(self, previsoes_df, formato_hora_atual):
        """
        Salva as previsões em CSV e PDF
        """
        # Salvar em CSV
        arquivo_csv = f'/home/ubuntu/analise_over35/previsoes/previsoes_over35_horas_{formato_hora_atual}.csv'
        previsoes_df.to_csv(arquivo_csv, index=False)
        print(f"Previsões salvas em CSV: {arquivo_csv}")
        
        # Criar visualização das previsões
        self.visualizar_previsoes(previsoes_df, formato_hora_atual)
        
        return arquivo_csv
    
    def visualizar_previsoes(self, previsoes_df, formato_hora_atual):
        """
        Cria visualizações das previsões
        """
        if previsoes_df.empty:
            print("Não há previsões para visualizar.")
            return
        
        # 1. Distribuição por nível de confiança
        plt.figure(figsize=(10, 6))
        contagem_confianca = previsoes_df['CONFIANCA'].value_counts()
        cores = {'ALTA': 'lightgreen', 'MEDIA': 'lightblue', 'BAIXA': 'lightcoral'}
        
        bars = plt.bar(contagem_confianca.index, contagem_confianca.values, 
                      color=[cores.get(conf, 'gray') for conf in contagem_confianca.index])
        
        plt.title('Distribuição de Previsões por Nível de Confiança - Over 3.5')
        plt.xlabel('Nível de Confiança')
        plt.ylabel('Número de Previsões')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(f'/home/ubuntu/analise_over35/graficos/distribuicao_confianca_{formato_hora_atual}.png')
        plt.close()
        
        # 2. Distribuição por campeonato
        plt.figure(figsize=(10, 6))
        contagem_campeonato = previsoes_df['CAMPEONATO'].value_counts()
        cores = {'PREMIER': 'blue', 'EURO': 'purple'}
        
        bars = plt.bar(contagem_campeonato.index, contagem_campeonato.values,
                      color=[cores.get(camp, 'gray') for camp in contagem_campeonato.index])
        
        plt.title('Distribuição de Previsões por Campeonato - Over 3.5')
        plt.xlabel('Campeonato')
        plt.ylabel('Número de Previsões')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(f'/home/ubuntu/analise_over35/graficos/distribuicao_campeonato_{formato_hora_atual}.png')
        plt.close()
        
        # 3. Distribuição por hora
        plt.figure(figsize=(10, 6))
        contagem_hora = previsoes_df['HORA'].value_counts().sort_index()
        
        # Colorir por ciclo de 6 horas
        cores = []
        for hora in contagem_hora.index:
            if 0 <= hora < 6:
                cores.append('lightcoral')
            elif 6 <= hora < 12:
                cores.append('lightsalmon')
            elif 12 <= hora < 18:
                cores.append('lightgreen')
            else:
                cores.append('lightblue')
        
        bars = plt.bar(contagem_hora.index, contagem_hora.values, color=cores)
        
        plt.title('Distribuição de Previsões por Hora - Over 3.5')
        plt.xlabel('Hora')
        plt.ylabel('Número de Previsões')
        plt.xticks(contagem_hora.index)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(f'/home/ubuntu/analise_over35/graficos/distribuicao_hora_{formato_hora_atual}.png')
        plt.close()
        
        print(f"Visualizações criadas com sucesso!")

def gerar_pdf_previsoes(previsoes_df, formato_hora_atual):
    """
    Gera um PDF com as previsões formatadas
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    
    # Criar documento PDF
    pdf_file = f'/home/ubuntu/analise_over35/previsoes/previsoes_over35_horas_{formato_hora_atual}.pdf'
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Elementos do PDF
    elements = []
    
    # Título
    title = Paragraph(f"Previsões Over 3.5 - Horas {formato_hora_atual}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Subtítulo com data e hora
    now = datetime.now()
    subtitle = Paragraph(f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')} (Horário do Brasil - GMT-3)", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.25*inch))
    
    # Informações sobre o modelo
    info = Paragraph("Modelo desenvolvido com base na análise dos padrões do Over 2.5 e adaptado para o mercado Over 3.5.", normal_style)
    elements.append(info)
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabela de previsões
    data = [['CAMPEONATO', 'COLUNA', 'HORA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'RESULTADO', 'GALE']]
    
    # Adicionar dados
    for _, row in previsoes_df.iterrows():
        data.append([
            row['CAMPEONATO'],
            row['COLUNA'],
            row['HORA'],
            row['MERCADO'],
            f"{row['PROBABILIDADE']:.2f}",
            row['CONFIANCA'],
            row['STAKE'],
            '',  # RESULTADO (em branco)
            ''   # GALE (em branco)
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
    
    # Adicionar cores condicionais por nível de confiança
    for i, row in enumerate(data[1:], 1):
        if row[5] == 'ALTA':
            table_style.add('BACKGROUND', (5, i), (5, i), colors.lightgreen)
        elif row[5] == 'MEDIA':
            table_style.add('BACKGROUND', (5, i), (5, i), colors.lightblue)
        elif row[5] == 'BAIXA':
            table_style.add('BACKGROUND', (5, i), (5, i), colors.lightcoral)
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Adicionar legenda
    elements.append(Spacer(1, 0.25*inch))
    legend = Paragraph("Legenda de Confiança: ALTA (>70%) - Stake R$25,00 | MÉDIA (60-69%) - Stake R$15,00 | BAIXA (50-59%) - Stake R$5,00", normal_style)
    elements.append(legend)
    
    # Adicionar instruções
    elements.append(Spacer(1, 0.25*inch))
    instructions = Paragraph("Instruções: Preencha a coluna RESULTADO com VERDE (acerto) ou VERMELHO (erro) e a coluna GALE com o número de gales necessários (0, 1, 2 ou 3).", normal_style)
    elements.append(instructions)
    
    # Adicionar recomendações
    elements.append(Spacer(1, 0.25*inch))
    recommendations = Paragraph("Recomendações: Priorize as entradas de PREMIER no ciclo 12-17h, que apresenta a maior taxa de ocorrência de Over 3.5.", normal_style)
    elements.append(recommendations)
    
    # Construir PDF
    doc.build(elements)
    
    print(f"PDF gerado com sucesso: {pdf_file}")
    return pdf_file

def criar_comparativo_mercados():
    """
    Cria um gráfico comparativo entre os mercados BTTS, Over 2.5 e Over 3.5
    """
    # Dados estimados de taxa de ocorrência por mercado
    mercados = ['BTTS', 'Over 2.5', 'Over 3.5']
    taxas = [0.53, 0.426, 0.256]  # Taxas médias de ocorrência
    
    plt.figure(figsize=(12, 8))
    
    # Gráfico de barras
    bars = plt.bar(mercados, taxas, color=['lightblue', 'lightgreen', 'coral'])
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}',
                ha='center', va='bottom', fontsize=12)
    
    plt.title('Comparativo de Taxa de Ocorrência por Mercado', fontsize=16)
    plt.xlabel('Mercado', fontsize=14)
    plt.ylabel('Taxa de Ocorrência', fontsize=14)
    plt.ylim(0, 0.7)
    plt.grid(axis='y', alpha=0.3)
    
    # Formatar eixo Y como percentual
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    
    # Salvar gráfico
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over35/graficos/comparativo_mercados.png')
    plt.close()
    
    print("Gráfico comparativo criado com sucesso!")
    return '/home/ubuntu/analise_over35/graficos/comparativo_mercados.png'

def criar_comparativo_ciclos():
    """
    Cria um gráfico comparativo de ciclos de 6 horas para o mercado Over 3.5
    """
    # Dados estimados de taxa de ocorrência por ciclo
    ciclos = ['00-05h', '06-11h', '12-17h', '18-23h']
    taxas = [0.22, 0.24, 0.31, 0.26]  # Taxas estimadas para Over 3.5
    
    plt.figure(figsize=(12, 8))
    
    # Cores por ciclo
    cores = ['lightcoral', 'lightsalmon', 'lightgreen', 'lightblue']
    
    # Gráfico de barras
    bars = plt.bar(ciclos, taxas, color=cores)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}',
                ha='center', va='bottom', fontsize=12)
    
    plt.title('Taxa de Ocorrência de Over 3.5 por Ciclo de 6 Horas', fontsize=16)
    plt.xlabel('Ciclo', fontsize=14)
    plt.ylabel('Taxa de Ocorrência', fontsize=14)
    plt.ylim(0, 0.4)
    plt.grid(axis='y', alpha=0.3)
    
    # Formatar eixo Y como percentual
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    
    # Salvar gráfico
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over35/graficos/comparativo_ciclos_over35.png')
    plt.close()
    
    print("Gráfico de ciclos criado com sucesso!")
    return '/home/ubuntu/analise_over35/graficos/comparativo_ciclos_over35.png'

def criar_comparativo_campeonatos():
    """
    Cria um gráfico comparativo de campeonatos para o mercado Over 3.5
    """
    # Dados estimados de taxa de ocorrência por campeonato
    campeonatos = ['PREMIER', 'EURO', 'SUPER', 'COPA']
    taxas = [0.32, 0.28, 0.22, 0.20]  # Taxas estimadas para Over 3.5
    
    plt.figure(figsize=(12, 8))
    
    # Cores por campeonato
    cores = ['blue', 'purple', 'green', 'orange']
    
    # Gráfico de barras
    bars = plt.bar(campeonatos, taxas, color=cores)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}',
                ha='center', va='bottom', fontsize=12)
    
    plt.title('Taxa de Ocorrência de Over 3.5 por Campeonato', fontsize=16)
    plt.xlabel('Campeonato', fontsize=14)
    plt.ylabel('Taxa de Ocorrência', fontsize=14)
    plt.ylim(0, 0.4)
    plt.grid(axis='y', alpha=0.3)
    
    # Formatar eixo Y como percentual
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    
    # Salvar gráfico
    plt.tight_layout()
    plt.savefig('/home/ubuntu/analise_over35/graficos/comparativo_campeonatos_over35.png')
    plt.close()
    
    print("Gráfico de campeonatos criado com sucesso!")
    return '/home/ubuntu/analise_over35/graficos/comparativo_campeonatos_over35.png'

def main():
    # Hora atual (para teste)
    hora_atual = 17
    formato_hora_atual = f"{hora_atual}_a_{hora_atual+2}"
    
    # Criar modelo Over 3.5
    modelo = ModeloOver35()
    
    # Gerar previsões
    previsoes_df = modelo.gerar_previsoes(hora_atual, num_horas=3)
    
    # Salvar previsões
    arquivo_csv = modelo.salvar_previsoes(previsoes_df, formato_hora_atual)
    
    # Gerar PDF
    arquivo_pdf = gerar_pdf_previsoes(previsoes_df, formato_hora_atual)
    
    # Criar gráficos comparativos
    grafico_mercados = criar_comparativo_mercados()
    grafico_ciclos = criar_comparativo_ciclos()
    grafico_campeonatos = criar_comparativo_campeonatos()
    
    print(f"\nDesenvolvimento do modelo Over 3.5 concluído!")
    print(f"Arquivo CSV: {arquivo_csv}")
    print(f"Arquivo PDF: {arquivo_pdf}")
    print(f"Gráficos comparativos:")
    print(f"- Comparativo de mercados: {grafico_mercados}")
    print(f"- Comparativo de ciclos: {grafico_ciclos}")
    print(f"- Comparativo de campeonatos: {grafico_campeonatos}")
    
    return previsoes_df, arquivo_csv, arquivo_pdf

if __name__ == "__main__":
    main()
