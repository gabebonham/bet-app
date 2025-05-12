import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Criar diretórios para resultados se não existirem
os.makedirs('/home/ubuntu/tabelas_operacionais/consolidado', exist_ok=True)
os.makedirs('/home/ubuntu/tabelas_operacionais/consolidado/graficos', exist_ok=True)

def criar_tabela_operacional_consolidada():
    """
    Cria uma tabela operacional consolidada que integra os três mercados:
    BTTS, Over 2.5 e Over 3.5
    """
    # Definir orientações específicas para cada mercado
    orientacoes = {
        'BTTS': 'Usar os DOIS melhores campeonatos (PREMIER e EURO)',
        'OVER 2.5': 'Usar SOMENTE o campeonato PREMIER (95% de acerto)',
        'OVER 3.5': 'Usar TODOS os 4 campeonatos (PREMIER, EURO, SUPER e COPA)'
    }
    
    # Definir ciclos de horários e suas características
    ciclos = {
        '00-05h': {
            'BTTS': '48,5% de ocorrência (baixo)',
            'OVER 2.5': '37,2% de ocorrência (baixo)',
            'OVER 3.5': '22,0% de ocorrência (baixo)'
        },
        '06-11h': {
            'BTTS': '52,3% de ocorrência (médio)',
            'OVER 2.5': '40,5% de ocorrência (médio)',
            'OVER 3.5': '24,0% de ocorrência (médio)'
        },
        '12-17h': {
            'BTTS': '56,5% de ocorrência (alto)',
            'OVER 2.5': '48,7% de ocorrência (alto)',
            'OVER 3.5': '31,0% de ocorrência (alto)'
        },
        '18-23h': {
            'BTTS': '54,2% de ocorrência (médio-alto)',
            'OVER 2.5': '44,3% de ocorrência (médio-alto)',
            'OVER 3.5': '26,0% de ocorrência (médio)'
        }
    }
    
    # Definir horários recomendados por mercado
    horarios_recomendados = {
        'BTTS': [12, 13, 14, 18, 19, 20],
        'OVER 2.5': [12, 14, 15, 18, 19],
        'OVER 3.5': [12, 13, 14, 15]
    }
    
    # Definir campeonatos recomendados por mercado
    campeonatos_recomendados = {
        'BTTS': ['PREMIER', 'EURO'],
        'OVER 2.5': ['PREMIER'],
        'OVER 3.5': ['PREMIER', 'EURO', 'SUPER', 'COPA']
    }
    
    # Definir combinações específicas de alto desempenho
    combinacoes_alto_desempenho = {
        'BTTS': [
            ('PREMIER', 12, '92% de acerto'),
            ('PREMIER', 14, '89% de acerto'),
            ('EURO', 14, '85% de acerto'),
            ('PREMIER', 18, '87% de acerto')
        ],
        'OVER 2.5': [
            ('PREMIER', 12, '100% de acerto'),
            ('PREMIER', 14, '90% de acerto'),
            ('PREMIER', 13, '93% de acerto')
        ],
        'OVER 3.5': [
            ('PREMIER', 12, 'Alta probabilidade'),
            ('PREMIER', 14, 'Alta probabilidade'),
            ('EURO', 14, 'Média probabilidade')
        ]
    }
    
    # Definir níveis de confiança e stakes por mercado
    niveis_confianca = {
        'BTTS': {
            'ALTA': {'probabilidade': '>0.80', 'stake': 'R$25.00'},
            'MEDIA': {'probabilidade': '0.70-0.79', 'stake': 'R$15.00'},
            'BAIXA': {'probabilidade': '0.55-0.69', 'stake': 'R$5.00'}
        },
        'OVER 2.5': {
            'ALTA': {'probabilidade': '>0.73', 'stake': 'R$25.00'},
            'MEDIA': {'probabilidade': '0.64-0.72', 'stake': 'R$15.00'},
            'BAIXA': {'probabilidade': '0.55-0.63', 'stake': 'R$5.00'}
        },
        'OVER 3.5': {
            'ALTA': {'probabilidade': '>0.70', 'stake': 'R$25.00'},
            'MEDIA': {'probabilidade': '0.60-0.69', 'stake': 'R$15.00'},
            'BAIXA': {'probabilidade': '0.50-0.59', 'stake': 'R$5.00'}
        }
    }
    
    # Criar gráfico de heatmap para horários recomendados
    criar_heatmap_horarios_recomendados(horarios_recomendados)
    
    # Criar gráfico comparativo de mercados
    criar_grafico_comparativo_mercados()
    
    # Gerar PDF com a tabela operacional consolidada
    gerar_pdf_tabela_operacional(
        orientacoes,
        ciclos,
        horarios_recomendados,
        campeonatos_recomendados,
        combinacoes_alto_desempenho,
        niveis_confianca
    )

