import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

# ============================
# 1️⃣ Leitura e preparação
# ============================
df = pd.read_csv("C:\\Users\\claudio.barradas\\PycharmProjects\\Domotic\\teste\\tabela_final.csv")

# Converte estado para numérico
estado_map = {"nao piscou": 0, "piscou curto": 1, "piscou longo": 2}
df["estado_num"] = df["estado"].map(estado_map)

# Marca início de cada novo vídeo/pessoa
df["nova_pessoa"] = df["frame_idx"] == 1
df["pessoa_id"] = df["nova_pessoa"].cumsum()

# ============================
# 2️⃣ Separar treino/teste por pessoa
# ============================
pessoas = df["pessoa_id"].unique()
pessoas_train, pessoas_test = train_test_split(pessoas, test_size=0.2, random_state=42)

train_df = df[df["pessoa_id"].isin(pessoas_train)].reset_index(drop=True)
test_df = df[df["pessoa_id"].isin(pessoas_test)].reset_index(drop=True)

# ============================
# 3️⃣ Criar janelas temporais
# ============================
window_size = 20  # ajuste quantos frames quiser por janela

def criar_janelas(df, window_size=20):
    X, y = [], []
    for start in range(len(df) - window_size):
        end = start + window_size
        window = df.iloc[start:end]

        # Features: EAR + timestamp
        seq = window[["ear", "timestamp"]].values
        X.append(seq)

        # Label: estado do último frame
        y.append(window["estado_num"].iloc[-1])
    return np.array(X), np.array(y)

X_train, y_train = criar_janelas(train_df, window_size)
X_test, y_test = criar_janelas(test_df, window_size)

# One-hot encoding do label
y_train_cat = to_categorical(y_train, num_classes=3)
y_test_cat = to_categorical(y_test, num_classes=3)

# ============================
# 4️⃣ Criar e treinar LSTM
# ============================
model = Sequential()
model.add(LSTM(64, input_shape=(window_size, 2), return_sequences=False))
model.add(Dense(32, activation="relu"))
model.add(Dense(3, activation="softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()

# Treinamento
model.fit(X_train, y_train_cat, epochs=20, batch_size=32, validation_split=0.2)

# ============================
# 5️⃣ Avaliar
# ============================
loss, acc = model.evaluate(X_test, y_test_cat)
print(f"Accuracy no teste: {acc*100:.2f}%")

# ============================
# 6️⃣ Previsões
# ============================
y_pred_prob = model.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)

# Converte de volta para rótulos originais
estado_map_inv = {0:"nao piscou", 1:"piscou curto", 2:"piscou longo"}
y_pred_labels = [estado_map_inv[i] for i in y_pred]

# Exemplo de visualização
for i in range(10):
    print(f"Predito: {y_pred_labels[i]}, Real: {estado_map_inv[y_test[i]]}")
