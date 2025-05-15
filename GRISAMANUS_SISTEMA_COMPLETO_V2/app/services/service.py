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

from services.file_util import get_most_recent_file, get_most_recent_file_prev
from ml.implementacao_drisamanus_corrigida import execute, create_dated_filename
from ml.betting_config import BettingConfig

class Service:
    def __init__(self):
        self.df_btts = pd.DataFrame()  # BTTS market data
        self.df_prev = pd.DataFrame()  # Over 2.5 goals
        self.df_table = pd.DataFrame()  # Over 3.5 goals
        self.df_pred = pd.DataFrame()
        self.betconfig = BettingConfig()
        self.current_file = None
        self.current_model_file = None
        self.x_path = None
        self.y_path = None
        self.mercados_selecionados = [
            "BTTS",
            "OVER 2.5",
            "OVER 3.5",
            "UNDER 1.5",
            "UNDER 2.5",
            "UNDER 3.5",
        ]
        self.current_y_table_file = None
        # Variáveis para valores de stake
        self.stake_alta = tk.DoubleVar(value=self.betconfig.stake_alta_pct)
        self.stake_media =tk.DoubleVar(value=self.betconfig.stake_media_pct)
        self.stake_baixa =tk.DoubleVar(value=self.betconfig.stake_baixa_pct)
        # Variáveis para n# Variáveis para
        self.nivel_alta = tk.DoubleVar(value=self.betconfig.conf_alta )
        self.nivel_media =tk.DoubleVar(value=self.betconfig.conf_media_min)
        self.nivel_baixa =tk.DoubleVar(value=self.betconfig.conf_baixa_min)
        self.current_table_input_file =None
        self.current_table_file =None
        self.old_x_path = None
        self.old_y_path = None
        self.train = tk.BooleanVar(value=True)
        self.create = tk.BooleanVar(value=True)
    def gerar_previsoes(self, hora_atual, num_horas, tree_frame, mercado, create, train):
        """
        Gera previsões para os mercados selecionados e popula os treeviews correspondentes.
        """
        if (self.x_path and not self.y_path) or (not self.x_path and self.y_path):
            messagebox.showerror('Erro','Se dados de treino ou de compare forem selecionados, o outro tambem deve ser selecionado.')
            return
        for widget in tree_frame.winfo_children():
            widget.destroy()
        self.rodar_previsao(create, train,horas=hora_atual, max=num_horas)
        self.current_table_file = None
        self.load_data(True)
        df = self.df_prev
        df_filtrado = df
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        
        tree = ttk.Treeview(tree_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        if mercado == "BTTS":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        elif mercado == "OVER 2.5":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        elif mercado == "OVER 3.5":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        elif mercado == "UNDER 1.5":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        elif mercado == "UNDER 2.5":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        elif mercado == "UNDER 3.5":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        elif mercado == "MERCADOS":
            self.populate_treeview(tree, df_filtrado,scroll_y,scroll_x)
        

    def filter_by_time(self, df, hora_atual, num_horas):
        """Filter dataframe rows where HORA is within the next num_horas from hora_atual."""
        try:
            df = df.copy()  # Prevent SettingWithCopyWarning
            
            # Try converting 'HORA' to hour if it's not numeric
            if df['HORA'].dtype == 'O':  # object, likely string
                df['HORA'] = pd.to_datetime(df['HORA'], format='%H:%M', errors='coerce').dt.hour

            df['HORA'] = pd.to_numeric(df['HORA'], errors='coerce')

            hora_min = hora_atual
            hora_max = hora_atual + num_horas

            print("Filtering between", hora_min, "and", hora_max)
            print("Before filtering, df shape:", df.shape)

            df_filtered = df[df['HORA'] >= hora_min]
            df_filtered = df[df_filtered['HORA'] <= hora_max]

            print("After filtering, df shape:", df_filtered.shape)

            return df

        except Exception as e:
            print(f"Error in filter_by_time: {e}")
            return df

    def populate_treeview(self, tree, filtered_df,scroll_y,scroll_x):
        
        # Carrega os dados do CSV
        df = filtered_df

        # Limpa a tabela atual
        for item in tree.get_children():
            tree.delete(item)

        # Define novas colunas com base no CSV
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        # Define o cabeçalho das colunas
        for coluna in df.columns:
            tree.heading(coluna, text=coluna)
            tree.column(coluna, anchor="center", width=100)

        # Insere as linhas na tabela
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        
        tree.pack(fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

                


    # Specific filter functions
    def filter_over25(self,tree, df, hora_atual=0, num_horas=24):
        # Your filtering logic here
        df_filtered = df[(df['MERCADO'] == 'OVER 2.5')]  # Simplified example
        # Add any other filters like HORA range
        return df_filtered

    def filter_over35(self,tree, df, hora_atual=0, num_horas=24):
        # Your filtering logic here
        df_filtered = df[(df['MERCADO'] == 'OVER 3.5')]  # Simplified example
        # Add any other filters like HORA range
        return df_filtered

    def filter_under25(self,tree, df, hora_atual=0, num_horas=24):
        # Your filtering logic here
        df_filtered = df[(df['MERCADO'] == 'UNDER 2.5')]  # Simplified example
        # Add any other filters like HORA range
        return df_filtered

    def filter_under35(self,tree, df, hora_atual=0, num_horas=24):
        # Your filtering logic here
        df_filtered = df[(df['MERCADO'] == 'UNDER 3.5')]  # Simplified example
        # Add any other filters like HORA range
        return df_filtered

    def filter_under15(self,tree, df, hora_atual=0, num_horas=24):
        # Your filtering logic here
        df_filtered = df[(df['MERCADO'] == 'UNDER 1.5')]  # Simplified example
        # Add any other filters like HORA range
        return df_filtered

    def filter_btts(self,tree, df, hora_atual=0, num_horas=24):
        # Your filtering logic here
        df_filtered = df[(df['MERCADO'] == 'BTTS')]  # Simplified example
        # Add any other filters like HORA range
        return df_filtered
    
    def load_data(self,flag=False):
        if flag:
            if self.current_table_file:
                self.df_prev = pd.read_csv(self.current_table_file)
            else:
                self.df_prev = pd.read_csv(get_most_recent_file_prev('pred','../generated'))
            return
        if self.current_table_file:
            df = pd.read_csv(self.current_table_file)
        else:
            df = pd.read_csv(get_most_recent_file_prev('pred','../generated'))
        
        df['OCORRENCIA'] = (df['Gols time casa'] > 0) & (df['Gols time contra'] > 0)
          
        self.df_btts = df.copy()
        self.df_prev = df.copy()
    
        self.df_table = df.copy()
        self.df_pred = df.copy()
        # Convert columns if needed
        
        self.df_btts['CICLO'] = pd.to_datetime(self.df_pred['Tempo'], format='%H:%M').dt.minute.apply(
            lambda x: '1st Half' if x <= 45 else '2nd Half')
        self.df_pred['CICLO'] = pd.to_datetime(self.df_pred['Tempo'], format='%H:%M').dt.minute.apply(
            lambda x: '1st Half' if x <= 45 else '2nd Half')
        self.df_table['CICLO'] = pd.to_datetime(self.df_pred['Tempo'], format='%H:%M').dt.minute.apply(
            lambda x: '1st Half' if x <= 45 else '2nd Half')
        self.df_btts['HORA'] = pd.to_datetime(self.df_btts['Tempo'], format='%H:%M').dt.hour
        self.df_pred['HORA'] = pd.to_datetime(self.df_pred['Tempo'], format='%H:%M').dt.hour
        self.df_table['HORA'] = pd.to_datetime(self.df_table['Tempo'], format='%H:%M').dt.hour
        
        
    def carregar_previsoes(self):
        try:
            df = self.df_pred
            self.load_data(True)
            # Limpa a tabela
            for item in self.treeview_tabela.get_children():
                self.treeview_tabela.delete(item)

            # Insere previsões na tabela
            for _, row in df.iterrows():
                self.treeview_tabela.insert("", tk.END, values=(
                    row['HORA'],
                    row['CAMPEONATO'],
                    row['COLUNA'],
                    f"{row['PRED_PROB']:.2f}"
                ))

            # Atualiza status
            self.status_label.config(text="Previsões carregadas na tabela")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar previsões: {str(e)}")
    
    

    

    

    
    def extrair_features_match(df):
        """
        Extrai features relevantes do dataframe de partidas.
        """
        features = []
        try:

            for index, row in df.iterrows():
                # Features we might extract (you can expand this)
                time_casa = row['Time da casa']
                time_contra = row['Time contra']
                gols_time_casa = row['Gols time casa']
                gols_time_contra = row['Gols time contra']
                odd_over_2_5 = row['Odd Over 2.5']
                odd_under_2_5 = row['Odd Under 2.5']
                odd_over_3_5 = row['Odd Over 3.5']
                odd_under_3_5 = row['Odd Under 3.5']
                odd_casa_vence = row['Odd Casa Vence']
                odd_empate = row['Odd Empate']
                odd_visitante_vence = row['Odd Visitante Vence']
                
                # Example of extracting the total goals
                total_gols = gols_time_casa + gols_time_contra
                
                # Combine features into a dictionary
                features.append({
                    'TIME_CASA': time_casa,
                    'TIME_CONTRA': time_contra,
                    'GOLS_TIME_CASA': gols_time_casa,
                    'GOLS_TIME_CONTRA': gols_time_contra,
                    'TOTAL_GOLS': total_gols,
                    'ODD_OVER_2_5': odd_over_2_5,
                    'ODD_UNDER_2_5': odd_under_2_5,
                    'ODD_OVER_3_5': odd_over_3_5,
                    'ODD_UNDER_3_5': odd_under_3_5,
                    'ODD_CASA_VENCE': odd_casa_vence,
                    'ODD_EMPATE': odd_empate,
                    'ODD_VISITANTE_VENCE': odd_visitante_vence
                })
            
            # Return as a DataFrame for easier manipulation
            return pd.DataFrame(features)
        except Exception as e:
            print(e)

    def rodar_previsao(self, create, train, horas, max):
        """Executa a previsão com base no modelo treinado"""
        execute(max=max,hora=horas, config=self.get_current_config(),input_csv=self.current_table_file,actuals_path=f'../generated/actuals_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv',pred_path=f'../generated/pred_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv', model_path=self.current_model_file,x_path=self.x_path,y_path=self.y_path,train=train,create=create)
            
          
        messagebox.showinfo("Sucesso", 'Previsões criadas.')
    def get_current_config(self):
        """Helper method to extract current config"""
        return {
            "conf_alta": self.nivel_alta.get(),
            "conf_media_min": self.nivel_media.get(),
            "conf_baixa_min": self.nivel_baixa.get(),
            "stake_alta_pct": self.stake_alta.get(),
            "stake_media_pct": self.stake_media.get(),
            "stake_baixa_pct": self.stake_baixa.get(),
            "stake_base": 20.00,
            "conf_media_max": self.nivel_media.get(),
            "conf_baixa_max": self.nivel_baixa.get()
        }
    
    def processar_previsoes(self):
        execute(self.get_current_config(),input_csv=self.current_table_file,actuals_path=self.current_table_file,pred_path=f'../generated/pred_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv',history_path=f'../generated/historico_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv', model_path=self.current_model_file,x_path=f'../generated/x_in_novo_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv',y_path=f'../generated/y_out_novo_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv',x_old_path=self.old_x_path+'.csv',y_old_path=self.old_y_path+'.csv',train=self.train.get(),create=self.create.get())
            
        messagebox.showinfo(title='Sucesso',message='Previsões geradas com sucesso.')
    

    def _refresh_all_predictions(self, hora_atual, num_horas,treeview):
        """Refresh predictions for all markets"""
        
        for market_id in ['btts', 'over25', 'over35', 'under15', 'under25', 'under35']:
            try:
                self.gerar_previsoes(hora_atual, num_horas, market_id,treeview)
            except Exception as e:
                print(f"Erro ao atualizar {market_id}: {str(e)}")
        messagebox.showinfo("Sucesso", "Previsões geradas com sucesso!")
        
        
    def clear_treeview(self, tree):
        """Clear all items from a treeview"""
        tree.delete(*tree.get_children())
    
    
    
    
    
    def load_filtered_data(self, hora_atual=None, num_horas=None):
        """Load and filter the prediction data"""
        try:
            df = pd.read_csv(get_most_recent_file('pred', 'generated'))
            
            # Convert and filter by time if parameters provided
            if hora_atual is not None and num_horas is not None:
                df['HORA'] = pd.to_datetime(df['Tempo'], format='%H:%M').dt.hour
                df = df[(df['HORA'] >= hora_atual) & 
                    (df['HORA'] <= hora_atual + num_horas)]
            
            return df
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    def get_market_predictions(self, market_id, hora_atual=None, num_horas=None):
        """Generate predictions for the specified market"""
        try:
            # 1. Load and filter the data
            df = self.load_filtered_data(hora_atual, num_horas)
            
            # 2. Market-specific calculations
            predictions = []
            
            if market_id == "btts":
                df['probability'] = 1 / df['Odd BTTS']
                df['prediction'] = (df['Gols time casa'] > 0) & (df['Gols time contra'] > 0)
            elif market_id == "over25":
                df['probability'] = 1 / df['Odd Over 2.5']
                df['prediction'] = df['Gols totais'] > 2.5
            elif market_id == "over35":
                df['probability'] = 1 / df['Odd Over 3.5']
                df['prediction'] = df['Gols totais'] > 3.5
            elif market_id == "under15":
                df['probability'] = 1 / df['Odd Under 1.5'] if 'Odd Under 1.5' in df.columns else (1 - (df['Gols totais']/1.5))
                df['prediction'] = df['Gols totais'] < 1.5
            elif market_id == "under25":
                df['probability'] = 1 / df['Odd Under 2.5']
                df['prediction'] = df['Gols totais'] < 2.5
            elif market_id == "under35":
                df['probability'] = 1 / df['Odd Under 3.5']
                df['prediction'] = df['Gols totais'] < 3.5
            
            # 3. Format the results
            for _, row in df.iterrows():
                predictions.append({
                    'league': row['Campeonato'],
                    'home_team': row['Time da casa'],
                    'away_team': row['Time contra'],
                    'time': row['Tempo'],
                    'probability': row['probability'],
                    'confidence': "High" if row['probability'] > 0.7 else ("Medium" if row['probability'] > 0.5 else "Low"),
                    'stake': self.calculate_stake(row['probability']),
                    'odds': row[f'Odd {market_id.replace("under","Under ").replace("over","Over ")}'],
                    'result': "",  # To be filled later
                    'gale': ""     # To be filled later
                })
            
            return predictions
            
        except Exception as e:
            print(f"Error generating {market_id} predictions: {str(e)}")
            return []
    
    
    def atualizar_dados_partidas(self, treeview):
        """Atualiza os dados das partidas"""
        
        try:
            self.carregar_dados_partidas(treeview)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {str(e)}")
    
    def carregar_dados_partidas(self, treeview_tabela):
        """Carrega os dados das partidas na tabela"""
        try:
            from ml.implementacao_drisamanus_corrigida import generate_actuals
            file_path = filedialog.askopenfilename(title="Selecione um Arquivo", filetypes=[("Todos os Arquivos", "*.*")])
            # Limpar tabela existente
            for item in treeview_tabela.get_children():
                treeview_tabela.delete(item)
                
            # Carregar dados (substitua por sua fonte de dados real)
            dados = self.obter_dados_partidas(file_path)  # Implemente este método
            
            # Preencher tabela
            for partida in dados:
                treeview_tabela.insert("", tk.END, values=(
                    partida["id_da_partida"],
                    partida["campeonato"],
                    partida["data"],
                    partida["tempo"],
                    partida["time_da_casa"],
                    partida["time_contra"],
                    partida["gols_time_casa"],
                    partida["gols_time_contra"],
                    partida["gols_totais"],
                    partida["odd_over_25"],
                    partida["odd_under_25"],
                    partida["odd_over_35"],
                    partida["odd_under_35"],
                    partida["odd_casa_vence"],
                    partida["odd_empate"],
                    partida["odd_visitante_vence"],
                    partida["placar_exato"],
                    partida["odd_placar_exato"],
                    partida["data_das_odds"]
                ))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    def open_file(self, type, path):
        
        file_path = filedialog.askopenfilename(title="Selecione um Arquivo", filetypes=[("Todos os Arquivos", "*.*")])
        if type=='tabela':
            self.current_table_file = file_path
            
        if type=='modelo':
            self.current_model_file = file_path
        if type=='tabela_y':
            self.current_y_table_file = file_path
        if type=='x_file':
            self.x_path = file_path
        if type=='y_file':
            self.y_path = file_path
        path.set(os.path.basename(file_path))
    def create_file(self, table_label,model_label,x_label,y_label):
        self.current_table_input_file =None
        self.current_table_file =None
        self.old_x_path = None
        self.old_y_path = None
        self.train = tk.Variable(value=False)
        self.create = tk.Variable(value=False)
        self.x_path = None
        self.y_path = None
        table_label.set('')
        model_label.set('')
        x_label.set('')
        y_label.set('')

    def obter_dados_partidas(self, file_path):
        
        
        df = pd.read_csv(file_path)
        
        # Padroniza os nomes das colunas
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(".", "", regex=False)
        )

        # Converte datas, se existirem
        for col in ["data", "data_das_odds"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

        return df.to_dict(orient="records")


    
    def carregar_configuracoes(self):
        """Carrega as configurações salvas"""
        try:
            gui_config = self.betconfig.load_config()
            self.nivel_alta.set(gui_config['conf_alta']),
            self.nivel_media.set(gui_config['conf_media_min']),
            self.nivel_baixa.set(gui_config['conf_baixa_min']),
            self.stake_alta.set(gui_config['stake_alta_pct']),
            self.stake_media.set(gui_config['stake_media_pct']),
            self.stake_baixa.set(gui_config['stake_baixa_pct'])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {str(e)}")
            return False
    
    def limpar_treeview(self, treeview):
        """Limpa o treeview de um mercado específico"""
        for widget in treeview.winfo_children():
            widget.destroy()
    
    def exportar_csv(self, treeview):
        """Exporta as previsões de um mercado para CSV"""
        
        if not treeview.get_children():
            messagebox.showwarning("Aviso", "Não há previsões para exportar.")
            return
        
        # Solicitar local para salvar
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar previsões como CSV"
        )
        
        if not filename:
            return
        
        try:
            # Obter dados do treeview
            data = []
            columns = ["CAMPEONATO", "COLUNA", "HORA", "PROBABILIDADE", 
                      "CONFIANCA", "STAKE", "RESULTADO", "GALE"]
            
            for item in treeview.get_children():
                values = treeview.item(item)["values"]
                data.append(dict(zip(columns, values)))
            
            # Criar DataFrame e salvar
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            
            messagebox.showinfo("Sucesso", f"Previsões exportadas para {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar previsões: {str(e)}")
    
    def exportar_pdf(self, treeview, mercado):
        """Exporta as previsões de um mercado para PDF"""
        
        if not treeview.get_children():
            messagebox.showwarning("Aviso", "Não há previsões para exportar.")
            return
        
        # Solicitar local para salvar
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Salvar previsões como PDF"
        )
        
        if not filename:
            return
        
        try:
            # Obter dados do treeview
            data = []
            columns = ["CAMPEONATO", "COLUNA", "HORA", "PROBABILIDADE", 
                      "CONFIANCA", "STAKE", "RESULTADO", "GALE"]
            
            for item in treeview.get_children():
                values = treeview.item(item)["values"]
                data.append(dict(zip(columns, values)))
            
            # Criar DataFrame
            df = pd.DataFrame(data)
            
            # Gerar PDF usando reportlab
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import letter, landscape
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                
                # Criar documento PDF
                doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
                
                # Estilos
                styles = getSampleStyleSheet()
                title_style = styles['Heading1']
                subtitle_style = styles['Heading2']
                normal_style = styles['Normal']
                
                # Elementos do PDF
                elements = []
                
                # Título
                mercado_nome = {"btts": "BTTS", "over25": "Over 2.5", "over35": "Over 3.5"}
                title = Paragraph(f"Previsões {mercado_nome.get(mercado, mercado)}", title_style)
                elements.append(title)
                elements.append(Spacer(1, 0.25*inch))
                
                # Subtítulo com data e hora
                now = datetime.now()
                subtitle = Paragraph(f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')}", subtitle_style)
                elements.append(subtitle)
                elements.append(Spacer(1, 0.25*inch))
                
                # Tabela de previsões
                data_table = [columns]
                
                # Adicionar dados
                for _, row in df.iterrows():
                    data_table.append([
                        row['CAMPEONATO'],
                        row['COLUNA'],
                        row['HORA'],
                        row['PROBABILIDADE'],
                        row['CONFIANCA'],
                        row['STAKE'],
                        row['RESULTADO'],
                        row['GALE']
                    ])
                
                # Criar tabela
                table = Table(data_table, repeatRows=1)
                
                # Estilo da tabela
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ])
                
                # Aplicar estilo à tabela
                table.setStyle(table_style)
                
                # Adicionar tabela ao documento
                elements.append(table)
                
                # Construir PDF
                doc.build(elements)
                
                messagebox.showinfo("Sucesso", f"Previsões exportadas para {filename}")
            except ImportError:
                messagebox.showerror("Erro", "Biblioteca reportlab não encontrada. Instale-a com 'pip install reportlab'.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar previsões: {str(e)}")
    

    
    
    
    def exportar_tabela_csv(self, mercado):
        """Exporta a tabela operacional de um mercado para CSV"""
        # Caminho para o arquivo CSV
        arquivo = create_dated_filename(directory='../generated', extension='csv', name=mercado)
        
        if not os.path.exists(arquivo):
            messagebox.showerror("Erro", f"Tabela não encontrada: {arquivo}")
            return
        
        # Solicitar local para salvar
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar tabela como CSV"
        )
        
        if not filename:
            return
        
        try:
            # Copiar arquivo
            import shutil
            shutil.copy2(arquivo, filename)
            
            messagebox.showinfo("Sucesso", f"Tabela exportada para {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar tabela: {str(e)}")
    
    
    def salvar_configuracoes(self):
        """Salva as configurações atuais"""
        try:
            # Criar dicionário com configurações
            config = {
            "conf_alta": self.nivel_alta.get(),
            "conf_media_min": self.nivel_media.get(),
            "conf_media_max": 0,
            "conf_baixa_min": self.nivel_baixa.get(),
            "conf_baixa_max": 0,
            "stake_base": 0,
            "stake_alta_pct": self.stake_alta.get(),
            "stake_media_pct": self.stake_media.get(),
            "stake_baixa_pct": self.stake_baixa.get()
        }
            
            # Salvar em arquivo JSON
            import json
            with open("../generated/grisamanus_config.json", "w") as f:
                json.dump(config, f, indent=4)
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
    
    def restaurar_padroes(self):
        """Restaura as configurações padrão"""
        # Valores padrão
        self.stake_alta.set(25.0)
        self.stake_media.set(15.0)
        self.stake_baixa.set(5.0)
        
        self.nivel_alta.set(0.70)
        self.nivel_media.set(0.60)
        self.nivel_baixa.set(0.50)
        
        messagebox.showinfo("Sucesso", "Configurações padrão restauradas!")
    def exportar_dados_csv(self, treeview):
        """Exporta os dados da tabela para CSV"""
        if not treeview.get_children():
            messagebox.showwarning("Aviso", "Não há dados para exportar.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar dados como CSV"
        )
        
        if not filename:
            return
        
        try:
            # Obter dados do treeview
            dados = []
            colunas = [treeview.heading(col)["text"] for col in treeview["columns"]]
            
            for item in treeview.get_children():
                valores = treeview.item(item)["values"]
                dados.append(dict(zip(colunas, valores)))
            
            # Criar DataFrame e salvar
            df = pd.DataFrame(dados)
            df.to_csv(filename, index=False)
            
            messagebox.showinfo("Sucesso", f"Dados exportados para {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")
