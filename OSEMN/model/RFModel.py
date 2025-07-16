import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

# Obter os dados
df = pd.read_csv("../tabelas/saida.aviMP.csv")

# Limpeza e pré-processamento
# Converter a coluna 'piscando' para numérica
le = LabelEncoder()
df['piscando'] = le.fit_transform(df['piscando'])  # Ex: vermelho -> 1, verde -> 0

# slecionar as colunas e o alvo
X = df[['ear', 'fps', 'tempo_processamento']]  # colunas que ajudam na previsão
y = df['piscando']                             # variável alvo

# Normalizar as colunas
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

acr = []

for i in range(100): # testando varias seeds dos dados
# treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=i)

    # treinar o modelo
    clf = RandomForestClassifier(n_estimators=50, random_state=10)
    clf.fit(X_train, y_train)

    # fazer previsões
    y_pred = clf.predict(X_test)

    acr.append(accuracy_score(y_test, y_pred))
    print("Acurácia:", accuracy_score(y_test, y_pred))
    #print(classification_report(y_test, y_pred))

minAcr = min(acr)
maxAcr = max(acr)
mediaAcr = np.mean(np.array(acr))
print("Acuracia media final ",mediaAcr)
print("Menor acuracia: ", minAcr)
print("Maior acuracia: ", maxAcr)