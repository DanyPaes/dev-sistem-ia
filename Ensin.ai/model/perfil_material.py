import pandas as pd
from schema.material import MaterialSchema

def gerar_perfis_material(df: pd.DataFrame) -> list[str]:
    perfis = []

    for _, row in df.iterrows():
        try:
            material = MaterialSchema(**row.to_dict())
            perfis.append(material.gerar_perfil())
        except Exception as e:
            print(f"Erro ao gerar perfil do material: {e}")
            continue

    return perfis
