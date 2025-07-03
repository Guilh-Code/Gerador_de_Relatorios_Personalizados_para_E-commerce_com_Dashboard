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
        """ Inicializa o DataManager com o caminho para o arquivo CSV. """
        self.csv_file = csv_file
        self.df_vendas = pd.DataFrame()

    def load_data(self):
        """ Carrega os dados do CSV para o DataFrame.
            Retorna True se o Carregamento for bem-sucedido, False caso contrário. """
        if not os.path.exists(self.csv_file):
            print(f"Erro: O arquivo '{self.csv_file}' não foi encontrado.")
            return False
        try:
            self.df_vendas = pd.read_csv(self.csv_file)
            print(f"Arquivo '{self.csv_file}' carregado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao carregar o arquivo CSV: {e}")
            return False

    def preprocess_data(self):
        """ Realiza o pré-processamento dos dados:
            - Converte 'Data_Venda' para datetime.
            - Calcula 'Valor_Total_Venda'.
            - Extrai 'Mes_Venda'. """
        if self.df_vendas.empty:
            print("DataFrame vazio. Carregue os dados primeiro.")
            return

        # Converter Data_Venda
        self.df_vendas['Data_Venda'] = pd.to_datetime(self.df_vendas['Data_Venda'])
        # Calcular Valor_Total_Venda
        self.df_vendas['Valor_Total_Venda'] = self.df_vendas['Preco_Unitario'] * self.df_vendas['Quantidade_Vendida']
        # Extrair Mes_Venda
        self.df_vendas['Mes_Venda'] = self.df_vendas['Data_Venda'].dt.to_period('M')
        print("Dados pré-processados com sucesso.")

    def get_df_vendas(self):
        """ Retorna o DataFrame de vendas processados. """       
        return self.df_vendas

    def get_sales_by_category(self):
        """ Calcula e retorna vendas totais por categoria. """
        return self.df_vendas.groupby('Categoria_Produto')['Valor_Total_Venda'].sum().sort_values(ascending=False)

    def get_sales_by_region(self):
        """ Calcula e retorna vendas totais por região. """
        return self.df_vendas.groupby('Regiao_Cliente')['Valor_Total_Venda'].sum().sort_values(ascending=False)

    def get_sales_by_month(self):
        """ Calcula e retorna vendas totais por mês, ordenadas cronologicamente. """
        return self.df_vendas.groupby('Mes_Venda')['Valor_Total_Venda'].sum().sort_index(ascending=True).reset_index()

    
