# controllers/aluno_controller.py
from model.dados_alunos import carregar_alunos

def listar_alunos():
    df = carregar_alunos()
    df['disciplinas_cursadas'] = df['disciplinas_cursadas'].apply(lambda x: [i.strip() for i in x.split(',')])
    df['areas_interesse'] = df['areas_interesse'].apply(lambda x: [i.strip() for i in x.split(',')])
    return df

def obter_aluno_por_id(id_aluno):
    df = carregar_alunos()
    df['disciplinas_cursadas'] = df['disciplinas_cursadas'].apply(lambda x: [i.strip() for i in x.split(',')])
    df['areas_interesse'] = df['areas_interesse'].apply(lambda x: [i.strip() for i in x.split(',')])
    return df[df['id_aluno'] == id_aluno].to_dict(orient='records')
