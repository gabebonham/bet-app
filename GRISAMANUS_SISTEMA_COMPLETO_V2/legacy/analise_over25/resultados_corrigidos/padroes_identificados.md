# Análise de Padrões de Sucesso e Falha - Over 2.5

## Resumo Geral

Após analisar as 131 previsões do modelo Over 2.5 com os resultados reais, identificamos uma taxa de acerto geral de **80,15%**, o que é considerado excelente para este mercado. Das 131 previsões, 105 foram acertos e 26 foram erros.

## Padrões de Sucesso

### 1. Campeonatos com Melhor Desempenho

- **PREMIER**: Taxa de acerto de **95,00%** (38/40)
  - Hora 12: 100% de acerto (15/15)
  - Hora 13: 93% de acerto (13/14)
  - Hora 14: 90% de acerto (10/11)

- **EURO**: Taxa de acerto de **81,82%** (18/22)
  - Hora 12: 86% de acerto (6/7)
  - Hora 14: 88% de acerto (7/8)

### 2. Faixas de Probabilidade Mais Eficientes

- **Probabilidade 0.65-0.70**: Taxa de acerto de **88,89%** (32/36)
- **Probabilidade 0.60-0.65**: Taxa de acerto de **83,33%** (35/42)

Estas faixas de probabilidade tiveram desempenho significativamente superior ao esperado, com diferenças de +21,39% e +20,83% respectivamente em relação à probabilidade média da faixa.

### 3. Nível de Confiança com Melhor Desempenho

- **MÉDIA**: Taxa de acerto de **84,78%** (39/46)

Curiosamente, o nível de confiança MÉDIA superou o nível ALTA, indicando que o modelo está subestimando as previsões de média confiança.

### 4. Combinações Específicas de Alto Desempenho

- **PREMIER na Hora 12**: 100% de acerto (15/15)
- **PREMIER na Hora 14**: 90% de acerto (10/11)
- **EURO na Hora 14**: 88% de acerto (7/8)

### 5. Acertos Diretos (Sem Gale)

- 76,19% dos acertos (80/105) foram diretos, sem necessidade de gale
- Previsões de ALTA confiança: 100% de acertos diretos (2/2)
- Previsões de BAIXA confiança com acerto direto: 41,46% (34/82)

## Padrões de Falha

### 1. Campeonatos com Pior Desempenho

- **COPA**: Taxa de acerto de **70,37%** (19/27)
  - Hora 12: 55% de acerto (6/11)

- **SUPER**: Taxa de acerto de **71,43%** (30/42)
  - Hora 13: 60% de acerto (9/15)

### 2. Faixas de Probabilidade Problemáticas

- **Probabilidade 0.75-0.80**: Taxa de acerto de **66,67%** (2/3)
  - Desempenho 10,83% abaixo da probabilidade média da faixa

### 3. Nível de Confiança com Pior Desempenho

- **ALTA**: Taxa de acerto de **66,67%** (2/3)

Embora a amostra seja pequena (apenas 3 previsões), é preocupante que o nível de confiança mais alto tenha o pior desempenho.

### 4. Combinações Específicas Problemáticas

- **SUPER na Hora 13**: 60% de acerto (9/15)
- **COPA na Hora 12**: 55% de acerto (6/11)

### 5. Necessidade de Gales por Faixa de Probabilidade

- **Probabilidade 0.70-0.75**: 83,33% dos acertos precisaram de gale
  - Apenas 16,67% foram acertos diretos

## Pontos Fora da Curva

### 1. Previsões de ALTA Confiança que Falharam

- SUPER 4, Hora 12 (Probabilidade: 0.78)

### 2. Desempenho por Campeonato em Relação à Média

- PREMIER: +14,85% acima da média geral
- COPA: -9,78% abaixo da média geral
- SUPER: -8,72% abaixo da média geral

### 3. Faixas de Probabilidade com Desempenho Muito Diferente do Esperado

- Probabilidade 0.55-0.60: +13,09% acima do esperado
- Probabilidade 0.60-0.65: +20,83% acima do esperado
- Probabilidade 0.65-0.70: +21,39% acima do esperado
- Probabilidade 0.75-0.80: -10,83% abaixo do esperado

## Calibrações Recomendadas

### 1. Níveis de Confiança

**Níveis atuais:**
- ALTA: probabilidade > 0.75
- MÉDIA: probabilidade entre 0.65 e 0.74
- BAIXA: probabilidade entre 0.55 e 0.64

**Níveis propostos:**
- ALTA: probabilidade > 0.73
- MÉDIA: probabilidade entre 0.64 e 0.72
- BAIXA: probabilidade entre 0.55 e 0.63

### 2. Pesos por Campeonato

**Pesos atuais:**
- PREMIER: +0.03
- SUPER: +0.02
- COPA: +0.01
- EURO: -0.01

**Pesos propostos:**
- PREMIER: +0.30
- EURO: +0.03
- SUPER: -0.17
- COPA: -0.20

### 3. Pesos por Ciclo de 6 Horas

**Pesos atuais:**
- 00-05h: -0.02
- 06-11h: 0.00
- 12-17h: +0.04
- 18-23h: +0.02

**Pesos propostos:**
- 12-17h: +0.00 (Taxa média: 80,38%)

### 4. Estratégia de Martingale

**Estratégia proposta:**
- ALTA: Até 1 gale
- MÉDIA: Até 2 gales
- BAIXA: Até 3 gales

### 5. Valores de Stake

**Valores atuais:**
- ALTA: R$20.00
- MÉDIA: R$10.00
- BAIXA: R$5.00

**Valores propostos:**
- ALTA: R$25.00
- MÉDIA: R$15.00
- BAIXA: R$5.00

## Conclusões e Recomendações

1. O modelo Over 2.5 demonstrou excelente desempenho geral (80,15% de acerto), superando significativamente a taxa média de ocorrência do mercado (42,6%).

2. O campeonato PREMIER deve receber maior peso no modelo, enquanto COPA e SUPER devem ter seus pesos reduzidos.

3. As faixas de probabilidade intermediárias (0.60-0.70) tiveram desempenho excepcional e devem ser priorizadas.

4. Os níveis de confiança precisam ser recalibrados, com redução do limiar para ALTA confiança.

5. A estratégia de Martingale deve ser ajustada conforme o nível de confiança, com mais gales permitidos para previsões de BAIXA confiança.

6. Os valores de stake devem ser aumentados para os níveis ALTA e MÉDIA, mantendo o valor atual para BAIXA.

7. Recomenda-se focar as operações no campeonato PREMIER, especialmente na hora 12, que teve 100% de acerto.

8. Evitar operações em COPA na hora 12 e SUPER na hora 13, que tiveram os piores desempenhos.

Estas calibrações e recomendações devem ser implementadas antes de desenvolver o modelo para o mercado Over 3.5, garantindo que as lições aprendidas com o Over 2.5 sejam aplicadas ao novo modelo.
