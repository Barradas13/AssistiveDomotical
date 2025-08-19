def calcula_novo_ponto(ponto_base, ponto_antigo):
    ponto_novo = (ponto_antigo[0] - ponto_base[0], ponto_antigo[1] - ponto_base[1])
    
    return ponto_novo

import pandas as pd
import numpy as np
import ast
import os



for tabela in os.listdir("/home/barradas/Downloads/AssistiveDomotical/OSEMN/obtain/tabelasBrutas"):
    resultados = []
    
    df = pd.read_csv(f"/home/barradas/Downloads/AssistiveDomotical/OSEMN/obtain/tabelasBrutas/{tabela}")

    linhas_nulas = df[df["pontos_olho"].isna()]

    df.loc[df["pontos_olho"].isna(), "ear"] = np.nan

    l_s = 35
    l_i = 0

    df.loc[df["ear"] > l_s, "ear"] = l_s
    df.loc[df["ear"] < l_i, "ear"] = l_i


    for i in range(0, len(df) - 4, 5):
        janela = df.iloc[i:i+5]
        ears = janela["ear"].values
        piscando_vals = janela["piscando"].values
        
        for j in ears:
            if pd.isna(j):
                continue

        novo = {
            "ear1": ears[0],
            "ear2": ears[1],
            "ear3": ears[2],
            "ear4": ears[3],
            "ear5": ears[4],
        }

        novo["id"] = tabela
        
        if list(piscando_vals).count("vermelho") >= 4:
            novo["piscando"] = False
        elif list(piscando_vals).count("verde") >= 4:
            novo["piscando"] = True
        else:
            continue
        
        j = 1

        for frame in janela["pontos_olho"].values:
            pontos_olhos = []
        
            frame = ast.literal_eval(frame)

            for ponto in frame:

                pb = frame[15]

                pontos_olhos.append(calcula_novo_ponto(pb, ponto))
            novo[f"pontos_olhos {j}"] = pontos_olhos
            j += 1

        resultados.append(novo)


    df_final = pd.DataFrame(resultados)
    df_final.to_csv(f"/home/barradas/Downloads/AssistiveDomotical/OSEMN/scrub/tabelas_pessoa_pos_tratamento/{tabela}")

    print()
    print(tabela)
    print(df_final[df_final["piscando"] == True].shape)
    print(df_final[df_final["piscando"] == False].shape)
    print()
