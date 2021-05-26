import pandas as pd
import json

# Considerando que seria um projeto de Big Data, o ideal seria ter utilizado spark
# E, considerando esse volume maior, o ideal seria enviar esses dados para um banco de dados relacional

# Outro ponto de melhora seria na transformação das tabelas fato e dimensão, não acredito que essa seja a melhor solução disponível
# (Ex: acabei tendo que fazer um drop da coluna ItemList)

dataset = pd.read_json("data.json")
print(dataset.head())
# A coluna de ItemList possui dicionário, vou verificar qual o formato do dicionário:
print("\nVerificar um dicionário:",dataset['ItemList'][0])
#'ProductName','Value','Quantity'

def um_dataframe():
    '''
    Cria um dataframe unificado, com as colunas do ItemList
    '''
    with open('data.json','r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data, 'ItemList', ['CreateDate','EmissionDate','Discount','NFeNumber','NFeID'], record_prefix='ItemList_')
    df = df[['CreateDate','EmissionDate','Discount','NFeNumber','NFeID','ItemList_ProductName','ItemList_Value','ItemList_Quantity']]
    print("\n",df.head())
    return df

def tabela_fato():
    '''
    Cria a tabela fato.
    '''
    fato = pd.read_json("data.json")
    fato.drop(columns='ItemList', inplace=True)
    print("\n",fato.head())
    return fato

def tabela_dimensao():
    '''
    Cria a tabela dimensão com detalhamento dos itens contidos na nota fiscal.
    É importante considerar que a chave é a coluna de NFeID.
    '''
    with open('data.json','r') as f:
        data = json.loads(f.read())
    dim_itens = pd.json_normalize(data, 'ItemList', ['NFeID'])
    print("\n",dim_itens.head())
    return dim_itens


if __name__ == "__main__":
    df_geral = um_dataframe()
    df_fato = tabela_fato()
    df_dim = tabela_dimensao()

    # salvar em formato csv se necessário:
    df_fato.to_csv('fato.csv')
    df_dim.to_csv('dim_itens.csv')




