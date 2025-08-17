import pandas as pd

df = pd.read_csv("AssistiveDomotical\\OSEMN\\scrub\\tabela_tratada_mp.csv")

df['frame_global'] = range(1, len(df) + 1)

df.to_csv("AssistiveDomotical\\OSEMN\\scrub\\tabela_tratada_mp.csv", index=False)
