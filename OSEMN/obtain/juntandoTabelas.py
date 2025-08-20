import pandas as pd
import glob
import os

# Caminho da pasta onde estão os arquivos CSV
pasta = "AssistiveDomotical\\OSEMN\\obtain\\tabelasBrutas"

# Pega todos os arquivos .csv da pasta
arquivos = glob.glob(os.path.join(pasta, "*.csv"))

# Lê e junta todos os CSVs
dfs = [pd.read_csv(arquivo) for arquivo in arquivos]
df_final = pd.concat(dfs, ignore_index=True)

# Salva em um novo CSV
df_final.to_csv("AssistiveDomotical\\OSEMN\\obtain\\tabela_unica.csv", index=False)

print("Tabelas unidas em 'tabela_unica.csv'")
print(df_final.shape)