import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.ndimage import label, find_objects
import os

# Caminho da imagem
imagem_path = '/home/ubuntu/upload/screencapture-thtips-br-futebol-horarios-2025-04-25-12_11_53.png'

# Carregar a imagem
imagem = cv2.imread(imagem_path)

# Verificar se a imagem foi carregada corretamente
if imagem is None:
    print(f"Erro ao carregar a imagem: {imagem_path}")
    exit()

# Converter para RGB (OpenCV carrega como BGR)
imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

# Criar diretório para salvar resultados
output_dir = '/home/ubuntu/analise_btts/resultados'
os.makedirs(output_dir, exist_ok=True)

# Função para detectar células verdes e vermelhas
def detectar_cores(imagem):
    # Converter para HSV para melhor detecção de cores
    imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_RGB2HSV)
    
    # Definir intervalos de cores para verde e vermelho em HSV
    # Vermelho em HSV pode estar em dois intervalos (próximo a 0° e próximo a 180°)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    
    # Criar máscaras para cada cor
    mask_red1 = cv2.inRange(imagem_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(imagem_hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_green = cv2.inRange(imagem_hsv, lower_green, upper_green)
    
    return mask_red, mask_green

# Detectar cores
mask_red, mask_green = detectar_cores(imagem_rgb)

# Função para extrair a matriz de dados (0 para vermelho, 1 para verde)
def extrair_matriz_dados(mask_red, mask_green, imagem_rgb):
    # Encontrar contornos das células
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Combinar todos os contornos
    all_contours = contours_red + contours_green
    
    # Extrair coordenadas dos centros dos contornos
    centers = []
    for contour in all_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Verificar se é vermelho ou verde
            if mask_red[cY, cX] > 0:
                color = 0  # Vermelho
            else:
                color = 1  # Verde
            centers.append((cX, cY, color))
    
    # Ordenar por Y (linhas) e depois por X (colunas)
    centers.sort(key=lambda p: (p[1], p[0]))
    
    # Identificar linhas únicas (agrupando por coordenada Y similar)
    y_coords = [center[1] for center in centers]
    y_unique = []
    last_y = -100
    for y in y_coords:
        if abs(y - last_y) > 10:  # Threshold para considerar uma nova linha
            y_unique.append(y)
            last_y = y
    
    # Criar matriz vazia
    num_rows = len(y_unique)
    # Assumindo 20 colunas conforme informado pelo usuário
    num_cols = 20
    matriz = np.full((num_rows, num_cols), -1)  # -1 indica célula não identificada
    
    # Preencher matriz
    for center in centers:
        x, y, color = center
        # Encontrar índice da linha
        row_idx = min(range(len(y_unique)), key=lambda i: abs(y_unique[i] - y))
        
        # Estimar índice da coluna com base na posição X
        # Isso é uma aproximação, pode precisar de ajustes
        col_idx = min(int(x / (imagem_rgb.shape[1] / num_cols)), num_cols - 1)
        
        matriz[row_idx, col_idx] = color
    
    return matriz

# Tentar extrair a matriz de dados
try:
    matriz_dados = extrair_matriz_dados(mask_red, mask_green, imagem_rgb)
    print(f"Matriz de dados extraída com forma: {matriz_dados.shape}")
except Exception as e:
    print(f"Erro ao extrair matriz de dados: {e}")
    # Criar uma matriz aproximada com base na imagem
    # Vamos usar uma abordagem diferente, dividindo a imagem em uma grade
    altura, largura = imagem_rgb.shape[:2]
    
    # Cortar apenas a parte da tabela (estimativa)
    y_start = int(altura * 0.1)  # Ignorar o cabeçalho
    y_end = altura
    x_start = 0
    x_end = largura
    
    imagem_tabela = imagem_rgb[y_start:y_end, x_start:x_end]
    
    # Dividir em 24 linhas (horas) e 20 colunas (campeonatos)
    num_rows = 24
    num_cols = 20
    
    altura_tabela, largura_tabela = imagem_tabela.shape[:2]
    altura_celula = altura_tabela // num_rows
    largura_celula = largura_tabela // num_cols
    
    matriz_dados = np.zeros((num_rows, num_cols))
    
    for i in range(num_rows):
        for j in range(num_cols):
            y1 = i * altura_celula
            y2 = (i + 1) * altura_celula
            x1 = j * largura_celula
            x2 = (j + 1) * largura_celula
            
            celula = imagem_tabela[y1:y2, x1:x2]
            
            # Contar pixels verdes e vermelhos
            hsv = cv2.cvtColor(celula, cv2.COLOR_RGB2HSV)
            
            # Vermelho
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            red_pixels = cv2.countNonZero(mask_red)
            
            # Verde
            lower_green = np.array([40, 100, 100])
            upper_green = np.array([80, 255, 255])
            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            green_pixels = cv2.countNonZero(mask_green)
            
            # Determinar cor predominante
            if green_pixels > red_pixels:
                matriz_dados[i, j] = 1  # Verde
            else:
                matriz_dados[i, j] = 0  # Vermelho

# Salvar a matriz como CSV
np.savetxt(f"{output_dir}/matriz_dados.csv", matriz_dados, delimiter=',', fmt='%d')

# Visualizar a matriz como imagem
plt.figure(figsize=(12, 24))
cmap = LinearSegmentedColormap.from_list('rg', ['red', 'green'], N=2)
plt.imshow(matriz_dados, cmap=cmap, interpolation='nearest')
plt.colorbar(ticks=[0, 1], label='Vermelho (0) / Verde (1)')
plt.title('Matriz de Dados BTTS')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Linhas (Horários)')
plt.grid(True, color='black', linestyle='-', linewidth=0.5)
plt.savefig(f"{output_dir}/matriz_visualizacao.png", dpi=300, bbox_inches='tight')

# Função para identificar padrões geométricos
def identificar_padroes(matriz):
    padroes = {
        'triangulos': [],
        'retangulos': [],
        'diagonais': [],
        'clusters': []
    }
    
    # 1. Identificar triângulos (3 ou mais células da mesma cor em formato triangular)
    for cor in [0, 1]:  # 0 para vermelho, 1 para verde
        mascara = (matriz == cor)
        # Corrigido: estrutura para label deve ter a mesma dimensão que a matriz de entrada
        estrutura = np.ones((3, 3), dtype=np.int32)  # Estrutura 3x3 para conectividade
        rotulos, num_features = label(mascara, structure=estrutura)
        
        for i in range(1, num_features + 1):
            obj = (rotulos == i)
            if np.sum(obj) >= 3:  # Pelo menos 3 células
                # Verificar se forma um triângulo (simplificação)
                objetos = find_objects(obj)
                if objetos:
                    slice_y, slice_x = objetos[0]
                    altura = slice_y.stop - slice_y.start
                    largura = slice_x.stop - slice_x.start
                    
                    # Se a forma se aproxima de um triângulo (altura diferente da largura)
                    if altura != largura and altura >= 2 and largura >= 2:
                        padroes['triangulos'].append({
                            'cor': 'verde' if cor == 1 else 'vermelho',
                            'posicao': (slice_y.start, slice_x.start),
                            'tamanho': (altura, largura)
                        })
    
    # 2. Identificar retângulos (blocos de células da mesma cor)
    for cor in [0, 1]:
        mascara = (matriz == cor)
        estrutura = np.ones((3, 3), dtype=np.int32)  # Corrigido para 3x3
        rotulos, num_features = label(mascara, structure=estrutura)
        
        for i in range(1, num_features + 1):
            obj = (rotulos == i)
            if np.sum(obj) >= 4:  # Pelo menos 4 células
                objetos = find_objects(obj)
                if objetos:
                    slice_y, slice_x = objetos[0]
                    altura = slice_y.stop - slice_y.start
                    largura = slice_x.stop - slice_x.start
                    
                    # Se forma um retângulo (pelo menos 2x2)
                    if altura >= 2 and largura >= 2:
                        area = altura * largura
                        contagem = np.sum(obj)
                        # Se pelo menos 80% das células no retângulo são da mesma cor
                        if contagem / area >= 0.8:
                            padroes['retangulos'].append({
                                'cor': 'verde' if cor == 1 else 'vermelho',
                                'posicao': (slice_y.start, slice_x.start),
                                'tamanho': (altura, largura),
                                'area': int(contagem)
                            })
    
    # 3. Identificar diagonais (sequências diagonais da mesma cor)
    for cor in [0, 1]:
        # Diagonais principais
        for i in range(matriz.shape[0] - 2):  # Pelo menos 3 células
            for j in range(matriz.shape[1] - 2):
                # Verificar diagonal principal
                diagonal = [matriz[i+k, j+k] for k in range(3)]
                if all(d == cor for d in diagonal):
                    # Estender a diagonal se possível
                    k = 3
                    while (i+k < matriz.shape[0] and j+k < matriz.shape[1] and 
                           matriz[i+k, j+k] == cor):
                        k += 1
                    
                    if k >= 3:  # Diagonal de pelo menos 3 células
                        padroes['diagonais'].append({
                            'cor': 'verde' if cor == 1 else 'vermelho',
                            'tipo': 'principal',
                            'inicio': (i, j),
                            'comprimento': k
                        })
        
        # Diagonais secundárias
        for i in range(matriz.shape[0] - 2):
            for j in range(2, matriz.shape[1]):
                # Verificar diagonal secundária
                diagonal = [matriz[i+k, j-k] for k in range(3)]
                if all(d == cor for d in diagonal):
                    # Estender a diagonal se possível
                    k = 3
                    while (i+k < matriz.shape[0] and j-k >= 0 and 
                           matriz[i+k, j-k] == cor):
                        k += 1
                    
                    if k >= 3:
                        padroes['diagonais'].append({
                            'cor': 'verde' if cor == 1 else 'vermelho',
                            'tipo': 'secundaria',
                            'inicio': (i, j),
                            'comprimento': k
                        })
    
    # 4. Identificar clusters usando K-means
    # Preparar dados para clustering
    pontos = []
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            pontos.append([i, j, matriz[i, j]])
    
    pontos = np.array(pontos)
    
    # Determinar número ideal de clusters
    max_clusters = min(10, matriz.shape[0] * matriz.shape[1] // 10)  # Limitar número de clusters
    max_clusters = max(2, min(max_clusters, 8))  # Entre 2 e 8 clusters
    
    melhor_score = -1
    melhor_n_clusters = 2
    
    for n_clusters in range(2, max_clusters + 1):
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(pontos[:, :2])  # Usar apenas coordenadas
            
            if len(set(cluster_labels)) > 1:  # Verificar se há mais de um cluster
                score = silhouette_score(pontos[:, :2], cluster_labels)
                if score > melhor_score:
                    melhor_score = score
                    melhor_n_clusters = n_clusters
        except:
            continue
    
    # Aplicar K-means com o melhor número de clusters
    kmeans = KMeans(n_clusters=melhor_n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(pontos[:, :2])
    
    # Analisar cada cluster
    for cluster_id in range(melhor_n_clusters):
        cluster_points = pontos[cluster_labels == cluster_id]
        
        # Contar ocorrências de verde e vermelho no cluster
        verdes = np.sum(cluster_points[:, 2] == 1)
        vermelhos = np.sum(cluster_points[:, 2] == 0)
        total = len(cluster_points)
        
        # Determinar cor predominante
        if verdes > vermelhos:
            cor_predominante = 'verde'
            porcentagem = verdes / total * 100
        else:
            cor_predominante = 'vermelho'
            porcentagem = vermelhos / total * 100
        
        # Calcular centro do cluster
        centro_y = np.mean(cluster_points[:, 0])
        centro_x = np.mean(cluster_points[:, 1])
        
        # Adicionar informações do cluster
        if porcentagem >= 60:  # Cluster com predominância clara (pelo menos 60%)
            padroes['clusters'].append({
                'cor_predominante': cor_predominante,
                'centro': (int(centro_y), int(centro_x)),
                'tamanho': len(cluster_points),
                'porcentagem': round(porcentagem, 2)
            })
    
    return padroes

# Identificar padrões na matriz
padroes = identificar_padroes(matriz_dados)

# Salvar resultados dos padrões
with open(f"{output_dir}/padroes_identificados.txt", 'w') as f:
    f.write("PADRÕES GEOMÉTRICOS IDENTIFICADOS\n")
    f.write("================================\n\n")
    
    f.write("1. TRIÂNGULOS\n")
    f.write("--------------\n")
    for i, triangulo in enumerate(padroes['triangulos']):
        f.write(f"Triângulo {i+1}: Cor {triangulo['cor']}, Posição {triangulo['posicao']}, Tamanho {triangulo['tamanho']}\n")
    f.write(f"Total de triângulos: {len(padroes['triangulos'])}\n\n")
    
    f.write("2. RETÂNGULOS\n")
    f.write("--------------\n")
    # Ordenar retângulos por área (do maior para o menor)
    retangulos_ordenados = sorted(padroes['retangulos'], key=lambda x: x['area'], reverse=True)
    for i, retangulo in enumerate(retangulos_ordenados):
        f.write(f"Retângulo {i+1}: Cor {retangulo['cor']}, Posição {retangulo['posicao']}, Tamanho {retangulo['tamanho']}, Área {retangulo['area']}\n")
    f.write(f"Total de retângulos: {len(padroes['retangulos'])}\n\n")
    
    f.write("3. DIAGONAIS\n")
    f.write("--------------\n")
    # Ordenar diagonais por comprimento (da maior para a menor)
    diagonais_ordenadas = sorted(padroes['diagonais'], key=lambda x: x['comprimento'], reverse=True)
    for i, diagonal in enumerate(diagonais_ordenadas):
        f.write(f"Diagonal {i+1}: Cor {diagonal['cor']}, Tipo {diagonal['tipo']}, Início {diagonal['inicio']}, Comprimento {diagonal['comprimento']}\n")
    f.write(f"Total de diagonais: {len(padroes['diagonais'])}\n\n")
    
    f.write("4. CLUSTERS\n")
    f.write("--------------\n")
    # Ordenar clusters por tamanho (do maior para o menor)
    clusters_ordenados = sorted(padroes['clusters'], key=lambda x: x['tamanho'], reverse=True)
    for i, cluster in enumerate(clusters_ordenados):
        f.write(f"Cluster {i+1}: Cor predominante {cluster['cor_predominante']} ({cluster['porcentagem']}%), Centro {cluster['centro']}, Tamanho {cluster['tamanho']}\n")
    f.write(f"Total de clusters: {len(padroes['clusters'])}\n")

# Visualizar padrões na matriz
plt.figure(figsize=(15, 30))
plt.imshow(matriz_dados, cmap=cmap, interpolation='nearest')

# Marcar triângulos
for triangulo in padroes['triangulos']:
    y, x = triangulo['posicao']
    h, w = triangulo['tamanho']
    cor = 'lime' if triangulo['cor'] == 'verde' else 'yellow'
    rect = plt.Rectangle((x-0.5, y-0.5), w, h, linewidth=2, edgecolor=cor, facecolor='none')
    plt.gca().add_patch(rect)

# Marcar retângulos
for retangulo in padroes['retangulos']:
    y, x = retangulo['posicao']
    h, w = retangulo['tamanho']
    cor = 'lime' if retangulo['cor'] == 'verde' else 'yellow'
    rect = plt.Rectangle((x-0.5, y-0.5), w, h, linewidth=2, edgecolor=cor, facecolor='none')
    plt.gca().add_patch(rect)

# Marcar diagonais
for diagonal in padroes['diagonais']:
    y, x = diagonal['inicio']
    comprimento = diagonal['comprimento']
    cor = 'lime' if diagonal['cor'] == 'verde' else 'yellow'
    
    if diagonal['tipo'] == 'principal':
        plt.plot([x-0.5+i for i in range(comprimento)], 
                 [y-0.5+i for i in range(comprimento)], 
                 color=cor, linewidth=2)
    else:  # secundária
        plt.plot([x+0.5-i for i in range(comprimento)], 
                 [y-0.5+i for i in range(comprimento)], 
                 color=cor, linewidth=2)

# Marcar clusters
for cluster in padroes['clusters']:
    y, x = cluster['centro']
    cor = 'lime' if cluster['cor_predominante'] == 'verde' else 'yellow'
    plt.scatter(x, y, s=100, color=cor, edgecolor='white', linewidth=2)

plt.colorbar(ticks=[0, 1], label='Vermelho (0) / Verde (1)')
plt.title('Padrões Geométricos Identificados')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Linhas (Horários)')
plt.grid(True, color='black', linestyle='-', linewidth=0.5)
plt.savefig(f"{output_dir}/padroes_visualizacao.png", dpi=300, bbox_inches='tight')

print("Análise de padrões geométricos concluída. Resultados salvos em:", output_dir)