def criar_heatmap_horarios_recomendados(horarios_recomendados):
    """
    Cria um heatmap mostrando os horários recomendados para cada mercado
    """
    # Criar matriz para o heatmap
    horas = list(range(24))
    mercados = ['BTTS', 'OVER 2.5', 'OVER 3.5']
    
    # Inicializar matriz com zeros
    matriz = np.zeros((len(mercados), len(horas)))
    
    # Preencher matriz com valores
    for i, mercado in enumerate(mercados):
        for hora in horarios_recomendados[mercado]:
            matriz[i, hora] = 1
    
    # Criar figura
    plt.figure(figsize=(15, 6))
    
    # Criar heatmap
    sns.heatmap(
        matriz,
        annot=False,
        cmap=['white', 'lightgreen'],
        cbar=False,
        linewidths=1,
        linecolor='gray',
        xticklabels=horas,
        yticklabels=mercados
    )
    
    # Adicionar título e labels
    plt.title('Horários Recomendados por Mercado', fontsize=16)
    plt.xlabel('Hora (Horário de Brasília - GMT-3)', fontsize=12)
    plt.ylabel('Mercado', fontsize=12)
    
    # Adicionar linhas verticais para separar os ciclos de 6 horas
    for i in range(0, 25, 6):
        plt.axvline(x=i, color='black', linestyle='--', alpha=0.5)
    
    # Adicionar textos para os ciclos
    plt.text(3, -0.5, 'Ciclo 00-05h', ha='center', fontsize=10)
    plt.text(9, -0.5, 'Ciclo 06-11h', ha='center', fontsize=10)
    plt.text(15, -0.5, 'Ciclo 12-17h', ha='center', fontsize=10)
    plt.text(21, -0.5, 'Ciclo 18-23h', ha='center', fontsize=10)
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('/home/ubuntu/tabelas_operacionais/consolidado/graficos/heatmap_horarios_recomendados.png')
    plt.close()
    
    print("Heatmap de horários recomendados criado com sucesso!")

def criar_grafico_comparativo_mercados():
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
    plt.savefig('/home/ubuntu/tabelas_operacionais/consolidado/graficos/comparativo_mercados.png')
    plt.close()
    
    print("Gráfico comparativo de mercados criado com sucesso!")

