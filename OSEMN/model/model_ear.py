import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

df_bruno = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/bruno.csv")
df_erik = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/erik.csv")
df_felipe = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/felipe.csv")
df_guilherme = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/guilherme.csv")
df_jao = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/jao.csv")
df_jose = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/jose.csv")
df_lo = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/lo.csv")


# Lista de dataframes
dfs = [
    df_bruno, df_erik, df_felipe, df_guilherme, df_jao, df_jose, df_lo
]

# Normaliza coluna "piscando" para 0 e 1
for i in dfs:
    i["piscando"] = i["piscando"].map({False: 0, True: 1})

cm_total = np.zeros((2,2))

for idx, df_test in enumerate(dfs):
    df_train = pd.concat([df for j, df in enumerate(dfs) if j != idx], ignore_index=True)
    
    X_train = df_train[["ear1","ear2","ear3","ear4","ear5"]]
    y_train = df_train["piscando"]
    
    X_test = df_test[["ear1","ear2","ear3","ear4","ear5"]]
    y_test = df_test["piscando"]
    
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    cm = confusion_matrix(y_test, y_pred)
    cm_total += cm


disp = ConfusionMatrixDisplay(confusion_matrix=cm_total, display_labels=[0,1])
disp.plot()
plt.title("Matriz de Confusão Média")
plt.show()