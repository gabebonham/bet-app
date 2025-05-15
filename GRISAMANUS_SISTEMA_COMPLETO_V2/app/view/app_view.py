import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from view.graphs.visualizer import BetMarketVisualizer
from services.service import Service
from view.graphs.graph import Graph
class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("GRISAMANUS - Sistema de Análise de Mercados")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.pred_treeview = ttk.Treeview()
        self.configurar_estilo()
        
        self.graph = Graph()
        self.visualizer = BetMarketVisualizer()
        self.service = Service()
        # Variáveis para valores de stake
        self.stake_alta = self.service.stake_alta 
        self.stake_media =self.service.stake_media
        self.stake_baixa =self.service.stake_baixa
        # Variáveis para n# Variáveis para
        self.nivel_alta = self.service.nivel_alta 
        self.nivel_media =self.service.nivel_media
        self.nivel_baixa =self.service.nivel_baixa
        # Criar estrutura principal
        self.criar_estrutura()
        self.current_image = ''
        self.image_label = tk.Label(root)
        self.label_grafico_comparativo = tk.Label(root)
        self.grafico_selecionado = tk.StringVar()
        # Inicializar variáveis
        self.hora_atual = tk.IntVar()
        self.num_horas = tk.IntVar()
        self.mercados_selecionados = {
            "BTTS": tk.BooleanVar(value=True),
            "OVER 2.5": tk.BooleanVar(value=True),
            "OVER 3.5": tk.BooleanVar(value=False),
            "UNDER 1.5": tk.BooleanVar(value=False),
            "UNDER 2.5": tk.BooleanVar(value=False),
            "UNDER 3.5": tk.BooleanVar(value=False)
        }
        self.tree_btts = ttk.Treeview()
        self.tree_over25 = ttk.Treeview()
        self.tree_over35 = ttk.Treeview()
        self.tree_under15 = ttk.Treeview()
        self.tree_under25 = ttk.Treeview()
        self.tree_under35 = ttk.Treeview()
        self.mercado_treeviews = {
            "BTTS": self.tree_btts,
            "OVER 2.5": self.tree_over25,
            "OVER 3.5": self.tree_over35,
            "UNDER 1.5": self.tree_under15,
            "UNDER 2.5": self.tree_under25,
            "UNDER 3.5": self.tree_under35
        }
        self.train = tk.BooleanVar(value=True)
        self.create = tk.BooleanVar(value=True)
        self.current_graph = ''
        self.grafico_comparativo_selecionado = tk.StringVar()
        # Preencher interface
        self.table_path = tk.StringVar(value='')
        self.model_label = tk.StringVar(value='')
        self.x_table_path = tk.StringVar(value='')
        self.y_table_path = tk.StringVar(value='')
        self.preencher_interface()
        
    def atualizar_datetime(self):
        """Atualiza o label de data e hora"""
        self.datetime_label.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.root.after(1000, self.atualizar_datetime)
    def carregar_configuracoes(self):
        """Carrega as configurações salvas"""
        try:
            config = self.service.carregar_configuracoes()
            
           
            messagebox.showinfo("Sucesso", "Configurações carregadas com sucesso!")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {str(e)}")
            return False
    def configurar_estilo(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Notebook
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
    def criar_estrutura(self):
        """Cria a estrutura principal da interface"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior - Título e controles
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Título
        ttk.Label(self.top_frame, text="GRISAMANUS - Sistema de Análise de Mercados", 
                 style='Title.TLabel').pack(side=tk.LEFT, padx=10)
        
        # Frame de controles
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controles")
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Abas
        self.tab_previsoes = ttk.Frame(self.notebook)
        self.tab_analise = ttk.Frame(self.notebook)
        self.tab_tabelas = ttk.Frame(self.notebook)
        self.tab_configuracoes = ttk.Frame(self.notebook)
        self.tab_treinamento = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_previsoes, text="Previsões")
        self.notebook.add(self.tab_analise, text="Análise")
        self.notebook.add(self.tab_tabelas, text="Tabelas Operacionais")
        self.notebook.add(self.tab_configuracoes, text="Configurações")
        
        # Frame inferior - Status
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(self.status_frame, text="Pronto")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Data e hora
        self.datetime_label = ttk.Label(self.status_frame, 
                                       text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.datetime_label.pack(side=tk.RIGHT, padx=10)
        self.root.after(1000, self.atualizar_datetime)
    def preencher_interface(self):
        """Preenche a interface com os widgets específicos"""
        # Preencher frame de controles
        self.preencher_controles()
        
        # Preencher abas
        
        self.criar_treeview_previsoes(self.pred_treeview)
        self.preencher_aba_analise()
        self.preencher_aba_tabelas()
        self.preencher_aba_configuracoes()
    def preencher_aba_configuracoes(self):
        """Preenche a aba de configurações"""
        # Frame para configurações
        frame_config = ttk.LabelFrame(self.tab_configuracoes, text="Configurações Gerais")
        frame_config.pack(fill=tk.X, padx=5, pady=5)
        
        # Configurações de stake
        frame_stake = ttk.LabelFrame(frame_config, text="Valores de Stake")
        frame_stake.pack(fill=tk.X, padx=5, pady=5)
        
        
        # Widgets para configuração de stake
        ttk.Label(frame_stake, text="Confiança ALTA:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_stake, from_=1, to=100, increment=1, textvariable=self.stake_alta, 
                   width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_stake, text="Confiança MÉDIA:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_stake, from_=1, to=100, increment=1, textvariable=self.stake_media, 
                   width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_stake, text="Confiança BAIXA:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_stake, from_=1, to=100, increment=1, textvariable=self.stake_baixa, 
                   width=10).grid(row=2, column=1, padx=5, pady=5)
        
        # Configurações de níveis de confiança
        frame_confianca = ttk.LabelFrame(frame_config, text="Níveis de Confiança")
        frame_confianca.pack(fill=tk.X, padx=5, pady=5)
        
        
        
        # Widgets para configuração de níveis de confiança
        ttk.Label(frame_confianca, text="ALTA (>):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_confianca, from_=0.5, to=1.0, increment=0.01, textvariable=self.nivel_alta, 
                   width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_confianca, text="MÉDIA (>):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_confianca, from_=0.5, to=1.0, increment=0.01, textvariable=self.nivel_media, 
                   width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_confianca, text="BAIXA (>):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_confianca, from_=0.5, to=1.0, increment=0.01, textvariable=self.nivel_baixa, 
                   width=10).grid(row=2, column=1, padx=5, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(self.tab_configuracoes)
        frame_botoes.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_botoes, text="Salvar Configurações", 
                  command=self.service.salvar_configuracoes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Carregar Configurações", 
                  command=self.service.carregar_configuracoes).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botoes, text="Restaurar Padrões", 
                  command=self.service.restaurar_padroes).pack(side=tk.LEFT, padx=5)
        
        # Sobre
        frame_sobre = ttk.LabelFrame(self.tab_configuracoes, text="Sobre")
        frame_sobre.pack(fill=tk.X, padx=5, pady=5)
        
        texto_sobre = """GRISAMANUS - Sistema de Análise de Mercados
    
Versão: 1.0.0
Data: 26/04/2025

Este sistema foi desenvolvido para análise e previsão dos mercados BTTS, Over 2.5 e Over 3.5 
em futebol virtual, com base em padrões geométricos e análise estatística.

O sistema inclui:
- Modelos calibrados para os três mercados
- Tabelas operacionais com recomendações por hora
- Análises comparativas entre mercados
- Geração de previsões com diferentes níveis de confiança
"""
    

    def preencher_aba_treinamento(self):
        # Main frame for the tab
        frame_config = ttk.LabelFrame(self.tab_previsoes, text="Sessão de Treinamento", padding=(10, 10))
        frame_config.pack(fill=tk.X,side=tk.LEFT, padx=10, pady=10)

        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Segoe UI", 10), padding=6)
        ttk.Checkbutton(frame_config, text='Incluir Geração de nova Entrada', variable=self.create).pack(
                padx=10, pady=5)
        ttk.Checkbutton(frame_config, text='Treinar Modelo', variable=self.train).pack(
                padx=10, pady=5)
        # File selection button - Tabela Verdadeira
        btn_tabela = ttk.Button(
            frame_config, 
            text="Selecionar Tabela Fonte", 
            style="Custom.TButton",
            command=lambda: self.service.open_file('tabela', self.table_path)
        )
        btn_tabela.pack(pady=(5, 10), anchor='w', padx=10)
        table_label = ttk.Label(frame_config, textvariable=self.table_path)
        table_label.pack(fill=tk.X,padx=10, pady=10)
        
        btn_modelo_train = ttk.Button(
            frame_config, 
            text="Selecionar Dados para Treino", 
            style="Custom.TButton",
            command=lambda:self.service.open_file('x_file',self.x_table_path)
        )
        btn_modelo_train.pack(pady=(0, 10), anchor='w', padx=10)
        x_label = ttk.Label(frame_config, textvariable=self.x_table_path)
        x_label.pack(fill=tk.X,padx=10, pady=10)

        btn_modelo_y = ttk.Button(
            frame_config, 
            text="Selecionar Dados para Compare", 
            style="Custom.TButton",
            command=lambda:self.service.open_file('y_file',self.y_table_path)
        )
        btn_modelo_y.pack(pady=(0), anchor='w', padx=10)
        y_label = ttk.Label(frame_config, textvariable=self.y_table_path)
        y_label.pack(fill=tk.X,padx=10, pady=10)
        # File selection button - Modelo
        btn_modelo = ttk.Button(
            frame_config, 
            text="Selecionar Modelo", 
            style="Custom.TButton",
            command=lambda: self.service.open_file('modelo',self.model_label)
        )
        
        btn_modelo.pack(pady=(0), anchor='w', padx=10)
        model_label = ttk.Label(frame_config, textvariable=self.model_label)
        model_label.pack(fill=tk.X,padx=10, pady=10)
        btn_modelo_create = ttk.Button(
            frame_config, 
            text="Limpar Seleções", 
            style="Custom.TButton",
            command=lambda:self.service.create_file(self.model_label,self.table_path, self.x_table_path, self.y_table_path)
        )
        
        btn_modelo_create.pack(pady=(0, 10), anchor='w', padx=10)
    def preencher_aba_tabela_consolidada(self):
        """Preenche a aba de tabela consolidada"""
        # Frame para exibir a tabela
        frame_tabela = ttk.Frame(self.tab_tabela_consolidada)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label para exibir a tabela como imagem
        self.label_tabela_consolidada = ttk.Label(frame_tabela)
        self.label_tabela_consolidada.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(self.tab_tabela_consolidada)
        frame_botoes.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_botoes, text="Carregar Tabela", 
                  command=self.carregar_tabela_consolidada).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botoes, text="Exportar CSV", 
                  command=self.exportar_tabela_consolidada_csv).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botoes, text="Atualizar Tabela Consolidada", 
                  command=self.atualizar_tabela_consolidada).pack(side=tk.LEFT, padx=5)
    
    
        
        text_widget = tk.Text(frame_sobre, height=10, width=80, wrap=tk.WORD)
        text_widget.insert(tk.END, texto_sobre)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.X, padx=5, pady=5)
    def preencher_aba_tabela(self, parent, mercado):
        """Preenche a aba de tabela para um mercado específico"""
        # Frame para exibir a tabela
        frame_tabela = ttk.Frame(parent)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label para exibir a tabela como imagem
        label_tabela = ttk.Label(frame_tabela)
        label_tabela.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Salvar referência ao label
        setattr(self, f"label_tabela_{mercado}", label_tabela)
        
        # Botões
        frame_botoes = ttk.Frame(parent)
        frame_botoes.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_botoes, text="Carregar Tabela", 
                  command=lambda m=mercado: self.carregar_tabela(m)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botoes, text="Exportar CSV", 
                  command=lambda m=mercado: self.service.exportar_tabela_csv(m)).pack(side=tk.LEFT, padx=5)
    def preencher_aba_analise(self):
        """Preenche a aba de análise"""
        # Frame para exibir gráficos
        self.analise_frame = ttk.Frame(self.tab_analise)
        self.analise_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Notebook para separar análises por mercado
        self.analise_notebook = ttk.Notebook(self.analise_frame)
        self.analise_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas para cada mercado
        self.tab_analise_btts = ttk.Frame(self.analise_notebook)
        self.tab_analise_over25 = ttk.Frame(self.analise_notebook)
        self.tab_analise_over35 = ttk.Frame(self.analise_notebook)
        self.tab_analise_comparativa = ttk.Frame(self.analise_notebook)
        self.tab_analise_under25 = ttk.Frame(self.analise_notebook)
        self.tab_analise_under35 = ttk.Frame(self.analise_notebook)
        self.tab_analise_under15 = ttk.Frame(self.analise_notebook)
        
        self.analise_notebook.add(self.tab_analise_btts, text="BTTS")
        self.analise_notebook.add(self.tab_analise_over25, text="OVER 2.5")
        self.analise_notebook.add(self.tab_analise_over35, text="OVER 3.5")
        self.analise_notebook.add(self.tab_analise_under15, text="UNDER 1.5")
        self.analise_notebook.add(self.tab_analise_under25, text="UNDER 2.5")
        self.analise_notebook.add(self.tab_analise_under35, text="UNDER 3.5")
        self.analise_notebook.add(self.tab_analise_comparativa, text="Comparativa")
        
        # Preencher abas de análise
        self.preencher_aba_analise_mercado(self.tab_analise_btts, "btts")
        self.preencher_aba_analise_mercado(self.tab_analise_over25, "over25")
        self.preencher_aba_analise_mercado(self.tab_analise_over35, "over35")
        self.preencher_aba_analise_mercado(self.tab_analise_under25, "under25")
        
        self.preencher_aba_analise_mercado(self.tab_analise_under15, "under15")
        self.preencher_aba_analise_mercado(self.tab_analise_under35, "under35")
        self.preencher_aba_analise_comparativa()
    
    def preencher_aba_analise_mercado(self, parent, mercado):
        """Preenche a aba de análise para um mercado específico"""
        # Frame para seleção de gráficos
        
        frame_selecao = ttk.LabelFrame(parent, text="Selecione o Gráfico")
        frame_selecao.pack(fill=tk.X, padx=5, pady=5)  # Changed fill and side
        # Frame para exibir o gráfico
        frame_grafico = ttk.LabelFrame(parent, text="Gráfico")
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Variável para armazenar o gráfico selecionado
        
        
        # Opções de gráficos
        opcoes = [
            "Taxa de Ocorrência por Campeonato",
            "Taxa de Ocorrência por Hora",
            "Taxa de Ocorrência por Ciclo",
            "Heatmap Campeonato x Hora",
            "Heatmap Campeonato x Ciclo",
            "Comparação de Mercados",
            "Tendências por Hora",
            "Correlações entre Mercados"
        ]
        
        # Combobox para seleção de gráficos
        cb_graficos = ttk.Combobox(
            frame_selecao,
            textvariable=self.grafico_selecionado,
            values=opcoes,
            state="readonly",
            width=40)
        cb_graficos.current(0)
        cb_graficos.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Frame para exibição do gráfico
        # Botão para exibir gráfico
        
        btn_exibir = ttk.Button(
            frame_selecao,
            text="Exibir Gráfico",
            command=lambda: self.display(mercado, frame_grafico)
        )
        btn_exibir.pack(fill=tk.NONE, side='left', padx=5, pady=5)
        self.image_label = ttk.Label(frame_grafico)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.comparison_label = ttk.Label(frame_grafico)
        self.comparison_label.pack(fill=tk.BOTH, expand=True)

    def display(self, mercado, frame):
        image_path = ''
        if mercado:
            image_path = self.graph.exibir_grafico(mercado, self.grafico_selecionado.get())
        else:
            image_path = self.graph.exibir_grafico_comparativo(self.grafico_comparativo_selecionado.get())

        try:
            # Clear previous image (if any)
            for widget in frame.winfo_children():
                widget.destroy()

            # Create scrollable canvas
            canvas = tk.Canvas(frame, width=600, height=400)
            scroll_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
            scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

            scroll_x.pack(side="bottom", fill="x")
            scroll_y.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            # Create inner frame to hold the image
            image_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=image_frame, anchor="nw")

            # Load image
            img = Image.open(image_path)
            self.original_img_size = img.size  # Save original size in case of zoom/pan features later
            img = img.resize((800, 600), Image.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img)

            # Create and place label inside the frame
            image_label = ttk.Label(image_frame, image=self.current_image)
            image_label.image = self.current_image  # Keep reference
            image_label.pack()

            # Update scroll region
            image_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exibir imagem: {str(e)}")
    def preencher_aba_analise_comparativa(self):
        """Preenche a aba de análise comparativa"""
        
        # Frame para seleção de gráficos
        frame_selecao = ttk.LabelFrame(self.tab_analise_comparativa, text="Selecione o Gráfico")
        frame_selecao.pack(fill=tk.X, padx=5, pady=5)
        
        # Variável para armazenar o gráfico selecionado
        
        
        # Opções de gráficos
        opcoes = [
            'Comparação de Ciclos entre Mercados',
'Comparação de Taxas entre Mercados'
        ]
        
        # Combobox para seleção
        combo = ttk.Combobox(frame_selecao, textvariable=self.grafico_comparativo_selecionado, 
                            values=opcoes, state="readonly", width=40)
        combo.current(0)
        combo.pack(side=tk.LEFT, padx=10, pady=5)
        # Frame para exibir o gráfico
        frame_grafico = ttk.LabelFrame(self.tab_analise_comparativa, text="Gráfico")
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Botão para exibir gráfico
        ttk.Button(frame_selecao, text="Exibir", 
                  command=lambda:self.display(mercado=None,frame=frame_grafico)).pack(side=tk.LEFT, padx=5, pady=5)
        
    def preencher_aba_tabelas(self):
        """Preenche a aba de tabelas operacionais com uma única tabela consolidada"""
        # Frame principal para a tabela
        self.tabela_frame = ttk.Frame(self.tab_tabelas)
        self.tabela_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        self.hscroll = ttk.Scrollbar(self.tabela_frame, orient=tk.HORIZONTAL)
        self.vscroll = ttk.Scrollbar(self.tabela_frame, orient=tk.VERTICAL)
        
        # Treeview com todas as colunas
        columns = [
            "id_partida", "campeonato", "data", "tempo", 
            "time_casa", "time_contra", "gols_casa", "gols_contra",
            "gols_totais", "odd_over25", "odd_under25", "odd_over35",
            "odd_under35", "odd_casa", "odd_empate", "odd_visitante",
            "placar_exato", "odd_placar_exato", "data_odds"
        ]
        
        self.treeview_tabela = ttk.Treeview(
            self.tabela_frame,
            columns=columns,
            show="headings",
            xscrollcommand=self.hscroll.set,
            yscrollcommand=self.vscroll.set
        )
        
        # Configurar colunas
        colunas = [
            ("ID Partida", 80),
            ("Campeonato", 100),
            ("Data", 80),
            ("Tempo", 60),
            ("Time Casa", 100),
            ("Time Contra", 100),
            ("Gols Casa", 70),
            ("Gols Contra", 70),
            ("Gols Totais", 70),
            ("Odd Over 2.5", 90),
            ("Odd Under 2.5", 90),
            ("Odd Over 3.5", 90),
            ("Odd Under 3.5", 90),
            ("Odd Casa", 80),
            ("Odd Empate", 80),
            ("Odd Visitante", 80),
            ("Placar Exato", 80),
            ("Odd Placar", 80),
            ("Data Odds", 120)
        ]
        
        for (col_text, width), col_id in zip(colunas, columns):
            self.treeview_tabela.heading(col_id, text=col_text)
            self.treeview_tabela.column(col_id, width=width, anchor=tk.CENTER)
        
        # Posicionar widgets
        self.treeview_tabela.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll.grid(row=1, column=0, sticky="ew")
        
        # Configurar scrollbars
        self.vscroll.config(command=self.treeview_tabela.yview)
        self.hscroll.config(command=self.treeview_tabela.xview)
        
        # Configurar expansão
        self.tabela_frame.grid_rowconfigure(0, weight=1)
        self.tabela_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para botões
        btn_frame = ttk.Frame(self.tab_tabelas)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botões
        ttk.Button(btn_frame, text="Carregar Dados", command=lambda:self.service.carregar_dados_partidas(self.treeview_tabela)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exportar CSV", command=lambda:self.service.exportar_dados_csv(self.treeview_tabela)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar Dados", command=lambda:self.service.atualizar_dados_partidas(self.treeview_tabela)).pack(side=tk.LEFT, padx=5)

    def preencher_controles(self):
        """Preenche o frame de controles"""
        # Frame para hora e número de horas
        frame_hora = ttk.Frame(self.control_frame)
        frame_hora.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_hora, text="Hora Atual:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        hora_spin = ttk.Spinbox(frame_hora, from_=0, to=23, width=5, textvariable=self.hora_atual)
        hora_spin.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_hora, text="Número de Horas:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        num_horas_spin = ttk.Spinbox(frame_hora, from_=1, to=5, width=5, textvariable=self.num_horas)
        num_horas_spin.grid(row=0, column=3, padx=5, pady=5)
        
        # Frame para seleção de mercados
        frame_mercados = ttk.LabelFrame(self.control_frame, text="Mercados")
        frame_mercados.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
        
        for i, (mercado, var) in enumerate(self.mercados_selecionados.items()):
            ttk.Checkbutton(frame_mercados, text=mercado, variable=var).grid(
                row=0, column=i, padx=10, pady=5)
        
        
    def preencher_aba_previsoes(self):
        """Preenche a aba de previsões"""
        # Frame para exibir previsões
        self.previsoes_frame = ttk.Frame(self.tab_previsoes)
        self.previsoes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Notebook para separar previsões por mercado
        self.previsoes_notebook = ttk.Notebook(self.previsoes_frame)
        self.previsoes_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas para cada mercado
        self.mercado_treeviews['MERCADOS'] = ttk.Frame(self.previsoes_notebook)
        
        self.previsoes_notebook.add(self.mercado_treeviews['MERCADOS'], text="BTTS")
        
        
        
    
    def criar_treeview_previsoes(self, treeview):
        """Preenche a aba de previsões com notebooks para cada mercado"""
        self.preencher_aba_treinamento()
        # Main frame
        self.previsoes_frame = ttk.Frame(self.tab_previsoes)
        self.previsoes_frame.pack(fill=tk.BOTH,side=tk.RIGHT, anchor='e',expand=True, padx=5, pady=5)
        
        # Notebook (tabbed interface)
        self.previsoes_notebook = ttk.Notebook(self.previsoes_frame)
        self.previsoes_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for all markets
        markets = [
            ("MERCADOS", "MERCADOS"),
        ]
        
        # Create tabs dynamically
        self.market_frames = {}
        for market_id, market_name in markets:
            frame = ttk.Frame(self.previsoes_notebook)
            self.previsoes_notebook.add(frame, text=market_name)
            self.market_frames[market_id] = frame
            self._create_market_tab(frame, market_name)
        

    def _create_market_tab(self, parent, market_id):
        """Creates UI elements for a specific market tab"""
        # Main container
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        mercados = [
            "BTTS",
            "OVER 2.5",
            "OVER 3.5",
            "UNDER 1.5",
            "UNDER 2.5",
            "UNDER 3.5",
        ]
        # for mercado in mercados:
        #     self.mercado_treeviews[mercado] = treeview = ttk.Treeview(
        #     tree_frame,
        #     show="headings",
        #     yscrollcommand=scrollbar.set,
        #     selectmode="browse"
        # )
        
        # Configure columns
        
        # Store reference
        # setattr(self, f"treeview_{market_id}", treeview)
        # Button panel
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=5)
        """Gera previsões para os mercados selecionados"""
        hora_atual = self.hora_atual.get()
        num_horas = self.num_horas.get()
        # tree_to_view = getattr(self, f"treeview_{market_id}")
        self.status_label.config(text="Gerando previsões...")
        self.root.update()
        # self.pred_treeview = tree_to_view
        action_buttons = [
            ("Gerar Previsões", lambda m=market_id: self.service.gerar_previsoes(self.hora_atual.get(),self.num_horas.get(),tree_frame,market_id, self.create, self.train))
        ]
        
        for btn_text, cmd in action_buttons:
            ttk.Button(btn_frame, text=btn_text, command=cmd).pack(side=tk.LEFT, padx=2)





def main():
    root = tk.Tk()
    app = AppView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
