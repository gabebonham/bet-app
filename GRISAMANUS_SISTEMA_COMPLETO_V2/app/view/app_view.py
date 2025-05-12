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
        self.service = Service()
        self.graph = Graph()
        self.visualizer = BetMarketVisualizer()
        # Variáveis para valores de stake
        self.stake_alta = tk.DoubleVar(value=25.0)
        self.stake_media = tk.DoubleVar(value=15.0)
        self.stake_baixa = tk.DoubleVar(value=5.0)
        # Variáveis para níveis de confiança
        self.nivel_alta = tk.DoubleVar(value=0.70)
        self.nivel_media = tk.DoubleVar(value=0.60)
        self.nivel_baixa = tk.DoubleVar(value=0.50)
        # Criar estrutura principal
        self.criar_estrutura()
        self.current_image = ''
        self.image_label = tk.Label(root)
        self.label_grafico_comparativo = tk.Label(root)
        self.grafico_selecionado = tk.StringVar()
        # Inicializar variáveis
        self.hora_atual = tk.IntVar(value=datetime.now().hour)
        self.num_horas = tk.IntVar(value=3)
        self.mercados_selecionados = {
            "BTTS": tk.BooleanVar(value=True),
            "OVER 2.5": tk.BooleanVar(value=True),
            "OVER 3.5": tk.BooleanVar(value=True)
        }
        self.current_graph = ''
        self.grafico_comparativo_selecionado = tk.StringVar()
        # Preencher interface
        self.preencher_interface()
    def atualizar_datetime(self):
        """Atualiza o label de data e hora"""
        self.datetime_label.config(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.root.after(1000, self.atualizar_datetime)
    def carregar_configuracoes(self):
        """Carrega as configurações salvas"""
        try:
            config = self.service.carregar_configuracoes()
            
            # Atualizar os valores da interface
            self.stake_alta.set(config["stake"]["ALTA"])
            self.stake_media.set(config["stake"]["MEDIA"])
            self.stake_baixa.set(config["stake"]["BAIXA"])
            
            self.nivel_alta.set(config["niveis_confianca"]["ALTA"])
            self.nivel_media.set(config["niveis_confianca"]["MEDIA"])
            self.nivel_baixa.set(config["niveis_confianca"]["BAIXA"])
            
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
        ttk.Spinbox(frame_stake, from_=1, to=100, increment=1, textvariable=self.stake_alta.get(), 
                   width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_stake, text="Confiança MÉDIA:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_stake, from_=1, to=100, increment=1, textvariable=self.stake_media.get(), 
                   width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_stake, text="Confiança BAIXA:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_stake, from_=1, to=100, increment=1, textvariable=self.stake_baixa.get(), 
                   width=10).grid(row=2, column=1, padx=5, pady=5)
        
        # Configurações de níveis de confiança
        frame_confianca = ttk.LabelFrame(frame_config, text="Níveis de Confiança")
        frame_confianca.pack(fill=tk.X, padx=5, pady=5)
        
        
        
        # Widgets para configuração de níveis de confiança
        ttk.Label(frame_confianca, text="ALTA (>):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_confianca, from_=0.5, to=1.0, increment=0.01, textvariable=self.nivel_alta.get(), 
                   width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_confianca, text="MÉDIA (>):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_confianca, from_=0.5, to=1.0, increment=0.01, textvariable=self.nivel_media.get(), 
                   width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_confianca, text="BAIXA (>):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(frame_confianca, from_=0.5, to=1.0, increment=0.01, textvariable=self.nivel_baixa.get(), 
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

    def display(self, mercado,frame ):
        image_path = ''
        if mercado:
            image_path = self.graph.exibir_grafico(mercado,self.grafico_selecionado.get())
        else:
            image_path = self.graph.exibir_grafico_comparativo(self.grafico_comparativo_selecionado.get())
        """Display the generated image in the GUI"""
        try:
            
            self.image_label.destroy()
            self.image_label = ttk.Label(frame)
            # Load and display new image
            img = Image.open(image_path)  # Use the parameter instead of hardcoded path
            img = img.resize((600, 400), Image.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image)
            self.image_label.image = self.current_image  # Keep a referenc
            self.current_graph = self.image_label
            self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            self.label_grafico_comparativo.destroy()
            self.label_grafico_comparativo = ttk.Label(frame)
            # Load and display new image
            img = Image.open(image_path)  # Use the parameter instead of hardcoded path
            img = img.resize((600, 400), Image.LANCZOS)
            current_img = ImageTk.PhotoImage(img)
            self.label_grafico_comparativo.config(image=current_img)
            self.label_grafico_comparativo.image = current_img  # Keep a referenc
            self.current_graph = self.label_grafico_comparativo
            self.label_grafico_comparativo.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            

            # img = Image.open(arquivo)
            # img = img.resize((800, 500), Image.LANCZOS)
            # photo = ImageTk.PhotoImage(img)
            # print('exibir_grafico_comparativo')
            # # Exibir imagem
            # self.label_grafico_comparativo.config(image=photo)
            # self.label_grafico_comparativo.image = photo  # Manter referência
            
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
        
        # Botão de gerar previsões
        ttk.Button(self.control_frame, text="Gerar Previsões", 
                  command=lambda:self.service.processar_previsoes()).pack(side=tk.RIGHT, padx=10, pady=5)
    
    def preencher_aba_previsoes(self):
        """Preenche a aba de previsões"""
        # Frame para exibir previsões
        self.previsoes_frame = ttk.Frame(self.tab_previsoes)
        self.previsoes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Notebook para separar previsões por mercado
        self.previsoes_notebook = ttk.Notebook(self.previsoes_frame)
        self.previsoes_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas para cada mercado
        self.tab_btts = ttk.Frame(self.previsoes_notebook)
        self.tab_over25 = ttk.Frame(self.previsoes_notebook)
        self.tab_over35 = ttk.Frame(self.previsoes_notebook)
        self.tab_under25 = ttk.Frame(self.previsoes_notebook)
        self.tab_under35 = ttk.Frame(self.previsoes_notebook)
        self.tab_under15 = ttk.Frame(self.previsoes_notebook)
        
        self.previsoes_notebook.add(self.tab_btts, text="BTTS")
        self.previsoes_notebook.add(self.tab_over25, text="OVER 2.5")
        self.previsoes_notebook.add(self.tab_over35, text="OVER 3.5")
        self.previsoes_notebook.add(self.tab_under15, text="UNDER 1.5")
        self.previsoes_notebook.add(self.tab_under25, text="UNDER 2.5")
        self.previsoes_notebook.add(self.tab_under35, text="UNDER 3.5")
        
        
        
    
    def criar_treeview_previsoes(self, treeview):
        """Preenche a aba de previsões com notebooks para cada mercado"""
        # Main frame
        self.previsoes_frame = ttk.Frame(self.tab_previsoes)
        self.previsoes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Notebook (tabbed interface)
        self.previsoes_notebook = ttk.Notebook(self.previsoes_frame)
        self.previsoes_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for all markets
        markets = [
            ("btts", "BTTS"),
            ("over25", "OVER 2.5"),
            ("over35", "OVER 3.5"), 
            ("under15", "UNDER 1.5"),
            ("under25", "UNDER 2.5"),
            ("under35", "UNDER 3.5")
        ]
        
        # Create tabs dynamically
        self.market_frames = {}
        for market_id, market_name in markets:
            frame = ttk.Frame(self.previsoes_notebook)
            self.previsoes_notebook.add(frame, text=market_name)
            self.market_frames[market_id] = frame
            self._create_market_tab(frame, market_id)
        
        # Add refresh button
        refresh_btn = ttk.Button(
            self.previsoes_frame, 
            text="Atualizar Todas as Previsões",
            command=lambda:self.service._refresh_all_predictions(self.hora_atual.get(),self.num_horas.get(), self.pred_treeview)
        )
        refresh_btn.pack(side=tk.BOTTOM, pady=5)

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
        
        columns = [
            ("CAMPEONATO", "Campeonato", 120),
            ("PARTIDA", "Partida", 150),
            ("HORA", "Hora", 80),
            ("PROB.", "Probabilidade", 100),
            ("CONF.", "Confiança", 80),
            ("STAKE", "Stake", 60),
            ("ODD", "Odd", 60),
            ("RESULT.", "Resultado", 80),
            ("GALE", "Gale", 60)
        ]
        
        treeview = ttk.Treeview(
            tree_frame,
            columns=[col[0] for col in columns],
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )
        
        # Configure columns
        for col_id, heading, width in columns:
            treeview.column(col_id, width=width, anchor=tk.CENTER)
            treeview.heading(col_id, text=heading)
        
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=treeview.yview)
        
        # Store reference
        setattr(self, f"treeview_{market_id}", treeview)
        
        # Button panel
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=5)
        """Gera previsões para os mercados selecionados"""
        hora_atual = self.hora_atual.get()
        num_horas = self.num_horas.get()
        tree_to_view = getattr(self, f"treeview_{market_id}")
        self.status_label.config(text="Gerando previsões...")
        self.root.update()
        self.pred_treeview = tree_to_view
        action_buttons = [
            ("Ver Previsões", lambda m=market_id: self.service.gerar_previsoes(hora_atual,num_horas,market_id,tree_to_view)),
            ("Exportar CSV", lambda m=market_id: self.service.exportar_dados_csv(tree_to_view)),
            ("Exportar PDF", lambda m=market_id: self.service.exportar_pdf(tree_to_view, market_id)),
            ("Limpar", lambda m=market_id: self.service.limpar_treeview(tree_to_view))
        ]
        
        for btn_text, cmd in action_buttons:
            ttk.Button(btn_frame, text=btn_text, command=cmd).pack(side=tk.LEFT, padx=2)





def main():
    root = tk.Tk()
    app = AppView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
