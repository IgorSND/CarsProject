import pandas as pd

# Lista de arquivos Excel para unir
arquivos = ['resultados_carrosIPVAPAGO1.xlsx', 'resultados_carrosIPVAPAGO2.xlsx', 'resultados_carrosIPVAPAGO3.xlsx', 'resultados_carrosIPVAPAGO4.xlsx', 'resultados_carrosIPVAPAGO5.xlsx', 'resultados_carrosIPVAPAGO6.xlsx']

# Lista para armazenar os DataFrames
dfs = []

for arquivo in arquivos:
    # Carrega o DataFrame do arquivo Excel
    df = pd.read_excel(arquivo, sheet_name='Sheet1')  # Ajuste o nome da planilha se necessário
    dfs.append(df)

# Concatena todos os DataFrames na lista
tabela_unida = pd.concat(dfs, ignore_index=True)

# Salva o DataFrame unido em um novo arquivo Excel
tabela_unida.to_excel('tabela_unidaCarrosIPVAPago.xlsx', index=False)
