import pandas as pd
import numpy as np

df = pd.read_csv("/home/barradas/Downloads/AssistiveDomotical/tabelas/totalMP.csv")

print(df.isnull().sum()) #note, nenhum nulo
