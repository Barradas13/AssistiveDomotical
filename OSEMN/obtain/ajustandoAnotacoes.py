import pandas as pd

# Lê a tabela
df = pd.read_csv("AssistiveDomotical\\OSEMN\\scrub\\tabela_tratada_mp.csv")

inicio_idx = None  # índice do início da piscada

for i in range(len(df)):
    if df.loc[i, "piscando"]:
        if inicio_idx is None:
            inicio_idx = i  # marca início da piscada
    else:
        if inicio_idx is not None:
            # fim da piscada no frame anterior
            fim_idx = i - 1
            duracao = df.loc[fim_idx, "timestamp"] - df.loc[inicio_idx, "timestamp"]

            # classifica
            if 0.5 <= duracao < 1:
                estado = "piscou curto"
            elif 1 <= duracao <= 2:
                estado = "piscou longo"
            else:
                estado = "nao piscou"

            # aplica o estado apenas no último frame do piscar
            df.loc[fim_idx, "estado"] = estado

            inicio_idx = None  # reseta para próxima piscada

# Caso o último frame seja piscada
if inicio_idx is not None:
    fim_idx = len(df) - 1
    duracao = df.loc[fim_idx, "timestamp"] - df.loc[inicio_idx, "timestamp"]
    if 0.5 <= duracao < 1:
        estado = "piscou curto"
    elif 1 <= duracao <= 2:
        estado = "piscou longo"
    else:
        estado = "nao piscou"
    df.loc[fim_idx, "estado"] = estado

# Salva em novo CSV
df.to_csv("tabela_com_estado.csv", index=False)

print(df[["piscando", "timestamp", "estado"]].head(50))
