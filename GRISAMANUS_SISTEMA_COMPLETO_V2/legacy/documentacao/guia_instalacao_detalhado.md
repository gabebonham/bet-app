# Guia de Instalação Detalhado do Sistema GRISAMANUS

## Pré-requisitos

1. **Python 3.8 ou superior**
   - Se não tiver instalado, baixe em: https://www.python.org/downloads/
   - Durante a instalação, marque a opção "Add Python to PATH"
   - Para verificar se o Python está instalado, abra o Prompt de Comando e digite: `python --version`

2. **Bibliotecas necessárias**
   - pandas: para manipulação de dados
   - numpy: para cálculos numéricos
   - matplotlib: para geração de gráficos
   - seaborn: para visualizações estatísticas
   - pillow (PIL): para manipulação de imagens
   - reportlab: para geração de PDFs
   - tkinter: para a interface gráfica (geralmente já vem com Python)

## Passo 1: Preparar a estrutura de diretórios

1. Crie uma pasta principal chamada `GRISAMANUS` em seu computador
   - No Windows: `C:\Users\SeuUsuario\Documents\GRISAMANUS`
   - No Mac/Linux: `/home/SeuUsuario/GRISAMANUS`

2. Dentro dela, crie as seguintes subpastas:
   - `analise_btts`
   - `analise_over25`
   - `analise_over35`
   - `tabelas_operacionais`
   - `graficos`

3. Dentro de cada pasta de análise, crie as seguintes subpastas:
   - `previsoes`
   - `graficos`
   - `resultados`

## Passo 2: Instalar as bibliotecas necessárias

1. Abra o Prompt de Comando (Windows) ou Terminal (Mac/Linux)

2. Execute o seguinte comando para instalar todas as bibliotecas necessárias:

```
pip install pandas numpy matplotlib seaborn pillow reportlab
```

3. Verifique se as bibliotecas foram instaladas corretamente:

```
pip list
```

## Passo 3: Baixar e organizar os arquivos do sistema

1. Descompacte o arquivo `GRISAMANUS_SISTEMA_COMPLETO.zip` que você recebeu

2. Copie os arquivos para as respectivas pastas:

   **Pasta principal `GRISAMANUS`:**
   - `grisamanus_app_completo.py`
   - `documentacao_grisamanus.md`
   - `relatorio_final_grisamanus.md`

   **Pasta `analise_btts`:**
   - `modelo_btts_calibrado.py`
   - `modelo_btts_otimizado.py`

   **Pasta `analise_over25`:**
   - `modelo_over25_calibrado.py`
   - `modelo_over25_otimizado.py`
   - `analisar_comportamento_over25.py`
   - `desenvolver_modelo_over25.py`

   **Pasta `analise_over35`:**
   - `modelo_over35_calibrado.py`
   - `modelo_over35_4campeonatos.py`
   - `analisar_over35.py`
   - `documentacao_over35.md`

   **Pasta `tabelas_operacionais`:**
   - `tabela_operacional_over35.py`
   - `criar_tabela_horarios_recomendados.py`
   - `criar_tabela_operacional_consolidada.py`

3. Copie também os arquivos de gráficos para as respectivas pastas de gráficos

## Passo 4: Ajustar os caminhos nos arquivos

Como você está instalando em seu próprio computador, é necessário ajustar os caminhos nos arquivos:

1. Abra cada arquivo Python (`.py`) em um editor de texto

2. Procure por caminhos que começam com `/home/ubuntu/` e substitua pelo caminho da sua instalação:
   - No Windows: `C:\\Users\\SeuUsuario\\Documents\\GRISAMANUS\\`
   - No Mac/Linux: `/home/SeuUsuario/GRISAMANUS/`

3. Certifique-se de usar as barras corretas:
   - Windows: use barras duplas `\\` ou barras invertidas simples `/`
   - Mac/Linux: use barras normais `/`

## Passo 5: Executar o aplicativo

1. Abra o Prompt de Comando (Windows) ou Terminal (Mac/Linux)

