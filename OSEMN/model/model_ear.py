import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib  # para salvar o modelo

# Carregar CSVs
file_paths = [
    "bruno.csv", "erik.csv", "felipe.csv", "guilherme.csv",
    "jao.csv", "jose.csv", "lo.csv"
]

dfs = [pd.read_csv(f"/home/barradas/Downloads/AssistiveDomotical-1/OSEMN/scrub/tabelas_pessoa_pos_tratamento/{fp}") for fp in file_paths]

# Normalizar coluna "piscando"
for df in dfs:
    df["piscando"] = df["piscando"].map({False: 0, True: 1})

# Inicializa matriz de confusão acumulada
cm_total = np.zeros((2, 2))

# Validação leave-one-subject-out
for idx, df_test in enumerate(dfs):
    df_train = pd.concat([df for j, df in enumerate(dfs) if j != idx], ignore_index=True)
    
    X_train = df_train[["ear1","ear2","ear3","ear4","ear5"]]
    y_train = df_train["piscando"]
    
    X_test = df_test[["ear1","ear2","ear3","ear4","ear5"]]
    y_test = df_test["piscando"]
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    cm = confusion_matrix(y_test, y_pred)
    cm_total += cm

# Mostrar matriz de confusão acumulada
disp = ConfusionMatrixDisplay(confusion_matrix=cm_total.astype(int), display_labels=[0,1])
disp.plot()
plt.title("Matriz de Confusão Média")
plt.show()

# Treinar modelo final em todos os dados
df_all = pd.concat(dfs, ignore_index=True)
X_all = df_all[["ear1","ear2","ear3","ear4","ear5"]]
y_all = df_all["piscando"]

final_model = RandomForestClassifier(random_state=42)
final_model.fit(X_all, y_all)

# Salvar modelo em .joblib
joblib.dump(final_model, "/home/barradas/Downloads/AssistiveDomotical-1/")
print("Modelo salvo em final_model.joblib")
