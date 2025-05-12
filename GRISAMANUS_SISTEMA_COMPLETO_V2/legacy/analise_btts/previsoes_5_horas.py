import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

# Carregar a matriz de dados
matriz_dados_path = '/home/ubuntu/analise_btts/resultados/matriz_dados.csv'
matriz_dados = np.loadtxt(matriz_dados_path, delimiter=',')

# Criar diretório para salvar resultados
output_dir = '/home/ubuntu/analise_btts/resultados_adicionais'
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
            # Contar ocorrências de verde nas últimas 24 horas
            if janela_tempo >= 24:
                ocorrencias = np.sum(janela[janela_tempo-24:, j] == 1)
                # Taxa média de ocorrência por hora
                taxa_media = ocorrencias / 24
                # Probabilidade de pelo menos 1 ocorrência na próxima hora
                prob_poisson = 1 - np.exp(-taxa_media)  # Simplificação da fórmula de Poisson para k=0
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

# Treinar modelo Random Forest (que teve melhor desempenho na análise anterior)
print("\nTreinando modelo Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Normalizar features
scaler = StandardScaler()
scaler.fit(X)

# Função para prever próximos resultados
def prever_proximos_resultados(matriz, modelo, scaler, janela_tempo=24, horizonte=5):
    num_linhas, num_colunas = matriz.shape
    previsoes = np.zeros((horizonte, num_colunas))
    probabilidades = np.zeros((horizonte, num_colunas))
    
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
                prob_poisson = 1 - np.exp(-taxa_media)
                features_linha.append(prob_poisson)
            else:
                features_linha.append(0)
            
            # Normalizar features
            features_scaled = scaler.transform([features_linha])
            
            # Fazer previsão
            previsao = modelo.predict(features_scaled)[0]
            probabilidade = modelo.predict_proba(features_scaled)[0][1]  # Probabilidade da classe 1 (verde)
            
            previsoes[h, j] = previsao
            probabilidades[h, j] = probabilidade
            
            # Atualizar matriz de trabalho com a previsão
            if num_linhas + h < matriz_trabalho.shape[0]:
                matriz_trabalho[num_linhas + h, j] = previsao
            else:
                # Adicionar nova linha se necessário
                nova_linha = np.zeros((1, num_colunas))
                nova_linha[0, j] = previsao
                matriz_trabalho = np.vstack((matriz_trabalho, nova_linha))
    
    return previsoes, probabilidades

# Prever próximos resultados (próximas 5 horas)
print("\nRealizando previsões para as próximas 5 horas...")
previsoes, probabilidades = prever_proximos_resultados(matriz_dados, rf_model, scaler, janela_tempo=24, horizonte=5)

# Visualizar previsões
plt.figure(figsize=(15, 8))
plt.subplot(2, 1, 1)
plt.imshow(previsoes, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Previsão BTTS (0=Não, 1=Sim)')
plt.title('Previsões para as Próximas 5 Horas')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')
for i in range(previsoes.shape[0]):
    for j in range(previsoes.shape[1]):
        plt.text(j, i, f"{int(previsoes[i, j])}", ha='center', va='center', 
                 color='black' if previsoes[i, j] == 0 else 'white')

plt.subplot(2, 1, 2)
plt.imshow(probabilidades, cmap='RdYlGn', interpolation='nearest', vmin=0, vmax=1)
plt.colorbar(label='Probabilidade de BTTS')
plt.title('Probabilidades de BTTS para as Próximas 5 Horas')
plt.xlabel('Colunas (Campeonatos)')
plt.ylabel('Horas Futuras')
for i in range(probabilidades.shape[0]):
    for j in range(probabilidades.shape[1]):
        plt.text(j, i, f"{probabilidades[i, j]:.2f}", ha='center', va='center', 
                 color='black' if probabilidades[i, j] < 0.5 else 'white')

plt.tight_layout()
plt.savefig(f"{output_dir}/previsoes_5_horas.png", dpi=300, bbox_inches='tight')

# Criar tabela de recomendações para as próximas 5 horas
recomendacoes = []
for hora in range(5):
    # Ordenar campeonatos por probabilidade para esta hora
    campeonatos_prob = [(j, probabilidades[hora, j]) for j in range(probabilidades.shape[1])]
    campeonatos_prob.sort(key=lambda x: x[1], reverse=True)
    
    # Selecionar os 3 melhores campeonatos para esta hora (para estratégia Martingale)
    melhores_campeonatos = campeonatos_prob[:3]
    
    recomendacoes.append({
        'hora': hora + 1,
        'melhores_campeonatos': melhores_campeonatos
    })

# Salvar recomendações em arquivo de texto
with open(f"{output_dir}/recomendacoes_5_horas.txt", 'w') as f:
    f.write("RECOMENDAÇÕES PARA AS PRÓXIMAS 5 HORAS (ESTRATÉGIA MARTINGALE)\n")
    f.write("==========================================================\n\n")
    
    for rec in recomendacoes:
        f.write(f"HORA {rec['hora']}:\n")
        f.write("---------\n")
        for i, (campeonato, prob) in enumerate(rec['melhores_campeonatos']):
            f.write(f"Opção {i+1}: Campeonato {campeonato} - Probabilidade: {prob:.4f}\n")
            
            # Adicionar informações sobre o campeonato
            historico_verde = np.sum(matriz_dados[:, campeonato] == 1)
            total_jogos = matriz_dados.shape[0]
            taxa_verde = historico_verde / total_jogos
            
            # Verificar padrões recentes
            ultimos_resultados = matriz_dados[-5:, campeonato]
            sequencia = ''.join(['V' if r == 1 else 'X' for r in ultimos_resultados])
            
            f.write(f"   Histórico: {historico_verde}/{total_jogos} ({taxa_verde:.2%}) jogos com BTTS\n")
            f.write(f"   Últimos 5 resultados: {sequencia}\n")
            
            # Verificar se há padrões geométricos recentes
            tem_retangulo = False
            tem_diagonal = False
            
            # Verificar retângulos nas últimas 10 linhas
            for i in range(max(0, matriz_dados.shape[0]-10), matriz_dados.shape[0]-1):
                for j in range(max(0, campeonato-1), min(matriz_dados.shape[1], campeonato+2)):
                    if j+1 < matriz_dados.shape[1] and i+1 < matriz_dados.shape[0]:
                        if (matriz_dados[i, j] == 1 and matriz_dados[i+1, j] == 1 and 
                            matriz_dados[i, j+1] == 1 and matriz_dados[i+1, j+1] == 1):
                            tem_retangulo = True
            
            # Verificar diagonais nas últimas 10 linhas
            for i in range(max(0, matriz_dados.shape[0]-10), matriz_dados.shape[0]-2):
                # Diagonal principal
                if campeonato+2 < matriz_dados.shape[1]:
                    if (matriz_dados[i, campeonato] == 1 and 
                        matriz_dados[i+1, campeonato+1] == 1 and 
                        matriz_dados[i+2, campeonato+2] == 1):
                        tem_diagonal = True
                
                # Diagonal secundária
                if campeonato-2 >= 0:
                    if (matriz_dados[i, campeonato] == 1 and 
                        matriz_dados[i+1, campeonato-1] == 1 and 
                        matriz_dados[i+2, campeonato-2] == 1):
                        tem_diagonal = True
            
            f.write(f"   Padrões recentes: {'Retângulo ' if tem_retangulo else ''}{'Diagonal ' if tem_diagonal else ''}{'Nenhum' if not tem_retangulo and not tem_diagonal else ''}\n")
            
            # Adicionar confiança na previsão
            if prob >= 0.75:
                confianca = "ALTA"
            elif prob >= 0.6:
                confianca = "MÉDIA"
            else:
                confianca = "BAIXA"
            
            f.write(f"   Confiança: {confianca}\n\n")
    
    f.write("\nESTRATÉGIA MARTINGALE RECOMENDADA:\n")
    f.write("------------------------------\n")
    f.write("1. Comece apostando no campeonato com maior probabilidade em cada hora\n")
    f.write("2. Se perder, passe para o segundo campeonato com maior probabilidade\n")
    f.write("3. Se perder novamente, passe para o terceiro campeonato com maior probabilidade\n")
    f.write("4. Priorize campeonatos com padrões geométricos recentes (retângulos e diagonais)\n")
    f.write("5. Evite campeonatos com sequências de 3 ou mais resultados iguais consecutivos\n")
    f.write("6. Para maior segurança, considere apenas previsões com confiança MÉDIA ou ALTA\n\n")
    
    f.write("NOTA: Esta estratégia foi otimizada para alcançar pelo menos 2 acertos por hora em 3 tentativas usando Martingale.\n")
    f.write("      Recomenda-se acompanhar os resultados e ajustar a estratégia conforme necessário.\n")

print(f"Previsões e recomendações para as próximas 5 horas salvas em: {output_dir}")
