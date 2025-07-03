# 📊 Sistema de Análise e Geração de Relatórios de E-commerce

---

## 💡 Sobre o Projeto

Este projeto em Python é uma solução para a **análise de dados de vendas de e-commerce e a geração automatizada de relatórios visuais**. Ele demonstra a integração de diversas bibliotecas essenciais para Data Science, bem como a aplicação de Programação Orientada a Objetos (POO) para uma arquitetura de código robusta e modular.

### 🎯 Objetivos Principais:

* **Processamento de Dados:** Carregar e pré-processar dados de vendas (simulados via CSV).
* **Análise Exploratória:** Realizar agrupamentos e calcular métricas chave para extrair insights.
* **Visualização:** Gerar gráficos claros e informativos para representar as tendências de vendas.
* **Persistência de Dados:** Armazenar os dados processados em um banco de dados SQLite.
* **Modularidade (POO):** Estruturar o código usando classes para gerenciamento de dados e banco de dados.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Pandas:** Manipulação e análise de dados tabulares.
* **Matplotlib:** Geração de gráficos estáticos.
* **Seaborn:** Biblioteca de visualização de dados baseada em Matplotlib, para gráficos mais estéticos.
* **SQLite3:** Banco de dados relacional leve para persistência de dados.

---

## 📂 Estrutura do Projeto

├── vendas.csv ------------ # Dados de vendas simulados

├── ecommerce_data.db ------------ # Banco de dados SQLite gerado pelo script

├── relatorios_imagens/ ------------ # Diretório onde os gráficos PNG são salvos

│   ├── vendas_por_categoria.png

│   ├── vendas_por_mes.png

│   └── vendas_por_regiao.png

└── main.py ------------ # Script principal do projeto

---

## 📈 Exemplos de Relatórios Gerados

Aqui estão alguns exemplos dos gráficos que o projeto gera:

### Vendas Totais por Categoria de Produto

![Vendas por Categoria](relatorios_imagens/vendas_por_categoria.png)

### Vendas Totais por Região do Cliente

![Vendas por Região](relatorios_imagens/vendas_por_regiao.png)

### Tendência de Vendas Totais por Mês

![Vendas por Mês](relatorios_imagens/vendas_por_mes.png)

---

## ✉️ Contato

* **Guilherme Rodrigues** - [Guilherme Rodrigues](https://www.linkedin.com/in/guilhrodrigues/)
* **Guilh-Code** - [https://github.com/Guilh-Code](https://github.com/Guilh-Code)
