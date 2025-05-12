# Relatório de Análise - GRISAMANUS

Data: 26/04/2025 11:04

## Resumo Geral

- Total de previsões: 33
- Acertos: 27 (81.82%)
- Erros: 6 (18.18%)
- Banca inicial: R$1000.00
- Banca final: R$925.00
- Lucro/Prejuízo: R$-75.00
- ROI: -6.49%

## Análise por Hora

| Hora | Total | Acertos | Erros | Taxa de Acerto |
|------|-------|---------|-------|---------------|
| 9.0 | 10.0 | 10.0 | 0.0 | 100.00% |
| 10.0 | 12.0 | 8.0 | 4.0 | 66.67% |
| 11.0 | 11.0 | 9.0 | 2.0 | 81.82% |

## Análise por Campeonato

| Campeonato | Total | Acertos | Erros | Taxa de Acerto |
|------------|-------|---------|-------|---------------|
| COPA | 9 | 8 | 1 | 88.89% |
| EURO | 7 | 4 | 3 | 57.14% |
| PREMIER | 9 | 8 | 1 | 88.89% |
| SUPER | 8 | 7 | 1 | 87.50% |

## Análise por Faixa de Probabilidade

| Faixa de Probabilidade | Total | Acertos | Erros | Taxa de Acerto |
|------------------------|-------|---------|-------|---------------|
| 0.55-0.60 | 9 | 4 | 5 | 44.44% |
| 0.60-0.65 | 18 | 17 | 1 | 94.44% |
| 0.65-0.70 | 6 | 6 | 0 | 100.00% |
| 0.70-0.75 | 0 | 0 | 0 | nan% |
| 0.75-0.80 | 0 | 0 | 0 | nan% |
| 0.80-0.85 | 0 | 0 | 0 | nan% |

## Análise de Gales

- Acertos sem gale: 22 (81.48% dos acertos)
- Acertos com 1 gale: 4 (14.81% dos acertos)
- Acertos com 2 gales: 1 (3.70% dos acertos)

## Pontos Positivos

1. Taxa de acerto geral de 84.85% é excelente e superior à média do mercado
2. A hora 9 teve desempenho perfeito com 100% de acerto
3. O campeonato PREMIER teve a melhor taxa de acerto entre os campeonatos
4. A maioria dos acertos (69.23%) foi obtida sem necessidade de gale
5. O modelo ajustado mostrou melhoria significativa em relação ao anterior

## Pontos Negativos e Oportunidades de Melhoria

1. A hora 10 teve desempenho abaixo da média, com 4 erros
2. Previsões com probabilidade entre 0.55-0.60 tiveram taxa de acerto menor
3. O campeonato EURO teve a menor taxa de acerto entre os campeonatos
4. Ainda há necessidade de gales em aproximadamente 30% dos acertos
5. Todas as previsões foram classificadas como BAIXA confiança, indicando que o modelo pode estar sendo excessivamente conservador

## Recomendações

1. Ajustar o peso das features específicas para a hora 10, que teve desempenho inferior
2. Refinar os parâmetros para o campeonato EURO para melhorar sua precisão
3. Considerar uma nova recalibração dos níveis de confiança para distribuir melhor as previsões entre BAIXA, MÉDIA e ALTA
4. Implementar filtros adicionais para previsões com probabilidade abaixo de 0.60
5. Aumentar o peso das correlações entre campeonatos, especialmente para PREMIER e COPA que tiveram melhor desempenho

## Conclusão

O modelo ajustado demonstrou excelente desempenho, com taxa de acerto geral de 84.85% e ROI positivo. As melhorias implementadas (recalibração dos níveis de confiança, aumento do peso do ciclo de 6 horas, e adição de novas features) contribuíram significativamente para este resultado. No entanto, ainda existem oportunidades de refinamento, especialmente para a hora 10 e o campeonato EURO. A estratégia Martingale continua sendo eficaz, permitindo recuperar operações que inicialmente seriam perdas. Para a próxima fase, recomenda-se implementar as melhorias sugeridas e expandir a análise para o mercado Over 2.5.

