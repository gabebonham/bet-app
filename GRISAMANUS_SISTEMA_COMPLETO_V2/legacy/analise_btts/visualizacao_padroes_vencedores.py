import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
import cv2
import os

# Carregar a matriz de dados
matriz_dados_path = '/home/ubuntu/analise_btts/resultados/matriz_dados.csv'
matriz_dados = np.loadtxt(matriz_dados_path, delimiter=',')

# Criar diretório para salvar resultados
output_dir = '/home/ubuntu/analise_btts/resultados_adicionais'
os.makedirs(output_dir, exist_ok=True)

# Definir os padrões vencedores com base na análise anterior
# 1. Retângulos (taxa de acerto: 29.81%)
# 2. Triângulos (taxa de acerto: 28.54%)
# 3. Diagonais Secundárias (taxa de acerto: 27.63%)
# 4. Diagonais Principais (taxa de acerto: 25.67%)

def identificar_retangulos(matriz, min_tamanho=2):
    """Identifica retângulos de células verdes na matriz."""
    num_linhas, num_colunas = matriz.shape
    retangulos = []
    
    # Para cada posição na matriz
    for i in range(num_linhas - min_tamanho + 1):
        for j in range(num_colunas - min_tamanho + 1):
            # Verificar se há um retângulo de tamanho mínimo
            if (matriz[i:i+min_tamanho, j:j+min_tamanho] == 1).all():
                # Expandir o retângulo horizontalmente
                largura = min_tamanho
                while j + largura < num_colunas and (matriz[i:i+min_tamanho, j+largura] == 1).all():
                    largura += 1
                
                # Expandir o retângulo verticalmente
                altura = min_tamanho
                while i + altura < num_linhas and (matriz[i+altura, j:j+largura] == 1).all():
                    altura += 1
                
                retangulos.append({
                    'posicao': (i, j),
                    'tamanho': (altura, largura),
                    'area': altura * largura
                })
    
    return retangulos

def identificar_triangulos(matriz):
    """Identifica triângulos de células verdes na matriz."""
    num_linhas, num_colunas = matriz.shape
    triangulos = []
    
    # Para cada posição na matriz
    for i in range(num_linhas - 2):
        for j in range(num_colunas - 2):
            # Verificar padrão de triângulo (simplificado como L)
            if matriz[i, j] == 1 and matriz[i+1, j] == 1 and matriz[i, j+1] == 1:
                triangulos.append({
                    'posicao': (i, j),
                    'tipo': 'L'
                })
            # Verificar padrão de triângulo invertido
            if matriz[i, j] == 1 and matriz[i, j+1] == 1 and matriz[i+1, j+1] == 1:
                triangulos.append({
                    'posicao': (i, j),
                    'tipo': 'L_invertido'
                })
    
    return triangulos

def identificar_diagonais(matriz, min_tamanho=3):
    """Identifica diagonais de células verdes na matriz."""
    num_linhas, num_colunas = matriz.shape
    diagonais_principais = []
    diagonais_secundarias = []
    
    # Diagonais principais (↘)
    for i in range(num_linhas - min_tamanho + 1):
        for j in range(num_colunas - min_tamanho + 1):
            # Verificar se há uma diagonal principal
            diagonal = True
            for k in range(min_tamanho):
                if matriz[i+k, j+k] != 1:
                    diagonal = False
                    break
            
            if diagonal:
                # Expandir a diagonal
                comprimento = min_tamanho
                while (i + comprimento < num_linhas and 
                       j + comprimento < num_colunas and 
                       matriz[i+comprimento, j+comprimento] == 1):
                    comprimento += 1
                
                diagonais_principais.append({
                    'inicio': (i, j),
                    'comprimento': comprimento
                })
    
    # Diagonais secundárias (↙)
    for i in range(num_linhas - min_tamanho + 1):
        for j in range(min_tamanho - 1, num_colunas):
            # Verificar se há uma diagonal secundária
            diagonal = True
            for k in range(min_tamanho):
                if matriz[i+k, j-k] != 1:
                    diagonal = False
                    break
            
            if diagonal:
                # Expandir a diagonal
                comprimento = min_tamanho
                while (i + comprimento < num_linhas and 
                       j - comprimento >= 0 and 
                       matriz[i+comprimento, j-comprimento] == 1):
                    comprimento += 1
                
                diagonais_secundarias.append({
                    'inicio': (i, j),
                    'comprimento': comprimento
                })
    
    return diagonais_principais, diagonais_secundarias

