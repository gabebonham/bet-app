import sys
import os
import pandas as pd
import seaborn as sns
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.service import Service
from view.graphs.visualizer import BetMarketVisualizer
class Graph:
    def __init__(self):
        self.service = Service()
        self.visulizer = BetMarketVisualizer()
        self.current_image = ''
        self.grafico_selecionado = tk.StringVar()
    def exibir_grafico(self, mercado, grafico):
        """Exibe gráficos adaptando-se às colunas disponíveis"""
        try:
            
            
            df_path = filedialog.askopenfilename(title="Selecione um Arquivo", filetypes=[("Todos os Arquivos", "*.*")])
            if not df_path:
                return
            df = pd.read_csv(df_path)
            
            if df is None or df.empty:
                messagebox.showwarning("Aviso", "Nenhum dado disponível para análise")
                return

           
            colunas_disponiveis = set(df.columns.str.upper())
            required_cols = {
                'Taxa de Ocorrência por Campeonato': {'CAMPEONATO', 'OCORRENCIA'},
                'Taxa de Ocorrência por Hora': {'HORA', 'OCORRENCIA'},
                'Taxa de Ocorrência por Ciclo': {'CICLO', 'OCORRENCIA'},  # New option
                'Heatmap Campeonato x Hora': {'CAMPEONATO', 'HORA', 'OCORRENCIA'},
                'Heatmap Campeonato x Ciclo': {'CAMPEONATO', 'CICLO', 'OCORRENCIA'}  # New option
            }
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
            

            output_file = None
            if grafico == "Taxa de Ocorrência por Campeonato":
                output_file = self.visulizer.plot_occurrence_by_championship(df, mercado)
            elif grafico == "Taxa de Ocorrência por Hora":
                output_file = self.visulizer.plot_occurrence_by_hour(df, mercado)
            elif grafico == "Taxa de Ocorrência por Ciclo":
                output_file = self.visulizer.plot_occurrence_by_cycle(df, mercado)
            elif grafico == "Heatmap Campeonato x Hora":
                output_file = self.visulizer.plot_heatmap_championship_hour(df, mercado)
            elif grafico == "Heatmap Campeonato x Ciclo":
                output_file = self.visulizer.plot_heatmap_championship_cycle(df, mercado)
            else:
                messagebox.showerror("Erro", f"Tipo de gráfico não suportado: {grafico}")
                return
        
            return output_file
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha inesperada: {str(e)}")
    

    def _display_image(self, image_path, frame):
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
            

        except Exception as e:
            pass
    def exibir_grafico_comparativo(self, grafico):
        """Exibe um gráfico comparativo entre mercados"""
        df_path = filedialog.askopenfilename(title="Selecione um Arquivo", filetypes=[("Todos os Arquivos", "*.*")])
        if not df_path:
            return
        arquivo = None
        # Mapear nome do gráfico para arquivo
        mapeamento = {
            "Comparação de Taxas entre Mercados": "../analise_over35/graficos/comparacao_mercados.png",
            "Comparação de Ciclos entre Mercados": "../analise_over35/graficos/comparacao_ciclos_mercados.png"
        }
        df = pd.read_csv(df_path)
        if grafico == 'Comparação de Ciclos entre Mercados': arquivo = self.visulizer.plot_cycle_comparison(df)
        if grafico == 'Comparação de Taxas entre Mercados': arquivo = self.visulizer.plot_market_comparison(df)
        
        print(arquivo)
        if not arquivo or not os.path.exists(arquivo):
            messagebox.showerror("Erro", f"Gráfico não encontrado: {arquivo}")
            return
        
        try:
            return arquivo
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir gráfico: {str(e)}")
    
    