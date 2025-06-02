# controllers/material_controller.py
from model.materiais_didaticos import carregar_materiais

def listar_materiais():
    return carregar_materiais()

def obter_material_por_id(id_material):
    materiais = carregar_materiais()
    return materiais[materiais['id_material'] == id_material].to_dict(orient='records')