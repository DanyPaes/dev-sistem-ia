# controllers/recomendacao_conteudo_controller.py
from model.perfil_aluno import gerar_perfis_aluno
from model.perfil_material import gerar_perfis_material
from model.materiais_didaticos import carregar_materiais
from model.dados_alunos import carregar_alunos
from models.recomendador_TFIDF import RecomendadorMaterial

def recomendar_por_conteudo(id_aluno, top_n=5):
    materiais = carregar_materiais()
    if 'perfil_material' not in materiais.columns:
        materiais['perfil_material'] = gerar_perfis_material(materiais)

    alunos = carregar_alunos()
    perfis_alunos = gerar_perfis_aluno(alunos)

    recomendador = RecomendadorMaterial(materiais)
    perfil_aluno = perfis_alunos[id_aluno]
    return recomendador.recomendar(perfil_aluno, top_n)