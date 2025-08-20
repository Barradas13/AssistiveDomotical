import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from joblib import dump
import ast  # para converter string em lista de tuplas
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

# Criar modelo
knn_model = KNeighborsClassifier(n_neighbors=5)  # n_neighbors é o número de vizinhos

# Criar modelo
lr_model = LogisticRegression(random_state=42, max_iter=1000)

# Lista dos arquivos
file_paths = [
    "bruno.csv", "erik.csv", "felipe.csv", "guilherme.csv",
    "jao.csv", "jose.csv", "lo.csv"
]

dfs = [pd.read_csv(f"/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/{fp}") for fp in file_paths]

# Normaliza coluna "piscando"
for df in dfs:
    df["piscando"] = df["piscando"].map({False: 0, True: 1})

# Converte colunas de pontos em listas de tuplas e achata para colunas numéricas
pontos_cols = ["pontos_olhos 1", "pontos_olhos 2", "pontos_olhos 3", "pontos_olhos 4", "pontos_olhos 5"]

for df in dfs:
    for col in pontos_cols:
        df[col] = df[col].apply(ast.literal_eval)  # transforma string em lista de tuplas
        # cria 19 colunas x e 19 colunas y para cada pontos_olhos
        df[[f"{col}_x{j}" for j in range(19)]] = pd.DataFrame(df[col].apply(lambda pts: [p[0] for p in pts]).tolist())
        df[[f"{col}_y{j}" for j in range(19)]] = pd.DataFrame(df[col].apply(lambda pts: [p[1] for p in pts]).tolist())

# Lista de todas as novas colunas numéricas dos olhos
feature_cols = []
for col in pontos_cols:
    feature_cols += [f"{col}_x{j}" for j in range(19)] + [f"{col}_y{j}" for j in range(19)]

# Matriz de confusão total
cm_total = np.zeros((2,2))

# Leave-one-subject-out
for idx, df_test in enumerate(dfs):
    df_train = pd.concat([df for j, df in enumerate(dfs) if j != idx], ignore_index=True)
    
    X_train = df_train[feature_cols]
    y_train = df_train["piscando"]
    
    X_test = df_test[feature_cols]
    y_test = df_test["piscando"]
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    cm = confusion_matrix(y_test, y_pred)
    cm_total += cm

# Exibe matriz de confusão
disp = ConfusionMatrixDisplay(confusion_matrix=cm_total.astype(int), display_labels=[0,1])
disp.plot()
plt.title("Matriz de Confusão Média LogisticRegression")
plt.show()

# Treina modelo final em todos os dados
df_all = pd.concat(dfs, ignore_index=True)
X_all = df_all[feature_cols]
y_all = df_all["piscando"]

final_model = DecisionTreeClassifier(random_state=42)
final_model.fit(X_all, y_all)

# Salvar modelo
dump(final_model, "/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/final_model-2.joblib")
print("Modelo salvo em modelo_piscando_olhos.joblib")
