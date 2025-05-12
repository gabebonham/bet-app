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
from ml.implementacao_drisamanus_corrigida import execute


class Service:
    def __init__(self):
        self.df_btts = pd.DataFrame()  # BTTS market data
        self.df_prev = pd.DataFrame()  # Over 2.5 goals
        self.df_table = pd.DataFrame()  # Over 3.5 goals
        self.df_pred = pd.DataFrame()
        # Variáveis para valores de stake
        self.stake_alta = tk.DoubleVar(value=25.0)
        self.stake_media = tk.DoubleVar(value=15.0)
        self.stake_baixa = tk.DoubleVar(value=5.0)
        # Variáveis para níveis de confiança
        self.nivel_alta = tk.DoubleVar(value=0.70)
        self.nivel_media = tk.DoubleVar(value=0.60)
        self.nivel_baixa = tk.DoubleVar(value=0.50)
    def gerar_previsoes(self, hora_atual, num_horas,mercados_selecionados, mercado_treeview):
        self.load_data(True)
        self.setup_treeview(mercado_treeview)
        df = self.df_prev
        try:
            # Verificar quais mercados estão selecionados
            if mercados_selecionados.lower()=='btts':
                
                self.filter_btts(mercado_treeview, df, hora_atual, num_horas)
            
            if mercados_selecionados.lower()=='over25':
                self.filter_over25(mercado_treeview, df, hora_atual, num_horas)
            
            if mercados_selecionados.lower()=='over35':
                self.filter_over35(mercado_treeview, df, hora_atual, num_horas)
            
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar previsões: {str(e)}")
    


    def setup_treeview(self,tree):
        # Clear existing data and columns
        tree.delete(*tree.get_children())
        tree["columns"] = ("hora", "campeonato", "coluna", "probabilidade", "outcome", 
                        "prediction", "probability", "confidence", "stake")
        
        # Define column headings
        tree.heading("#0", text="ID")
        tree.heading("hora", text="Hora")
        tree.heading("campeonato", text="Campeonato")
        tree.heading("coluna", text="Coluna")
        tree.heading("probabilidade", text="Probabilidade")
        tree.heading("outcome", text="Outcome")
        tree.heading("prediction", text="Prediction")
        tree.heading("probability", text="Probability")
        tree.heading("confidence", text="Confidence")
        tree.heading("stake", text="Stake")
        
        # Configure column widths
        tree.column("#0", width=40)
        tree.column("hora", width=50)
        tree.column("campeonato", width=100)
        tree.column("coluna", width=60)
        tree.column("probabilidade", width=100)
        tree.column("outcome", width=70)
        tree.column("prediction", width=80)
        tree.column("probability", width=80)
        tree.column("confidence", width=80)
        tree.column("stake", width=60)

    def filter_by_time(self,df, hora_atual, num_horas):
        """Filter dataframe by time range"""
        hora_min = hora_atual
        hora_max = hora_atual + num_horas
        return df[(df['HORA'] >= hora_min) & (df['HORA'] <= hora_max)]

    def populate_treeview(self,tree, filtered_df):
        """Populate treeview with filtered data"""
        self.setup_treeview(tree)
        for i, row in filtered_df.iterrows():
            tree.insert("", "end", text=str(i), 
                    values=(row['HORA'], row['CAMPEONATO'], row['COLUNA'],
                            row['PROBABILIDADE'], row['OUTCOME'],
                            row['PREDICTION'], row['PROBABILITY'],
                            row['CONFIDENCE_LEVEL'], row['RECOMMENDED_STAKE']))

    # Specific filter functions
    def filter_over25(self,tree, df, hora_atual=0, num_horas=24):
        filtered = self.filter_by_time(df, hora_atual, num_horas)
        filtered = filtered[filtered['PREDICTION'] == 'over25']  # Adjust column name as needed
        self.populate_treeview(tree, filtered)

    def filter_over35(self,tree, df, hora_atual=0, num_horas=24):
        filtered = self.filter_by_time(df, hora_atual, num_horas)
        filtered = filtered[filtered['PREDICTION'] == 'over35']  # Adjust column name as needed
        self.populate_treeview(tree, filtered)

    def filter_under25(self,tree, df, hora_atual=0, num_horas=24):
        filtered = self.filter_by_time(df, hora_atual, num_horas)
        filtered = filtered[filtered['PREDICTION'] == 'under25']  # Adjust column name as needed
        self.populate_treeview(tree, filtered)

    def filter_under35(self,tree, df, hora_atual=0, num_horas=24):
        filtered = self.filter_by_time(df, hora_atual, num_horas)
        filtered = filtered[filtered['PREDICTION'] == 'under35']  # Adjust column name as needed
        self.populate_treeview(tree, filtered)

    def filter_under15(self,tree, df, hora_atual=0, num_horas=24):
        filtered = self.filter_by_time(df, hora_atual, num_horas)
        filtered = filtered[filtered['PREDICTION'] == 'under15']  # Adjust column name as needed
        self.populate_treeview(tree, filtered)

    def filter_btts(self,tree, df, hora_atual=0, num_horas=24):
        filtered = self.filter_by_time(df, hora_atual, num_horas)
        filtered = filtered[filtered['PREDICTION'] == 'btts']  # Adjust column name as needed
        self.populate_treeview(tree, filtered)
    def load_data(self,flag=False):
        if flag:
            self.df_prev = pd.read_csv(get_most_recent_file_prev('pred','generated/'))
            return
        df = pd.read_csv(get_most_recent_file_prev('tabela','generated/'))
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
            self.load_data()
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

    def rodar_previsao(self, treeview):
        """Executa a previsão com base no modelo treinado"""
        try:
            from ml.implementacao_drisamanus_corrigida import predict
            
            # 1. Carregar dados e verificar arquivos
            self.load_data()
            
            # Obter arquivo de entrada
            try:
                input_csv = get_most_recent_file_prev('tabela', 'generated')
                if not os.path.exists(input_csv):
                    raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_csv}")
                print(f"Arquivo de entrada válido: {input_csv}")
            except Exception as e:
                raise ValueError(f"Erro ao localizar arquivo de dados: {str(e)}")

            # Verificar modelo
            model_path = "./generated/model.pkl"
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

            # 2. Configurar saída
            output_dir = "../generated"
            os.makedirs(output_dir, exist_ok=True)
            output_csv = os.path.join(
                output_dir,
                f"pred_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.csv"
            )

            # 3. Executar previsão
            execute(True,self.get_current_config())  # Seu método de execução existente
            
            # 4. Processar resultados
            pred_file = get_most_recent_file_prev('pred', 'generated')
            df_previsoes = pd.read_csv(pred_file)
            
            # Verificar resultados
            if df_previsoes.empty:
                self.status_label.config(text="Nenhuma previsão gerada (arquivo vazio)")
                messagebox.showinfo("Informação", "Nenhuma previsão foi gerada para os dados atuais.")
                return

            # 5. Mapear colunas (INGLÊS -> PORTUGUÊS)
            column_map = {
                'PREDICTION': 'PREDICAO',
                'PROBABILITY': 'PROBABILIDADE',
                'Tempo': 'HORA',
                'Time da casa': 'COLUNA'  # Ajuste conforme necessário
            }
            df_previsoes = df_previsoes.rename(columns=column_map)

            # 6. Validar colunas obrigatórias
            required_columns = {
                'PREDICAO': int,
                'PROBABILIDADE': float,
                'Campeonato': str,
                'HORA': str,
                'COLUNA': str
            }
            
            missing = [col for col in required_columns if col not in df_previsoes.columns]
            if missing:
                raise ValueError(f"Colunas faltando após mapeamento: {', '.join(missing)}")

            # Converter tipos
            for col, dtype in required_columns.items():
                df_previsoes[col] = df_previsoes[col].astype(dtype)

            # 7. Exibir na interface
            self.limpar_treeview("over25")
            for i, row in df_previsoes.iterrows():
                treeview_over25.insert("", "end", values=(
                    row['Campeonato'],
                    i + 1,
                    f"{row['HORA']}:{row['COLUNA']}",
                    "CASA" if row['PREDICAO'] == 1 else "FORA",
                    f"{row['PROBABILIDADE']*100:.1f}%",
                    "1 UNIDADE",
                    "",
                    "SIM" if row['PREDICAO'] == 1 else "NÃO"
                ))

            # 8. Feedback
            success_msg = f"{len(df_previsoes)} previsões processadas\nSalvo em: {output_csv}"
            self.status_label.config(text=success_msg)
            messagebox.showinfo("Sucesso", success_msg)

        except Exception as e:
            error_msg = f"Falha na previsão: {str(e)}"
            messagebox.showerror("Erro", error_msg)
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
        execute(just_predict=False,config=self.get_current_config())
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
            generate_actuals()
            # Limpar tabela existente
            for item in treeview_tabela.get_children():
                treeview_tabela.delete(item)
                
            # Carregar dados (substitua por sua fonte de dados real)
            dados = self.obter_dados_partidas()  # Implemente este método
            
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


    def obter_dados_partidas(self):
        
        self.load_data()
        df = self.df_table
        
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
            import json
            # Verificar se o arquivo de configuração existe
            config_path = "generated/grisamanus_config.json"
            if not os.path.exists(config_path):
                messagebox.showwarning("Aviso", "Nenhum arquivo de configuração encontrado!")
                return False
            
            # Carregar o arquivo JSON
            with open(config_path, "r") as f:
                config = json.load(f)
            
            return config
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {str(e)}")
            return False
    
    def limpar_treeview(self, treeview):
        """Limpa o treeview de um mercado específico"""
        for item in treeview.get_children():
            treeview.delete(item)
    
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
        arquivo = f"/home/ubuntu/tabelas_operacionais/tabela_operacional_{mercado}.csv"
        
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
                "stake": {
                    "ALTA": self.stake_alta.get(),
                    "MEDIA": self.stake_media.get(),
                    "BAIXA": self.stake_baixa.get()
                },
                "niveis_confianca": {
                    "ALTA": self.nivel_alta.get(),
                    "MEDIA": self.nivel_media.get(),
                    "BAIXA": self.nivel_baixa.get()
                }
            }
            
            # Salvar em arquivo JSON
            import json
            with open("generated/grisamanus_config.json", "w") as f:
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