def gerar_pdf_tabela_operacional(
    orientacoes,
    ciclos,
    horarios_recomendados,
    campeonatos_recomendados,
    combinacoes_alto_desempenho,
    niveis_confianca
):
    """
    Gera um PDF com a tabela operacional consolidada
    """
    # Criar documento PDF
    pdf_file = '/home/ubuntu/tabelas_operacionais/consolidado/GRISAMANUS_tabela_operacional_consolidada.pdf'
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    section_style = styles['Heading3']
    normal_style = styles['Normal']
    
    # Criar estilo para texto centralizado
    centered_style = ParagraphStyle(
        'CenteredStyle',
        parent=styles['Normal'],
        alignment=1,  # 0=left, 1=center, 2=right
        spaceAfter=12
    )
    
    # Elementos do PDF
    elements = []
    
    # Título
    title = Paragraph("GRISAMANUS - Tabela Operacional Consolidada", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Subtítulo com data e hora
    now = datetime.now()
    subtitle = Paragraph(f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')} (Horário do Brasil - GMT-3)", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.25*inch))
    
    # Introdução
    intro = Paragraph(
        "Esta tabela operacional consolidada integra os três mercados (BTTS, Over 2.5 e Over 3.5) "
        "e fornece orientações específicas para cada um, baseadas na análise de dados históricos "
        "e nos padrões identificados pelo sistema GRISAMANUS.",
        normal_style
    )
    elements.append(intro)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 1: Orientações Específicas por Mercado
    section1 = Paragraph("1. Orientações Específicas por Mercado", section_style)
    elements.append(section1)
    elements.append(Spacer(1, 0.1*inch))
    
    # Tabela de orientações
    data_orientacoes = [['Mercado', 'Orientação']]
    for mercado, orientacao in orientacoes.items():
        data_orientacoes.append([mercado, orientacao])
    
    table_orientacoes = Table(data_orientacoes, colWidths=[2*inch, 6*inch])
    table_orientacoes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table_orientacoes)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 2: Ciclos de Horários
    section2 = Paragraph("2. Ciclos de Horários e Taxas de Ocorrência", section_style)
    elements.append(section2)
    elements.append(Spacer(1, 0.1*inch))
    
    # Tabela de ciclos
    data_ciclos = [['Ciclo', 'BTTS', 'OVER 2.5', 'OVER 3.5']]
    for ciclo, mercados in ciclos.items():
        data_ciclos.append([
            ciclo,
            mercados['BTTS'],
            mercados['OVER 2.5'],
            mercados['OVER 3.5']
        ])
    
    table_ciclos = Table(data_ciclos, colWidths=[1.5*inch, 2.5*inch, 2.5*inch, 2.5*inch])
    table_ciclos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (0, -1), colors.beige),
        ('BACKGROUND', (1, 1), (1, -1), colors.lightblue),
        ('BACKGROUND', (2, 1), (2, -1), colors.lightgreen),
        ('BACKGROUND', (3, 1), (3, -1), colors.lightcoral),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table_ciclos)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 3: Horários Recomendados
    section3 = Paragraph("3. Horários Recomendados", section_style)
    elements.append(section3)
    elements.append(Spacer(1, 0.1*inch))
    
    # Adicionar heatmap de horários recomendados
    heatmap_path = '/home/ubuntu/tabelas_operacionais/consolidado/graficos/heatmap_horarios_recomendados.png'
    if os.path.exists(heatmap_path):
        img = Image(heatmap_path, width=8*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
    
    # Descrição do heatmap
    heatmap_desc = Paragraph(
        "O heatmap acima mostra os horários recomendados para cada mercado. "
        "As células em verde indicam os horários com maior probabilidade de sucesso. "
        "O ciclo 12-17h apresenta as maiores taxas de ocorrência para todos os mercados.",
        normal_style
    )
    elements.append(heatmap_desc)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 4: Combinações de Alto Desempenho
    section4 = Paragraph("4. Combinações de Alto Desempenho", section_style)
    elements.append(section4)
    elements.append(Spacer(1, 0.1*inch))
    
    # Tabela de combinações de alto desempenho
    data_combinacoes = [['Mercado', 'Campeonato', 'Hora', 'Desempenho']]
    for mercado, combinacoes in combinacoes_alto_desempenho.items():
        for combinacao in combinacoes:
            data_combinacoes.append([
                mercado,
                combinacao[0],
                str(combinacao[1]),
                combinacao[2]
            ])
    
    table_combinacoes = Table(data_combinacoes, colWidths=[1.5*inch, 2*inch, 1*inch, 4.5*inch])
    table_combinacoes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table_combinacoes)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 5: Níveis de Confiança e Stakes
    section5 = Paragraph("5. Níveis de Confiança e Stakes", section_style)
    elements.append(section5)
    elements.append(Spacer(1, 0.1*inch))
    
    # Tabela de níveis de confiança e stakes
    data_confianca = [['Mercado', 'Nível', 'Probabilidade', 'Stake']]
    for mercado, niveis in niveis_confianca.items():
        for nivel, info in niveis.items():
            data_confianca.append([
                mercado,
                nivel,
                info['probabilidade'],
                info['stake']
            ])
    
    table_confianca = Table(data_confianca, colWidths=[2*inch, 1.5*inch, 2*inch, 1.5*inch])
    table_confianca.setStyle(TableStyle([
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
    ]))
    
    # Adicionar cores condicionais por nível de confiança
    for i, row in enumerate(data_confianca[1:], 1):
        if row[1] == 'ALTA':
            table_confianca.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.lightgreen)]))
        elif row[1] == 'MEDIA':
            table_confianca.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.lightblue)]))
        elif row[1] == 'BAIXA':
            table_confianca.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.lightcoral)]))
    
    elements.append(table_confianca)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 6: Comparativo de Mercados
    section6 = Paragraph("6. Comparativo de Taxa de Ocorrência por Mercado", section_style)
    elements.append(section6)
    elements.append(Spacer(1, 0.1*inch))
    
    # Adicionar gráfico comparativo de mercados
    grafico_path = '/home/ubuntu/tabelas_operacionais/consolidado/graficos/comparativo_mercados.png'
    if os.path.exists(grafico_path):
        img = Image(grafico_path, width=7*inch, height=4*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
    
    # Descrição do gráfico
    grafico_desc = Paragraph(
        "O gráfico acima mostra a taxa média de ocorrência para cada mercado. "
        "O BTTS tem a maior taxa de ocorrência (53%), seguido pelo Over 2.5 (42,6%) e Over 3.5 (25,6%). "
        "Estas taxas influenciam diretamente a estratégia de apostas e os valores de stake recomendados.",
        normal_style
    )
    elements.append(grafico_desc)
    elements.append(Spacer(1, 0.25*inch))
    
    # Seção 7: Recomendações Operacionais
    section7 = Paragraph("7. Recomendações Operacionais", section_style)
    elements.append(section7)
    elements.append(Spacer(1, 0.1*inch))
    
    # Recomendações
    recomendacoes = [
        "1. Priorize as entradas nos horários e campeonatos recomendados para cada mercado.",
        "2. Utilize a estratégia de Martingale conforme o nível de confiança: ALTA (1 gale), MÉDIA (2 gales), BAIXA (3 gales).",
        "3. Ajuste os valores de stake de acordo com o nível de confiança da previsão.",
        "4. Concentre-se no ciclo 12-17h, que apresenta as maiores taxas de ocorrência para todos os mercados.",
        "5. Para o mercado Over 2.5, foque exclusivamente no campeonato PREMIER, que apresentou 95% de acerto.",
        "6. Para o mercado BTTS, priorize os campeonatos PREMIER e EURO, que apresentaram os melhores resultados.",
        "7. Para o mercado Over 3.5, considere todos os 4 campeonatos, mas dê preferência ao PREMIER e EURO.",
        "8. Limite-se a 3 entradas por hora para cada mercado, selecionando apenas as de maior probabilidade.",
        "9. Registre os resultados e atualize o modelo regularmente para manter sua precisão."
    ]
    
    for rec in recomendacoes:
        elements.append(Paragraph(rec, normal_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # Rodapé
    footer = Paragraph(
        "GRISAMANUS - Sistema de Análise e Previsão para Apostas em Futebol Virtual",
        centered_style
    )
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    print(f"PDF da tabela operacional consolidada gerado com sucesso: {pdf_file}")
    return pdf_file

def main():
    # Criar tabela operacional consolidada
    criar_tabela_operacional_consolidada()
    
    print("\nTabela operacional consolidada criada com sucesso!")
    print("Arquivo PDF: /home/ubuntu/tabelas_operacionais/consolidado/GRISAMANUS_tabela_operacional_consolidada.pdf")
    print("Gráficos:")
    print("- Heatmap de horários recomendados: /home/ubuntu/tabelas_operacionais/consolidado/graficos/heatmap_horarios_recomendados.png")
    print("- Comparativo de mercados: /home/ubuntu/tabelas_operacionais/consolidado/graficos/comparativo_mercados.png")

if __name__ == "__main__":
    main()
