# schemas/aluno.py

from pydantic import BaseModel
from typing import List

class AlunoSchema(BaseModel):
    id_aluno: int
    nome: str
    curso: str
    periodo: int
    disciplinas_cursadas: List[str]
    areas_interesse: List[str]

    def gerar_perfil(self) -> str:
        """Texto objetivo para usar com TF-IDF"""
        partes = [self.curso] + self.disciplinas_cursadas + self.areas_interesse
        return ' '.join(partes).lower()
