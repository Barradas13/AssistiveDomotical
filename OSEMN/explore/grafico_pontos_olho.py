import matplotlib.pyplot as plt

# Lista de pontos
pontos = [(-12, -3), (-9, -2), (-4, 0), (1, 1), (6, 2), (10, 2), (13, 2), (13, 2), (10, 3), (-1, 5), (1, 2), (-4, 1), (-9, -1), (-12, -2), (-7, -1), (0, 0), (6, 1), (-14, -3), (6, 3)]

# Separar coordenadas X e Y
labels = [398, 384, 385, 386, 387, 388, 466, 249, 390, 477, 
          374, 380, 381, 382, 476, 473, 474, 362, 373]

# Separar coordenadas X e Y
x, y = zip(*pontos)

# Criar gráfico de dispersão
plt.figure(figsize=(6, 6))
plt.scatter(x, y, color="blue", marker="o", s=50)

# Adicionar rótulos em cada ponto
for (xi, yi, label) in zip(x, y, labels):
    plt.text(xi + 0.3, yi + 0.3, str(label), fontsize=9, color="red")

# Configurações
plt.title("Pontos com numeração")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.show()