# Identificar os padrões na matriz
retangulos = identificar_retangulos(matriz_dados)
triangulos = identificar_triangulos(matriz_dados)
diagonais_principais, diagonais_secundarias = identificar_diagonais(matriz_dados)

print(f"Padrões identificados:")
print(f"- Retângulos: {len(retangulos)}")
print(f"- Triângulos: {len(triangulos)}")
print(f"- Diagonais Principais: {len(diagonais_principais)}")
print(f"- Diagonais Secundárias: {len(diagonais_secundarias)}")

# Ordenar retângulos por área (do maior para o menor)
retangulos_ordenados = sorted(retangulos, key=lambda x: x['area'], reverse=True)
# Pegar os 10 maiores retângulos
top_retangulos = retangulos_ordenados[:10]

# Ordenar diagonais por comprimento (da maior para a menor)
diagonais_principais_ordenadas = sorted(diagonais_principais, key=lambda x: x['comprimento'], reverse=True)
diagonais_secundarias_ordenadas = sorted(diagonais_secundarias, key=lambda x: x['comprimento'], reverse=True)
# Pegar as 10 maiores diagonais de cada tipo
top_diagonais_principais = diagonais_principais_ordenadas[:10]
top_diagonais_secundarias = diagonais_secundarias_ordenadas[:10]

# Visualizar os padrões vencedores na matriz original
plt.figure(figsize=(15, 30))
cmap = LinearSegmentedColormap.from_list('rg', ['red', 'green'], N=2)
plt.imshow(matriz_dados, cmap=cmap, interpolation='nearest')

# Marcar os top retângulos
for retangulo in top_retangulos:
    y, x = retangulo['posicao']
    h, w = retangulo['tamanho']
    rect = plt.Rectangle((x-0.5, y-0.5), w, h, linewidth=2, edgecolor='yellow', facecolor='none')
    plt.gca().add_patch(rect)
    plt.text(x+w/2-0.5, y+h/2-0.5, f"R{retangulo['area']}", color='yellow', fontsize=10, ha='center', va='center')

# Marcar os top triângulos
for i, triangulo in enumerate(triangulos[:20]):
    y, x = triangulo['posicao']
    if triangulo['tipo'] == 'L':
        plt.plot([x-0.5, x+0.5, x-0.5, x-0.5], [y-0.5, y-0.5, y+0.5, y-0.5], color='cyan', linewidth=2)
    else:  # L_invertido
        plt.plot([x-0.5, x+1.5, x+1.5, x-0.5], [y-0.5, y-0.5, y+0.5, y-0.5], color='cyan', linewidth=2)
    plt.text(x, y, f"T{i+1}", color='cyan', fontsize=8, ha='center', va='center')

# Marcar as top diagonais principais
for i, diagonal in enumerate(top_diagonais_principais):
    y, x = diagonal['inicio']
    comprimento = diagonal['comprimento']
    plt.plot([x-0.5+i for i in range(comprimento)], 
             [y-0.5+i for i in range(comprimento)], 
             color='magenta', linewidth=2)
    plt.text(x, y, f"DP{i+1}", color='magenta', fontsize=8, ha='center', va='center')

# Marcar as top diagonais secundárias
for i, diagonal in enumerate(top_diagonais_secundarias):
    y, x = diagonal['inicio']
    comprimento = diagonal['comprimento']
    plt.plot([x+0.5-i for i in range(comprimento)], 
             [y-0.5+i for i in range(comprimento)], 
             color='white', linewidth=2)
    plt.text(x, y, f"DS{i+1}", color='white', fontsize=8, ha='center', va='center')

plt.colorbar(ticks=[0, 1], label='Vermelho (0) / Verde (1)')
plt.title('Padrões Geométricos Vencedores Identificados')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Linhas (Horários)')
plt.grid(True, color='black', linestyle='-', linewidth=0.5)

# Adicionar legenda
plt.figtext(0.15, 0.01, "Legenda:", fontsize=12, weight='bold')
plt.figtext(0.15, 0.005, "R = Retângulo (amarelo) | T = Triângulo (ciano) | DP = Diagonal Principal (magenta) | DS = Diagonal Secundária (branco)", fontsize=10)

