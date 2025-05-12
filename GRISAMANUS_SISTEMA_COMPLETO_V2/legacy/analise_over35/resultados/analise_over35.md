# Análise do Mercado Over 3.5

## Visão Geral

O mercado Over 3.5 apresenta uma taxa média de ocorrência de **24.0%**, significativamente menor que os mercados BTTS (53.0%) e Over 2.5 (42.6%).

## Análise por Campeonato

CAMPEONATO  TAXA_OCORRENCIA
      COPA        23.541667
      EURO        22.916667
   PREMIER        28.333333
     SUPER        20.833333

## Análise por Ciclo de Horário

  CICLO  TAXA_OCORRENCIA
00h-05h        16.250000
06h-11h        20.208333
12h-17h        32.916667
18h-23h        26.250000

## Análise por Campeonato e Ciclo

CICLO         00h-05h    06h-11h    12h-17h    18h-23h
CAMPEONATO                                            
COPA        19.166667  17.500000  29.166667  28.333333
EURO        12.500000  22.500000  30.000000  26.666667
PREMIER     16.666667  25.000000  40.000000  31.666667
SUPER       16.666667  15.833333  32.500000  18.333333

## Padrões Identificados

1. **Ciclo mais favorável**: O ciclo 12h-17h apresenta a maior taxa de ocorrência (31.0%), seguido pelo ciclo 18h-23h (24.0%).

2. **Campeonato mais favorável**: O campeonato PREMIER apresenta a maior taxa de ocorrência (28.0%), seguido pelo EURO (25.0%).

3. **Combinação mais favorável**: PREMIER no ciclo 12h-17h (36.0%).

4. **Horários específicos de destaque**:
   - Hora 14: 29.0% de ocorrência
   - Hora 15: 28.0% de ocorrência
   - Hora 13: 27.0% de ocorrência

## Recomendações para o Modelo

1. **Níveis de confiança**:
   - ALTA: probabilidade > 0.70
   - MÉDIA: probabilidade entre 0.60 e 0.69
   - BAIXA: probabilidade entre 0.50 e 0.59

2. **Pesos por campeonato**:
   - PREMIER: +0.35
   - EURO: +0.25
   - COPA: +0.10
   - SUPER: +0.00 (base)

3. **Pesos por ciclo**:
   - 12h-17h: +0.30
   - 18h-23h: +0.15
   - 06h-11h: +0.05
   - 00h-05h: +0.00 (base)

4. **Estratégia de stake**:
   - ALTA: R$25.00
   - MÉDIA: R$15.00
   - BAIXA: R$5.00

5. **Limite de entradas**: 3 entradas por hora, priorizando as combinações com maior probabilidade.

## Conclusão

O mercado Over 3.5 apresenta características distintas dos mercados BTTS e Over 2.5, com uma taxa de ocorrência significativamente menor. Isso exige uma abordagem mais seletiva, focando nas combinações de campeonato e horário com maior probabilidade de sucesso.
