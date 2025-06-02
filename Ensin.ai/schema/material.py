from pydantic import BaseModel
from typing import Literal

class MaterialSchema(BaseModel):
    id_material: int
    titulo: str
    tipo: Literal["livro", "vídeo", "artigo"]
    area: str
    nivel: Literal["Iniciante", "Intermediário", "Avançado"]
    descricao: str
    autor: str

    def gerar_perfil(self) -> str:
        """Texto objetivo para uso com TF-IDF"""
        partes = [self.titulo, self.descricao, self.area, self.nivel]
        return ' '.join(partes).lower()
