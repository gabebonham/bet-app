# Documentação do Modelo Over 3.5 - Sistema GRISAMANUS

## Visão Geral

O modelo Over 3.5 foi desenvolvido como parte do sistema GRISAMANUS, complementando os modelos já existentes para os mercados BTTS e Over 2.5. Este modelo foi calibrado com base na análise de dados reais de 240 horas para os 4 campeonatos (PREMIER, EURO, COPA e SUPER), seguindo a mesma metodologia rigorosa aplicada aos outros mercados.

## Características do Mercado Over 3.5

O mercado Over 3.5 apresenta características distintas em comparação com os outros mercados:

- **Taxa média de ocorrência**: 24% (significativamente menor que BTTS: 53% e Over 2.5: 42.6%)
- **Distribuição por campeonato**:
  - PREMIER: 28% (maior taxa entre os campeonatos)
  - EURO: 22%
  - COPA: 23%
  - SUPER: 20% (menor taxa entre os campeonatos)
- **Distribuição por ciclo horário**:
  - Ciclo 12h-17h: 33% (período mais favorável)
  - Ciclo 18h-23h: 26%
  - Ciclo 06h-11h: 20%
  - Ciclo 00h-05h: 16% (período menos favorável)

## Padrões Identificados

A análise dos dados revelou padrões específicos para o mercado Over 3.5:

1. **Combinações de alta ocorrência**:
   - PREMIER nas horas 13-14: 50% de ocorrência
   - PREMIER nas horas 16-17: 45% de ocorrência
   - PREMIER na hora 21: 45% de ocorrência
   - EURO nas horas 8 e 22: 40% de ocorrência

2. **Padrões geométricos**:
   - PREMIER: colunas múltiplas de 3 apresentam maior probabilidade
   - EURO: colunas múltiplas de 5 apresentam maior probabilidade
   - SUPER: colunas múltiplas de 4 apresentam maior probabilidade
   - COPA: colunas múltiplas de 7 apresentam maior probabilidade

3. **Correlação com outros mercados**:
   - O Over 3.5 mantém a mesma tendência de ciclos que o BTTS e Over 2.5, com o ciclo 12h-17h sendo o mais favorável para todos os mercados
   - A diferença de taxa entre os mercados é mais acentuada no ciclo 00h-05h

## Calibrações do Modelo

O modelo foi calibrado com os seguintes parâmetros:

### Níveis de Confiança
- ALTA: probabilidade > 0.70
- MÉDIA: probabilidade entre 0.60 e 0.69
- BAIXA: probabilidade entre 0.50 e 0.59

### Pesos por Campeonato
- PREMIER: +0.35
- EURO: +0.25
- COPA: +0.10
- SUPER: +0.00 (base)

### Pesos por Ciclo
- 12h-17h: +0.30
- 18h-23h: +0.15
- 06h-11h: +0.05
- 00h-05h: +0.00 (base)

### Valores de Stake
- ALTA: R$25.00
- MÉDIA: R$15.00
- BAIXA: R$5.00

### Estratégia de Martingale
- ALTA: até 1 gale
- MÉDIA: até 2 gales
- BAIXA: até 3 gales

## Implementação

O modelo foi implementado na classe `ModeloOver35Calibrado` no arquivo `modelo_over35_calibrado.py`. Esta classe contém métodos para:

1. Calcular a probabilidade de ocorrência do Over 3.5 para cada combinação de campeonato, coluna e hora
2. Determinar o nível de confiança com base na probabilidade calculada
3. Gerar previsões para as próximas horas, limitando a 3 entradas por hora
4. Salvar as previsões em formato CSV e PDF
5. Visualizar a distribuição das previsões por nível de confiança, campeonato e hora

## Integração com o Sistema GRISAMANUS

O modelo Over 3.5 foi integrado ao sistema GRISAMANUS, que já incluía os modelos para BTTS e Over 2.5. A integração seguiu os seguintes princípios:

1. **Consistência metodológica**: O modelo Over 3.5 segue a mesma metodologia rigorosa aplicada aos outros mercados
2. **Padronização de saída**: As previsões são geradas no mesmo formato que os outros mercados, facilitando a operação
3. **Limitação de entradas**: Exatamente 3 entradas por hora, conforme definido para todos os mercados
4. **Calibração específica**: Parâmetros ajustados para refletir as características específicas do mercado Over 3.5

## Recomendações Operacionais

Com base na análise dos dados e nas características do modelo, recomendamos:

1. **Foco no ciclo 12h-17h**: Este ciclo apresenta a maior taxa de ocorrência (33%)
2. **Priorização do PREMIER**: Este campeonato apresenta a maior taxa de ocorrência (28%)
3. **Atenção especial às combinações de alta ocorrência**: PREMIER nas horas 13-14 (50%)
4. **Estratégia de stake conservadora**: Devido à menor taxa de ocorrência geral do Over 3.5, recomenda-se uma abordagem mais conservadora na gestão de banca

## Conclusão

O modelo Over 3.5 complementa o sistema GRISAMANUS, oferecendo mais uma opção de mercado para operação. Apesar de ter uma taxa de ocorrência significativamente menor que os outros mercados, o Over 3.5 apresenta padrões claros que podem ser explorados para obter resultados positivos, especialmente quando se foca nas combinações de campeonato e hora com maior probabilidade de sucesso.
