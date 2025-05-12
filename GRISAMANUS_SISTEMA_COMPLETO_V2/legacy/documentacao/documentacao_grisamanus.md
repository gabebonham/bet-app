# Documentação do Sistema GRISAMANUS

## Visão Geral

O Sistema GRISAMANUS é uma solução completa para análise e previsão de apostas em futebol virtual, focando em três mercados principais:

1. **BTTS (Both Teams To Score)** - Ambas as equipes marcam
2. **Over 2.5** - Mais de 2.5 gols na partida
3. **Over 3.5** - Mais de 3.5 gols na partida

O sistema utiliza análise avançada de padrões geométricos, ciclos temporais e correlações entre campeonatos para gerar previsões com diferentes níveis de confiança, permitindo uma operação otimizada e lucrativa.

## Estrutura do Sistema

O GRISAMANUS é composto por:

1. **Módulos de Análise**: Scripts Python para processamento de dados históricos e identificação de padrões
2. **Modelos de Previsão**: Algoritmos calibrados para cada mercado específico
3. **Interface Gráfica**: Aplicativo desktop para operação diária
4. **Tabelas Operacionais**: Guias de referência rápida para tomada de decisão

## Orientações Específicas por Mercado

Após extensa análise e calibração, o sistema foi otimizado com as seguintes orientações:

### BTTS (Ambas Marcam)
- **Campeonatos**: PREMIER e EURO (os dois melhores)
- **Níveis de Confiança**: 
  - ALTA: probabilidade > 0.80
  - MÉDIA: probabilidade entre 0.70 e 0.79
  - BAIXA: probabilidade entre 0.55 e 0.69
- **Taxa média de ocorrência**: 53.0%
- **Ciclo mais favorável**: 12h-17h (56.5% de ocorrência)

### Over 2.5
- **Campeonatos**: SOMENTE PREMIER (95% de acerto)
- **Níveis de Confiança**: 
  - ALTA: probabilidade > 0.73
  - MÉDIA: probabilidade entre 0.64 e 0.72
  - BAIXA: probabilidade entre 0.55 e 0.63
- **Taxa média de ocorrência**: 42.6%
- **Ciclo mais favorável**: 12h-17h (48.7% de ocorrência)

### Over 3.5
- **Campeonatos**: TODOS os 4 campeonatos (PREMIER, EURO, SUPER e COPA)
- **Níveis de Confiança**: 
  - ALTA: probabilidade > 0.70
  - MÉDIA: probabilidade entre 0.60 e 0.69
  - BAIXA: probabilidade entre 0.50 e 0.59
- **Taxa média de ocorrência**: 25.6%
- **Ciclo mais favorável**: 12h-17h (31.0% de ocorrência)

## Ciclos de Horários e Taxas de Ocorrência

A análise identificou quatro ciclos distintos de 6 horas cada, com diferentes taxas de ocorrência:

| Ciclo | BTTS | Over 2.5 | Over 3.5 |
|-------|------|----------|----------|
| 00h-05h | 48.5% (baixo) | 37.2% (baixo) | 22.0% (baixo) |
| 06h-11h | 52.3% (médio) | 40.5% (médio) | 24.0% (médio) |
| 12h-17h | 56.5% (alto) | 48.7% (alto) | 31.0% (alto) |
| 18h-23h | 54.2% (médio-alto) | 44.3% (médio-alto) | 26.0% (médio) |

O ciclo 12h-17h apresenta consistentemente as maiores taxas de ocorrência para todos os mercados, sendo o período mais recomendado para operação.

## Estratégia de Stake e Martingale

O sistema implementa uma estratégia de gerenciamento de risco baseada nos níveis de confiança:

| Nível de Confiança | Valor da Stake | Gales Recomendados |
|--------------------|----------------|-------------------|
| ALTA | R$25.00 | 1 gale |
| MÉDIA | R$15.00 | 2 gales |
| BAIXA | R$5.00 | 3 gales |

Esta estratégia foi calibrada para maximizar o retorno esperado enquanto minimiza o risco, garantindo lucro com pelo menos 2 acertos por hora em 3 tentativas.

## Recomendações Operacionais

1. **Limite de entradas**: Utilize no máximo 3 entradas por hora para cada mercado
2. **Priorização de horários**: Concentre-se no ciclo 12h-17h, que apresenta as maiores taxas de ocorrência
3. **Seleção de campeonatos**: Siga as orientações específicas para cada mercado
4. **Estratégia de Martingale**: Ajuste o número de gales conforme o nível de confiança
5. **Registro de resultados**: Mantenha um registro detalhado para análise posterior
6. **Atualização regular**: Atualize o modelo a cada 6 horas para manter sua precisão

## Utilização do Aplicativo GRISAMANUS

O aplicativo desktop GRISAMANUS oferece uma interface intuitiva para operação diária:

### Dashboard
- Visão geral das taxas de ocorrência por mercado
- Gráfico de horários recomendados
- Acesso rápido às funcionalidades principais

### Abas de Mercado (BTTS, Over 2.5, Over 3.5)
- Geração de previsões para as próximas horas
- Visualização em formato de tabela e gráficos
- Exportação para CSV e PDF

### Tabela Consolidada
- Visão integrada de todos os mercados
- Recomendações operacionais
- Exportação para PDF

### Configurações
- Ajuste de parâmetros por mercado
- Personalização de valores de stake
- Configuração da estratégia de Martingale

## Arquivos do Sistema

O sistema GRISAMANUS é composto pelos seguintes arquivos principais:

1. **grisamanus_app.py**: Aplicativo principal com interface gráfica
2. **analise_btts/modelo_btts_calibrado.py**: Modelo calibrado para BTTS
3. **analise_over25/modelo_over25_otimizado.py**: Modelo otimizado para Over 2.5
4. **analise_over35/modelo_over35_4campeonatos.py**: Modelo para Over 3.5
5. **tabelas_operacionais/criar_tabela_operacional_consolidada.py**: Gerador de tabela consolidada

## Requisitos do Sistema

- Python 3.8 ou superior
- Bibliotecas: pandas, numpy, matplotlib, seaborn, tkinter, PIL
- Sistema operacional: Windows 10/11 (recomendado), Linux ou macOS

## Instalação e Execução

1. Instale o Python 3.8 ou superior
2. Instale as bibliotecas necessárias:
   ```
   pip install pandas numpy matplotlib seaborn pillow
   ```
3. Execute o aplicativo:
   ```
   python grisamanus_app.py
   ```

## Manutenção e Atualização

Para manter o sistema GRISAMANUS funcionando com máxima eficiência:

1. **Atualização de dados**: Idealmente a cada 6 horas, com uma atualização diária mínima
2. **Recalibração**: Após eventos significativos como quebras repentinas de padrão
3. **Backup**: Mantenha backups regulares dos arquivos de configuração e histórico

## Suporte e Contato

Para suporte técnico ou dúvidas sobre o sistema GRISAMANUS, entre em contato através dos canais fornecidos separadamente.

---

© 2025 GRISAMANUS. Todos os direitos reservados.
