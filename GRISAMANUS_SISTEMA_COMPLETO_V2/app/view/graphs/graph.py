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
            self.service.load_data()
            # 1. Verificar inputs e carregar dados
            if not hasattr(self, 'grafico_selecionado'):
                messagebox.showerror("Erro", "Controle gráfico_selecionado não encontrado")
                return
                
            
            if not grafico:
                messagebox.showerror("Erro", "Nenhum tipo de gráfico selecionado")
                return

            df = self.service.df_table
            
            if df is None or df.empty:
                messagebox.showwarning("Aviso", "Nenhum dado disponível para análise")
                return

            # 2. Mapear nomes de colunas alternativos
            col_mapping = {
                'Ocorrencia': 'OCORRENCIA',
                'Hora': 'HORA',
                'Campeonato': 'Campeonato'
            }

            # Rename columns if needed
            for alt_name, correct_name in col_mapping.items():
                if alt_name in df.columns and correct_name not in df.columns:
                    df = df.rename(columns={alt_name: correct_name})

            # 3. Verificar colunas disponíveis
            # In your exibir_grafico method, update these parts:

            # 2. Mapear nomes de colunas alternativos
            col_mapping = {
                'Ocorrencia': 'OCORRENCIA',
                'Hora': 'HORA',
                'Ciclo': 'CICLO',  # Add mapping for ciclo
                'Campeonato': 'Campeonato'
            }

            # 3. Verificar colunas disponíveis
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
            # 4. Verificar se o gráfico solicitado é possível
            if grafico in required_cols:
                missing = [c for c in required_cols[grafico] 
                        if c not in colunas_disponiveis]
                if missing:
                    messagebox.showerror(
                        "Erro", 
                        f"Não é possível gerar '{grafico}'\n"
                        f"Colunas faltando: {', '.join(missing)}\n"
                        f"Colunas disponíveis: {', '.join(sorted(df.columns))}"
                    )
                    print(
                        "Erro", 
                        f"Não é possível gerar '{grafico}'\n"
                        f"Colunas faltando: {', '.join(missing)}\n"
                        f"Colunas disponíveis: {', '.join(sorted(df.columns))}"
                    )
                    return

            # 5. Criar visualizador e gerar gráfico
            
            
            # Ensure hour column exists
            if 'HORA' not in df.columns and 'Tempo' in df.columns:
                df['HORA'] = pd.to_datetime(df['Tempo'], format='%H:%M').dt.hour
            # Label para exibir o gráfico - use the main image_label
            
            # Call appropriate visualization method
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
            

            # img = Image.open(arquivo)
            # img = img.resize((800, 500), Image.LANCZOS)
            # photo = ImageTk.PhotoImage(img)
            # print('exibir_grafico_comparativo')
            # # Exibir imagem
            # self.label_grafico_comparativo.config(image=photo)
            # self.label_grafico_comparativo.image = photo  # Manter referência
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exibir imagem: {str(e)}")
    def exibir_grafico_comparativo(self, grafico):
        """Exibe um gráfico comparativo entre mercados"""
        self.service.load_data()
        arquivo = None
        # Mapear nome do gráfico para arquivo
        mapeamento = {
            "Comparação de Taxas entre Mercados": "../analise_over35/graficos/comparacao_mercados.png",
            "Comparação de Ciclos entre Mercados": "../analise_over35/graficos/comparacao_ciclos_mercados.png"
        }
        df = self.service.df_pred
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
    
    