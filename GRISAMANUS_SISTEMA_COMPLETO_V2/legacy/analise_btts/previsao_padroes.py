import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from scipy.stats import poisson
import os
import warnings
warnings.filterwarnings('ignore')

# Carregar a matriz de dados
matriz_dados_path = '/home/ubuntu/analise_btts/resultados/matriz_dados.csv'
matriz_dados = np.loadtxt(matriz_dados_path, delimiter=',')

# Criar diretório para salvar resultados de previsão
output_dir = '/home/ubuntu/analise_btts/resultados_previsao'
os.makedirs(output_dir, exist_ok=True)

print(f"Matriz de dados carregada com forma: {matriz_dados.shape}")

# Função para criar features baseadas em padrões geométricos
def extrair_features_padroes(matriz, janela_tempo=24):
    num_linhas, num_colunas = matriz.shape
    features = []
    labels = []
    
    # Para cada posição na matriz (exceto as últimas linhas que serão usadas como labels)
    for i in range(num_linhas - janela_tempo):
        for j in range(num_colunas):
            # Extrair janela de tempo anterior
            janela = matriz[i:i+janela_tempo, :]
            
            # Features baseadas em padrões geométricos
            features_linha = []
            
            # 1. Proporção de verde/vermelho na janela
            proporcao_verde = np.sum(janela == 1) / (janela_tempo * num_colunas)
            features_linha.append(proporcao_verde)
            
            # 2. Proporção de verde/vermelho na coluna específica
            proporcao_verde_coluna = np.sum(janela[:, j] == 1) / janela_tempo
            features_linha.append(proporcao_verde_coluna)
            
            # 3. Tendência (aumento ou diminuição de verdes)
            # Dividir a janela em duas metades e comparar
            metade1 = janela[:janela_tempo//2, :]
            metade2 = janela[janela_tempo//2:, :]
            tendencia = (np.sum(metade2 == 1) / (metade2.size)) - (np.sum(metade1 == 1) / (metade1.size))
            features_linha.append(tendencia)
            
            # 4. Tendência na coluna específica
            metade1_coluna = janela[:janela_tempo//2, j]
            metade2_coluna = janela[janela_tempo//2:, j]
            tendencia_coluna = (np.sum(metade2_coluna == 1) / len(metade2_coluna)) - (np.sum(metade1_coluna == 1) / len(metade1_coluna))
            features_linha.append(tendencia_coluna)
            
            # 5. Detecção de diagonais (principal)
            diagonais_principais = 0
            for k in range(janela_tempo - 2):
                for l in range(num_colunas - 2):
                    if (janela[k, l] == 1 and janela[k+1, l+1] == 1 and janela[k+2, l+2] == 1):
                        diagonais_principais += 1
            features_linha.append(diagonais_principais / (janela_tempo * num_colunas))
            
            # 6. Detecção de diagonais (secundária)
            diagonais_secundarias = 0
            for k in range(janela_tempo - 2):
                for l in range(2, num_colunas):
                    if (janela[k, l] == 1 and janela[k+1, l-1] == 1 and janela[k+2, l-2] == 1):
                        diagonais_secundarias += 1
            features_linha.append(diagonais_secundarias / (janela_tempo * num_colunas))
            
            # 7. Detecção de retângulos
            retangulos = 0
            for k in range(janela_tempo - 1):
                for l in range(num_colunas - 1):
                    if (janela[k, l] == 1 and janela[k+1, l] == 1 and 
                        janela[k, l+1] == 1 and janela[k+1, l+1] == 1):
                        retangulos += 1
            features_linha.append(retangulos / (janela_tempo * num_colunas))
            
            # 8. Alternância (mudanças de verde para vermelho e vice-versa)
            alternancia_coluna = 0
            for k in range(1, janela_tempo):
                if janela[k, j] != janela[k-1, j]:
                    alternancia_coluna += 1
            features_linha.append(alternancia_coluna / janela_tempo)
            
            # 9. Últimos 3 resultados na coluna
            for k in range(1, 4):
                if i+janela_tempo-k >= 0:
                    features_linha.append(janela[janela_tempo-k, j])
                else:
                    features_linha.append(0)
            
            # 10. Média móvel de 5 períodos
            if janela_tempo >= 5:
                media_movel = np.mean(janela[janela_tempo-5:, j])
                features_linha.append(media_movel)
            else:
                features_linha.append(0)
            
            # 11. Desvio padrão dos últimos 10 períodos
            if janela_tempo >= 10:
                desvio_padrao = np.std(janela[janela_tempo-10:, j])
                features_linha.append(desvio_padrao)
            else:
                features_linha.append(0)
            
            # 12. Ciclos (periodicidade)
            # Verificar se há um padrão de repetição a cada 6 horas
            ciclo_6h = 0
            if janela_tempo >= 12:
                for k in range(6, janela_tempo):
                    if janela[k, j] == janela[k-6, j]:
                        ciclo_6h += 1
                ciclo_6h = ciclo_6h / (janela_tempo - 6)
            features_linha.append(ciclo_6h)
            
            # 13. Ciclos (periodicidade) - 12 horas
            ciclo_12h = 0
            if janela_tempo >= 24:
                for k in range(12, janela_tempo):
                    if janela[k, j] == janela[k-12, j]:
                        ciclo_12h += 1
                ciclo_12h = ciclo_12h / (janela_tempo - 12)
            features_linha.append(ciclo_12h)
            
            # 14. Probabilidade baseada em Poisson
            # Contar ocorrências de verde nas últimas 24 horas
            if janela_tempo >= 24:
                ocorrencias = np.sum(janela[janela_tempo-24:, j] == 1)
                # Taxa média de ocorrência por hora
                taxa_media = ocorrencias / 24
                # Probabilidade de pelo menos 1 ocorrência na próxima hora
                prob_poisson = 1 - poisson.pmf(0, taxa_media)
                features_linha.append(prob_poisson)
            else:
                features_linha.append(0)
            
            # Adicionar features e label
            features.append(features_linha)
            # O label é o próximo valor na mesma coluna
            if i + janela_tempo < num_linhas:
                labels.append(matriz[i + janela_tempo, j])
            else:
                # Se não houver próximo valor, usar o último conhecido
                labels.append(matriz[i + janela_tempo - 1, j])
    
    return np.array(features), np.array(labels)

# Extrair features e labels com janela de 24 horas (1 dia)
print("Extraindo features baseadas em padrões geométricos...")
X, y = extrair_features_padroes(matriz_dados, janela_tempo=24)
print(f"Features extraídas: {X.shape}, Labels: {y.shape}")

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinar modelos
print("\nTreinando modelos de previsão...")

# 1. Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
rf_pred = rf_model.predict(X_test_scaled)
rf_prob = rf_model.predict_proba(X_test_scaled)[:, 1]

# 2. Rede Neural
nn_model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
nn_model.fit(X_train_scaled, y_train)
nn_pred = nn_model.predict(X_test_scaled)
nn_prob = nn_model.predict_proba(X_test_scaled)[:, 1]

# Avaliar modelos
print("\nAvaliação dos modelos:")
print("\nRandom Forest:")
print(f"Acurácia: {accuracy_score(y_test, rf_pred):.4f}")
# Corrigido: usar average='macro' para classificação multiclasse
print(f"Precisão: {precision_score(y_test, rf_pred, average='macro'):.4f}")
print(f"Recall: {recall_score(y_test, rf_pred, average='macro'):.4f}")
print(f"F1-Score: {f1_score(y_test, rf_pred, average='macro'):.4f}")

print("\nRede Neural:")
print(f"Acurácia: {accuracy_score(y_test, nn_pred):.4f}")
print(f"Precisão: {precision_score(y_test, nn_pred, average='macro'):.4f}")
print(f"Recall: {recall_score(y_test, nn_pred, average='macro'):.4f}")
print(f"F1-Score: {f1_score(y_test, nn_pred, average='macro'):.4f}")

# Identificar features mais importantes (Random Forest)
feature_names = [
    'Proporção Verde Global', 'Proporção Verde Coluna', 'Tendência Global', 
    'Tendência Coluna', 'Diagonais Principais', 'Diagonais Secundárias', 
    'Retângulos', 'Alternância', 'Último Resultado', 'Penúltimo Resultado', 
    'Antepenúltimo Resultado', 'Média Móvel 5h', 'Desvio Padrão 10h', 
    'Ciclo 6h', 'Ciclo 12h', 'Probabilidade Poisson'
]

importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 8))
plt.title('Importância das Features')
plt.bar(range(X.shape[1]), importances[indices], align='center')
plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
plt.tight_layout()
plt.savefig(f"{output_dir}/importancia_features.png", dpi=300, bbox_inches='tight')

# Função para prever próximos resultados
def prever_proximos_resultados(matriz, modelo, scaler, janela_tempo=24, horizonte=10):
    num_linhas, num_colunas = matriz.shape
    previsoes = np.zeros((horizonte, num_colunas))
    
    # Matriz de trabalho que será atualizada com previsões
    matriz_trabalho = matriz.copy()
    
    for h in range(horizonte):
        for j in range(num_colunas):
            # Extrair janela de tempo atual
            i = num_linhas - janela_tempo + h
            janela = matriz_trabalho[i:i+janela_tempo, :]
            
            # Extrair features (mesmo processo da função extrair_features_padroes)
            features_linha = []
            
            # 1. Proporção de verde/vermelho na janela
            proporcao_verde = np.sum(janela == 1) / (janela_tempo * num_colunas)
            features_linha.append(proporcao_verde)
            
            # 2. Proporção de verde/vermelho na coluna específica
            proporcao_verde_coluna = np.sum(janela[:, j] == 1) / janela_tempo
            features_linha.append(proporcao_verde_coluna)
            
            # 3. Tendência (aumento ou diminuição de verdes)
            metade1 = janela[:janela_tempo//2, :]
            metade2 = janela[janela_tempo//2:, :]
            tendencia = (np.sum(metade2 == 1) / (metade2.size)) - (np.sum(metade1 == 1) / (metade1.size))
            features_linha.append(tendencia)
            
            # 4. Tendência na coluna específica
            metade1_coluna = janela[:janela_tempo//2, j]
            metade2_coluna = janela[janela_tempo//2:, j]
            tendencia_coluna = (np.sum(metade2_coluna == 1) / len(metade2_coluna)) - (np.sum(metade1_coluna == 1) / len(metade1_coluna))
            features_linha.append(tendencia_coluna)
            
            # 5. Detecção de diagonais (principal)
            diagonais_principais = 0
            for k in range(janela_tempo - 2):
                for l in range(num_colunas - 2):
                    if (janela[k, l] == 1 and janela[k+1, l+1] == 1 and janela[k+2, l+2] == 1):
                        diagonais_principais += 1
            features_linha.append(diagonais_principais / (janela_tempo * num_colunas))
            
            # 6. Detecção de diagonais (secundária)
            diagonais_secundarias = 0
            for k in range(janela_tempo - 2):
                for l in range(2, num_colunas):
                    if (janela[k, l] == 1 and janela[k+1, l-1] == 1 and janela[k+2, l-2] == 1):
                        diagonais_secundarias += 1
            features_linha.append(diagonais_secundarias / (janela_tempo * num_colunas))
            
            # 7. Detecção de retângulos
            retangulos = 0
            for k in range(janela_tempo - 1):
                for l in range(num_colunas - 1):
                    if (janela[k, l] == 1 and janela[k+1, l] == 1 and 
                        janela[k, l+1] == 1 and janela[k+1, l+1] == 1):
                        retangulos += 1
            features_linha.append(retangulos / (janela_tempo * num_colunas))
            
            # 8. Alternância (mudanças de verde para vermelho e vice-versa)
            alternancia_coluna = 0
            for k in range(1, janela_tempo):
                if janela[k, j] != janela[k-1, j]:
                    alternancia_coluna += 1
            features_linha.append(alternancia_coluna / janela_tempo)
            
            # 9. Últimos 3 resultados na coluna
            for k in range(1, 4):
                if i+janela_tempo-k >= 0:
                    features_linha.append(janela[janela_tempo-k, j])
                else:
                    features_linha.append(0)
            
            # 10. Média móvel de 5 períodos
            if janela_tempo >= 5:
                media_movel = np.mean(janela[janela_tempo-5:, j])
                features_linha.append(media_movel)
            else:
                features_linha.append(0)
            
            # 11. Desvio padrão dos últimos 10 períodos
            if janela_tempo >= 10:
                desvio_padrao = np.std(janela[janela_tempo-10:, j])
                features_linha.append(desvio_padrao)
            else:
                features_linha.append(0)
            
            # 12. Ciclos (periodicidade) - 6 horas
            ciclo_6h = 0
            if janela_tempo >= 12:
                for k in range(6, janela_tempo):
                    if janela[k, j] == janela[k-6, j]:
                        ciclo_6h += 1
                ciclo_6h = ciclo_6h / (janela_tempo - 6)
            features_linha.append(ciclo_6h)
            
            # 13. Ciclos (periodicidade) - 12 horas
            ciclo_12h = 0
            if janela_tempo >= 24:
                for k in range(12, janela_tempo):
                    if janela[k, j] == janela[k-12, j]:
                        ciclo_12h += 1
                ciclo_12h = ciclo_12h / (janela_tempo - 12)
            features_linha.append(ciclo_12h)
            
            # 14. Probabilidade baseada em Poisson
            if janela_tempo >= 24:
                ocorrencias = np.sum(janela[janela_tempo-24:, j] == 1)
                taxa_media = ocorrencias / 24
                prob_poisson = 1 - poisson.pmf(0, taxa_media)
                features_linha.append(prob_poisson)
            else:
                features_linha.append(0)
            
            # Normalizar features
            features_scaled = scaler.transform([features_linha])
            
            # Fazer previsão
            previsao = modelo.predict(features_scaled)[0]
            previsoes[h, j] = previsao
            
            # Atualizar matriz de trabalho com a previsão
            if num_linhas + h < matriz_trabalho.shape[0]:
                matriz_trabalho[num_linhas + h, j] = previsao
            else:
                # Adicionar nova linha se necessário
                nova_linha = np.zeros((1, num_colunas))
                nova_linha[0, j] = previsao
                matriz_trabalho = np.vstack((matriz_trabalho, nova_linha))
    
    return previsoes

# Prever próximos resultados (curto prazo - 10 horas)
print("\nRealizando previsões de curto prazo (próximas 10 horas)...")
previsoes_curto_prazo_rf = prever_proximos_resultados(matriz_dados, rf_model, scaler, janela_tempo=24, horizonte=10)
previsoes_curto_prazo_nn = prever_proximos_resultados(matriz_dados, nn_model, scaler, janela_tempo=24, horizonte=10)

# Prever resultados de médio prazo (próximas 24 horas)
print("Realizando previsões de médio prazo (próximas 24 horas)...")
previsoes_medio_prazo_rf = prever_proximos_resultados(matriz_dados, rf_model, scaler, janela_tempo=24, horizonte=24)
previsoes_medio_prazo_nn = prever_proximos_resultados(matriz_dados, nn_model, scaler, janela_tempo=24, horizonte=24)

# Prever resultados de longo prazo (próximas 48 horas)
print("Realizando previsões de longo prazo (próximas 48 horas)...")
previsoes_longo_prazo_rf = prever_proximos_resultados(matriz_dados, rf_model, scaler, janela_tempo=24, horizonte=48)
previsoes_longo_prazo_nn = prever_proximos_resultados(matriz_dados, nn_model, scaler, janela_tempo=24, horizonte=48)

# Função para identificar pontos de reversão
def identificar_pontos_reversao(previsoes, limiar=0.5):
    num_horas, num_colunas = previsoes.shape
    pontos_reversao = []
    
    for j in range(num_colunas):
        for i in range(1, num_horas):
            # Verificar se houve mudança de vermelho para verde ou vice-versa
            if (previsoes[i-1, j] < limiar and previsoes[i, j] >= limiar) or \
               (previsoes[i-1, j] >= limiar and previsoes[i, j] < limiar):
                pontos_reversao.append((i, j))
    
    return pontos_reversao

# Identificar pontos de reversão nas previsões de longo prazo
print("\nIdentificando pontos de reversão nas previsões...")
pontos_reversao_rf = identificar_pontos_reversao(previsoes_longo_prazo_rf)
pontos_reversao_nn = identificar_pontos_reversao(previsoes_longo_prazo_nn)

print(f"Pontos de reversão identificados (Random Forest): {len(pontos_reversao_rf)}")
print(f"Pontos de reversão identificados (Rede Neural): {len(pontos_reversao_nn)}")

# Visualizar previsões de curto prazo
plt.figure(figsize=(15, 10))
plt.subplot(2, 1, 1)
plt.imshow(previsoes_curto_prazo_rf, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Previsões de Curto Prazo (10h) - Random Forest')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')

plt.subplot(2, 1, 2)
plt.imshow(previsoes_curto_prazo_nn, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Previsões de Curto Prazo (10h) - Rede Neural')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')
plt.tight_layout()
plt.savefig(f"{output_dir}/previsoes_curto_prazo.png", dpi=300, bbox_inches='tight')

# Visualizar previsões de médio prazo
plt.figure(figsize=(15, 10))
plt.subplot(2, 1, 1)
plt.imshow(previsoes_medio_prazo_rf, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Previsões de Médio Prazo (24h) - Random Forest')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')

plt.subplot(2, 1, 2)
plt.imshow(previsoes_medio_prazo_nn, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Previsões de Médio Prazo (24h) - Rede Neural')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')
plt.tight_layout()
plt.savefig(f"{output_dir}/previsoes_medio_prazo.png", dpi=300, bbox_inches='tight')

# Visualizar previsões de longo prazo com pontos de reversão
plt.figure(figsize=(15, 20))
plt.subplot(2, 1, 1)
plt.imshow(previsoes_longo_prazo_rf, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Previsões de Longo Prazo (48h) - Random Forest')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')

# Marcar pontos de reversão
for ponto in pontos_reversao_rf:
    hora, campeonato = ponto
    plt.scatter(campeonato, hora, c='blue', s=50, marker='x')

plt.subplot(2, 1, 2)
plt.imshow(previsoes_longo_prazo_nn, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Previsões de Longo Prazo (48h) - Rede Neural')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')

# Marcar pontos de reversão
for ponto in pontos_reversao_nn:
    hora, campeonato = ponto
    plt.scatter(campeonato, hora, c='blue', s=50, marker='x')

plt.tight_layout()
plt.savefig(f"{output_dir}/previsoes_longo_prazo.png", dpi=300, bbox_inches='tight')

# Análise de confiabilidade dos padrões geométricos
print("\nAnalisando confiabilidade dos padrões geométricos...")

# Função para calcular a confiabilidade de cada tipo de padrão
def analisar_confiabilidade_padroes(matriz, janela_tempo=24):
    num_linhas, num_colunas = matriz.shape
    
    # Dicionário para armazenar estatísticas de cada padrão
    estatisticas = {
        'diagonais_principais': {'acertos': 0, 'total': 0},
        'diagonais_secundarias': {'acertos': 0, 'total': 0},
        'retangulos': {'acertos': 0, 'total': 0},
        'triangulos': {'acertos': 0, 'total': 0}
    }
    
    # Para cada posição na matriz (exceto as últimas linhas)
    for i in range(num_linhas - janela_tempo - 1):
        for j in range(num_colunas):
            # Extrair janela de tempo
            janela = matriz[i:i+janela_tempo, :]
            
            # Verificar diagonais principais
            for k in range(janela_tempo - 2):
                for l in range(num_colunas - 2):
                    if j == l + 2 and (janela[k, l] == 1 and janela[k+1, l+1] == 1 and janela[k+2, l+2] == 1):
                        estatisticas['diagonais_principais']['total'] += 1
                        # Verificar se o próximo valor após a diagonal foi verde
                        if i + janela_tempo < num_linhas and matriz[i + janela_tempo, j] == 1:
                            estatisticas['diagonais_principais']['acertos'] += 1
            
            # Verificar diagonais secundárias
            for k in range(janela_tempo - 2):
                for l in range(2, num_colunas):
                    if j == l - 2 and (janela[k, l] == 1 and janela[k+1, l-1] == 1 and janela[k+2, l-2] == 1):
                        estatisticas['diagonais_secundarias']['total'] += 1
                        # Verificar se o próximo valor após a diagonal foi verde
                        if i + janela_tempo < num_linhas and matriz[i + janela_tempo, j] == 1:
                            estatisticas['diagonais_secundarias']['acertos'] += 1
            
            # Verificar retângulos
            for k in range(janela_tempo - 1):
                for l in range(num_colunas - 1):
                    if (j == l or j == l + 1) and (janela[k, l] == 1 and janela[k+1, l] == 1 and 
                        janela[k, l+1] == 1 and janela[k+1, l+1] == 1):
                        estatisticas['retangulos']['total'] += 1
                        # Verificar se o próximo valor após o retângulo foi verde
                        if i + janela_tempo < num_linhas and matriz[i + janela_tempo, j] == 1:
                            estatisticas['retangulos']['acertos'] += 1
            
            # Verificar triângulos (simplificação: 3 células em formato L)
            for k in range(janela_tempo - 1):
                for l in range(num_colunas - 1):
                    if (j == l or j == l + 1) and (janela[k, l] == 1 and janela[k+1, l] == 1 and janela[k, l+1] == 1):
                        estatisticas['triangulos']['total'] += 1
                        # Verificar se o próximo valor após o triângulo foi verde
                        if i + janela_tempo < num_linhas and matriz[i + janela_tempo, j] == 1:
                            estatisticas['triangulos']['acertos'] += 1
    
    # Calcular taxas de acerto
    resultados = {}
    for padrao, stats in estatisticas.items():
        if stats['total'] > 0:
            taxa_acerto = stats['acertos'] / stats['total']
        else:
            taxa_acerto = 0
        resultados[padrao] = {
            'taxa_acerto': taxa_acerto,
            'total': stats['total'],
            'acertos': stats['acertos']
        }
    
    return resultados

# Analisar confiabilidade dos padrões
confiabilidade_padroes = analisar_confiabilidade_padroes(matriz_dados)

# Visualizar confiabilidade dos padrões
plt.figure(figsize=(10, 6))
padroes = list(confiabilidade_padroes.keys())
taxas_acerto = [confiabilidade_padroes[p]['taxa_acerto'] for p in padroes]
totais = [confiabilidade_padroes[p]['total'] for p in padroes]

# Criar gráfico de barras com cores baseadas na taxa de acerto
cores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
plt.bar(padroes, taxas_acerto, color=cores)
plt.xlabel('Tipo de Padrão Geométrico')
plt.ylabel('Taxa de Acerto')
plt.title('Confiabilidade dos Padrões Geométricos')
plt.ylim(0, 1)

# Adicionar valores nas barras
for i, v in enumerate(taxas_acerto):
    plt.text(i, v + 0.02, f'{v:.2f}\n({totais[i]} ocorrências)', ha='center')

plt.tight_layout()
plt.savefig(f"{output_dir}/confiabilidade_padroes.png", dpi=300, bbox_inches='tight')

# Salvar resultados em arquivo de texto
with open(f"{output_dir}/resultados_analise.txt", 'w') as f:
    f.write("ANÁLISE DE PADRÕES GEOMÉTRICOS E PREVISÕES PARA BTTS\n")
    f.write("=================================================\n\n")
    
    f.write("1. AVALIAÇÃO DOS MODELOS\n")
    f.write("------------------------\n")
    f.write("Random Forest:\n")
    f.write(f"Acurácia: {accuracy_score(y_test, rf_pred):.4f}\n")
    f.write(f"Precisão: {precision_score(y_test, rf_pred, average='macro'):.4f}\n")
    f.write(f"Recall: {recall_score(y_test, rf_pred, average='macro'):.4f}\n")
    f.write(f"F1-Score: {f1_score(y_test, rf_pred, average='macro'):.4f}\n\n")
    
    f.write("Rede Neural:\n")
    f.write(f"Acurácia: {accuracy_score(y_test, nn_pred):.4f}\n")
    f.write(f"Precisão: {precision_score(y_test, nn_pred, average='macro'):.4f}\n")
    f.write(f"Recall: {recall_score(y_test, nn_pred, average='macro'):.4f}\n")
    f.write(f"F1-Score: {f1_score(y_test, nn_pred, average='macro'):.4f}\n\n")
    
    f.write("2. FEATURES MAIS IMPORTANTES\n")
    f.write("---------------------------\n")
    for i in range(len(feature_names)):
        f.write(f"{i+1}. {feature_names[indices[i]]}: {importances[indices[i]]:.4f}\n")
    f.write("\n")
    
    f.write("3. CONFIABILIDADE DOS PADRÕES GEOMÉTRICOS\n")
    f.write("----------------------------------------\n")
    for padrao, stats in confiabilidade_padroes.items():
        f.write(f"{padrao.replace('_', ' ').title()}:\n")
        f.write(f"  Taxa de acerto: {stats['taxa_acerto']:.4f}\n")
        f.write(f"  Total de ocorrências: {stats['total']}\n")
        f.write(f"  Número de acertos: {stats['acertos']}\n\n")
    
    f.write("4. PONTOS DE REVERSÃO\n")
    f.write("-------------------\n")
    f.write("Random Forest:\n")
    for i, ponto in enumerate(pontos_reversao_rf):
        hora, campeonato = ponto
        f.write(f"  Ponto {i+1}: Hora futura {hora}, Campeonato {campeonato}\n")
    f.write(f"  Total de pontos de reversão: {len(pontos_reversao_rf)}\n\n")
    
    f.write("Rede Neural:\n")
    for i, ponto in enumerate(pontos_reversao_nn):
        hora, campeonato = ponto
        f.write(f"  Ponto {i+1}: Hora futura {hora}, Campeonato {campeonato}\n")
    f.write(f"  Total de pontos de reversão: {len(pontos_reversao_nn)}\n\n")
    
    f.write("5. RECOMENDAÇÕES PARA APOSTAS\n")
    f.write("----------------------------\n")
    f.write("Com base na análise dos padrões geométricos e nas previsões dos modelos, recomendamos:\n\n")
    
    # Identificar os campeonatos mais confiáveis para BTTS
    campeonatos_confiaveis = []
    for j in range(matriz_dados.shape[1]):
        taxa_verde = np.sum(matriz_dados[:, j] == 1) / matriz_dados.shape[0]
        campeonatos_confiaveis.append((j, taxa_verde))
    
    # Ordenar por taxa de ocorrência de BTTS
    campeonatos_confiaveis.sort(key=lambda x: x[1], reverse=True)
    
    f.write("Campeonatos mais confiáveis para BTTS (histórico):\n")
    for i, (campeonato, taxa) in enumerate(campeonatos_confiaveis[:5]):
        f.write(f"  {i+1}. Campeonato {campeonato}: {taxa:.4f} (taxa de ocorrência)\n")
    f.write("\n")
    
    # Identificar horários mais confiáveis para BTTS
    horarios_confiaveis = []
    for i in range(24):  # 24 horas do dia
        # Filtrar linhas correspondentes a este horário
        indices_hora = [j for j in range(matriz_dados.shape[0]) if j % 24 == i]
        if indices_hora:
            dados_hora = matriz_dados[indices_hora, :]
            taxa_verde = np.sum(dados_hora == 1) / dados_hora.size
            horarios_confiaveis.append((i, taxa_verde))
    
    # Ordenar por taxa de ocorrência de BTTS
    horarios_confiaveis.sort(key=lambda x: x[1], reverse=True)
    
    f.write("Horários mais confiáveis para BTTS (histórico):\n")
    for i, (hora, taxa) in enumerate(horarios_confiaveis[:5]):
        f.write(f"  {i+1}. Hora {hora}: {taxa:.4f} (taxa de ocorrência)\n")
    f.write("\n")
    
    # Identificar as melhores oportunidades nas próximas horas
    f.write("Melhores oportunidades para BTTS nas próximas 10 horas (Random Forest):\n")
    melhores_oportunidades = []
    for i in range(previsoes_curto_prazo_rf.shape[0]):
        for j in range(previsoes_curto_prazo_rf.shape[1]):
            melhores_oportunidades.append((i, j, previsoes_curto_prazo_rf[i, j]))
    
    # Ordenar por probabilidade
    melhores_oportunidades.sort(key=lambda x: x[2], reverse=True)
    
    for i, (hora, campeonato, prob) in enumerate(melhores_oportunidades[:10]):
        f.write(f"  {i+1}. Hora futura {hora}, Campeonato {campeonato}: {prob:.4f} (probabilidade)\n")
    f.write("\n")
    
    # Identificar padrões mais confiáveis
    padroes_ordenados = sorted(confiabilidade_padroes.items(), key=lambda x: x[1]['taxa_acerto'], reverse=True)
    
    f.write("Padrões geométricos mais confiáveis para previsão:\n")
    for i, (padrao, stats) in enumerate(padroes_ordenados):
        if stats['total'] >= 10:  # Considerar apenas padrões com pelo menos 10 ocorrências
            f.write(f"  {i+1}. {padrao.replace('_', ' ').title()}: {stats['taxa_acerto']:.4f} (taxa de acerto)\n")
    
    f.write("\n")
    f.write("NOTA: As previsões e recomendações são baseadas em análise estatística e identificação de padrões geométricos nos dados históricos. Os resultados reais podem variar devido à natureza aleatória dos eventos esportivos.")

print("\nAnálise e previsões concluídas. Resultados salvos em:", output_dir)
