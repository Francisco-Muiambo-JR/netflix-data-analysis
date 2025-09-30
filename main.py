import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent
CHARTS = BASE / "outputs" / "charts"
TABLES = BASE / "outputs" / "tables"
CHARTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)



'''
print("\n== Executar... ==")
print("Digite: ")
escolha = input("Quais? ").upper().split(",")

RUN_C1 = "C1" in escolha
RUN_P1 = "P1" in escolha
RUN_P2 = "P2" in escolha
RUN_P3 = "P3" in escolha
RUN_P4 = "P4" in escolha
RUN_P5 = "P5" in escolha
RUN_P6 = "P6" in escolha
RUN_P7 = "P7" in escolha
'''

RUN_C1 = True
RUN_P1 = True
RUN_P2 = True
RUN_P3 = True
RUN_P4 = True
RUN_P5 = True
RUN_P6 = True
RUN_P7 = True


# --------------carregamento dos Dados----------------
dt = pd.read_csv("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\Data\\netflix_data.csv")



# --------------Compreendendo o Dataframe----------------
if RUN_C1:
    print(dt.head())

    #Conhecendo o resumo técnico do DataFrame
    print(dt.info())

    #Conhecendo a quantidade de linhas e colunas
    print(dt.shape)

    #Conhecendo a distribuicao dos dados
    print(dt.describe())

    #Conhecendo os nomes das colunas
    print(dt.columns)

    #Verificando valores nulos
    print(dt.isna().sum())



# --------------Limpeza dos Dados----------------
# Padronizando os nomes no Type
dt['type'] = dt['type'].str.upper().str.strip()

#Separar a duracao, Minutos para filmes e Temporadas para TV SHOW
dt["duration_num"] = pd.to_numeric(dt["duration"], errors="coerce")
dt["movie_minutes"] = np.where(dt["type"]=="MOVIE", dt["duration_num"], np.nan)
dt["seasons"]       = np.where(dt["type"]=="TV SHOW", dt["duration_num"], np.nan)

# Adicionado coluna de conteúdos lancados recentes > 2015
dt['release_recently'] = dt['release_year'] > 2015



# --------------Exploracao dos Dados----------------
# P1: O catálogo tem mais Movies ou TV Shows?
if RUN_P1:
    quantidadeP1 = dt['type'].value_counts()
    perc = dt['type'].value_counts(normalize = True)
    tabela1 = pd.DataFrame(
        {
            'Quantidade' : quantidadeP1,
            'Percentagem' : perc
        }
    )
    print(tabela1)
    print()

    tabela = tabela1.reset_index().rename(columns={'index': 'type'})
    tabela1.plot(kind='bar', y = 'Quantidade', legend=False, title='Distribuição de Filmes vs TV SHOW')
    plt.xlabel('Type')
    plt.xticks(rotation=0)
    plt.ylabel('Quantidade')
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs/\\Charts\\grafico1.png")
    plt.show()
    plt.close()

    tabela1.to_csv(TABLES / "tabelaP1.csv", index=False, encoding="utf-8")

    print("\n[P1] Markdown pra README:\n")

# P2: Em que anos houve mais lançamentos? Crescimento ou retração?
if RUN_P2:
    quantidadeP2 = dt['release_year'].value_counts()
    tabela22 = pd.DataFrame(
        {
            'Quantidade' : quantidadeP2
        }
    )
    tabela222 = tabela22.head(5)
    tabela2 = tabela222.sort_index()
    print(tabela2)

    #Tendencia TOP 5
    tabela2.plot(kind='bar', y='Quantidade', legend=False, title='Tendência de Lançamentos por Ano - TOP 5')
    plt.xlabel('Ano de Lancamento')
    plt.xticks(rotation=0)
    plt.ylabel('Quantidade')
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs\\Charts\\grafico2.png")
    plt.show()
    plt.close()

    #Tendencia Cronológica
    tabela21 = tabela22.sort_index()
    tabela21.plot(kind='line', y='Quantidade', legend=False, title='Tendência de Lançamentos por Ano')
    plt.xlabel('Ano de Lancamento')
    plt.xticks(rotation=0)
    plt.ylabel('Quantidade')
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs\\Charts\\grafico3.png")
    plt.show()
    plt.close()

    tabela2.to_csv(TABLES / "tabelaP2.csv", index=False, encoding="utf-8")
    tabela21.to_csv(TABLES / "tabelaP21.csv", index=False, encoding="utf-8")
    print("\n[P1] Markdown pra README:\n")



