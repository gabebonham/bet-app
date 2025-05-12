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

# Criar diretório para resultados corrigidos
os.makedirs('/home/ubuntu/analise_btts/resultados_corrigidos', exist_ok=True)

def criar_relatorio_consolidado_corrigido():
    """
    Cria um relatório consolidado corrigido com base nos valores corretos
    """
    print("Criando relatório consolidado corrigido...")
    
    # Valores corretos do relatório anterior (ontem)
    dados_ontem = {
        'total_previsoes': 79,
        'acertos': 73,
        'taxa_acerto': 92.41,
        'banca_inicial': 1000.00,
        'banca_final': 1155.00,
        'lucro': 155.00,
        'roi': 15.50,
        'acertos_sem_gale': 70.00,  # porcentagem
        'acertos_com_gale': 30.00   # porcentagem
    }
    
    # Valores de hoje
    dados_hoje = {
        'total_previsoes': 33,
        'acertos': 27,
        'taxa_acerto': 81.82,
        'banca_inicial': 1155.00,  # banca final de ontem
        'banca_final': 1312.50,
        'lucro': 157.50,
        'roi': 13.64,
        'acertos_sem_gale': 66.67,  # porcentagem
        'acertos_com_gale': 33.33   # porcentagem
    }
    
    # Dados consolidados
    dados_consolidados = {
        'total_previsoes': dados_ontem['total_previsoes'] + dados_hoje['total_previsoes'],
        'acertos': dados_ontem['acertos'] + dados_hoje['acertos'],
        'taxa_acerto': (dados_ontem['acertos'] + dados_hoje['acertos']) / (dados_ontem['total_previsoes'] + dados_hoje['total_previsoes']) * 100,
        'banca_inicial': dados_ontem['banca_inicial'],
        'banca_final': dados_hoje['banca_final'],
        'lucro': dados_ontem['lucro'] + dados_hoje['lucro'],
        'roi': ((dados_hoje['banca_final'] / dados_ontem['banca_inicial']) - 1) * 100,
        'acertos_sem_gale': (dados_ontem['acertos_sem_gale'] * dados_ontem['acertos'] + dados_hoje['acertos_sem_gale'] * dados_hoje['acertos']) / (dados_ontem['acertos'] + dados_hoje['acertos']),
        'acertos_com_gale': (dados_ontem['acertos_com_gale'] * dados_ontem['acertos'] + dados_hoje['acertos_com_gale'] * dados_hoje['acertos']) / (dados_ontem['acertos'] + dados_hoje['acertos'])
    }
    
    # Criar gráfico de evolução da banca
    plt.figure(figsize=(10, 6))
    
    dias = ['Inicial', 'Dia 1', 'Dia 2']
    valores = [dados_ontem['banca_inicial'], dados_ontem['banca_final'], dados_hoje['banca_final']]
    
    plt.plot(dias, valores, marker='o', linestyle='-', linewidth=2, markersize=10)
    
    for i, valor in enumerate(valores):
        plt.text(i, valor + 10, f'R${valor:.2f}', ha='center')
    
    plt.title('Evolução da Banca - GRISAMANUS', fontsize=16)
    plt.ylabel('Valor da Banca (R$)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Adicionar anotações de lucro
    plt.annotate(f'+R${dados_ontem["lucro"]:.2f} (+{dados_ontem["roi"]:.2f}%)', 
                 xy=(0.5, (valores[0] + valores[1])/2), 
                 xytext=(0.3, (valores[0] + valores[1])/2 + 50),
                 arrowprops=dict(facecolor='green', shrink=0.05))
    
    plt.annotate(f'+R${dados_hoje["lucro"]:.2f} (+{dados_hoje["roi"]:.2f}%)', 
                 xy=(1.5, (valores[1] + valores[2])/2), 
                 xytext=(1.3, (valores[1] + valores[2])/2 + 50),
                 arrowprops=dict(facecolor='green', shrink=0.05))
    
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico1 = '/home/ubuntu/analise_btts/resultados_corrigidos/evolucao_banca.png'
    plt.savefig(arquivo_grafico1)
    plt.close()
    
    # Criar gráfico de comparação de taxa de acerto
    plt.figure(figsize=(10, 6))
    
    categorias = ['Taxa de Acerto', 'Acertos sem Gale', 'ROI (%)']
    valores_ontem = [dados_ontem['taxa_acerto'], dados_ontem['acertos_sem_gale'], dados_ontem['roi']]
    valores_hoje = [dados_hoje['taxa_acerto'], dados_hoje['acertos_sem_gale'], dados_hoje['roi']]
    
    x = np.arange(len(categorias))
    width = 0.35
    
    plt.bar(x - width/2, valores_ontem, width, label='Dia 1', color='#99CCFF')
    plt.bar(x + width/2, valores_hoje, width, label='Dia 2', color='#99FF99')
    
    plt.title('Comparação de Desempenho - GRISAMANUS', fontsize=16)
    plt.ylabel('Valor (%)', fontsize=12)
    plt.xticks(x, categorias)
    plt.legend()
    
    # Adicionar valores nas barras
    for i, v in enumerate(valores_ontem):
        plt.text(i - width/2, v + 1, f'{v:.2f}%', ha='center')
    
    for i, v in enumerate(valores_hoje):
        plt.text(i + width/2, v + 1, f'{v:.2f}%', ha='center')
    
    plt.tight_layout()
    
    # Salvar gráfico
    arquivo_grafico2 = '/home/ubuntu/analise_btts/resultados_corrigidos/comparacao_desempenho.png'
    plt.savefig(arquivo_grafico2)
    plt.close()
    
    # Criar PDF com relatório consolidado
    criar_pdf_relatorio_consolidado(dados_ontem, dados_hoje, dados_consolidados, 
                                   arquivo_grafico1, arquivo_grafico2,
                                   '/home/ubuntu/analise_btts/resultados_corrigidos/GRISAMANUS_consolidado_corrigido.pdf')
    
    print("Relatório consolidado corrigido criado com sucesso!")
    
    return '/home/ubuntu/analise_btts/resultados_corrigidos/GRISAMANUS_consolidado_corrigido.pdf'

def criar_pdf_relatorio_consolidado(dados_ontem, dados_hoje, dados_consolidados, grafico1, grafico2, arquivo_pdf):
    """
    Cria um PDF com o relatório consolidado
    """
    print(f"Criando PDF com relatório consolidado: {arquivo_pdf}")
    
    # Criar documento PDF
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Título
    elements.append(Paragraph("RELATÓRIO CONSOLIDADO GRISAMANUS", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Data de geração
    elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabela 1: Resumo Consolidado
    elements.append(Paragraph("1. Resumo Consolidado", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Preparar dados para tabela de resumo
    data_resumo = [
        ['Métrica', 'Valor'],
        ['Total de Previsões', f"{dados_consolidados['total_previsoes']}"],
        ['Total de Acertos', f"{dados_consolidados['acertos']}"],
        ['Taxa de Acerto', f"{dados_consolidados['taxa_acerto']:.2f}%"],
        ['Banca Inicial', f"R${dados_consolidados['banca_inicial']:.2f}"],
        ['Banca Final', f"R${dados_consolidados['banca_final']:.2f}"],
        ['Lucro Total', f"R${dados_consolidados['lucro']:.2f}"],
        ['ROI', f"{dados_consolidados['roi']:.2f}%"],
        ['Acertos sem Gale', f"{dados_consolidados['acertos_sem_gale']:.2f}%"],
        ['Acertos com Gale', f"{dados_consolidados['acertos_com_gale']:.2f}%"]
    ]
    
    # Criar tabela de resumo
    table_resumo = Table(data_resumo, colWidths=[2*inch, 2*inch])
    
    # Estilo da tabela de resumo
    table_style_resumo = TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (1, -1), 10),
        ('GRID', (0, 0), (1, -1), 1, colors.black)
    ])
    
    table_resumo.setStyle(table_style_resumo)
    elements.append(table_resumo)
    elements.append(Spacer(1, 0.25*inch))
    
    # Tabela 2: Comparação Dia a Dia
    elements.append(Paragraph("2. Comparação Dia a Dia", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Preparar dados para tabela de comparação
    data_comp = [
        ['Métrica', 'Dia 1', 'Dia 2', 'Variação'],
        ['Total de Previsões', f"{dados_ontem['total_previsoes']}", f"{dados_hoje['total_previsoes']}", f"{dados_hoje['total_previsoes'] - dados_ontem['total_previsoes']}"],
        ['Taxa de Acerto', f"{dados_ontem['taxa_acerto']:.2f}%", f"{dados_hoje['taxa_acerto']:.2f}%", f"{dados_hoje['taxa_acerto'] - dados_ontem['taxa_acerto']:.2f}%"],
        ['Banca Inicial', f"R${dados_ontem['banca_inicial']:.2f}", f"R${dados_hoje['banca_inicial']:.2f}", f"R${dados_hoje['banca_inicial'] - dados_ontem['banca_inicial']:.2f}"],
        ['Banca Final', f"R${dados_ontem['banca_final']:.2f}", f"R${dados_hoje['banca_final']:.2f}", f"R${dados_hoje['banca_final'] - dados_ontem['banca_final']:.2f}"],
        ['Lucro', f"R${dados_ontem['lucro']:.2f}", f"R${dados_hoje['lucro']:.2f}", f"R${dados_hoje['lucro'] - dados_ontem['lucro']:.2f}"],
        ['ROI', f"{dados_ontem['roi']:.2f}%", f"{dados_hoje['roi']:.2f}%", f"{dados_hoje['roi'] - dados_ontem['roi']:.2f}%"],
        ['Acertos sem Gale', f"{dados_ontem['acertos_sem_gale']:.2f}%", f"{dados_hoje['acertos_sem_gale']:.2f}%", f"{dados_hoje['acertos_sem_gale'] - dados_ontem['acertos_sem_gale']:.2f}%"]
    ]
    
    # Criar tabela de comparação
    table_comp = Table(data_comp, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    
    # Estilo da tabela de comparação
    table_style_comp = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (3, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (3, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (3, 0), 12),
        ('BOTTOMPADDING', (0, 0), (3, 0), 12),
        ('BACKGROUND', (0, 1), (3, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (3, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (3, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (3, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (3, -1), 10),
        ('GRID', (0, 0), (3, -1), 1, colors.black)
    ])
    
    # Aplicar cores específicas para variações
    for i in range(2, len(data_comp)):
        valor = data_comp[i][3]
        if "%" in valor:
            valor_num = float(valor.replace("%", ""))
        elif "R$" in valor:
            valor_num = float(valor.replace("R$", ""))
        else:
            valor_num = float(valor)
        
        if valor_num > 0:
            table_style_comp.add('TEXTCOLOR', (3, i), (3, i), colors.green)
        elif valor_num < 0:
            table_style_comp.add('TEXTCOLOR', (3, i), (3, i), colors.red)
    
    table_comp.setStyle(table_style_comp)
    elements.append(table_comp)
    elements.append(Spacer(1, 0.25*inch))
    
    # Adicionar gráficos
    elements.append(Paragraph("3. Evolução da Banca", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    img1 = Image(grafico1, width=6*inch, height=3.5*inch)
    elements.append(img1)
    elements.append(Spacer(1, 0.25*inch))
    
    elements.append(Paragraph("4. Comparação de Desempenho", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    img2 = Image(grafico2, width=6*inch, height=3.5*inch)
    elements.append(img2)
    elements.append(Spacer(1, 0.25*inch))
    
    # Adicionar conclusões
    elements.append(Paragraph("5. Conclusões e Recomendações", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("O modelo GRISAMANUS continua apresentando excelente desempenho, com uma taxa de acerto consolidada de 89,29% e um ROI de 31,25% em dois dias de operação.", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("Observações importantes:", normal_style))
    elements.append(Paragraph("• Houve uma pequena redução na taxa de acerto no segundo dia (de 92,41% para 81,82%), mas ainda mantendo um nível excelente", normal_style))
    elements.append(Paragraph("• O lucro do segundo dia (R$157,50) foi ligeiramente superior ao do primeiro dia (R$155,00)", normal_style))
    elements.append(Paragraph("• A porcentagem de acertos sem gale diminuiu levemente (de 70,00% para 66,67%)", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("Recomendações para otimização:", normal_style))
    elements.append(Paragraph("1. Manter o limite mínimo de probabilidade em 0.65 para o grupo BAIXA", normal_style))
    elements.append(Paragraph("2. Continuar priorizando operações nos horários de maior ocorrência (12h-17h)", normal_style))
    elements.append(Paragraph("3. Focar nos campeonatos PREMIER e COPA para BTTS, e SUPER e PREMIER para Over 2.5", normal_style))
    elements.append(Paragraph("4. Utilizar a tabela operacional GRISAMANUS para otimizar as entradas por horário", normal_style))
    
    # Gerar PDF
    doc.build(elements)
    
    print(f"PDF gerado com sucesso: {arquivo_pdf}")
    
    return arquivo_pdf

if __name__ == "__main__":
    criar_relatorio_consolidado_corrigido()
