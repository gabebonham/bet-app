import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

# Criar diretório para tabelas
os.makedirs('/home/ubuntu/tabelas_operacionais', exist_ok=True)

def criar_tabela_horarios_recomendados():
    """
    Cria uma tabela detalhada mostrando os horários recomendados para cada mercado
    """
    print("Criando tabela de horários recomendados para cada mercado...")
    
    # Dados de ocorrência por hora e mercado
    dados = {
        'HORA': list(range(24)),
        'BTTS': [
            0.485, 0.480, 0.475, 0.490, 0.495, 0.485,  # 00-05
            0.510, 0.515, 0.520, 0.525, 0.530, 0.520,  # 06-11
            0.550, 0.560, 0.570, 0.580, 0.565, 0.560,  # 12-17
            0.540, 0.535, 0.530, 0.535, 0.540, 0.530   # 18-23
        ],
        'OVER_2.5': [
            0.368, 0.372, 0.365, 0.370, 0.375, 0.380,  # 00-05
            0.395, 0.400, 0.405, 0.410, 0.415, 0.405,  # 06-11
            0.475, 0.485, 0.490, 0.495, 0.490, 0.485,  # 12-17
            0.450, 0.445, 0.440, 0.435, 0.440, 0.445   # 18-23
        ]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Adicionar recomendações
    df['RECOMENDACAO_BTTS'] = pd.cut(
        df['BTTS'], 
        bins=[0, 0.5, 0.54, 1], 
        labels=['Não Recomendado', 'Recomendado', 'Altamente Recomendado']
    )
    
    df['RECOMENDACAO_OVER_2.5'] = pd.cut(
        df['OVER_2.5'], 
        bins=[0, 0.4, 0.47, 1], 
        labels=['Não Recomendado', 'Recomendado', 'Altamente Recomendado']
    )
    
    # Adicionar campeonatos prioritários
    df['CAMPEONATOS_PRIORITARIOS_BTTS'] = [
        'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA',
        'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA',
        'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA',
        'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA', 'PREMIER, COPA'
    ]
    
    df['CAMPEONATOS_PRIORITARIOS_OVER_2.5'] = [
        'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER',
        'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER',
        'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER',
        'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER', 'SUPER, PREMIER'
    ]
    
    # Adicionar stake recomendada
    def determinar_stake_btts(row):
        if row['RECOMENDACAO_BTTS'] == 'Altamente Recomendado':
            return 'R$15-20'
        elif row['RECOMENDACAO_BTTS'] == 'Recomendado':
            return 'R$10-15'
        else:
            return 'R$5-10'
    
    def determinar_stake_over25(row):
        if row['RECOMENDACAO_OVER_2.5'] == 'Altamente Recomendado':
            return 'R$15-20'
        elif row['RECOMENDACAO_OVER_2.5'] == 'Recomendado':
            return 'R$10-15'
        else:
            return 'R$5-10'
    
    df['STAKE_BTTS'] = df.apply(determinar_stake_btts, axis=1)
    df['STAKE_OVER_2.5'] = df.apply(determinar_stake_over25, axis=1)
    
    # Adicionar estratégia de Martingale
    def determinar_martingale_btts(row):
        if row['RECOMENDACAO_BTTS'] == 'Altamente Recomendado':
            return 'Até 2 gales'
        elif row['RECOMENDACAO_BTTS'] == 'Recomendado':
            return 'Até 1 gale'
        else:
            return 'Sem gale'
    
    def determinar_martingale_over25(row):
        if row['RECOMENDACAO_OVER_2.5'] == 'Altamente Recomendado':
            return 'Até 2 gales'
        elif row['RECOMENDACAO_OVER_2.5'] == 'Recomendado':
            return 'Até 1 gale'
        else:
            return 'Sem gale'
    
    df['MARTINGALE_BTTS'] = df.apply(determinar_martingale_btts, axis=1)
    df['MARTINGALE_OVER_2.5'] = df.apply(determinar_martingale_over25, axis=1)
    
    # Adicionar ciclo
    df['CICLO'] = df['HORA'] // 6
    df['NOME_CICLO'] = df['CICLO'].map({
        0: '00h-05h',
        1: '06h-11h',
        2: '12h-17h',
        3: '18h-23h'
    })
    
    # Salvar DataFrame em CSV
    arquivo_csv = '/home/ubuntu/tabelas_operacionais/horarios_recomendados.csv'
    df.to_csv(arquivo_csv, index=False)
    print(f"Tabela salva em CSV: {arquivo_csv}")
    
    # Criar tabela visual
    plt.figure(figsize=(15, 10))
    
    # Criar heatmap para BTTS
    plt.subplot(2, 1, 1)
    sns.heatmap(
        df.pivot_table(index='NOME_CICLO', columns='HORA', values='BTTS'),
        annot=True, 
        cmap='RdYlGn', 
        linewidths=0.5,
        fmt='.3f'
    )
    plt.title('Taxa de Ocorrência de BTTS por Hora', fontsize=14)
    
    # Criar heatmap para OVER 2.5
    plt.subplot(2, 1, 2)
    sns.heatmap(
        df.pivot_table(index='NOME_CICLO', columns='HORA', values='OVER_2.5'),
        annot=True, 
        cmap='RdYlGn', 
        linewidths=0.5,
        fmt='.3f'
    )
    plt.title('Taxa de Ocorrência de OVER 2.5 por Hora', fontsize=14)
    
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico = '/home/ubuntu/tabelas_operacionais/heatmap_horarios.png'
    plt.savefig(arquivo_grafico)
    plt.close()
    print(f"Heatmap salvo em: {arquivo_grafico}")
    
    # Criar PDF com tabela operacional
    criar_pdf_tabela_operacional(df, '/home/ubuntu/tabelas_operacionais/tabela_operacional_GRISAMANUS.pdf')
    
    return df

def criar_pdf_tabela_operacional(df, arquivo_pdf):
    """
    Cria um PDF com a tabela operacional
    """
    print(f"Criando PDF com tabela operacional: {arquivo_pdf}")
    
    # Criar documento PDF
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=landscape(letter))
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Título
    elements.append(Paragraph("TABELA OPERACIONAL GRISAMANUS", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Data de geração
    elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabela 1: Horários Recomendados por Ciclo
    elements.append(Paragraph("1. Horários Recomendados por Ciclo", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Preparar dados para tabela de ciclos
    ciclos = ['00h-05h', '06h-11h', '12h-17h', '18h-23h']
    
    data_ciclos = [['Ciclo', 'BTTS', 'OVER 2.5', 'Recomendação BTTS', 'Recomendação OVER 2.5']]
    
    for ciclo in ciclos:
        btts_media = df[df['NOME_CICLO'] == ciclo]['BTTS'].mean()
        over25_media = df[df['NOME_CICLO'] == ciclo]['OVER_2.5'].mean()
        
        # Determinar recomendação
        if btts_media > 0.54:
            rec_btts = 'Altamente Recomendado'
        elif btts_media > 0.5:
            rec_btts = 'Recomendado'
        else:
            rec_btts = 'Não Recomendado'
            
        if over25_media > 0.47:
            rec_over25 = 'Altamente Recomendado'
        elif over25_media > 0.4:
            rec_over25 = 'Recomendado'
        else:
            rec_over25 = 'Não Recomendado'
        
        data_ciclos.append([
            ciclo,
            f"{btts_media:.3f}",
            f"{over25_media:.3f}",
            rec_btts,
            rec_over25
        ])
    
    # Criar tabela de ciclos
    table_ciclos = Table(data_ciclos, repeatRows=1)
    
    # Estilo da tabela de ciclos
    table_style_ciclos = TableStyle([
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
    
    # Aplicar cores específicas para recomendações
    for i in range(1, len(data_ciclos)):
        # BTTS
        if data_ciclos[i][3] == 'Altamente Recomendado':
            table_style_ciclos.add('BACKGROUND', (3, i), (3, i), colors.lightgreen)
        elif data_ciclos[i][3] == 'Recomendado':
            table_style_ciclos.add('BACKGROUND', (3, i), (3, i), colors.lightblue)
        else:
            table_style_ciclos.add('BACKGROUND', (3, i), (3, i), colors.lightcoral)
        
        # OVER 2.5
        if data_ciclos[i][4] == 'Altamente Recomendado':
            table_style_ciclos.add('BACKGROUND', (4, i), (4, i), colors.lightgreen)
        elif data_ciclos[i][4] == 'Recomendado':
            table_style_ciclos.add('BACKGROUND', (4, i), (4, i), colors.lightblue)
        else:
            table_style_ciclos.add('BACKGROUND', (4, i), (4, i), colors.lightcoral)
    
    table_ciclos.setStyle(table_style_ciclos)
    elements.append(table_ciclos)
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabela 2: Estratégia Operacional Detalhada
    elements.append(Paragraph("2. Estratégia Operacional Detalhada", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Preparar dados para tabela operacional
    data_op = [['Mercado', 'Horário', 'Campeonatos Prioritários', 'Stake Recomendada', 'Estratégia Martingale']]
    
    # BTTS - Altamente Recomendado
    data_op.append([
        'BTTS',
        '12h-17h',
        'PREMIER, COPA',
        'R$15-20',
        'Até 2 gales'
    ])
    
    # BTTS - Recomendado
    data_op.append([
        'BTTS',
        '06h-11h, 18h-23h',
        'PREMIER, COPA',
        'R$10-15',
        'Até 1 gale'
    ])
    
    # BTTS - Não Recomendado
    data_op.append([
        'BTTS',
        '00h-05h',
        'PREMIER, COPA',
        'R$5-10',
        'Sem gale'
    ])
    
    # OVER 2.5 - Altamente Recomendado
    data_op.append([
        'OVER 2.5',
        '12h-17h',
        'SUPER, PREMIER',
        'R$15-20',
        'Até 2 gales'
    ])
    
    # OVER 2.5 - Recomendado
    data_op.append([
        'OVER 2.5',
        '18h-23h',
        'SUPER, PREMIER',
        'R$10-15',
        'Até 1 gale'
    ])
    
    # OVER 2.5 - Não Recomendado
    data_op.append([
        'OVER 2.5',
        '00h-05h, 06h-11h',
        'SUPER, PREMIER',
        'R$5-10',
        'Sem gale'
    ])
    
    # Criar tabela operacional
    table_op = Table(data_op, repeatRows=1)
    
    # Estilo da tabela operacional
    table_style_op = TableStyle([
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
    
    # Aplicar cores específicas para níveis de recomendação
    # BTTS
    table_style_op.add('BACKGROUND', (0, 1), (0, 1), colors.lightgreen)  # Altamente Recomendado
    table_style_op.add('BACKGROUND', (0, 2), (0, 2), colors.lightblue)   # Recomendado
    table_style_op.add('BACKGROUND', (0, 3), (0, 3), colors.lightcoral)  # Não Recomendado
    
    # OVER 2.5
    table_style_op.add('BACKGROUND', (0, 4), (0, 4), colors.lightgreen)  # Altamente Recomendado
    table_style_op.add('BACKGROUND', (0, 5), (0, 5), colors.lightblue)   # Recomendado
    table_style_op.add('BACKGROUND', (0, 6), (0, 6), colors.lightcoral)  # Não Recomendado
    
    table_op.setStyle(table_style_op)
    elements.append(table_op)
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabela 3: Resumo de Recomendações por Hora
    elements.append(Paragraph("3. Resumo de Recomendações por Hora", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Preparar dados para tabela de horas
    data_horas = [['Hora', 'BTTS', 'OVER 2.5', 'Mercado Recomendado']]
    
    for hora in range(24):
        btts_valor = df[df['HORA'] == hora]['BTTS'].values[0]
        over25_valor = df[df['HORA'] == hora]['OVER_2.5'].values[0]
        
        # Determinar mercado recomendado
        if btts_valor > over25_valor + 0.1:
            mercado_rec = 'BTTS'
        elif over25_valor > btts_valor + 0.05:
            mercado_rec = 'OVER 2.5'
        else:
            mercado_rec = 'Ambos'
        
        data_horas.append([
            f"{hora:02d}h",
            f"{btts_valor:.3f}",
            f"{over25_valor:.3f}",
            mercado_rec
        ])
    
    # Criar tabela de horas
    table_horas = Table(data_horas, repeatRows=1)
    
    # Estilo da tabela de horas
    table_style_horas = TableStyle([
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
    
    # Aplicar cores específicas para mercados recomendados
    for i in range(1, len(data_horas)):
        if data_horas[i][3] == 'BTTS':
            table_style_horas.add('BACKGROUND', (3, i), (3, i), colors.lightgreen)
        elif data_horas[i][3] == 'OVER 2.5':
            table_style_horas.add('BACKGROUND', (3, i), (3, i), colors.lightblue)
        else:
            table_style_horas.add('BACKGROUND', (3, i), (3, i), colors.lightyellow)
    
    table_horas.setStyle(table_style_horas)
    elements.append(table_horas)
    elements.append(Spacer(1, 0.25*inch))
    
    # Adicionar nota explicativa
    elements.append(Paragraph("Notas:", styles["Heading3"]))
    elements.append(Paragraph("1. Altamente Recomendado (verde): Horários com maior taxa de ocorrência, ideal para operações com stake completa e estratégia de Martingale.", normal_style))
    elements.append(Paragraph("2. Recomendado (azul): Horários com taxa de ocorrência moderada, adequado para operações com stake reduzida.", normal_style))
    elements.append(Paragraph("3. Não Recomendado (vermelho): Horários com baixa taxa de ocorrência, recomenda-se evitar ou operar apenas com padrões muito fortes e stake mínima.", normal_style))
    elements.append(Paragraph("4. Esta tabela deve ser usada como guia operacional e complementada com a análise de padrões geométricos específicos.", normal_style))
    
    # Gerar PDF
    doc.build(elements)
    
    print(f"PDF gerado com sucesso: {arquivo_pdf}")
    
    return arquivo_pdf

if __name__ == "__main__":
    criar_tabela_horarios_recomendados()
