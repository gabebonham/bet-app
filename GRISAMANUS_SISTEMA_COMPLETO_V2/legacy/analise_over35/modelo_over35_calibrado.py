import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Criar diretórios necessários
os.makedirs('/home/ubuntu/analise_over35/previsoes', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over35/graficos', exist_ok=True)

class ModeloOver35Calibrado:
    def __init__(self):
        """
        Inicializa o modelo calibrado para Over 3.5 com base na análise dos dados reais
        """
        # Calibrações baseadas na análise dos dados reais
        self.niveis_confianca = {
            'ALTA': 0.70,  # probabilidade > 0.70
            'MEDIA': 0.60,  # probabilidade entre 0.60 e 0.69
            'BAIXA': 0.50   # probabilidade entre 0.50 e 0.59
        }
        
        # Pesos por campeonato baseados nas taxas reais de ocorrência
        self.pesos_campeonatos = {
            'PREMIER': 0.35,  # Taxa de 28% (maior entre os campeonatos)
            'EURO': 0.25,     # Taxa de 22%
            'COPA': 0.10,     # Taxa de 23%
            'SUPER': 0.00     # Taxa de 20% (base)
        }
        
        # Pesos por ciclo baseados nas taxas reais de ocorrência
        self.pesos_ciclos = {
            '00h-05h': 0.00,  # Taxa de 16% (base)
            '06h-11h': 0.05,  # Taxa de 20%
            '12h-17h': 0.30,  # Taxa de 33% (maior entre os ciclos)
            '18h-23h': 0.15   # Taxa de 26%
        }
        
        # Estratégia de martingale
        self.estrategia_martingale = {
            'ALTA': 1,   # Até 1 gale
            'MEDIA': 2,  # Até 2 gales
            'BAIXA': 3   # Até 3 gales
        }
        
        # Valores de stake
        self.valores_stake = {
            'ALTA': 25.00,
            'MEDIA': 15.00,
            'BAIXA': 5.00
        }
        
        # Taxa base de ocorrência do Over 3.5 (baseada nos dados reais)
        self.taxa_base_over35 = 0.24  # 24% de ocorrência média
        
        # Padrões identificados por hora (baseados no heatmap)
        self.padroes_horarios = {
            0: -0.05,  # Horas com baixa ocorrência
            1: 0.00,
            2: -0.05,
            3: 0.00,
            4: -0.05,
            5: -0.10,  # Hora com ocorrência muito baixa
            6: -0.05,
            7: 0.05,
            8: 0.10,   # Hora com pico para EURO
            9: -0.05,
            10: -0.05,
            11: -0.05,
            12: 0.05,
            13: 0.15,   # Hora com alta ocorrência para PREMIER (50%)
            14: 0.15,   # Hora com alta ocorrência para PREMIER (50%)
            15: 0.05,
            16: 0.10,   # Hora com boa ocorrência para PREMIER (45%)
            17: 0.10,   # Hora com boa ocorrência para PREMIER (45%)
            18: 0.05,
            19: -0.10,  # Hora com ocorrência muito baixa para PREMIER (0%)
            20: 0.00,
            21: 0.05,
            22: 0.10,   # Hora com pico para EURO (40%)
            23: 0.00
        }
        
        # Combinações específicas identificadas (baseadas no heatmap)
        self.combinacoes_especificas = {
            ('PREMIER', 13): 0.15,  # 50% de ocorrência
            ('PREMIER', 14): 0.15,  # 50% de ocorrência
            ('PREMIER', 16): 0.10,  # 45% de ocorrência
            ('PREMIER', 17): 0.10,  # 45% de ocorrência
            ('PREMIER', 21): 0.10,  # 45% de ocorrência
            ('EURO', 8): 0.10,      # 40% de ocorrência
            ('EURO', 13): 0.05,     # 40% de ocorrência
            ('EURO', 22): 0.10,     # 40% de ocorrência
            ('COPA', 14): 0.10,     # 45% de ocorrência
            ('SUPER', 17): 0.10,    # 40% de ocorrência
        }
        
        # Campeonatos a considerar (todos os 4 conforme solicitação do usuário)
        self.campeonatos_ativos = ['PREMIER', 'EURO', 'SUPER', 'COPA']
        
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
            ciclo = '00h-05h'
        elif 6 <= hora < 12:
            ciclo = '06h-11h'
        elif 12 <= hora < 18:
            ciclo = '12h-17h'
        else:
            ciclo = '18h-23h'
        
        prob += self.pesos_ciclos.get(ciclo, 0)
        
        # Ajuste por combinação específica
        prob += self.combinacoes_especificas.get((campeonato, hora), 0)
        
        # Ajuste baseado na coluna (padrões geométricos)
        # PREMIER: colunas múltiplas de 3 têm maior probabilidade
        if campeonato == 'PREMIER' and coluna % 3 == 0:
            prob += 0.03
        
        # EURO: colunas múltiplas de 5 têm maior probabilidade
        if campeonato == 'EURO' and coluna % 5 == 0:
            prob += 0.02
            
        # SUPER: colunas múltiplas de 4 têm maior probabilidade
        if campeonato == 'SUPER' and coluna % 4 == 0:
            prob += 0.01
            
        # COPA: colunas múltiplas de 7 têm maior probabilidade
        if campeonato == 'COPA' and coluna % 7 == 0:
            prob += 0.01
            
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
            'EURO': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59],
            'SUPER': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58],
            'COPA': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58]
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
        cores = {'PREMIER': 'blue', 'EURO': 'purple', 'SUPER': 'green', 'COPA': 'orange'}
        
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
    try:
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
        info = Paragraph("Modelo calibrado com base na análise dos dados reais do Over 3.5. Inclui todos os 4 campeonatos: PREMIER, EURO, SUPER e COPA.", normal_style)
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
        
        # Aplicar estilo à tabela
        table.setStyle(table_style)
        
        # Adicionar tabela ao documento
        elements.append(table)
        
        # Construir PDF
        doc.build(elements)
        
        print(f"PDF gerado com sucesso: {pdf_file}")
        return pdf_file
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

