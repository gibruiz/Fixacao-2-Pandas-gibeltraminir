import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Top_scientists_2021.csv', index_col='authfull')
# print(data.head())
# print(data.isna().any(axis=0))

# Há nulos no nome da instituição, país e subárea de pesquisa. Para as análises deste documento, não precisaremos mexer com os valores faltantes
# Vamos tirar as colunas que não nos interessam
data.drop(index=[2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], axis=1, inplace=True)
print(data.columns())

# E agora renomear as colunas que ficaram
col_names = {
  'authfull': 'author_name',
  'inst_name': 'institution',
  'cntry': 'country',
  'firstyr': 'first_year_pub',
  'lastyr': 'last_year_pub',
  'h21': 'h_index_2021',
  'sm-field': 'field_of_study',
  'self%': 'self_citation_percent',
  'nc9621': 'total_citations_96_21',
  'ncs': 'cites_single',
  'ncsf': 'cites_single_first',
  'ncsfl': 'cites_single_first_last'
}
data = data.rename(col_names, axis=1)

### Qual a razão entre a quantidade de citações de um cientista como pesquisador principal (último autor, excluindo artigos como primeiro autor mas incluindo os como único autor) e o total de citações no período analisado?

data['ratio_last_author-total'] = (data['cites_single_first_last'] - data['cites_single_first'] + data['cites_single']) / data['total_citations_96_21']

# Utilizar as seguintes funções pelo menos uma vez:
    # fillna, drop ou dropna;
# drop nas colunas que nao quero


    # rename;


# Realizar duas manipulações aritméticas necessárias na base de dados (soma, multiplicação, divisão, etc.); OK



# Criar duas novas colunas, que venham a partir de alguma estatística (mean, median, max, etc.);OK



# Filtrar dados que sejam relevantes (filtros, query ou where);



# Utilizar o groupby, gerando alguma constatação estatística interessante;



# Exportar um dataframe para um CSV, desde que não seja igual ao original;



# Gerar um gráfico a partir de qualquer dataframe utilizado no programa (matplotlib);



# Utilizar o pd.qcut ou o pd.cut.