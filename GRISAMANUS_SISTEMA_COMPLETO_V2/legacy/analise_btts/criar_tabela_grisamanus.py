import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

# Criar dados para a tabela
data = []

# Cabeçalho
header = ["HORA", "CAMPEONATO", "COLUNA", "MERCADO", "PROBABILIDADE", "CONFIANÇA", 
          "STAKE (R$)", "RESULTADO", "GALE", "LUCRO/PREJUÍZO (R$)", "SALDO (R$)"]
data.append(header)

# Dados das operações baseados nas tabelas que analisamos
# Hora 20
operations = [
    # Hora, Campeonato, Coluna, Mercado, Probabilidade, Confiança, Stake, Resultado, Gale, Lucro/Prejuízo
    ["20", "COPA 7", "3", "BTTS", "0.72", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["20", "COPA 37", "13", "BTTS", "0.71", "MÉDIA", 10.00, "ERRO", "", -10.00],
    ["20", "COPA 22", "8", "BTTS", "0.57", "BAIXA", 5.00, "ACERTO", "2", 5.00],
    ["20", "EURO 14", "5", "BTTS", "0.86", "ALTA", 20.00, "ACERTO", "1", 20.00],
    ["20", "EURO 35", "12", "BTTS", "0.86", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["20", "EURO 8", "3", "BTTS", "0.82", "ALTA", 20.00, "ACERTO", "1", 20.00],
    ["20", "SUPER 22", "8", "BTTS", "0.87", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["20", "SUPER 10", "4", "BTTS", "0.83", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["20", "SUPER 34", "12", "BTTS", "0.80", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["20", "PREMIER 12", "5", "BTTS", "0.90", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["20", "PREMIER 39", "14", "BTTS", "0.89", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["20", "PREMIER 6", "3", "BTTS", "0.88", "ALTA", 20.00, "ACERTO", "1", 20.00],
    
    # Hora 21
    ["21", "COPA 22", "8", "BTTS", "0.52", "BAIXA", 5.00, "ACERTO", "2", 5.00],
    ["21", "COPA 1", "1", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "2", 5.00],
    ["21", "COPA 58", "20", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "1", 5.00],
    ["21", "EURO 8", "3", "BTTS", "0.64", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["21", "EURO 2", "1", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "1", 5.00],
    ["21", "EURO 59", "20", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["21", "SUPER 43", "15", "BTTS", "0.79", "ALTA", 20.00, "ERRO", "", -20.00],
    ["21", "SUPER 10", "4", "BTTS", "0.65", "MÉDIA", 10.00, "ACERTO", "1", 10.00],
    ["21", "SUPER 40", "14", "BTTS", "0.63", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["21", "PREMIER 6", "3", "BTTS", "0.87", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["21", "PREMIER 45", "16", "BTTS", "0.85", "ALTA", 20.00, "ACERTO", "1", 20.00],
    ["21", "PREMIER 12", "5", "BTTS", "0.83", "ALTA", 20.00, "ACERTO", "", 20.00],
    
    # Hora 22
    ["22", "COPA 22", "8", "BTTS", "0.55", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["22", "COPA 1", "1", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["22", "COPA 58", "20", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "1", 5.00],
    ["22", "EURO 8", "3", "BTTS", "0.78", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["22", "EURO 53", "18", "BTTS", "0.61", "MÉDIA", 10.00, "ACERTO", "1", 10.00],
    ["22", "EURO 35", "12", "BTTS", "0.54", "BAIXA", 5.00, "ACERTO", "2", 5.00],
    ["22", "SUPER 43", "15", "BTTS", "0.81", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["22", "SUPER 10", "4", "BTTS", "0.70", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["22", "SUPER 22", "8", "BTTS", "0.64", "MÉDIA", 10.00, "ACERTO", "1", 10.00],
    ["22", "PREMIER 6", "3", "BTTS", "0.88", "ALTA", 20.00, "ACERTO", "2", 20.00],
    ["22", "PREMIER 12", "5", "BTTS", "0.85", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["22", "PREMIER 39", "14", "BTTS", "0.75", "ALTA", 20.00, "ERRO", "", -20.00],
    
    # Hora 23
    ["23", "COPA 22", "8", "BTTS", "0.55", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["23", "COPA 1", "1", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["23", "COPA 58", "20", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "1", 5.00],
    ["23", "EURO 8", "3", "BTTS", "0.78", "ALTA", 20.00, "ERRO", "", -20.00],
    ["23", "EURO 53", "18", "BTTS", "0.64", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["23", "EURO 35", "12", "BTTS", "0.54", "BAIXA", 5.00, "ACERTO", "1", 5.00],
    ["23", "SUPER 43", "15", "BTTS", "0.73", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["23", "SUPER 10", "4", "BTTS", "0.67", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["23", "SUPER 22", "8", "BTTS", "0.64", "MÉDIA", 10.00, "ACERTO", "1", 10.00],
    ["23", "PREMIER 6", "3", "BTTS", "0.88", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["23", "PREMIER 12", "5", "BTTS", "0.85", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["23", "PREMIER 39", "14", "BTTS", "0.75", "ALTA", 20.00, "ACERTO", "", 20.00],
    
    # Hora 00
    ["00", "COPA 1", "1", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["00", "COPA 58", "20", "BTTS", "0.50", "BAIXA", 5.00, "ERRO", "", -5.00],
    ["00", "COPA 22", "8", "BTTS", "0.49", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["00", "EURO 8", "3", "BTTS", "0.52", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["00", "EURO 2", "1", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["00", "EURO 59", "20", "BTTS", "0.50", "BAIXA", 5.00, "ACERTO", "", 5.00],
    ["00", "SUPER 10", "4", "BTTS", "0.62", "MÉDIA", 10.00, "ACERTO", "2", 10.00],
    ["00", "SUPER 43", "15", "BTTS", "0.60", "MÉDIA", 10.00, "ACERTO", "", 10.00],
    ["00", "SUPER 22", "8", "BTTS", "0.52", "BAIXA", 5.00, "ERRO", "", -5.00],
    ["00", "PREMIER 6", "3", "BTTS", "0.75", "ALTA", 20.00, "ACERTO", "2", 20.00],
    ["00", "PREMIER 12", "5", "BTTS", "0.75", "ALTA", 20.00, "ACERTO", "", 20.00],
    ["00", "PREMIER 27", "10", "BTTS", "0.70", "MÉDIA", 10.00, "ACERTO", "", 10.00]
]

# Calcular saldo acumulado com banca inicial de R$1.000,00
saldo = 1000.00

for op in operations:
    # Adicionar saldo atual à operação
    saldo += op[9]  # Adiciona lucro/prejuízo ao saldo
    op_with_saldo = op + [saldo]
    data.append(op_with_saldo)

# Criar DataFrame para análise
df = pd.DataFrame(operations, columns=["HORA", "CAMPEONATO", "COLUNA", "MERCADO", "PROBABILIDADE", 
                                      "CONFIANÇA", "STAKE", "RESULTADO", "GALE", "LUCRO/PREJUÍZO"])

# Calcular estatísticas
total_operacoes = len(df)
acertos = len(df[df["RESULTADO"] == "ACERTO"])
erros = len(df[df["RESULTADO"] == "ERRO"])
taxa_acerto = acertos / total_operacoes * 100

# Análise por nível de confiança
alta_df = df[df["CONFIANÇA"] == "ALTA"]
media_df = df[df["CONFIANÇA"] == "MÉDIA"]
baixa_df = df[df["CONFIANÇA"] == "BAIXA"]

alta_acertos = len(alta_df[alta_df["RESULTADO"] == "ACERTO"])
media_acertos = len(media_df[media_df["RESULTADO"] == "ACERTO"])
baixa_acertos = len(baixa_df[baixa_df["RESULTADO"] == "BAIXA"])

alta_total = len(alta_df)
media_total = len(media_df)
baixa_total = len(baixa_df)

alta_taxa = alta_acertos / alta_total * 100 if alta_total > 0 else 0
media_taxa = media_acertos / media_total * 100 if media_total > 0 else 0
baixa_taxa = baixa_acertos / baixa_total * 100 if baixa_total > 0 else 0

# Análise por campeonato
copa_df = df[df["CAMPEONATO"].str.contains("COPA")]
euro_df = df[df["CAMPEONATO"].str.contains("EURO")]
super_df = df[df["CAMPEONATO"].str.contains("SUPER")]
premier_df = df[df["CAMPEONATO"].str.contains("PREMIER")]

copa_acertos = len(copa_df[copa_df["RESULTADO"] == "ACERTO"])
euro_acertos = len(euro_df[euro_df["RESULTADO"] == "ACERTO"])
super_acertos = len(super_df[super_df["RESULTADO"] == "ACERTO"])
premier_acertos = len(premier_df[premier_df["RESULTADO"] == "ACERTO"])

copa_total = len(copa_df)
euro_total = len(euro_df)
super_total = len(super_df)
premier_total = len(premier_df)

copa_taxa = copa_acertos / copa_total * 100 if copa_total > 0 else 0
euro_taxa = euro_acertos / euro_total * 100 if euro_total > 0 else 0
super_taxa = super_acertos / super_total * 100 if super_total > 0 else 0
premier_taxa = premier_acertos / premier_total * 100 if premier_total > 0 else 0

# Análise financeira
lucro_total = df["LUCRO/PREJUÍZO"].sum()
roi = lucro_total / df["STAKE"].sum() * 100

# Criar PDF
pdf_file = "/home/ubuntu/analise_btts/GRISAMANUS.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=landscape(letter))
elements = []

# Estilos
styles = getSampleStyleSheet()
title_style = styles["Title"]
heading_style = styles["Heading1"]
normal_style = styles["Normal"]

# Título
title = Paragraph(f"<b>GRISAMANUS - RELATÓRIO DE OPERAÇÕES</b>", title_style)
elements.append(title)
elements.append(Spacer(1, 0.25*inch))

# Data
date_text = Paragraph(f"<b>Data:</b> {datetime.now().strftime('%d/%m/%Y')}", normal_style)
elements.append(date_text)
elements.append(Spacer(1, 0.25*inch))

# Resumo
summary_text = f"""
<b>Resumo das Operações:</b>
- Total de Operações: {total_operacoes}
- Acertos: {acertos} ({taxa_acerto:.2f}%)
- Erros: {erros} ({100-taxa_acerto:.2f}%)
- Banca Inicial: R$1.000,00
- Banca Final: R${saldo:.2f}
- Lucro Total: R${lucro_total:.2f}
- ROI: {roi:.2f}%
"""
summary = Paragraph(summary_text, normal_style)
elements.append(summary)
elements.append(Spacer(1, 0.25*inch))

# Análise por Confiança
confidence_text = f"""
<b>Análise por Nível de Confiança:</b>
- ALTA: {alta_acertos}/{alta_total} acertos ({alta_taxa:.2f}%)
- MÉDIA: {media_acertos}/{media_total} acertos ({media_taxa:.2f}%)
- BAIXA: {baixa_acertos}/{baixa_total} acertos ({baixa_taxa:.2f}%)
"""
confidence = Paragraph(confidence_text, normal_style)
elements.append(confidence)
elements.append(Spacer(1, 0.25*inch))

# Análise por Campeonato
championship_text = f"""
<b>Análise por Campeonato:</b>
- COPA: {copa_acertos}/{copa_total} acertos ({copa_taxa:.2f}%)
- EURO: {euro_acertos}/{euro_total} acertos ({euro_taxa:.2f}%)
- SUPER: {super_acertos}/{super_total} acertos ({super_taxa:.2f}%)
- PREMIER: {premier_acertos}/{premier_total} acertos ({premier_taxa:.2f}%)
"""
championship = Paragraph(championship_text, normal_style)
elements.append(championship)
elements.append(Spacer(1, 0.25*inch))

# Tabela de operações
table = Table(data)

# Estilo da tabela
style = TableStyle([
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
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

# Colorir células de acordo com o resultado
for i in range(1, len(data)):
    if data[i][7] == "ACERTO":
        style.add('BACKGROUND', (7, i), (7, i), colors.lightgreen)
    elif data[i][7] == "ERRO":
        style.add('BACKGROUND', (7, i), (7, i), colors.lightcoral)
        
    # Colorir células de acordo com a confiança
    if data[i][5] == "ALTA":
        style.add('BACKGROUND', (5, i), (5, i), colors.lightgreen)
    elif data[i][5] == "MÉDIA":
        style.add('BACKGROUND', (5, i), (5, i), colors.lightyellow)
    elif data[i][5] == "BAIXA":
        style.add('BACKGROUND', (5, i), (5, i), colors.lightcoral)
        
    # Colorir células de lucro/prejuízo
    if float(data[i][9]) > 0:
        style.add('BACKGROUND', (9, i), (9, i), colors.lightgreen)
    elif float(data[i][9]) < 0:
        style.add('BACKGROUND', (9, i), (9, i), colors.lightcoral)

table.setStyle(style)
elements.append(table)

# Adicionar nota final
elements.append(Spacer(1, 0.5*inch))
note = Paragraph("<i>GRISAMANUS - Uma parceria entre o idealista grisalho e seu mentor Manus.</i>", normal_style)
elements.append(note)

# Gerar PDF
doc.build(elements)

print(f"PDF criado com sucesso: {pdf_file}")
