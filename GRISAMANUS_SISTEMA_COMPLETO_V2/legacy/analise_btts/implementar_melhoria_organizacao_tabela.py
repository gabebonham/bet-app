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

# Criar diretório para formato reorganizado
os.makedirs('/home/ubuntu/analise_btts/formato_reorganizado', exist_ok=True)

def reorganizar_formato_previsoes():
    """
    Implementa a melhoria na organização da tabela de previsões,
    separando por campeonato e ordem de horas
    """
    print("Implementando melhoria na organização da tabela de previsões...")
    
    # Simular dados de previsões (normalmente viriam de um arquivo CSV)
    # Estes dados são apenas para demonstração
    dados_previsoes = [
        {'CAMPEONATO': 'COPA', 'HORA': 9, 'COLUNA': 19, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.69, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 9, 'COLUNA': 45, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.67, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 9, 'COLUNA': 43, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.65, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'EURO', 'HORA': 9, 'COLUNA': 23, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.65, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 9, 'COLUNA': 1, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.65, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 9, 'COLUNA': 51, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.65, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 9, 'COLUNA': 52, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.63, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 9, 'COLUNA': 24, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.63, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 9, 'COLUNA': 25, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.62, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 9, 'COLUNA': 37, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.61, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 10, 'COLUNA': 10, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.68, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 10, 'COLUNA': 49, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.65, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 10, 'COLUNA': 43, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.64, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 10, 'COLUNA': 1, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.62, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 10, 'COLUNA': 39, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.62, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 10, 'COLUNA': 52, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.61, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'EURO', 'HORA': 10, 'COLUNA': 38, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.60, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'EURO', 'HORA': 11, 'COLUNA': 47, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.68, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 11, 'COLUNA': 10, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.66, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 11, 'COLUNA': 1, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.66, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 11, 'COLUNA': 27, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.64, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'EURO', 'HORA': 11, 'COLUNA': 23, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.63, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 11, 'COLUNA': 15, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.63, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'PREMIER', 'HORA': 11, 'COLUNA': 21, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.62, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'EURO', 'HORA': 11, 'COLUNA': 38, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.61, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 11, 'COLUNA': 49, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.60, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'COPA', 'HORA': 11, 'COLUNA': 46, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.59, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''},
        {'CAMPEONATO': 'SUPER', 'HORA': 11, 'COLUNA': 40, 'MERCADO': 'BTTS', 'PROBABILIDADE': 0.59, 'CONFIANCA': 'BAIXA', 'STAKE': 'R$5.00', 'RESULTADO': '', 'GALE': ''}
    ]
    
    # Converter para DataFrame
    df = pd.DataFrame(dados_previsoes)
    
    # Organizar por campeonato e hora (ordem crescente)
    df_organizado = df.sort_values(by=['CAMPEONATO', 'HORA', 'COLUNA'])
    
    # Salvar em CSV
    arquivo_csv = '/home/ubuntu/analise_btts/formato_reorganizado/previsoes_reorganizadas.csv'
    df_organizado.to_csv(arquivo_csv, index=False)
    print(f"Previsões reorganizadas salvas em CSV: {arquivo_csv}")
    
    # Criar PDF com formato reorganizado
    criar_pdf_formato_reorganizado(df_organizado, '/home/ubuntu/analise_btts/formato_reorganizado/previsoes_reorganizadas.pdf')
    
    # Criar visualização da distribuição por campeonato
    plt.figure(figsize=(10, 6))
    
    contagem_por_campeonato = df.groupby('CAMPEONATO').size()
    
    plt.bar(contagem_por_campeonato.index, contagem_por_campeonato.values, color='skyblue')
    
    plt.title('Distribuição de Previsões por Campeonato', fontsize=14)
    plt.xlabel('Campeonato', fontsize=12)
    plt.ylabel('Número de Previsões', fontsize=12)
    
    # Adicionar valores nas barras
    for i, v in enumerate(contagem_por_campeonato.values):
        plt.text(i, v + 0.1, str(v), ha='center')
    
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico = '/home/ubuntu/analise_btts/formato_reorganizado/distribuicao_por_campeonato.png'
    plt.savefig(arquivo_grafico)
    plt.close()
    print(f"Gráfico de distribuição salvo em: {arquivo_grafico}")
    
    return arquivo_csv, '/home/ubuntu/analise_btts/formato_reorganizado/previsoes_reorganizadas.pdf'

