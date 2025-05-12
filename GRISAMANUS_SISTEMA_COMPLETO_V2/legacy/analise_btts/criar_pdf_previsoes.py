import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

# Criar diretório para salvar resultados
output_dir = '/home/ubuntu/analise_btts/resultados_adicionais'
os.makedirs(output_dir, exist_ok=True)

# Ler o arquivo de previsões
previsoes_file = f"{output_dir}/previsoes_formato_tabela_original_a_partir_19.txt"

# Extrair as previsões do arquivo
with open(previsoes_file, 'r') as f:
    lines = f.readlines()

# Encontrar onde começam as previsões (após o cabeçalho)
start_line = 0
for i, line in enumerate(lines):
    if "HORA | CAMPEONATO" in line:
        start_line = i + 2  # Pular a linha de cabeçalho e a linha de separação
        break

# Extrair as previsões
previsoes = []
for i in range(start_line, len(lines)):
    line = lines[i].strip()
    if not line or "LEGENDA" in line:
        break
    
    # Dividir a linha pelos separadores |
    parts = [part.strip() for part in line.split('|')]
    if len(parts) >= 6:
        hora = parts[0]
        campeonato = parts[1]
        coluna = parts[2]
        mercado = parts[3]
        probabilidade = parts[4]
        confianca = parts[5]
        
        # Calcular stake recomendada com base na confiança
        if "BAIXA" in confianca:
            stake = "R$5,00"
        elif "MÉDIA" in confianca:
            stake = "R$10,00"
        else:  # ALTA
            stake = "R$20,00"
        
        previsoes.append({
            'HORA': hora,
            'CAMPEONATO': campeonato,
            'COLUNA': coluna,
            'MERCADO': mercado,
            'PROBABILIDADE': probabilidade,
            'CONFIANÇA': confianca,
            'STAKE': stake,
            'GALE': ""  # Campo vazio para anotações
        })

# Criar PDF com as previsões
pdf_file = f"{output_dir}/previsoes_btts_com_stake.pdf"

# Configurar o documento PDF
doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
styles = getSampleStyleSheet()


# Criar estilo personalizado para o título
title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=14,
    alignment=1,  # Centralizado
    spaceAfter=0.3*inch
)

# Criar estilo personalizado para subtítulos
subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Heading2'],
    fontSize=12,
    alignment=1,  # Centralizado
    spaceAfter=0.2*inch
)

# Criar estilo personalizado para notas
note_style = ParagraphStyle(
    'Note',
    parent=styles['Normal'],
    fontSize=9,
    alignment=0,  # Esquerda
    spaceAfter=0.1*inch
)

# Elementos para o PDF
elements = []

# Adicionar título
title = Paragraph("PREVISÕES BTTS PARA AS PRÓXIMAS 5 HORAS (A PARTIR DA HORA 19)", title_style)
elements.append(title)

# Adicionar subtítulo com data e hora
from datetime import datetime
now = datetime.now()
date_str = now.strftime("%d/%m/%Y %H:%M")
subtitle = Paragraph(f"Gerado em: {date_str}", subtitle_style)
elements.append(subtitle)

# Adicionar espaço
elements.append(Spacer(1, 0.2*inch))

# Cabeçalho da tabela
headers = ['HORA', 'CAMPEONATO', 'COLUNA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'GALE']

# Dados da tabela
data = [headers]
for prev in previsoes:
    row = [prev['HORA'], prev['CAMPEONATO'], prev['COLUNA'], prev['MERCADO'], 
           prev['PROBABILIDADE'], prev['CONFIANÇA'], prev['STAKE'], prev['GALE']]
    data.append(row)

# Criar tabela
table = Table(data, colWidths=[0.5*inch, 1.5*inch, 0.7*inch, 0.7*inch, 1.2*inch, 1*inch, 0.8*inch, 0.8*inch])

# Estilo da tabela
table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
])

# Adicionar cores baseadas na confiança
for i, prev in enumerate(previsoes, 1):
    if "BAIXA" in prev['CONFIANÇA']:
        table_style.add('BACKGROUND', (5, i), (5, i), colors.lightcoral)
    elif "MÉDIA" in prev['CONFIANÇA']:
        table_style.add('BACKGROUND', (5, i), (5, i), colors.lightyellow)
    else:  # ALTA
        table_style.add('BACKGROUND', (5, i), (5, i), colors.lightgreen)

table.setStyle(table_style)
elements.append(table)

# Adicionar espaço
elements.append(Spacer(1, 0.3*inch))

# Adicionar legenda de campeonatos
legenda_title = Paragraph("LEGENDA DE CAMPEONATOS:", subtitle_style)
elements.append(legenda_title)

legenda_text = """
COPA: 01, 04, 07, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58
EURO: 02, 05, 08, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 59
SUPER: 01, 04, 07, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58
PREMIER: 00, 03, 06, 09, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57
"""
legenda = Paragraph(legenda_text, note_style)
elements.append(legenda)

# Adicionar espaço
elements.append(Spacer(1, 0.2*inch))

# Adicionar instruções
instrucoes_title = Paragraph("INSTRUÇÕES PARA USO:", subtitle_style)
elements.append(instrucoes_title)

instrucoes_text = """
1. A coluna HORA indica a hora na tabela (lado esquerdo)
2. A coluna CAMPEONATO indica o nome e número do campeonato
3. A coluna COLUNA indica o número da coluna na tabela
4. Todas as previsões são para o mercado BTTS (Both Teams To Score)
5. A coluna STAKE indica o valor recomendado para apostar com base na confiança:
   - Confiança BAIXA: R$5,00 (25% da stake base de R$20,00)
   - Confiança MÉDIA: R$10,00 (50% da stake base de R$20,00)
   - Confiança ALTA: R$20,00 (100% da stake base de R$20,00)
6. A coluna GALE é para você anotar quantos gales foram necessários na operação
"""
instrucoes = Paragraph(instrucoes_text, note_style)
elements.append(instrucoes)

# Adicionar espaço
elements.append(Spacer(1, 0.2*inch))

# Adicionar estratégia Martingale
estrategia_title = Paragraph("ESTRATÉGIA MARTINGALE RECOMENDADA:", subtitle_style)
elements.append(estrategia_title)

estrategia_text = """
1. Para cada hora, comece apostando no campeonato com maior probabilidade
2. Se perder, passe para o segundo campeonato com maior probabilidade (Gale 1)
3. Se perder novamente, passe para o terceiro campeonato com maior probabilidade (Gale 2)
4. Valores de stake para Martingale:
   - Aposta inicial: valor da STAKE recomendada
   - Gale 1: 2x o valor da STAKE inicial
   - Gale 2: 2x o valor do Gale 1
"""
estrategia = Paragraph(estrategia_text, note_style)
elements.append(estrategia)

# Construir o PDF
doc.build(elements)

print(f"PDF com previsões e valores de stake criado: {pdf_file}")