# Salvar a visualização
plt.savefig(f"{output_dir}/padroes_vencedores_visualizacao.png", dpi=300, bbox_inches='tight')

# Criar uma visualização invertida (de baixo para cima) conforme solicitado pelo usuário
matriz_invertida = np.flipud(matriz_dados)

plt.figure(figsize=(15, 30))
plt.imshow(matriz_invertida, cmap=cmap, interpolation='nearest')

# Marcar os top retângulos na visualização invertida
for retangulo in top_retangulos:
    y, x = retangulo['posicao']
    h, w = retangulo['tamanho']
    # Ajustar a posição y para a matriz invertida
    y_inv = matriz_dados.shape[0] - y - h
    rect = plt.Rectangle((x-0.5, y_inv-0.5), w, h, linewidth=2, edgecolor='yellow', facecolor='none')
    plt.gca().add_patch(rect)
    plt.text(x+w/2-0.5, y_inv+h/2-0.5, f"R{retangulo['area']}", color='yellow', fontsize=10, ha='center', va='center')

# Marcar os top triângulos na visualização invertida
for i, triangulo in enumerate(triangulos[:20]):
    y, x = triangulo['posicao']
    # Ajustar a posição y para a matriz invertida
    y_inv = matriz_dados.shape[0] - y - 1
    if triangulo['tipo'] == 'L':
        plt.plot([x-0.5, x+0.5, x-0.5, x-0.5], [y_inv-0.5, y_inv-0.5, y_inv+0.5, y_inv-0.5], color='cyan', linewidth=2)
    else:  # L_invertido
        plt.plot([x-0.5, x+1.5, x+1.5, x-0.5], [y_inv-0.5, y_inv-0.5, y_inv+0.5, y_inv-0.5], color='cyan', linewidth=2)
    plt.text(x, y_inv, f"T{i+1}", color='cyan', fontsize=8, ha='center', va='center')

# Marcar as top diagonais principais na visualização invertida
for i, diagonal in enumerate(top_diagonais_principais):
    y, x = diagonal['inicio']
    comprimento = diagonal['comprimento']
    # Ajustar a posição y para a matriz invertida
    y_inv = matriz_dados.shape[0] - y - 1
    plt.plot([x-0.5+i for i in range(comprimento)], 
             [y_inv+0.5-i for i in range(comprimento)], 
             color='magenta', linewidth=2)
    plt.text(x, y_inv, f"DP{i+1}", color='magenta', fontsize=8, ha='center', va='center')

# Marcar as top diagonais secundárias na visualização invertida
for i, diagonal in enumerate(top_diagonais_secundarias):
    y, x = diagonal['inicio']
    comprimento = diagonal['comprimento']
    # Ajustar a posição y para a matriz invertida
    y_inv = matriz_dados.shape[0] - y - 1
    plt.plot([x+0.5-i for i in range(comprimento)], 
             [y_inv+0.5-i for i in range(comprimento)], 
             color='white', linewidth=2)
    plt.text(x, y_inv, f"DS{i+1}", color='white', fontsize=8, ha='center', va='center')

plt.colorbar(ticks=[0, 1], label='Vermelho (0) / Verde (1)')
plt.title('Padrões Geométricos Vencedores (Visualização de Baixo para Cima)')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Linhas (Horários - Entrada na parte superior)')
plt.grid(True, color='black', linestyle='-', linewidth=0.5)

# Adicionar seta indicando direção de entrada
plt.annotate('Direção de Entrada', xy=(matriz_dados.shape[1]/2, 5), xytext=(matriz_dados.shape[1]/2, 15),
             arrowprops=dict(facecolor='white', shrink=0.05), color='white',
             horizontalalignment='center', verticalalignment='center')

# Adicionar legenda
plt.figtext(0.15, 0.01, "Legenda:", fontsize=12, weight='bold')
plt.figtext(0.15, 0.005, "R = Retângulo (amarelo) | T = Triângulo (ciano) | DP = Diagonal Principal (magenta) | DS = Diagonal Secundária (branco)", fontsize=10)

# Salvar a visualização invertida
plt.savefig(f"{output_dir}/padroes_vencedores_visualizacao_invertida.png", dpi=300, bbox_inches='tight')

print(f"Visualizações salvas em: {output_dir}")
