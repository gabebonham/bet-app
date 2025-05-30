import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ===== HELPER FUNCTIONS =====
def load_and_combine_dfs(df_list, tournament_names):
    """Combine multiple DataFrames and add a 'Tournament' column."""
    dfs = []
    for df, name in zip(df_list, tournament_names):
        df["Tournament"] = name
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def add_derived_columns(df):
    """Add Outcome, Total Goals, and Goal Difference columns."""
    df["Outcome"] = np.where(
        df["Casa Gols Previsão"] > df["Visitante Gols Previsão"], "Vitória da Casa",
        np.where(df["Casa Gols Previsão"] == df["Visitante Gols Previsão"], "Empate", "Vitória Visitante")
    )
    df["Total Goals"] = df["Casa Gols Previsão"] + df["Visitante Gols Previsão"]
    df["Goal Difference"] = df["Casa Gols Previsão"] - df["Visitante Gols Previsão"]
    return df

# ===== PLOT FUNCTIONS =====
def plot_avg_goals_by_tournament(df):
    """1a. Average Predicted Goals by Tournament (Home vs Away)."""
    avg_goals = df.groupby("Tournament")[["Casa Gols Previsão", "Visitante Gols Previsão"]].mean()
    avg_goals.plot(kind="bar")
    plt.title("Média de Gols Previstos por Torneio")
    plt.ylabel("Média de Gols")
    plt.xlabel("Torneio")
    plt.xticks(rotation=45)
    plt.show()

def plot_outcomes_by_tournament(df):
    """1b. Predicted Match Outcomes (Home Win/Draw/Away Win) by Tournament."""
    outcome_counts = df.groupby(["Tournament", "Outcome"]).size().unstack()
    outcome_counts.plot(kind="bar", stacked=True)
    plt.title("Resultados Previstos por Torneio")
    plt.ylabel("Número de Partidas")
    plt.xlabel("Torneio")
    plt.xticks(rotation=45)
    plt.legend(title="Resultado")
    plt.show()

def plot_heatmap_goals_by_hour_tournament(df):
    """1c. Heatmap of Avg Goals by Hour and Tournament."""
    heatmap_data = df.pivot_table(index="HORA", columns="Tournament", values="Total Goals", aggfunc="mean")
    sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, fmt=".2f")
    plt.title("Média de Gols por Hora e Torneio")
    plt.xlabel("Torneio")
    plt.ylabel("Hora da Partida")
    plt.show()

def plot_goals_by_hour(df):
    """2a. Avg Predicted Goals by Hour of the Day."""
    hourly_goals = df.groupby("HORA")["Total Goals"].mean()
    hourly_goals.plot(kind="line", marker="o")
    plt.title("Média de Gols por Hora do Dia")
    plt.xlabel("Hora da Partida")
    plt.ylabel("Média Total de Gols")
    plt.grid(True)
    plt.show()

def plot_team_strength_scatter(df):
    """3b. Team Strength: Avg Goals Scored vs Conceded."""
    team_offense = df.groupby("Time_Casa")["Casa Gols Previsão"].mean()
    team_defense = df.groupby("Time_Casa")["Visitante Gols Previsão"].mean()
    team_strength = pd.DataFrame({"Gols Marcados": team_offense, "Gols Sofridos": team_defense})
    sns.scatterplot(data=team_strength, x="Gols Marcados", y="Gols Sofridos", hue=team_strength.index, s=100)
    plt.title("Força das Equipes: Média de Gols Marcados vs Sofridos")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.show()

def plot_head_to_head(df, team1, team2):
    """4a. Head-to-Head Predictions for Two Teams."""
    h2h = df[
        ((df["Time_Casa"] == team1) & (df["Time_Contra"] == team2)) |
        ((df["Time_Casa"] == team2) & (df["Time_Contra"] == team1))
    ]
    if not h2h.empty:
        h2h[["Time_Casa", "Time_Contra", "Casa Gols Previsão", "Visitante Gols Previsão"]].plot(
            kind="bar", xlabel="Partida"
        )
        plt.title(f"Confronto Direto: {team1} vs {team2}")
        plt.ylabel("Gols Previstos")
        plt.xticks(ticks=range(len(h2h)), labels=h2h["Time_Casa"] + " vs " + h2h["Time_Contra"], rotation=45)
        plt.show()
    else:
        print(f"Nenhuma partida encontrada entre {team1} e {team2}.")

def plot_favorite_win_rate(df):
    """4b. % of Matches Where the Favorite Wins."""
    df["Favorite Wins"] = np.where(df["Casa Gols Previsão"] > df["Visitante Gols Previsão"], 1, 0)
    favorite_rate = df.groupby("Tournament")["Favorite Wins"].mean() * 100
    favorite_rate.plot(kind="bar")
    plt.title("Percentual de Vitórias do Favorito por Torneio")
    plt.ylabel("Taxa de Vitória (%)")
    plt.xlabel("Torneio")
    plt.xticks(rotation=45)
    plt.show()

def plot_goals_distribution(df):
    """5a. Distribution of Predicted Total Goals by Tournament."""
    sns.violinplot(data=df, x="Tournament", y="Total Goals", inner="stick")
    plt.title("Distribuição de Gols Totais Previstos por Torneio")
    plt.xlabel("Torneio")
    plt.ylabel("Total de Gols")
    plt.xticks(rotation=45)
    plt.show()

def plot_avg_goal_difference(df):
    """5b. Avg Goal Difference (Home - Away) by Tournament."""
    avg_diff = df.groupby("Tournament")["Goal Difference"].mean()
    avg_diff.plot(kind="bar")
    plt.title("Diferença Média de Gols (Casa - Visitante) por Torneio")
    plt.ylabel("Diferença Média de Gols")
    plt.xlabel("Torneio")
    plt.xticks(rotation=45)
    plt.show()

def print_high_scoring_matches(df, threshold=3.5):
    """6a. High-Scoring Matches (Total Goals > threshold)."""
    high_scoring = df[df["Total Goals"] > threshold]
    if not high_scoring.empty:
        print(f"Partidas com muitos gols (Total > {threshold}):")
        print(high_scoring[["Tournament", "Time_Casa", "Time_Contra", "Total Goals"]])
    else:
        print(f"Nenhuma partida com mais de {threshold} gols previstos.")

def print_low_scoring_matches(df, threshold=1.5):
    """6b. Low-Scoring Matches (Total Goals < threshold)."""
    low_scoring = df[df["Total Goals"] < threshold]
    if not low_scoring.empty:
        print(f"\nPartidas com poucos gols (Total < {threshold}):")
        print(low_scoring[["Tournament", "Time_Casa", "Time_Contra", "Total Goals"]])
    else:
        print(f"Nenhuma partida com menos de {threshold} gols previstos.")


def run_plotting(dfs):
    euro_df,copa_df,super_df,premier_df = dfs 
    
    # Combine and preprocess
    df = load_and_combine_dfs(
        [euro_df, copa_df, super_df, premier_df],
        ["Euro", "Copa", "Super", "Premier"]
    )
    df = add_derived_columns(df)

    # Generate all plots
    plot_avg_goals_by_tournament(df)
    plot_outcomes_by_tournament(df)
    plot_heatmap_goals_by_hour_tournament(df)
    plot_goals_by_hour(df)
    plot_team_strength_scatter(df)
    # plot_head_to_head(df, "Argentina", "Marrocos")
    plot_favorite_win_rate(df)
    plot_goals_distribution(df)
    plot_avg_goal_difference(df)
    print_high_scoring_matches(df)
    print_low_scoring_matches(df)