2. Navegue até a pasta principal do GRISAMANUS:
   ```
   cd C:\Users\SeuUsuario\Documents\GRISAMANUS  # Windows
   cd /home/SeuUsuario/GRISAMANUS  # Mac/Linux
   ```

3. Execute o aplicativo:
   ```
   python grisamanus_app_completo.py
   ```

## Passo 6: Usar o sistema

1. **Gerar previsões**:
   - Na tela principal, selecione a hora atual e o número de horas desejado (1-5)
   - Marque os mercados que deseja analisar (BTTS, Over 2.5, Over 3.5)
   - Clique em "Gerar Previsões"
   - As previsões serão exibidas nas abas correspondentes

2. **Visualizar gráficos**:
   - Vá para a aba "Análise"
   - Selecione o mercado (BTTS, Over 2.5, Over 3.5 ou Comparativa)
   - Escolha o tipo de gráfico no menu suspenso
   - Clique em "Exibir"
   - O gráfico será mostrado na área principal

3. **Consultar tabelas operacionais**:
   - Vá para a aba "Tabelas Operacionais"
   - Selecione o mercado desejado ou a tabela consolidada
   - Clique em "Carregar Tabela"
   - A tabela será exibida na área principal
   - Você pode exportar a tabela para CSV clicando em "Exportar CSV"

4. **Configurar parâmetros**:
   - Vá para a aba "Configurações"
   - Ajuste os valores de stake para cada nível de confiança
   - Ajuste os níveis de confiança (limites de probabilidade)
   - Clique em "Salvar Configurações"
   - Para restaurar os valores padrão, clique em "Restaurar Padrões"

## Solução de problemas comuns

1. **Erro de módulo não encontrado**:
   - Mensagem: `ModuleNotFoundError: No module named 'xxx'`
   - Solução: Instale a biblioteca faltante com `pip install xxx`
   - Exemplo: `pip install reportlab`

2. **Erro de caminho não encontrado**:
   - Mensagem: `FileNotFoundError: [Errno 2] No such file or directory: '...'`
   - Solução: Verifique se os caminhos nos arquivos estão corretos para seu sistema
   - Certifique-se de que todas as pastas necessárias foram criadas

3. **Interface gráfica não abre**:
   - No Windows: Verifique se o Python foi instalado corretamente
   - No Linux: Instale o tkinter separadamente com `sudo apt-get install python3-tk`
   - No Mac: Instale o Python da python.org, não do Homebrew

4. **Gráficos não são exibidos**:
   - Verifique se matplotlib e pillow estão instalados
   - Certifique-se de que os arquivos de gráficos existem nas pastas corretas

5. **Erros ao gerar PDFs**:
   - Verifique se reportlab está instalado
   - Certifique-se de que tem permissão para escrever nas pastas de destino

## Dicas adicionais

1. **Backup dos dados**:
   - Faça backup regular das pastas de previsões e resultados
   - Isso garantirá que você não perca seu histórico de operações

2. **Atualização do sistema**:
   - Periodicamente, verifique se há atualizações dos modelos
   - Os modelos podem ser recalibrados com novos dados para melhorar a precisão

3. **Personalização**:
   - Você pode ajustar os parâmetros dos modelos nos arquivos Python
   - Experimente diferentes valores de stake e níveis de confiança

4. **Uso diário**:
   - Execute o sistema antes do início das operações
   - Gere previsões para as próximas 3-5 horas
   - Registre os resultados para análise posterior

## Suporte

Se encontrar problemas durante a instalação ou uso do sistema, verifique:

1. Se todos os pré-requisitos foram atendidos
2. Se a estrutura de diretórios está correta
3. Se os caminhos nos arquivos foram ajustados para seu sistema
4. Se todas as bibliotecas necessárias estão instaladas

Lembre-se que este sistema foi desenvolvido para análise e previsão dos mercados BTTS, Over 2.5 e Over 3.5 em futebol virtual, com base em padrões geométricos e análise estatística. Use-o como uma ferramenta de apoio à decisão, não como um sistema infalível.
