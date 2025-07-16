import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("OSEMN/scrub/tabelasLimpas/tabela_tratada_dlib.csv")

df = df[(df['timestamp'] > 400.0) & (df['timestamp'] < 430.0)]

cores = df['piscando'].map({'vermelho': 'red', 'verde': 'green'})

plt.figure(figsize=(14, 6))
plt.scatter(df['timestamp'], df['ear'], c=cores, s=10, alpha=0.8)


plt.title('EAR vs Tempo (com piscando em cores) DLIB')
plt.xlabel('Tempo (s)')
plt.ylabel('EAR')
plt.grid(True)
plt.tight_layout()


plt.show()

df = pd.read_csv("OSEMN/scrub/tabelasLimpas/tabela_tratada_mp.csv")

df = df[(df['timestamp'] > 400.0) & (df['timestamp'] < 430.0)]

cores = df['piscando'].map({'vermelho': 'red', 'verde': 'green'})

plt.figure(figsize=(14, 6))
plt.scatter(df['timestamp'], df['ear'], c=cores, s=10, alpha=0.8)


plt.title('EAR vs Tempo (com piscando em cores) MP')
plt.xlabel('Tempo (s)')
plt.ylabel('EAR')
plt.grid(True)
plt.tight_layout()


plt.show()