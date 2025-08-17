import pandas as pd
import matplotlib.pyplot as plt

# Leitura e filtro
df = pd.read_csv("tabela_final.csv")
df = df[(df['frame_global'] > 9790) & (df['frame_global'] < 9820)]

# Cores para os pontos
cores = df['piscando'].map({False: 'red', True: 'green'})

plt.figure(figsize=(14, 6))

# Scatter plot do EAR
plt.scatter(df['timestamp'], df['ear'], c=cores, s=10, alpha=0.8)

# Destacar piscadas curtas ou longas
estado_atual = None
inicio = None

for i, row in df.iterrows():
    if row['estado'] != "nao piscou":
        if estado_atual != row['estado']:
            # Começo de um novo estado de piscada
            inicio = row['timestamp']
            estado_atual = row['estado']
    else:
        if estado_atual is not None:
            # Fim do estado de piscada, desenha faixa
            fim = row['timestamp']
            cor = 'blue' if estado_atual == 'piscou curto' else 'purple'
            plt.axvspan(inicio, fim, color=cor, alpha=0.2)
            estado_atual = None
            inicio = None

# Caso o último frame seja uma piscada
if estado_atual is not None and inicio is not None:
    fim = df['timestamp'].iloc[-1]
    cor = 'blue' if estado_atual == 'piscou curto' else 'purple'
    plt.axvspan(inicio, fim, color=cor, alpha=0.2)

plt.title('EAR vs Tempo com piscadas destacadas')
plt.xlabel('Tempo (s)')
plt.ylabel('EAR')
plt.grid(True)
plt.tight_layout()
plt.show()
