# GRISAMANUS V2 - Sistema Completo de Análise de Mercados

Este documento descreve a versão 2 do sistema GRISAMANUS, que agora inclui análise e previsões para os seguintes mercados:

1. BTTS (Ambas Equipes Marcam)
2. Over 2.5 Gols
3. Over 3.5 Gols
4. Under 1.5 Gols
5. Placar Exato 0x0

## Estrutura do Sistema

O sistema GRISAMANUS V2 está organizado nos seguintes módulos:

### 1. Módulos de Análise

- **analise_btts**: Análise e previsões para o mercado BTTS
- **analise_over25**: Análise e previsões para o mercado Over 2.5
- **analise_over35**: Análise e previsões para o mercado Over 3.5
- **analise_under**: Análise e previsões para os mercados Under 1.5 e placar exato 0x0

### 2. Tabelas Operacionais

- **tabelas_operacionais**: Scripts para gerar tabelas operacionais para todos os mercados

### 3. Aplicação Principal

- **app**: Interface gráfica para gerenciar todos os componentes do sistema

### 4. Documentação

- **documentacao**: Documentação completa do sistema e guias de uso

## Novidades da Versão 2

A principal novidade da versão 2 é a inclusão dos mercados Under 1.5 e placar exato 0x0, com:

1. Análise detalhada das taxas de ocorrência por campeonato e ciclo horário
2. Identificação da correlação entre Under 1.5 e placar 0x0
3. Estratégia escalonada para explorar as odds elevadas do placar exato
4. Geração de previsões específicas para a madrugada

## Como Usar

1. Execute o aplicativo principal:
   ```
   python app/grisamanus_app_completo.py
   ```

2. Para gerar previsões específicas para Under 1.5 e placar 0x0:
   ```
   python analise_under/gerar_previsoes_under15_0x0.py
   ```

3. Para atualizar todas as tabelas operacionais:
   ```
   python tabelas_operacionais/criar_tabela_operacional_consolidada.py
   ```

## Requisitos

- Python 3.8 ou superior
- Bibliotecas: pandas, numpy, matplotlib, seaborn, tkinter, reportlab

## Instalação

Siga as instruções detalhadas no arquivo `documentacao/guia_instalacao_detalhado.md`

## Contato

Para suporte ou dúvidas, consulte a documentação completa ou entre em contato com a equipe GRISAMANUS.

---

Atualizado em: 26/04/2025