def criar_pdf_formato_reorganizado(df, arquivo_pdf):
    """
    Cria um PDF com as previsões no formato reorganizado
    """
    print(f"Criando PDF com formato reorganizado: {arquivo_pdf}")
    
    # Criar documento PDF
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=landscape(letter))
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Título
    elements.append(Paragraph("PREVISÕES GRISAMANUS - FORMATO REORGANIZADO", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Data de geração
    elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Explicação da melhoria
    elements.append(Paragraph("Melhoria implementada: Reorganização das previsões por campeonato e hora para facilitar a visualização e acompanhamento.", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Campeonatos únicos
    campeonatos = df['CAMPEONATO'].unique()
    
    # Para cada campeonato, criar uma tabela
    for campeonato in campeonatos:
        elements.append(Paragraph(f"Campeonato: {campeonato}", subtitle_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Filtrar dados para este campeonato
        df_camp = df[df['CAMPEONATO'] == campeonato]
        
        # Preparar dados para tabela
        data = [['CAMPEONATO', 'HORA', 'COLUNA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'RESULTADO', 'GALE']]
        
        for _, row in df_camp.iterrows():
            data.append([
                row['CAMPEONATO'],
                str(row['HORA']),
                str(row['COLUNA']),
                row['MERCADO'],
                f"{row['PROBABILIDADE']:.2f}",
                row['CONFIANCA'],
                row['STAKE'],
                row['RESULTADO'],
                row['GALE']
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
        for i, row in enumerate(data[1:], 1):
            if row[5] == 'ALTA':
                table_style.add('BACKGROUND', (5, i), (5, i), colors.lightgreen)
            elif row[5] == 'MEDIA':
                table_style.add('BACKGROUND', (5, i), (5, i), colors.lightblue)
            elif row[5] == 'BAIXA':
                table_style.add('BACKGROUND', (5, i), (5, i), colors.lightcoral)
        
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 0.25*inch))
    
    # Adicionar nota explicativa
    elements.append(Paragraph("Notas:", styles["Heading3"]))
    elements.append(Paragraph("1. As previsões estão organizadas por campeonato e hora para facilitar a visualização e acompanhamento.", normal_style))
    elements.append(Paragraph("2. Dentro de cada campeonato, as previsões estão ordenadas por hora e coluna.", normal_style))
    elements.append(Paragraph("3. CONFIANÇA: ALTA (verde), MÉDIA (azul), BAIXA (vermelho).", normal_style))
    elements.append(Paragraph("4. Preencha a coluna RESULTADO após o jogo (verde = acerto, vermelho = erro).", normal_style))
    elements.append(Paragraph("5. Preencha a coluna GALE com o número de gales necessários (se aplicável).", normal_style))
    
    # Gerar PDF
    doc.build(elements)
    
    print(f"PDF gerado com sucesso: {arquivo_pdf}")
    
    return arquivo_pdf

def criar_exemplo_comparativo():
    """
    Cria uma imagem comparando o formato antigo com o novo formato
    """
    print("Criando exemplo comparativo dos formatos...")
    
    # Criar figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Dados para o formato antigo (ordenado por probabilidade/confiança)
    dados_antigo = [
        ['SUPER 52', '9', 'BTTS', '0.63', 'BAIXA', 'R$5.00', '', ''],
        ['PREMIER 24', '9', 'BTTS', '0.63', 'BAIXA', 'R$5.00', '', ''],
        ['SUPER 25', '9', 'BTTS', '0.62', 'BAIXA', 'R$5.00', '', ''],
        ['COPA 37', '9', 'BTTS', '0.61', 'BAIXA', 'R$5.00', '', ''],
        ['COPA 10', '10', 'BTTS', '0.68', 'BAIXA', 'R$5.00', '', ''],
        ['SUPER 49', '10', 'BTTS', '0.65', 'BAIXA', 'R$5.00', '', ''],
        ['COPA 43', '10', 'BTTS', '0.64', 'BAIXA', 'R$5.00', '', ''],
        ['EURO 47', '11', 'BTTS', '0.68', 'BAIXA', 'R$5.00', '', ''],
        ['COPA 10', '11', 'BTTS', '0.66', 'BAIXA', 'R$5.00', '', ''],
        ['COPA 1', '11', 'BTTS', '0.66', 'BAIXA', 'R$5.00', '', '']
    ]
    
    # Dados para o formato novo (ordenado por campeonato e hora)
    dados_novo = [
        ['COPA', '9', '37', 'BTTS', '0.61', 'BAIXA', 'R$5.00', '', ''],
        ['COPA', '10', '10', 'BTTS', '0.68', 'BAIXA', 'R$5.00', '', ''],
        ['COPA', '10', '43', 'BTTS', '0.64', 'BAIXA', 'R$5.00', '', ''],
        ['COPA', '11', '1', 'BTTS', '0.66', 'BAIXA', 'R$5.00', '', ''],
        ['COPA', '11', '10', 'BTTS', '0.66', 'BAIXA', 'R$5.00', '', ''],
        ['EURO', '11', '47', 'BTTS', '0.68', 'BAIXA', 'R$5.00', '', ''],
        ['PREMIER', '9', '24', 'BTTS', '0.63', 'BAIXA', 'R$5.00', '', ''],
        ['SUPER', '9', '25', 'BTTS', '0.62', 'BAIXA', 'R$5.00', '', ''],
        ['SUPER', '9', '52', 'BTTS', '0.63', 'BAIXA', 'R$5.00', '', ''],
        ['SUPER', '10', '49', 'BTTS', '0.65', 'BAIXA', 'R$5.00', '', '']
    ]
    
    # Criar tabela para formato antigo
    ax1.axis('tight')
    ax1.axis('off')
    ax1.set_title("Formato Antigo (Ordenado por Probabilidade/Confiança)", fontsize=14)
    
    tabela1 = ax1.table(
        cellText=dados_antigo,
        colLabels=['CAMPEONATO', 'HORA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'RESULTADO', 'GALE'],
        loc='center',
        cellLoc='center'
    )
    
    tabela1.auto_set_font_size(False)
    tabela1.set_fontsize(10)
    tabela1.scale(1, 1.5)
    
    # Destacar cabeçalho
    for j in range(len(dados_antigo[0])):
        tabela1[(0, j)].set_facecolor('lightgrey')
        tabela1[(0, j)].set_text_props(weight='bold')
    
    # Destacar níveis de confiança
    for i in range(len(dados_antigo)):
        tabela1[(i+1, 4)].set_facecolor('lightcoral')
    
    # Criar tabela para formato novo
    ax2.axis('tight')
    ax2.axis('off')
    ax2.set_title("Formato Novo (Ordenado por Campeonato e Hora)", fontsize=14)
    
    tabela2 = ax2.table(
        cellText=dados_novo,
        colLabels=['CAMPEONATO', 'HORA', 'COLUNA', 'MERCADO', 'PROBABILIDADE', 'CONFIANÇA', 'STAKE', 'RESULTADO', 'GALE'],
        loc='center',
        cellLoc='center'
    )
    
    tabela2.auto_set_font_size(False)
    tabela2.set_fontsize(10)
    tabela2.scale(1, 1.5)
    
    # Destacar cabeçalho
    for j in range(len(dados_novo[0])):
        tabela2[(0, j)].set_facecolor('lightgrey')
        tabela2[(0, j)].set_text_props(weight='bold')
    
    # Destacar níveis de confiança
    for i in range(len(dados_novo)):
        tabela2[(i+1, 5)].set_facecolor('lightcoral')
    
    # Destacar campeonatos (para mostrar o agrupamento)
    for i in range(5):
        for j in range(9):
            tabela2[(i+1, j)].set_facecolor('lightyellow')
    
    for i in range(5, 6):
        for j in range(9):
            tabela2[(i+1, j)].set_facecolor('lightblue')
    
    for i in range(6, 7):
        for j in range(9):
            tabela2[(i+1, j)].set_facecolor('lightgreen')
    
    for i in range(7, 10):
        for j in range(9):
            tabela2[(i+1, j)].set_facecolor('lightpink')
    
    # Restaurar cor das células de confiança
    for i in range(len(dados_novo)):
        tabela2[(i+1, 5)].set_facecolor('lightcoral')
    
    plt.tight_layout()
    
    # Salvar comparativo
    arquivo_comparativo = '/home/ubuntu/analise_btts/formato_reorganizado/comparativo_formatos.png'
    plt.savefig(arquivo_comparativo, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Exemplo comparativo salvo em: {arquivo_comparativo}")
    
    return arquivo_comparativo

if __name__ == "__main__":
    reorganizar_formato_previsoes()
    criar_exemplo_comparativo()
