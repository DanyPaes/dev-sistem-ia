import pandas as pd
from schema.aluno import AlunoSchema

def gerar_perfis_aluno(df: pd.DataFrame) -> list[str]:
    perfis = []

    for _, row in df.iterrows():
        try:
            data = row.to_dict()

            # Converter strings para listas
            if isinstance(data.get("disciplinas_cursadas"), str):
                data["disciplinas_cursadas"] = [s.strip() for s in data["disciplinas_cursadas"].split(",")]

            if isinstance(data.get("areas_interesse"), str):
                data["areas_interesse"] = [s.strip() for s in data["areas_interesse"].split(",")]

            # Criar aluno e gerar perfil direto
            aluno = AlunoSchema(**data)
            perfis.append(aluno.gerar_perfil())

        except Exception as e:
            print(f"Erro ao gerar perfil do aluno: {e}")
            continue

    return perfis
