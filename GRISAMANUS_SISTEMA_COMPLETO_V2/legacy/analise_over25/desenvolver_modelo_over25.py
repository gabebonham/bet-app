import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Criar diretórios para resultados se não existirem
os.makedirs('/home/ubuntu/analise_over25/modelo', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over25/modelo/previsoes', exist_ok=True)
os.makedirs('/home/ubuntu/analise_over25/modelo/graficos', exist_ok=True)

class ModeloOver25:
    """
    Modelo específico para previsões do mercado Over 2.5
    """
    def __init__(self):
        """
        Inicializa o modelo com os parâmetros recomendados
        """
        print("Inicializando modelo específico para Over 2.5...")
        
        # Pesos dos padrões
        self.pesos_padroes = {
            'retangular_verde': 0.15,
            'retangular_vermelho': 0.15,
            'triangular_ascendente': 0.12,
            'triangular_descendente': 0.12,
            'diagonal_principal_verde': 0.08,
            'diagonal_principal_vermelho': 0.08,
            'diagonal_secundaria_verde': 0.08,
            'diagonal_secundaria_vermelho': 0.08
        }
        
        # Pesos dos campeonatos
        self.pesos_campeonatos = {
            'PREMIER': 0.03,  # bônus
            'SUPER': 0.02,    # bônus
            'COPA': 0.01,     # bônus
            'EURO': -0.01     # penalização
        }
        
        # Pesos temporais (ciclos de 6 horas)
        self.pesos_temporais = {
            0: -0.02,  # 00-05h (penalização)
            1: 0.00,   # 06-11h (neutro)
            2: 0.04,   # 12-17h (bônus)
            3: 0.02    # 18-23h (bônus)
        }
        
        # Pesos das features
        self.pesos_features = {
            'ciclo_6h': 0.15,
            'padroes_triangulares': 0.12,
            'padroes_retangulares': 0.11,
            'correlacao_campeonatos': 0.10,
            'tendencia_global': 0.09,
            'outros_fatores': 0.43
        }
        
        # Calibração de níveis de confiança
        self.niveis_confianca = {
            'ALTA': 0.75,    # probabilidade > 0.75
            'MEDIA': 0.65,   # probabilidade entre 0.65 e 0.74
            'BAIXA': 0.55    # probabilidade entre 0.55 e 0.64
        }
        
        # Valores de stake por nível de confiança
        self.stakes = {
            'ALTA': 20.00,   # 100% da stake base
            'MEDIA': 10.00,  # 50% da stake base
            'BAIXA': 5.00    # 25% da stake base
        }
        
        # Distribuição base de Over 2.5 por campeonato
        self.distribuicao_base = {
            'PREMIER': 0.4362,
            'COPA': 0.4167,
            'EURO': 0.4269,
            'SUPER': 0.4375
        }
        
        # Correlação entre campeonatos
        self.correlacao_campeonatos = {
            ('PREMIER', 'SUPER'): 0.72,
            ('PREMIER', 'COPA'): 0.65,
            ('PREMIER', 'EURO'): 0.58,
            ('SUPER', 'COPA'): 0.63,
            ('SUPER', 'EURO'): 0.60,
            ('COPA', 'EURO'): 0.55
        }
        
        print("Modelo inicializado com sucesso!")
    
    def calcular_probabilidade(self, campeonato, hora, coluna, padroes_detectados):
        """
        Calcula a probabilidade de Over 2.5 para uma combinação específica
        """
        # Probabilidade base do campeonato
        prob_base = self.distribuicao_base.get(campeonato, 0.42)
        
        # Ajuste por campeonato
        ajuste_campeonato = self.pesos_campeonatos.get(campeonato, 0)
        
        # Ajuste temporal (ciclo de 6 horas)
        ciclo_6h = hora // 6
        ajuste_temporal = self.pesos_temporais.get(ciclo_6h, 0)
        
        # Ajuste por padrões detectados
        ajuste_padroes = 0
        for padrao, forca in padroes_detectados.items():
            peso_padrao = self.pesos_padroes.get(padrao, 0)
            ajuste_padroes += peso_padrao * forca
        
        # Ajuste por correlação entre campeonatos
        ajuste_correlacao = 0
        for par, corr in self.correlacao_campeonatos.items():
            if campeonato in par:
                ajuste_correlacao += 0.01 * corr
        
        # Calcular probabilidade final
        probabilidade = prob_base + ajuste_campeonato + ajuste_temporal + ajuste_padroes + ajuste_correlacao
        
        # Limitar entre 0 e 1
        probabilidade = max(0, min(1, probabilidade))
        
        return probabilidade
    
    def determinar_nivel_confianca(self, probabilidade):
        """
        Determina o nível de confiança com base na probabilidade
        """
        if probabilidade > self.niveis_confianca['ALTA']:
            return 'ALTA'
        elif probabilidade > self.niveis_confianca['MEDIA']:
            return 'MEDIA'
        elif probabilidade > self.niveis_confianca['BAIXA']:
            return 'BAIXA'
        else:
            return None  # Probabilidade muito baixa, não gerar previsão
    
    def determinar_stake(self, nivel_confianca):
        """
        Determina o valor da stake com base no nível de confiança
        """
        return self.stakes.get(nivel_confianca, 0)
    
    def gerar_previsoes(self, dados_entrada):
        """
        Gera previsões para o mercado Over 2.5 com base nos dados de entrada
        """
        print("Gerando previsões para o mercado Over 2.5...")
        
        previsoes = []
        
        for entrada in dados_entrada:
            campeonato = entrada['CAMPEONATO']
            hora = entrada['HORA']
            coluna = entrada['COLUNA']
            padroes_detectados = entrada.get('PADROES', {})
            
            # Calcular probabilidade
            probabilidade = self.calcular_probabilidade(campeonato, hora, coluna, padroes_detectados)
            
            # Determinar nível de confiança
            nivel_confianca = self.determinar_nivel_confianca(probabilidade)
            
            # Se o nível de confiança for None, pular esta previsão
            if nivel_confianca is None:
                continue
            
            # Determinar stake
            stake = self.determinar_stake(nivel_confianca)
            
            # Adicionar previsão
            previsao = {
                'CAMPEONATO': campeonato,
                'COLUNA': coluna,
                'HORA': hora,
                'MERCADO': 'OVER 2.5',
                'PROBABILIDADE': probabilidade,
                'CONFIANCA': nivel_confianca,
                'STAKE': f'R${stake:.2f}',
                'RESULTADO': '',
                'GALE': ''
            }
            
            previsoes.append(previsao)
        
        # Ordenar previsões por probabilidade (decrescente)
        previsoes = sorted(previsoes, key=lambda x: x['PROBABILIDADE'], reverse=True)
        
        print(f"Geradas {len(previsoes)} previsões para o mercado Over 2.5.")
        
        return previsoes
    
    def salvar_previsoes_csv(self, previsoes, arquivo):
        """
        Salva as previsões em formato CSV
        """
        df = pd.DataFrame(previsoes)
        df.to_csv(arquivo, index=False)
        print(f"Previsões salvas em: {arquivo}")
        
        return arquivo
    
    def gerar_pdf_previsoes(self, previsoes, arquivo):
        """
        Gera um PDF com as previsões no formato padronizado
        """
        print(f"Gerando PDF de previsões: {arquivo}")
        
        # Criar documento PDF
        doc = SimpleDocTemplate(arquivo, pagesize=landscape(letter))
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        
        # Título
        elements.append(Paragraph("Previsões Over 2.5 - GRISAMANUS", title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Data de geração
        elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
        elements.append(Spacer(1, 0.25*inch))
        
        # Preparar dados para tabela
        data = [['CAMPEONATO', 'COLUNA', 'HORA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'RESULTADO', 'GALE']]
        
        for p in previsoes:
            data.append([
                p['CAMPEONATO'],
                str(p['COLUNA']),
                str(p['HORA']),
                p['MERCADO'],
                f"{p['PROBABILIDADE']:.2f}",
                p['CONFIANCA'],
                p['STAKE'],
                p['RESULTADO'],
                p['GALE']
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
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        
        # Aplicar cores específicas para níveis de confiança
        for i, p in enumerate(previsoes, 1):
            if p['CONFIANCA'] == 'ALTA':
                table_style.add('BACKGROUND', (5, i), (5, i), colors.lightgreen)
            elif p['CONFIANCA'] == 'MEDIA':
                table_style.add('BACKGROUND', (5, i), (5, i), colors.lightblue)
            elif p['CONFIANCA'] == 'BAIXA':
                table_style.add('BACKGROUND', (5, i), (5, i), colors.lightcoral)
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Adicionar nota explicativa
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Notas:", styles["Heading3"]))
        elements.append(Paragraph("1. CONFIANÇA: ALTA (>0.75), MÉDIA (0.65-0.74), BAIXA (0.55-0.64)", styles["Normal"]))
        elements.append(Paragraph("2. STAKE: R$20.00 (ALTA), R$10.00 (MÉDIA), R$5.00 (BAIXA)", styles["Normal"]))
        elements.append(Paragraph("3. Preencha a coluna RESULTADO após o jogo (verde = acerto, vermelho = erro)", styles["Normal"]))
        elements.append(Paragraph("4. Preencha a coluna GALE com o número de gales necessários (se aplicável)", styles["Normal"]))
        
        # Gerar PDF
        doc.build(elements)
        
        print(f"PDF gerado com sucesso: {arquivo}")
        
        return arquivo
    
    def visualizar_distribuicao_previsoes(self, previsoes, arquivo):
        """
        Gera um gráfico com a distribuição das previsões por nível de confiança
        """
        # Contar previsões por nível de confiança
        contagem = {'ALTA': 0, 'MEDIA': 0, 'BAIXA': 0}
        
        for p in previsoes:
            contagem[p['CONFIANCA']] += 1
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        
        cores = ['lightgreen', 'lightblue', 'lightcoral']
        plt.bar(['ALTA', 'MEDIA', 'BAIXA'], [contagem['ALTA'], contagem['MEDIA'], contagem['BAIXA']], color=cores)
        
        plt.title('Distribuição de Previsões por Nível de Confiança - Over 2.5')
        plt.xlabel('Nível de Confiança')
        plt.ylabel('Número de Previsões')
        
        # Adicionar valores nas barras
        for i, v in enumerate([contagem['ALTA'], contagem['MEDIA'], contagem['BAIXA']]):
            plt.text(i, v + 0.1, str(v), ha='center')
        
        plt.tight_layout()
        plt.savefig(arquivo)
        plt.close()
        
        print(f"Gráfico de distribuição salvo em: {arquivo}")
        
        return arquivo
    
    def visualizar_distribuicao_por_campeonato(self, previsoes, arquivo):
        """
        Gera um gráfico com a distribuição das previsões por campeonato
        """
        # Contar previsões por campeonato
        campeonatos = {}
        
        for p in previsoes:
            camp = p['CAMPEONATO']
            if camp not in campeonatos:
                campeonatos[camp] = {'ALTA': 0, 'MEDIA': 0, 'BAIXA': 0}
            
            campeonatos[camp][p['CONFIANCA']] += 1
        
        # Preparar dados para o gráfico
        labels = list(campeonatos.keys())
        alta = [campeonatos[c]['ALTA'] for c in labels]
        media = [campeonatos[c]['MEDIA'] for c in labels]
        baixa = [campeonatos[c]['BAIXA'] for c in labels]
        
        # Criar gráfico
        plt.figure(figsize=(12, 6))
        
        x = np.arange(len(labels))
        width = 0.25
        
        plt.bar(x - width, alta, width, label='ALTA', color='lightgreen')
        plt.bar(x, media, width, label='MEDIA', color='lightblue')
        plt.bar(x + width, baixa, width, label='BAIXA', color='lightcoral')
        
        plt.title('Distribuição de Previsões por Campeonato - Over 2.5')
        plt.xlabel('Campeonato')
        plt.ylabel('Número de Previsões')
        plt.xticks(x, labels)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(arquivo)
        plt.close()
        
        print(f"Gráfico de distribuição por campeonato salvo em: {arquivo}")
        
        return arquivo

def simular_dados_entrada():
    """
    Simula dados de entrada para o modelo
    """
    print("Simulando dados de entrada para o modelo...")
    
    # Campeonatos e colunas
    campeonatos = {
        'PREMIER': [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57],
        'COPA': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58],
        'EURO': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59],
        'SUPER': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58]
    }
    
    # Padrões possíveis
    padroes = [
        'retangular_verde',
        'retangular_vermelho',
        'triangular_ascendente',
        'triangular_descendente',
        'diagonal_principal_verde',
        'diagonal_principal_vermelho',
        'diagonal_secundaria_verde',
        'diagonal_secundaria_vermelho'
    ]
    
    # Horas para previsão (próximas 3 horas)
    hora_atual = datetime.now().hour
    horas_previsao = [(hora_atual + i) % 24 for i in range(1, 4)]
    
    # Gerar dados de entrada
    dados_entrada = []
    
    for hora in horas_previsao:
        for campeonato, colunas in campeonatos.items():
            for coluna in colunas:
                # Simular detecção de padrões (aleatório)
                num_padroes = np.random.randint(0, 3)  # 0 a 2 padrões detectados
                
                padroes_detectados = {}
                for _ in range(num_padroes):
                    padrao = np.random.choice(padroes)
                    forca = np.random.uniform(0.6, 0.95)  # Força entre 0.6 e 0.95
                    padroes_detectados[padrao] = forca
                
                # Adicionar entrada
                entrada = {
                    'CAMPEONATO': campeonato,
                    'HORA': hora,
                    'COLUNA': coluna,
                    'PADROES': padroes_detectados
                }
                
                dados_entrada.append(entrada)
    
    print(f"Simulados {len(dados_entrada)} dados de entrada para o modelo.")
    
    return dados_entrada

def main():
    """
    Função principal para desenvolver e testar o modelo específico para Over 2.5
    """
    print("Desenvolvendo modelo específico para o mercado Over 2.5...")
    
    # Inicializar modelo
    modelo = ModeloOver25()
    
    # Simular dados de entrada
    dados_entrada = simular_dados_entrada()
    
    # Gerar previsões
    previsoes = modelo.gerar_previsoes(dados_entrada)
    
    # Salvar previsões em CSV
    arquivo_csv = '/home/ubuntu/analise_over25/modelo/previsoes/previsoes_over25.csv'
    modelo.salvar_previsoes_csv(previsoes, arquivo_csv)
    
    # Gerar PDF com previsões
    arquivo_pdf = '/home/ubuntu/analise_over25/modelo/previsoes/previsoes_over25.pdf'
    modelo.gerar_pdf_previsoes(previsoes, arquivo_pdf)
    
    # Visualizar distribuição das previsões
    arquivo_grafico1 = '/home/ubuntu/analise_over25/modelo/graficos/distribuicao_previsoes.png'
    modelo.visualizar_distribuicao_previsoes(previsoes, arquivo_grafico1)
    
    # Visualizar distribuição por campeonato
    arquivo_grafico2 = '/home/ubuntu/analise_over25/modelo/graficos/distribuicao_por_campeonato.png'
    modelo.visualizar_distribuicao_por_campeonato(previsoes, arquivo_grafico2)
    
    print("\nModelo específico para Over 2.5 desenvolvido com sucesso!")
    print(f"Previsões disponíveis em: {arquivo_pdf}")
    print(f"Gráficos disponíveis em: {arquivo_grafico1} e {arquivo_grafico2}")
    print("\nPróximos passos: Testar o modelo com dados reais e ajustar parâmetros conforme necessário.")

if __name__ == "__main__":
    main()