# --- CLASSE 2: DatabaseManager (Gerenciador de Banco de Dados) ---
class DatabaseManager:
    def __init__(self, db_file):
        """ Inicializa o DatabaseManager com o caminho para o arquivo do banco de dados SQLite."""
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        """ Estabelece a conexão com o banco de dados. """
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print(f"Conexão com o banco de dados '{self.db_file}' estabelecida com sucesso.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def create_table(self):
        """ Cria a tabela 'vendas' se ela não existir. """
        if not self.conn:
            print("Não há conexão com o banco de dados. Conecte-se primeiro.")
            return False
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    ID_Venda INTEGER PRIMARY KEY,
                    Data_Venda TEXT,
                    Nome_Produto TEXT,
                    Categoria_Produto TEXT,
                    Preco_Unitario REAL,
                    Quantidade_Vendida INTEGER,
                    Cliente_ID TEXT,
                    Regiao_Cliente TEXT,
                    Valor_Total_Venda REAL,
                    Mes_Venda TEXT
                )
            ''')
            self.conn.commit()
            print("Tabela 'vendas' verificada/criada com sucesso.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
            return False

    def insert_data(self, df_data):
        """ Insere dados de um DataFrame na tabela 'vendas'. """
        if not self.conn:
            print("Não há conexão com o banco de dados. Conecte-se primeiro.")
            return False
        try:
            # Criar uma cópia para não alterar o DataFrame original
            df_to_insert = df_data.copy()
            # Converter Mes_Venda para string antes de inserir
            df_to_insert['Mes_Venda'] = df_to_insert['Mes_Venda'].astype(str)

            df_to_insert.to_sql('vendas', self.conn, if_exists = 'replace', index = False)
            self.conn.commit()
            print("Dados do DataFrame inseridos na tabela 'vendas' com sucesso.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")
            return False

    def fetch_all_vendas(self):
        """ Recupera todos os dados da tabela 'vendas' para um DataFrame. """
        if not self.conn:
            print("Não há conexão com o banco de dados. Conecte-se primeiro.")
            return pd.DataFrame() # Retorna DataFrame vazio se não houver conexão
        try:
            df_from_db = pd.read_sql_query("SELECT * FROM vendas", self.conn)
            print("Dados recuperados no SQLite com sucesso.")
            # converter Data_Venda de volta para datetime se necessário para análises futuras
            df_from_db['Data_Venda'] = pd.to_datetime(df_from_db['Data_Venda'])
            return df_from_db
        except sqlite3.Error as e:
            print(f"Erro ao recuperar dados: {e}")
            return pd.DataFrame()

    def close_connection(self):
        """ Fecha a conexão com o banco de dados. """
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")


# --- LÓGICA PRINCIPAL DO PROGRAMA ---
if __name__ == "__main__":
    csv_path = 'vendas.csv'
    db_path = 'ecommerce_data.db'
    output_dir = 'relatorios_imagens'

    # Criar o diretório de saída se ele não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Diretório '{output_dir}' criado para salvar os relatórios.")

    # 1. Gerenciar Dados
    data_manager = DataManager(csv_path)
    if data_manager.load_data():
        data_manager.preprocess_data()
        df_vendas = data_manager.get_df_vendas()

        # 2. Gerenciar Banco de Dados
        db_manager = DatabaseManager(db_path)
        if db_manager.connect():
            db_manager.create_table()
            db_manager.insert_data(df_vendas)

            # Recuperar dados do banco de dados para verificar
            df_vendas_from_db = db_manager.fetch_all_vendas()
            print("\n--- Primeiras 5 linhas do DataFrame lido do DB ---")
            print(df_vendas_from_db.head())
            print("\n--- Info do DataFrame lido do DB ---")
            df_vendas_from_db.info()
            db_manager.close_connection()

        # 3. Gerar, exibir e salvar visualizações
        print("\n--- Gerando Visualizações ---")

        # Vendas por Categoria
        vendas_por_categoria = data_manager.get_sales_by_category()
        plt.figure(figsize=(10, 6))
        sns.barplot(x = vendas_por_categoria.index, y = vendas_por_categoria.values, palette= 'viridis')
        plt.title('Vendas Totais por Categoria de Produto')
        plt.xlabel('Categoria de Produto')
        plt.ylabel('Valor Total de Vendas (R$)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'vendas_por_categori.png')) # Salva o gráfico
        plt.show()

        # Vendas por Região
        vendas_por_regiao = data_manager.get_sales_by_region()
        plt.figure(figsize=(10, 6))
        sns.barplot(x = vendas_por_regiao.index, y = vendas_por_regiao.values, palette= 'magma')
        plt.title('Vendas Totais por Região do Cliente')
        plt.xlabel('Região do Cliente')
        plt.ylabel('Valor Total de Vendas (R$)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'vendas_por_regiao.png')) # Salva o gráfico
        plt.show()

        # Vendas por Mês
        vendas_por_mes = data_manager.get_sales_by_month()
        plt.figure(figsize=(12, 6))
        sns.lineplot(x = vendas_por_mes['Mes_Venda'].astype(str), y = 'Valor_Total_Venda', data= vendas_por_mes, markers= 'o')
        plt.title('Tendência de Vendas Totais por Mês')
        plt.xlabel('Mês da Venda')
        plt.ylabel('Valor Total de Vendas (R$)')
        plt.xticks(rotation = 45, ha = 'right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'vendas_por_mes.png')) # Salva o gráfico
        plt.show()

    else:
        print("Não foi possível prosseguir devido a erros no carregamento/processamento dos dados.")

