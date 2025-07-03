import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
vendas_por_mes = df_vendas.groupby('Mes_Venda')['Valor_Total_Venda'].sum().sort_values(ascending=True)

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
sns.lineplot(x = vendas_por_mes.index.astype(str), y = vendas_por_mes.values, markers='o')
plt.title('Tendência de Vendas Totais por Mês')
plt.xlabel('Mês da Venda')
plt.ylabel('Valor Total de Vendas (R$)')
plt.xticks(rotation = 45, ha = 'right')
plt.tight_layout()
plt.show()