import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Configuração para melhorar a visualização dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6) # Define um tamanho padrão para os gráficos

# Carregar o arquivo CSV e realizar as transformações
try:
    df_vendas = pd.read_csv('vendas.csv')
    print("Arquivo 'vendas.csv' carregado com sucesso!")
except FileNotFoundError:
    print("ERRO: O arquivo 'vendas.csv' não foi encontrado. Verifique o caminho.")
    exit()

df_vendas['Data_Venda'] = pd.to_datetime(df_vendas['Data_Venda'])
df_vendas['Valor_Total_Venda'] = df_vendas['Preco_Unitario'] * df_vendas['Quantidade_Vendida']
df_vendas['Mes_Venda'] = df_vendas['Data_Venda'].dt.to_period('M') # Para o gráfico mensal
print("DataFrame preparado com sucesso.")

# --- Gerando Relatórios Agrupados ---
vendas_por_categoria = df_vendas.groupby('Categoria_Produto')['Valor_Total_Venda'].sum().sort_values(ascending=False)
vendas_por_regiao = df_vendas.groupby('Regiao_Cliente')['Valor_Total_Venda'].sum().sort_values(ascending=False)
vendas_por_mes = df_vendas.groupby('Mes_Venda')['Valor_Total_Venda'].sum().sort_index(ascending=True).reset_index()

# --- Visualização dos Dados ---

# 1. Gráfico de Barras: Vendas Totais por Categoria de Produto
plt.figure(figsize=(10, 6))
sns.barplot(x=vendas_por_categoria.index, y=vendas_por_categoria.values, palette='viridis')
plt.title('Vendas Totais por Categoria de Produto')
plt.xlabel('Categoria de Produto')
plt.ylabel('Valor Total de Vendas (R$)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 2. Gráfico de Barras: Vendas Totais por Região do Cliente
plt.figure(figsize=(10, 6))
sns.barplot(x = vendas_por_regiao.index, y = vendas_por_regiao.values, palette = 'magma')
plt.title('Vendas Totais por Região do Cliente')
plt.xlabel('Região do Cliente')
plt.ylabel('Valor Total de Vendas (R$)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 3. Gráfico de Linhas: Vendas Totais por Mês (Análise Temporal)
plt.figure(figsize=(12, 6))
sns.lineplot(x=vendas_por_mes['Mes_Venda'].astype(str), y='Valor_Total_Venda', data=vendas_por_mes, marker='o')
plt.title('Tendência de Vendas Totais por Mês')
plt.xlabel('Mês da Venda')
plt.ylabel('Valor Total de Vendas (R$)')
plt.xticks(rotation = 45, ha = 'right')
plt.tight_layout()
plt.show()


# --- Integração com SQL (SQLite) ---

# Define o nome do arquivo do banco de dados SQLite
db_file = 'ecommerce_data.db'

try:
    # 1. Conexão com o Banco de Dados
    # Se o arquivo não existir, ele será criado.
    con = sqlite3.connect(db_file)
    cursor = con.cursor() # Um cursor permite executar comandos SQL
    print(f"\nConexão com o banco de dados '{db_file}' estabelecida com sucesso.")

    # 2. Criação da Tabela (se não existir)
    # Usamos IF NOT EXISTS para evitar erro se a tabela já existir em execuções futuras.
    # Definimos os tipos de dados para cada coluna.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            ID_Venda INTEGER PRIMARY KEY,
            Data_Venda TEXT,
            Nome_Produto TEXT,
            Categoria_Produto TEXT,
            Preco_Unitario REAL,
            Quantidade_Vendida INTEGER,
            Cliente_ID TEXT,
            Regiao_Cliente TEXT,
            Valor_Total_Venda REAL
        )
    ''')
    con.commit() # Salva as alterações no banco de dados (confirma a criação da tabela)
    print("Tabela 'vendas' verificada/criada com sucesso.")

    # --- CORREÇÃO AQUI: Converter Mes_Venda para string antes de inserir no SQL ---
    # Criamos uma cópia do DataFrame para não alterar o original que usamos para os gráficos
    df_vendas_para_sql = df_vendas.copy()
    df_vendas_para_sql['Mes_Venda'] = df_vendas_para_sql['Mes_Venda'].astype(str)
    print("Coluna 'Mes_Venda' convertida para string para inserção no SQL.")

    # 3. Inserção de Dados do DataFrame no SQLite
    # A função to_sql() do Pandas é super útil para isso!
    # 'vendas' é o nome da tabela, 'con' é a conexão com o BD.
    # 'if_exists='replace'' sobrescreve a tabela se ela já existir (cuidado em produção!).
    # 'index=False' evita que o índice do DataFrame seja gravado como uma coluna.
    df_vendas_para_sql.to_sql('vendas', con, if_exists='replace', index=False)
    print("Dados do DataFrame inseridos na tabela 'vendas' com sucesso.")

    # 4. Consulta de Dados do SQLite para um Novo DataFrame (Teste)
    # Recuperamos os dados que acabamos de inserir para provar que funcionou.
    df_vendas_sql = pd.read_sql_query("SELECT * FROM vendas", con)
    print("\n--- Dados recuperados do SQLite para um novo DataFrame ---")
    print(df_vendas_sql.head())

    # Verifica se os tipos de dados foram preservados (especialmente a data)
    print("\n--- Informações do DataFrame recuperado do SQL ---")
    df_vendas_sql.info()

except sqlite3.Error as e:
    print(f"Erro no SQLite: {e}")
finally:
    # Fecha a conexão com o banco de dados
    if con:
        con.close()
        print("Conexão com o banco de dados fechada.")

