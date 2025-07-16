import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/tabelas/totalDLIB.csv")

df = df[df['timestamp'] < 30.0]

cores = df['piscando'].map({'vermelho': 'red', 'verde': 'green'})

plt.figure(figsize=(14, 6))
plt.scatter(df['timestamp'], df['ear'], c=cores, s=10, alpha=0.8)


plt.title('EAR vs Tempo (com piscando em cores) DLIB')
plt.xlabel('Tempo (s)')
plt.ylabel('EAR')
plt.grid(True)
plt.tight_layout()


plt.show()

df = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/tabelas/totalMP.csv")

df = df[df['timestamp'] < 30.0]

cores = df['piscando'].map({'vermelho': 'red', 'verde': 'green'})

plt.figure(figsize=(14, 6))
plt.scatter(df['timestamp'], df['ear'], c=cores, s=10, alpha=0.8)


plt.title('EAR vs Tempo (com piscando em cores) MP')
plt.xlabel('Tempo (s)')
plt.ylabel('EAR')
plt.grid(True)
plt.tight_layout()


plt.show()