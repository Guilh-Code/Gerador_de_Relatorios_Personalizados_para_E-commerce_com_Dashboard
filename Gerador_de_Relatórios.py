import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Configuração para melhorar a visualização dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# --- CLASSE 1: DataManager (Gerenciador de Dados) ---
class DataManager:
    def __init__(self, csv_file):
        """
        Inicializa o DataManager com o caminho para o arquivo CSV.
        """
        self.csv_file = csv_file
        self.df_vendas = pd.DataFrame()

    def load_data(self):