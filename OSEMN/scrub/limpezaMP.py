import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("OSEMN/obtain/tabelasBrutas/totalMP.csv")

# Trocando de negativo para positivo

df['ear'] = df['ear'].abs()


# Verificando nulos
print(df.isnull().sum())


# Verificando OUTLIERS

plt.figure(figsize=(4,5))
sns.boxplot(y=df['ear'])
plt.title('Boxplot das Ear - Identificação de Outliers')
plt.xlabel('ear')
plt.show()

# Perceba que existem diversos outliers
# dentro deles vão existir dois: os verdes, os vermelhos
# sendo os verdes aqueles que representam o olho aberto
# e os vermelhos os que representam o olho fechado


df_ear_verde = df[df["piscando"] == "verde"]["ear"]
df_ear_vermelho = df[df["piscando"] == "vermelho"]["ear"]

# Utilizando o metodo IQR (Intervalo Interquartil)

print("\nVERDES: ")

MIN = df_ear_verde.quantile(0.0)
Q1 = df_ear_verde.quantile(0.25)
Q3 = df_ear_verde.quantile(0.75)
Q2 = df_ear_verde.quantile(0.50)
MAX = df_ear_verde.quantile(1.0)

mediana = df_ear_verde.median()

IQR = Q3 - Q1


print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}, Q2: {Q2}, Median: {mediana}, MAX: {MAX}, MIN: {MIN}")

# Definindo Limites

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
print(f"Limite inferior: {limite_inferior}")
print(f"Limite superior: {limite_superior}")

df.loc[
    (df["piscando"] == "verde") &
    ((df["ear"] > limite_superior) |
    (df["ear"] < limite_inferior)),
    "ear"
] = mediana



print("\nVERMELHOS:")

MIN = df_ear_vermelho.quantile(0.0)
Q1 = df_ear_vermelho.quantile(0.25)
Q3 = df_ear_vermelho.quantile(0.75)
Q2 = df_ear_vermelho.quantile(0.50)
MAX = df_ear_vermelho.quantile(1.0)

mediana = df_ear_vermelho.median()

IQR = Q3 - Q1

print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}, Q2: {Q2}, Median: {mediana}, MAX: {MAX}, MIN: {MIN}")

# Definindo Limites

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
print(f"Limite inferior: {limite_inferior}")
print(f"Limite superior: {limite_superior}")

df.loc[
    (df["piscando"] == "vermelho") &
    ((df["ear"] > limite_superior) |
    (df["ear"] < limite_inferior)),
    "ear"
] = mediana


# Tabela pós tratamento

plt.figure(figsize=(4,5))
sns.boxplot(y=df['ear'])
plt.title('Boxplot das Ear - Identificação de Outliers')
plt.xlabel('ear')
plt.show()


df.to_csv("OSEMN/scrub/tabelasLimpas/tabela_tratada_mp.csv", index=False)
