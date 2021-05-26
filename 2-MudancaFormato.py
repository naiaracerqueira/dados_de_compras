import pandas as pd
import json

dataset = pd.read_json("data.json")
print(dataset.head())
# A coluna de ItemList possui dicionário, vou verificar qual o formato do dicionário:
print(dataset['ItemList'][0])
#'ProductName','Value','Quantity'

def um_dataframe():
    with open('data.json','r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data, 'ItemList', ['CreateDate','EmissionDate','Discount','NFeNumber','NFeID'], record_prefix='ItemList_')
    df = df[['CreateDate','EmissionDate','Discount','NFeNumber','NFeID','ItemList_ProductName','ItemList_Value','ItemList_Quantity']]
    print(df.head())
    return df

def tabela_fato():
    fato = pd.read_json("data.json")
    fato.drop(columns='ItemList', inplace=True)
    print(fato.head())
    return fato

def tabela_dimensao():
    with open('data.json','r') as f:
        data = json.loads(f.read())
    dim_itens = pd.json_normalize(data, 'ItemList', ['NFeID'])
    print(dim_itens.head())
    # A chave é a coluna de NFeID!!!
    return dim_itens


if __name__ == "__main__":
    df_geral = um_dataframe()
    df_fato = tabela_fato()
    df_dim = tabela_dimensao()

    # salvar em formato csv se necessário:
    df_fato.to_csv('fato.csv')
    df_dim.to_csv('dim_itens.csv')




