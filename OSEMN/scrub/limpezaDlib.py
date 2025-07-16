import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("OSEMN/obtain/tabelasBrutas/totalDLIB.csv")

# Verificando nulos
print(df.isnull().sum())


# Verificando OUTLIERS

plt.figure(figsize=(4,5))
sns.boxplot(y=df['ear'])
plt.title('Boxplot das Ear - Identificação de Outliers')
plt.xlabel('ear')
plt.show()

df.to_csv("OSEMN/scrub/tabelasLimpas/tabela_tratada_dlib.csv", index=False)