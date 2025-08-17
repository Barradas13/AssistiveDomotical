import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("AssistiveDomotical\\OSEMN\\obtain\\tabela_unica.csv")

df = df[(df['timestamp'] > 400.0) & (df['timestamp'] < 430.0)]

print(df.head())