import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sys
import os
import numpy as np
from app.view.graphs.visualizer import BetMarketVisualizer
from app.services.service import Service
from app.view.graphs.graph import Graph
from datetime import datetime
from app.view.graphs.plotting_graphs import run_plotting
class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("GRISAMANUS - Sistema de Análise de Mercados")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.pred_treeview = ttk.Treeview()
        self.job = tk.BooleanVar(value=False)
        self.configurar_estilo()
        self.tab_tabelas_graph = ttk.Treeview()
        self.predictions_tree_frame = None
        self.graph = Graph()
        self.last_prediction_hour = None
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
            "BTTS": tk.BooleanVar(value=False),
            "OVER 2.5": tk.BooleanVar(value=False),
            "OVER 3.5": tk.BooleanVar(value=False),
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
            "Odd BTTS": self.tree_btts,
            "Odd Over 2.5": self.tree_over25,
            "Odd Over 3.5": self.tree_over35,
            "Odd Under 3.5": self.tree_under15,
            "Odd Under 2.5": self.tree_under25,
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
        self.current_file = tk.StringVar(value='')
        self.current_table_file = tk.StringVar(value='')
        self.current_model_file = tk.StringVar(value='')
        self.target_columns = tk.Variable(value=[])
        self.support_columns = tk.Variable(value=[])
        
        self.preencher_interface()
        self.verify_job()
    def atualizar_datetime(self):
        """Atualiza o label de data e hora"""
        self.datetime_label.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.root.after(1000, self.atualizar_datetime)
    def verify_job(self):
        if self.job.get():
            self.run_prediction_job()
        self.root.after(6000, self.verify_job)
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
        # self.notebook.add(self.tab_configuracoes, text="Configurações")
        
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
        # ttk.Checkbutton(frame_config, text='Incluir Geração de nova Entrada', variable=self.create).pack(
        #         padx=10, pady=5)
        # ttk.Checkbutton(frame_config, text='Treinar Modelo', variable=self.train).pack(
        #         padx=10, pady=5)
        # File selection button - Tabela Verdadeira
        ttk.Checkbutton(frame_config, text='Ativar Previsão Automatica', variable=self.job).pack(
                 padx=10, pady=5)
        btn_tabela = ttk.Button(
            frame_config, 
            text="Selecionar Tabelas Fonte", 
            style="Custom.TButton",
            command=lambda: self.service.open_file('tables', self.current_table_file)
        )
        btn_tabela.pack(pady=(5, 10), anchor='w', padx=10)
        table_label = ttk.Label(frame_config, textvariable=self.current_table_file)
        # table_label.pack(fill=tk.X,padx=10, pady=10)
        

        # File selection button - Modelo
        btn_modelo = ttk.Button(
            frame_config, 
            text="Selecionar Modelo", 
            style="Custom.TButton",
            command=lambda: self.service.open_file('modelo',self.current_model_file)
        )
        
        # btn_modelo.pack(pady=(0), anchor='w', padx=10)
        # model_label = ttk.Label(frame_config, textvariable=self.current_model_file)
        # model_label.pack(fill=tk.X,padx=10, pady=10)
        btn_modelo_create = ttk.Button(
            frame_config, 
            text="Limpar Seleções", 
            style="Custom.TButton",
            command=lambda:self.service.create_file(self.current_table_file,self.current_model_file, self.x_table_path, self.y_table_path)
        )
        
        btn_modelo_create.pack(pady=(0, 10), anchor='w', padx=10)
    
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
        self.tab_analise_tabelas_graph = ttk.Frame(self.analise_notebook)
        # self.tab_analise_over25 = ttk.Frame(self.analise_notebook)
        # self.tab_analise_over35 = ttk.Frame(self.analise_notebook)
        # self.tab_analise_comparativa = ttk.Frame(self.analise_notebook)
        # self.tab_analise_under25 = ttk.Frame(self.analise_notebook)
        # self.tab_analise_under35 = ttk.Frame(self.analise_notebook)
        # self.tab_analise_under15 = ttk.Frame(self.analise_notebook)
        
        self.analise_notebook.add(self.tab_analise_tabelas_graph, text="GRAFICOS")
        # self.analise_notebook.add(self.tab_analise_over25, text="OVER 2.5")
        # self.analise_notebook.add(self.tab_analise_over35, text="OVER 3.5")
        # self.analise_notebook.add(self.tab_analise_under15, text="UNDER 1.5")
        # self.analise_notebook.add(self.tab_analise_under25, text="UNDER 2.5")
        # self.analise_notebook.add(self.tab_analise_under35, text="UNDER 3.5")
        # self.analise_notebook.add(self.tab_analise_comparativa, text="Comparativa")
        
        # Preencher abas de análise
        self.preencher_aba_analise_mercado(self.tab_analise_tabelas_graph, "GRAFICOS")
        # self.preencher_aba_analise_mercado(self.tab_analise_over25, "over25")
        # self.preencher_aba_analise_mercado(self.tab_analise_over35, "over35")
        # self.preencher_aba_analise_mercado(self.tab_analise_under25, "under25")
        
    
    def preencher_aba_analise_mercado(self, parent, mercado):
        """Preenche a aba de análise para um mercado específico"""
        frame_selecao = ttk.LabelFrame(parent, text="Selecione o Gráfico")
        frame_selecao.pack(fill=tk.X, padx=5, pady=5)
        
        frame_grafico = ttk.LabelFrame(parent, text="Gráfico")
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        opcoes = [
            "Taxa de Ocorrência por Campeonato",
            "Taxa de Ocorrência por Hora",
            "Heatmap Campeonato x Hora",
            "Taxa de Ocorrência por Ciclo",
            "Heatmap Campeonato x Ciclo",
        ]
        
        cb_graficos = ttk.Combobox(
            frame_selecao,
            textvariable=self.grafico_selecionado,
            values=opcoes,
            state="readonly",
            width=40)
        cb_graficos.current(0)
        # cb_graficos.pack(side=tk.LEFT, padx=10, pady=5)
        
        btn_exibir = ttk.Button(
            frame_selecao,
            text="Criar Gráfico",
            command=lambda: self.display(mercado, frame_grafico))
        btn_exibir.pack(fill=tk.NONE, side='left', padx=5, pady=5)
        
        self.image_label = ttk.Label(frame_grafico)
        self.image_label.pack(fill=tk.BOTH, expand=True)


    def display(self, mercado, frame):
        try:
            # Clear previous widgets in frame
            # for widget in frame.winfo_children():
            #     widget.destroy()
                
            # Get the plot image
            self.service.run_plotting_service()
            # if not image_path:
            #     return
                
            # # Create scrollable canvas
            # canvas = tk.Canvas(frame)
            # scroll_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
            # scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            # canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

            # scroll_x.pack(side="bottom", fill="x")
            # scroll_y.pack(side="right", fill="y")
            # canvas.pack(side="left", fill="both", expand=True)

            # # Load and display image
            # img = Image.open(image_path)
            # self.current_image = ImageTk.PhotoImage(img)
            
            # canvas.create_image(0, 0, image=self.current_image, anchor="nw")
            # canvas.config(scrollregion=canvas.bbox("all"))
            
            # # Clean up temporary file
            # os.unlink(image_path)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exibir imagem: {str(e)}")
   
    def preencher_aba_tabelas(self):
        """Preenche a aba de tabelas operacionais com uma tabela que se adapta ao DataFrame recebido"""
        # Frame principal para a tabela
        self.tabela_frame = ttk.Frame(self.tab_tabelas)
        self.tabela_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        self.hscroll = ttk.Scrollbar(self.tabela_frame, orient=tk.HORIZONTAL)
        self.vscroll = ttk.Scrollbar(self.tabela_frame, orient=tk.VERTICAL)
        
        # Treeview - colunas serão definidas dinamicamente
        self.treeview_tabela = ttk.Treeview(
            self.tabela_frame,
            show="headings",
            xscrollcommand=self.hscroll.set,
            yscrollcommand=self.vscroll.set
        )
        
        # Configurar scrollbars
        self.vscroll.config(command=self.treeview_tabela.yview)
        self.hscroll.config(command=self.treeview_tabela.xview)
        
        # Posicionar widgets
        self.treeview_tabela.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll.grid(row=1, column=0, sticky="ew")
        
        # Configurar expansão
        self.tabela_frame.grid_rowconfigure(0, weight=1)
        self.tabela_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para botões
        btn_frame = ttk.Frame(self.tab_tabelas)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botões
        ttk.Button(
            btn_frame, 
            text="Carregar Dados", 
            command=lambda: self.carregar_dados_na_tabela()
        ).pack(side=tk.LEFT, padx=5)

    def carregar_dados_na_tabela(self):
        """Carrega dados do DataFrame na treeview, adaptando-se às colunas existentes"""
        try:
            # Limpar treeview existente
            self.treeview_tabela.delete(*self.treeview_tabela.get_children())
            file_path = filedialog.askopenfilename(title="Selecione a Tabla ", filetypes=[("Todos os Arquivos", "*.*")])
        
            # Obter DataFrame do serviço
            df = pd.read_csv(file_path)  # Supondo que este método retorna o DataFrame
            
            if df is None or df.empty:
                messagebox.showwarning("Aviso", "Nenhum dado disponível para exibir")
                return
                
            # Configurar colunas dinamicamente
            colunas = df.columns.tolist()
            self.treeview_tabela["columns"] = colunas
            
            # Configurar cabeçalhos e larguras das colunas
            for col in colunas:
                # Converter nomes de colunas para formato mais amigável
                col_name = col.replace("_", " ").title()
                self.treeview_tabela.heading(col, text=col_name)
                
                # Definir largura baseada no tipo de dado
                if df[col].dtype in ['int64', 'float64']:
                    width = 80  # Colunas numéricas mais estreitas
                else:
                    width = 120  # Colunas de texto mais largas
                    
                self.treeview_tabela.column(col, width=width, anchor=tk.CENTER)
            
            # Inserir dados
            for _, row in df.iterrows():
                values = []
                for col in colunas:
                    value = row[col]
                    # Formatando valores numéricos para 2 casas decimais
                    if isinstance(value, (float, np.floating)):
                        values.append(f"{value:.2f}" if not pd.isna(value) else "")
                    else:
                        values.append(str(value) if not pd.isna(value) else "")
                
                self.treeview_tabela.insert("", tk.END, values=values)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")
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
        
        # for i, (mercado, var) in enumerate(self.mercados_selecionados.items()):
        #     ttk.Checkbutton(frame_mercados, text=mercado, variable=var).grid(
        #         row=0, column=i, padx=10, pady=5)
        
        
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
            ("EURO", "EURO"),
            ("SUPER", "SUPER"),
            ("PREMIER", "PREMIER"),
            ("COPA", "COPA"),
        ]
        
        # Create tabs dynamically
        self.market_frames = {}
        for market_id, market_name in markets:
            frame = ttk.Frame(self.previsoes_notebook)
            self.predictions_tree_frame = frame
            self.previsoes_notebook.add(frame, text=market_name)
            self.market_frames[market_id] = frame
            self._create_market_tab(frame, market_name)
        btn_frame = ttk.Frame(self.previsoes_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        butn = ttk.Button(btn_frame, text='Gerar Previsões', command=lambda:self.execute_foreach(frame))
        butn.pack(side=tk.LEFT, padx=2)
    def execute_foreach(self, frame):
        
        self.service.gerar_previsoes(
            self.hora_atual.get(),
            self.num_horas.get(),
            self.market_frames,
            self.create,
            self.train,
            self.current_file.get(),
            self.current_model_file.get(),
        )

    def _create_market_tab(self, parent, market_id):
        """Creates UI elements for a specific market tab"""
        # Main container
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.predictions_tree_frame = tree_frame
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        mercados = [
            "Odd BTTS",
            "Odd Over 2.5",
            "Odd Over 3.5",
            "Odd Under 2.5",
            "Odd Under 3.5",
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
        
        """Gera previsões para os mercados selecionados"""
        hora_atual = self.hora_atual.get()
        num_horas = self.num_horas.get()
        # tree_to_view = getattr(self, f"treeview_{market_id}")
        self.status_label.config(text="Gerando previsões...")
        self.root.update()
        # self.pred_treeview = tree_to_view
        action_buttons = [
            ("", )
        ]
        
        # butn = ttk.Button(btn_frame, text='Gerar Previsões', command=lambda: self.service.gerar_previsoes(
        #     self.hora_atual.get(),
        #     self.num_horas.get(),
        #     tree_frame,
        #     market_id,
        #     self.create,
        #     self.train,
        #     self.current_file.get(),
        #     self.current_model_file.get()
            
        # ))
        # butn.pack(side=tk.LEFT, padx=2)

    def delete_flag(self):
        if os.path.exists('flag.txt'):
            os.remove('flag.txt')
            print("File deleted.")
        else:
            print("File does not exist.")   
            
    def creates_flag(self):
        with open("flag.txt", "w") as f:
            pass  # creates an empty file   
        
    def run_prediction_job(self):
        hours = [0, 6, 12, 18, 20]
        now = datetime.now()
        current_hour = now.hour
        # frame = ttk.Frame(self.previsoes_notebook)
        # self._create_market_tab(frame, 'market_name')
        if current_hour in hours:
            if self.last_prediction_hour != current_hour:
                print(f"Running prediction at {current_hour}")
                self.service.gerar_previsoes(
                    self.hora_atual.get(),
                    self.num_horas.get(),
                    self.market_frames,
                    self.create,
                    self.train,
                    self.current_file.get(),
                    self.current_model_file.get(),
                )
                self.last_prediction_hour = current_hour
            else:
                print("Already ran for this hour.")
        else:
            self.last_prediction_hour = None  # Allow run in next valid hour
            




def app_main():
    root = tk.Tk()
    app = AppView(root)
    root.mainloop()
    

if __name__ == "__main__":
    app_main()
