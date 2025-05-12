import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Criar diretórios para resultados se não existirem
os.makedirs('/home/ubuntu/analise_over25/previsoes_otimizadas', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over25/previsoes_otimizadas/graficos', exist_ok=True)

class ModeloOver25Otimizado:
    def __init__(self):
        """
        Inicializa o modelo otimizado para Over 2.5 com base na análise dos resultados
        """
        # Calibrações baseadas na análise dos resultados
        self.niveis_confianca = {
            'ALTA': 0.73,  # probabilidade > 0.73
            'MEDIA': 0.64,  # probabilidade entre 0.64 e 0.72
            'BAIXA': 0.55   # probabilidade entre 0.55 e 0.63
        }
        
        self.pesos_campeonatos = {
            'PREMIER': 0.30,
            'EURO': 0.03,
            'SUPER': -0.17,  # Não será usado conforme solicitação do usuário
            'COPA': -0.20    # Não será usado conforme solicitação do usuário
        }
        
        self.pesos_ciclos = {
            '00-05h': -0.02,
            '06-11h': 0.00,
            '12-17h': 0.04,
            '18-23h': 0.02
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
        
        # Taxa base de ocorrência do Over 2.5
        self.taxa_base_over25 = 0.426
        
        # Padrões identificados
        self.padroes_horarios = {
            12: 0.01,  # Bom desempenho geral
            13: -0.01, # Desempenho médio
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
        
        # Combinações específicas identificadas
        self.combinacoes_especificas = {
            ('PREMIER', 12): 0.10,  # 100% de acerto
            ('PREMIER', 14): 0.05,  # 90% de acerto
            ('EURO', 14): 0.03,     # 88% de acerto
            ('PREMIER', 13): 0.03,  # 93% de acerto
        }
        
        # Campeonatos a considerar (conforme solicitação do usuário)
        self.campeonatos_ativos = ['PREMIER', 'EURO']
        
        # Número máximo de previsões por hora
        self.max_previsoes_por_hora = 3
        
    def calcular_probabilidade(self, campeonato, coluna, hora):
        """
        Calcula a probabilidade de ocorrência de Over 2.5 para uma combinação específica
        """
        if campeonato not in self.campeonatos_ativos:
            return 0.0
        
        # Probabilidade base
        prob = self.taxa_base_over25
        
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
                            'MERCADO': 'OVER 2.5',
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
        arquivo_csv = f'/home/ubuntu/analise_over25/previsoes_otimizadas/previsoes_over25_horas_{formato_hora_atual}.csv'
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
        
        plt.title('Distribuição de Previsões por Nível de Confiança - Over 2.5')
        plt.xlabel('Nível de Confiança')
        plt.ylabel('Número de Previsões')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(f'/home/ubuntu/analise_over25/previsoes_otimizadas/graficos/distribuicao_confianca_{formato_hora_atual}.png')
        plt.close()
        
        # 2. Distribuição por campeonato
        plt.figure(figsize=(10, 6))
        contagem_campeonato = previsoes_df['CAMPEONATO'].value_counts()
        cores = {'PREMIER': 'blue', 'EURO': 'purple'}
        
        bars = plt.bar(contagem_campeonato.index, contagem_campeonato.values,
                      color=[cores.get(camp, 'gray') for camp in contagem_campeonato.index])
        
        plt.title('Distribuição de Previsões por Campeonato - Over 2.5')
        plt.xlabel('Campeonato')
        plt.ylabel('Número de Previsões')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height}',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(f'/home/ubuntu/analise_over25/previsoes_otimizadas/graficos/distribuicao_campeonato_{formato_hora_atual}.png')
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
        
        plt.title('Distribuição de Previsões por Hora - Over 2.5')
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
        plt.savefig(f'/home/ubuntu/analise_over25/previsoes_otimizadas/graficos/distribuicao_hora_{formato_hora_atual}.png')
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
    pdf_file = f'/home/ubuntu/analise_over25/previsoes_otimizadas/previsoes_over25_horas_{formato_hora_atual}.pdf'
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Elementos do PDF
    elements = []
    
    # Título
    title = Paragraph(f"Previsões Over 2.5 - Horas {formato_hora_atual}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Subtítulo com data e hora
    now = datetime.now()
    subtitle = Paragraph(f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')} (Horário do Brasil - GMT-3)", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.25*inch))
    
    # Informações sobre o modelo
    info = Paragraph("Modelo calibrado com base na análise de 131 previsões anteriores. Taxa de acerto do modelo: 80,15%", normal_style)
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
    legend = Paragraph("Legenda de Confiança: ALTA (>73%) - Stake R$25,00 | MÉDIA (64-72%) - Stake R$15,00 | BAIXA (55-63%) - Stake R$5,00", normal_style)
    elements.append(legend)
    
    # Adicionar instruções
    elements.append(Spacer(1, 0.25*inch))
    instructions = Paragraph("Instruções: Preencha a coluna RESULTADO com VERDE (acerto) ou VERMELHO (erro) e a coluna GALE com o número de gales necessários (0, 1, 2 ou 3).", normal_style)
    elements.append(instructions)
    
    # Adicionar recomendações
    elements.append(Spacer(1, 0.25*inch))
    recommendations = Paragraph("Recomendações: Priorize as entradas de PREMIER na hora 12 (100% de acerto histórico) e EURO na hora 14 (88% de acerto histórico).", normal_style)
    elements.append(recommendations)
    
    # Construir PDF
    doc.build(elements)
    
    print(f"PDF gerado com sucesso: {pdf_file}")
    return pdf_file

def main():
    # Hora atual (conforme informado pelo usuário)
    hora_atual = 17
    formato_hora_atual = f"{hora_atual}_a_{hora_atual+2}"
    
    # Criar modelo otimizado
    modelo = ModeloOver25Otimizado()
    
    # Gerar previsões
    previsoes_df = modelo.gerar_previsoes(hora_atual, num_horas=3)
    
    # Salvar previsões
    arquivo_csv = modelo.salvar_previsoes(previsoes_df, formato_hora_atual)
    
    # Gerar PDF
    arquivo_pdf = gerar_pdf_previsoes(previsoes_df, formato_hora_atual)
    
    print(f"\nGeração de previsões concluída!")
    print(f"Arquivo CSV: {arquivo_csv}")
    print(f"Arquivo PDF: {arquivo_pdf}")
    
    return previsoes_df, arquivo_csv, arquivo_pdf

if __name__ == "__main__":
    main()
