import matplotlib.pyplot as plt

# Lista de pontos
pontos = [(-11, -3), (-8, -2), (-3, 0), (2, 1), (7, 2), (11, 2), (14, 2), (13, 2), (11, 2), (0, 5), (2, 2), (-4, 1), (-8, -1), (-11, -2), (-6, -1), (0, 0), (7, 0), (-13, -3), (7, 2)]

# Separar coordenadas X e Y
labels = [398, 384, 385, 386, 387, 388, 466, 249, 390, 477, 
          374, 380, 381, 382, 476, 473, 474, 362, 373]

# Separar coordenadas X e Y
x, y = zip(*pontos)

# Criar gráfico de dispersão
plt.figure(figsize=(6, 6))
plt.scatter(x, y, color="black", marker="o", s=50)

# Adicionar rótulos em cada ponto
for (xi, yi, label) in zip(x, y, labels):
    plt.text(xi + 0.3, yi + 0.3, str(label), fontsize=9, color="black")

# Configurações
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.show()
plt.savefig('olho_fechado.png', dpi=300)