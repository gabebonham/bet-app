import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from services.file_util import get_most_recent_file

class BetMarketVisualizer:
    def __init__(self, output_dir='../temp_plots'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.markets = {
            'btts': {
                'color': '#1abc9c',
                'condition': lambda df: (df['Gols time casa'] > 0) & (df['Gols time contra'] > 0),
                'odd_col': 'BTTS Odd'
            },
            'over25': {
                'color': '#e74c3c',
                'condition': lambda df: df['Gols totais'] > 2.5,
                'odd_col': 'Odd Over 2.5'
            },
            'under25': {
                'color': '#2ecc71',
                'condition': lambda df: df['Gols totais'] < 2.5,
                'odd_col': 'Odd Under 2.5'
            },
            'over35': {
                'color': '#9b59b6',  # Purple
                'condition': lambda df: df['Gols totais'] > 3.5,
                'odd_col': 'Odd Over 3.5'
            },
            'under35': {
                'color': '#3498db',  # Blue
                'condition': lambda df: df['Gols totais'] < 3.5,
                'odd_col': 'Odd Under 3.5'
            },
            'under15': {
                'color': '#f1c40f',  # Yellow
                'condition': lambda df: df['Gols totais'] < 1.5,
                'odd_col': 'Odd Under 1.5'
            }
        }   

    def _ensure_occurrence(self, df, market_name):
        """Ensure occurrence column exists for the specific market"""
        if market_name not in self.markets:
            raise ValueError(f"Unknown market: {market_name.replace(' ','').lower().replace('.','')}")
            
        # Calculate occurrence if not present
        if 'OCORRENCIA' not in df.columns:
            df['OCORRENCIA'] = df.apply(self.markets[market_name]['condition'], axis=1)
        
        # Ensure hour column exists
        if 'HORA' not in df.columns and 'Tempo' in df.columns:
            df['HORA'] = pd.to_datetime(df['Tempo'], format='%H:%M').dt.hour
            
        return df

    def plot_occurrence_by_hour(self, df, market_name, title_suffix=""):
        """Plot occurrence rate by hour of day for a specific market"""
        try:
            df = self._ensure_occurrence(df, market_name)
            
            # Group by hour and calculate occurrence rate
            hour_data = df.groupby('HORA')['OCORRENCIA'].mean().reset_index()
            
            # Create plot
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                x='HORA',
                y='OCORRENCIA',
                data=hour_data,
                color=self.markets[market_name]['color'],
                alpha=0.7
            )
            
            # Add line plot on top
            sns.lineplot(
                x='HORA',
                y='OCORRENCIA',
                data=hour_data,
                color=self.markets[market_name]['color'],
                linewidth=2,
                ax=ax
            )
            
            # Customize plot
            plt.title(f'Taxa de Ocorrência {market_name} por Hora\n{title_suffix}')
            plt.xlabel('Hora do Dia')
            plt.ylabel('Taxa de Ocorrência (%)')
            plt.ylim(0, 1)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                f'taxa_ocorrencia_hora_{market_name.lower().replace(" ", "_")}.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot occurrence by hour: {str(e)}")

    def plot_occurrence_by_championship(self, df, market_name, title_suffix="", top_n=10):
        """Plot occurrence rate by championship (top N) for a specific market"""
        try:
            df = self._ensure_occurrence(df, market_name)
            
            # Group by championship and calculate occurrence rate
            champ_data = df.groupby('Campeonato')['OCORRENCIA'].agg(['mean', 'count'])
            champ_data = champ_data[champ_data['count'] >= 5]  # Filter championships with few matches
            champ_data = champ_data.sort_values('mean', ascending=False).head(top_n)
            
            # Create plot
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                x=champ_data.index,
                y='mean',
                data=champ_data.reset_index(),
                color=self.markets[market_name]['color'],
                alpha=0.7
            )
            
            # Customize plot
            plt.title(f'Taxa de Ocorrência {market_name} por Campeonato (Top {top_n})\n{title_suffix}')
            plt.xlabel('Campeonato')
            plt.ylabel('Taxa de Ocorrência (%)')
            plt.ylim(0, 1)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                f'taxa_ocorrencia_campeonato_{market_name.lower().replace(" ", "_")}.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot occurrence by championship: {str(e)}")
    def plot_occurrence_by_cycle(self, df, market_name, title_suffix=""):
        """Plot occurrence rate by cycle for a specific market"""
        try:
            df = self._ensure_occurrence(df, market_name)
            
            # Group by cycle and calculate occurrence rate
            cycle_data = df.groupby('CICLO')['OCORRENCIA'].mean().reset_index()
            
            # Create plot
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                x='CICLO',
                y='OCORRENCIA',
                data=cycle_data,
                color=self.markets[market_name]['color'],
                alpha=0.7
            )
            
            # Add line plot on top
            sns.lineplot(
                x='CICLO',
                y='OCORRENCIA',
                data=cycle_data,
                color=self.markets[market_name]['color'],
                linewidth=2,
                ax=ax
            )
            
            # Customize plot
            plt.title(f'Taxa de Ocorrência {market_name} por Ciclo\n{title_suffix}')
            plt.xlabel('Ciclo')
            plt.ylabel('Taxa de Ocorrência (%)')
            plt.ylim(0, 1)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                f'taxa_ocorrencia_ciclo_{market_name.lower().replace(" ", "_")}.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot occurrence by cycle: {str(e)}")

    def plot_heatmap_championship_cycle(self, df, market_name, title_suffix=""):
        """Plot heatmap of occurrence rates by championship and cycle"""
        try:
            df = self._ensure_occurrence(df, market_name)
            
            # Prepare data - group by championship and cycle
            heatmap_data = df.groupby(['Campeonato', 'CICLO'])['OCORRENCIA'].mean().unstack()
            
            # Filter for championships with enough data
            champ_counts = df['Campeonato'].value_counts()
            valid_champs = champ_counts[champ_counts >= 5].index
            heatmap_data = heatmap_data.loc[valid_champs]
            
            # Create plot
            plt.figure(figsize=(14, 8))
            sns.heatmap(
                heatmap_data,
                cmap='YlOrRd',
                vmin=0,
                vmax=1,
                annot=True,
                fmt='.0%',
                linewidths=0.5,
                cbar_kws={'label': 'Taxa de Ocorrência'}
            )
            
            # Customize plot
            plt.title(f'Heatmap: Taxa de Ocorrência {market_name}\nCampeonato x Ciclo\n{title_suffix}')
            plt.xlabel('Ciclo')
            plt.ylabel('Campeonato')
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                f'heatmap_campeonato_ciclo_{market_name.lower().replace(" ", "_")}.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot heatmap: {str(e)}")
    def plot_heatmap_championship_hour(self, df, market_name, title_suffix=""):
        """Plot heatmap of occurrence rates by championship and hour"""
        try:
            df = self._ensure_occurrence(df, market_name)
            
            # Prepare data - group by championship and hour
            heatmap_data = df.groupby(['Campeonato', 'HORA'])['OCORRENCIA'].mean().unstack()
            
            # Filter for championships with enough data
            champ_counts = df['Campeonato'].value_counts()
            valid_champs = champ_counts[champ_counts >= 5].index
            heatmap_data = heatmap_data.loc[valid_champs]
            
            # Create plot
            plt.figure(figsize=(14, 8))
            sns.heatmap(
                heatmap_data,
                cmap='YlOrRd',
                vmin=0,
                vmax=1,
                annot=True,
                fmt='.0%',
                linewidths=0.5,
                cbar_kws={'label': 'Taxa de Ocorrência'}
            )
            
            # Customize plot
            plt.title(f'Heatmap: Taxa de Ocorrência {market_name}\nCampeonato x Hora\n{title_suffix}')
            plt.xlabel('Hora do Dia')
            plt.ylabel('Campeonato')
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                f'heatmap_campeonato_hora_{market_name.lower().replace(" ", "_")}.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot heatmap: {str(e)}")
    def plot_market_comparison(self, df, title_suffix=""):
        """Plot comparison of occurrence rates between different markets from a single DataFrame"""
        try:
            # Define market configurations
            market_config = [
                ('Over 2.5', 'Gols totais > 2.5'),
                ('Under 2.5', 'Gols totais < 2.5'),
                ('Over 3.5', 'Gols totais > 3.5'), 
                ('Under 3.5', 'Gols totais < 3.5')
            ]
            
            comparison_data = []
            
            for market_name, condition in market_config:
                # Calculate occurrence for each market
                if 'Over' in market_name:
                    threshold = float(market_name.split()[1])
                    occurrence = (df['Gols totais'] > threshold).mean()
                elif 'Under' in market_name:
                    threshold = float(market_name.split()[1])
                    occurrence = (df['Gols totais'] < threshold).mean()
                
                comparison_data.append({
                    'Mercado': market_name,
                    'Taxa': occurrence
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Create plot
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(
                data=comparison_df,
                x='Mercado',
                y='Taxa',
                hue='Mercado',
                palette='YlOrRd',
                order=['Over 2.5', 'Under 2.5', 'Over 3.5', 'Under 3.5']
            )
            
            # Add value labels
            for p in ax.patches:
                ax.annotate(
                    f"{p.get_height():.1%}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points'
                )
            
            # Customize plot
            plt.title(f'Comparação de Taxas entre Mercados\n{title_suffix}')
            plt.xlabel('Mercado')
            plt.ylabel('Taxa de Ocorrência')
            plt.ylim(0, 1)
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                'comparacao_taxas_mercados.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot market comparison: {str(e)}")


    def plot_cycle_comparison(self, df, title_suffix=""):
        """Plot comparison of occurrence rates by cycle between markets from single DataFrame"""
        try:
            # Define market configurations
            market_config = [
                ('Over 2.5', 'Gols totais > 2.5'),
                ('Under 2.5', 'Gols totais < 2.5'),
                ('Over 3.5', 'Gols totais > 3.5'),
                ('Under 3.5', 'Gols totais < 3.5')
            ]
            
            comparison_data = []
            
            for market_name, condition in market_config:
                # Calculate occurrence by cycle for each market
                if 'Over' in market_name:
                    threshold = float(market_name.split()[1])
                    df['OCORRENCIA'] = (df['Gols totais'] > threshold).astype(int)
                elif 'Under' in market_name:
                    threshold = float(market_name.split()[1])
                    df['OCORRENCIA'] = (df['Gols totais'] < threshold).astype(int)
                
                cycle_rates = df.groupby('CICLO')['OCORRENCIA'].mean().reset_index()
                cycle_rates['Mercado'] = market_name
                comparison_data.append(cycle_rates)
            
            comparison_df = pd.concat(comparison_data)
            
            # Create plot
            plt.figure(figsize=(14, 8))
            ax = sns.barplot(
                data=comparison_df,
                x='CICLO',
                y='OCORRENCIA',
                hue='Mercado',
                palette='YlOrRd',
                hue_order=['Over 2.5', 'Under 2.5', 'Over 3.5', 'Under 3.5']
            )
            
            # Add value labels
            for p in ax.patches:
                ax.annotate(
                    f"{p.get_height():.1%}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points'
                )
            
            # Customize plot
            plt.title(f'Comparação de Ciclos entre Mercados\n{title_suffix}')
            plt.xlabel('Ciclo')
            plt.ylabel('Taxa de Ocorrência')
            plt.ylim(0, 1)
            plt.legend(title='Mercado')
            plt.tight_layout()
            
            # Save plot
            output_file = os.path.join(
                self.output_dir,
                'comparacao_ciclos_mercados.png'
            )
            plt.savefig(output_file, dpi=300)
            plt.close()
            return output_file
            
        except Exception as e:
            plt.close()
            raise ValueError(f"Failed to plot cycle comparison: {str(e)}")
    def generate_specific_visualizations(self, df, market_name, title_suffix=""):
        """Generate all specific visualizations for a market"""
        try:
            # Generate the three specific visualizations
            self.plot_occurrence_by_hour(df.copy(), market_name, title_suffix)
            self.plot_occurrence_by_championship(df.copy(), market_name, title_suffix)
            self.plot_heatmap_championship_hour(df.copy(), market_name, title_suffix)
            
        except Exception as e:
            raise ValueError(f"Failed to generate specific visualizations: {str(e)}")


# Example Usage
if __name__ == "__main__":
    try:
        # Load data
        pred_df = pd.read_csv(get_most_recent_file("pred", '.'))
        table_df = pd.read_csv(get_most_recent_file("table", '..'))
        
        # Initialize and run visualizer
        visualizer = BetMarketVisualizer(output_dir='./temp_plots')
        
        # Generate specific visualizations for each market
        for market in ['BTTS', 'Over 2.5', 'Under 2.5']:
            visualizer.generate_specific_visualizations(pred_df, market, "Predictions")
            visualizer.generate_specific_visualizations(table_df, market, "Actual Results")
        
    except Exception as e:
        print(f"Error: {str(e)}")