# P3: Quais os Países dominam o catálogo? Existe concentracao?
if RUN_P3:
    tabelaP3 = dt.pivot_table(index = 'country', columns = 'type', values = 'title', aggfunc= 'count', fill_value=0)
    tabelaP3['Total'] = tabelaP3.sum(axis=1)
    tabelaP3['Percentual'] = tabelaP3['Total']/tabelaP3['Total'].sum()*100
    print(tabelaP3.sort_values('Total', ascending = False).head(10))

    graficoP3 = tabelaP3.sort_values('Total', ascending = False).head(10)
    graficoP3.plot(kind='barh', y = 'Total', legend=False, title='Paises dominantes do catálogo')
    plt.xlabel('Quantidade de títulos')
    plt.ylabel('Países')
    plt.xticks(rotation=0)
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs\\Charts\\grafico4.png")
    plt.show()
    plt.close()

    tabelaP3.to_csv(TABLES / "tabelaP3.csv", index=False, encoding="utf-8")



# P4: Quais os Géneros mais populares

if RUN_P4:
    tabelaP4 = dt.pivot_table(values = 'title', index = 'genre', columns = 'type', aggfunc = 'count', fill_value=0)
    tabelaP4['Total'] = tabelaP4.sum(axis=1)
    print(tabelaP4.sort_values('Total', ascending = False).head(10))

    graficoP4 = tabelaP4.sort_values('Total', ascending = False).head(10)
    graficoP4.plot(kind = 'barh', y = 'Total', legend = False, title = 'Gêneros mais Populares - TOP 10')
    plt.xlabel('Quantidade de títulos')
    plt.ylabel('Gêneros')
    plt.xticks(rotation = 0)
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs\\Charts\\grafico5.png")
    plt.show()
    plt.close()

    tabelaP4.to_csv(TABLES / "tabelaP4.csv", index=False, encoding="utf-8")



# P5: Qual é a duração típica? Filmes muito longos valem a pena?
if RUN_P5:
    print(dt['movie_minutes'].describe())
    tabelaP5 = dt['movie_minutes'].describe()

    #plt.subplot(1, 2, 1)
    plt.hist(dt['movie_minutes'], bins=30, edgecolor='black')
    plt.title('Distribuição das Durações dos Filmes')
    plt.xlabel('Duração (minutos)')
    plt.ylabel('Quantidade de Filmes')
    plt.xticks(rotation=0)
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs\\Charts\\grafico6.png")
    plt.show()
    plt.close()

    tabelaP5.to_csv(TABLES / "tabelaP5.csv", index=False, encoding="utf-8")



# P6: Quais diretores/Actores mais frequentes (potenciais parcerias)?
if RUN_P6:
    pessoas = dt['director'].fillna('') + ',' + dt['cast'].fillna('')
    pessoas = pessoas.str.split(',').explode().str.strip()
    pessoas = pessoas[pessoas != '']
    print("Total de pessoas únicas no catálogo:", pessoas.nunique())
    top20 = pessoas.value_counts().head(20)
    tabelaP6 = pd.DataFrame(
        {
            'Parceiros' : top20.index,
            'QuantidadeAparicões' : top20.values
        }
    )
    print(tabelaP6)

    top20.plot(kind = 'barh' ,legend = False, title = 'Top 20 Paceiros mais frequentes')
    plt.xlabel('Quantidade de Títulos')
    plt.ylabel('Parceiros')
    plt.xticks(rotation=0)
    plt.tight_layout();
    plt.savefig("D:\\Cursos\\Datacamp\\Projectos\\análise-de-dados-netflix\\outputs\\Charts\\grafico7.png")
    plt.show()
    plt.close()

    tabelaP6.to_csv(TABLES / "tabelaP6.csv", index=False, encoding="utf-8")



# P7: Quais géneros são fortes por país? Onde ajustar investimento?
if RUN_P7:
    top_countries = dt['country'].value_counts().head(10).index
    top_genres = dt['genre'].value_counts().head(6).index
    df_top = dt[dt['country'].isin(top_countries) & dt['genre'].isin(top_genres)]
    tabelaP7 = df_top.pivot_table(
        values='title',
        index='country',
        columns='genre',
        aggfunc='count',
        fill_value=0
    )
    print(tabelaP7)
    tabelaP7.to_csv(TABLES / "tabelaP7.csv", index=False, encoding="utf-8")
