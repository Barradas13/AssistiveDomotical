import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("AssistiveDomotical\\OSEMN\\obtain\\tabela_com_estado.csv")


# Mostra apenas as linhas onde pontos_olho é Null (NaN)
linhas_nulas = df[df["pontos_olho"].isna()]

df.loc[df["pontos_olho"].isna(), "ear"] = np.nan


# Verificando nulos
print(df.isnull().sum())

df["pontos_olho"] = df["pontos_olho"].fillna(method="ffill")

df["pontos_olho"] = df["pontos_olho"].fillna(method="bfill")


df["ear"] = df["ear"].fillna(method="ffill")

df["ear"] = df["ear"].fillna(method="bfill")

# Verificando OUTLIERS

plt.figure(figsize=(4,5))
sns.boxplot(y=df['ear'])
plt.title('Boxplot das Ear - Identificação de Outliers')
plt.xlabel('ear')
plt.show()

l_s = 35
l_i = 0

df.loc[df["ear"] > l_s, "ear"] = l_s
df.loc[df["ear"] < l_i, "ear"] = l_i


# Tabela pós tratamento

plt.figure(figsize=(4,5))
sns.boxplot(y=df['ear'])
plt.title('Boxplot das Ear - Identificação de Outliers')
plt.xlabel('ear')
plt.show()


df.to_csv("tabela_tratada_mp.csv", index=False)
