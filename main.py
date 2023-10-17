import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Top_scientists_2021.csv', index_col='authfull')
# print(data.head())
# print(data.isna().any(axis=0))

# Há nulos no nome da instituição, país e subárea de pesquisa. Para as análises deste documento, não precisaremos mexer com os valores faltantes
# Vamos tirar as colunas que não nos interessam
data.drop(columns=['np6021', 'rank (ns)', 'nc9621 (ns)',
                   'h21 (ns)', 'hm21 (ns)', 'nps (ns)',
                   'ncs (ns)', 'cpsf (ns)', 'ncsf (ns)',
                   'npsfl (ns)', 'ncsfl (ns)', 'c (ns)',
                   'npciting (ns)', 'cprat (ns)',
                   'np6021 cited9621 (ns)', 'rank','hm21', 
                   'nps', 'cpsf', 'npsfl', 'c',
                   'npciting', 'cprat', 'np6021 cited9621',
                   'np6021_d', 'nc9621_d','sm-subfield-1',
                   'sm-subfield-1-frac', 'sm-subfield-2',
                   'sm-subfield-2-frac', 'sm-field-frac',
                   'rank sm-subfield-1',
                   'rank sm-subfield-1 (ns)',
                   'sm-subfield-1 count'], axis=1, inplace=True)
# print(data.head())


# E agora renomear as colunas que ficaram
col_names = {
  'authfull': 'author_name',
  'inst_name': 'institution',
  'cntry': 'country',
  'firstyr': 'first_year_pub',
  'lastyr': 'last_year_pub',
  'h21': 'h_index_2021',
  'self%': 'self_citation_percent',
  'nc9621': 'total_citations_96_21',
  'ncs': 'cites_single',
  'ncsf': 'cites_single_first',
  'ncsfl': 'cites_single_first_last',
  'sm-field': 'field_of_study'
}
data.rename(col_names, axis=1, inplace = True)
# print(data.head())

### Qual a razão entre a quantidade de citações de um cientista como pesquisador principal (último autor, excluindo artigos como primeiro autor mas incluindo os como único autor) e o total de citações no período analisado?

data['ratio_last_author-total'] = (data['cites_single_first_last'] - data['cites_single_first'] + data['cites_single']) / data['total_citations_96_21']
print(data['ratio_last_author-total'])



### Esse cientista está na ativa há mais ou menos anos que a média? (desvio com relação à media)
data['years_active'] = data['last_year_pub'] - data['first_year_pub']
def desvio(row):
    return data['years_active'].mean() - row['years_active']
data['deviation'] = data.apply(desvio, axis=1)
print('\n', data['deviation'])



### Quantos e quais são os cientistas brasileiros nessa base?
### Em média, têm mais ou menos anos de atividade que a média geral?
brasileiros = data[data['country'] == 'bra']
print(f'\nHá {len(brasileiros)} pesquisadores brasileiros dentre os mais citados no mundo.\nAqui estão seus nomes e instituições de origem:')
print(brasileiros.iloc[:,0])
desv_bra = brasileiros['deviation']
print(f'Em média, os cientistas brasileiros desviam {round(desv_bra.mean())} da média (para cima) em anos de atividade')



### Quantos cientistas já não estão mais na ativa?
# a base é de 2021 mas há cientistas com publicações com datas posteriores - prática comum quando um artigo é aprovado mas não será publicado de imediato.
# para facilitar, trocamos todas essas extras para 2021.
data['last_year_pub'].replace([2022, 2023, 2024], 2021, inplace=True)
print('\n', data['last_year_pub'].head())

# consideramos que um cientista que não publicou em 2021 não está mais em atividade
print('\n', len(data[data['last_year_pub'] != data['last_year_pub'].max()]), 'cientistas da base não estão mais em atividade.')



### Sabemos que o índice de citações (h-index) é diferente de acordo com a área de pesquisa.
### Qual a média e o valor máximo do h-index por área de estudo ao final de 2021?

x = {'h_index_2021': ['mean', 'min', 'max', 'median']}
estatisticas = data.groupby('field_of_study').agg(x)
print('\n', estatisticas)


### Uma prática ruim na ciência é a auto-citação, feita com a intenção de aumentar as métricas de citação.
### Com relação à porcentagem de auto-citação por autor, como se distribui?

plt.hist(data['self_citation_percent'])
plt.show(block = False)

### Quais os quartis?
data['self_citation_percent_q'], quartis = pd.qcut(data['self_citation_percent'], 4, labels=['min a Q1', 'Q1 a Q2', 'Q2 a Q3', 'Q3 a max'], retbins=True)
print('\n', quartis)

### Classificando pelos quartis, qual a média e os valores mínimos e máximos de h-index? Isto é, autores com essa prática são de fato mais bem-sucedidos em citações?
y = {'h_index_2021': ['mean', 'min', 'max']}
stat = data.groupby('self_citation_percent_q').agg(y)
print('\n', stat)


### Exportando o dataframe para um arquivo csv
data.to_csv('citations_cientists.csv')