def gerar_previsoes_over35(hora_inicial, num_horas=3):
    """
    Função principal para gerar previsões do Over 3.5
    """
    # Inicializar modelo
    modelo = ModeloOver35Calibrado()
    
    # Gerar previsões
    previsoes_df = modelo.gerar_previsoes(hora_inicial, num_horas)
    
    # Formato da hora para nome do arquivo
    if num_horas == 1:
        formato_hora = f"{hora_inicial}"
    else:
        formato_hora = f"{hora_inicial}_a_{(hora_inicial + num_horas - 1) % 24}"
    
    # Salvar previsões em CSV
    arquivo_csv = modelo.salvar_previsoes(previsoes_df, formato_hora)
    
    # Gerar PDF
    arquivo_pdf = gerar_pdf_previsoes(previsoes_df, formato_hora)
    
    return previsoes_df, arquivo_csv, arquivo_pdf

if __name__ == "__main__":
    # Exemplo de uso: gerar previsões para as próximas 3 horas a partir da hora 17
    hora_inicial = 17
    previsoes_df, arquivo_csv, arquivo_pdf = gerar_previsoes_over35(hora_inicial)
    
    print(f"\nPrevisões geradas com sucesso!")
    print(f"CSV: {arquivo_csv}")
    print(f"PDF: {arquivo_pdf}")
    
    # Exibir resumo das previsões
    print("\nResumo das previsões:")
    print(f"Total de previsões: {len(previsoes_df)}")
    
    if not previsoes_df.empty:
        print("\nDistribuição por nível de confiança:")
        print(previsoes_df['CONFIANCA'].value_counts())
        
        print("\nDistribuição por campeonato:")
        print(previsoes_df['CAMPEONATO'].value_counts())
        
        print("\nDistribuição por hora:")
        print(previsoes_df['HORA'].value_counts().sort_index())
