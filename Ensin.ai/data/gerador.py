import csv
import random
from datetime import datetime, timedelta

#os dados fornecidos estão duplicados e invalidos, isso serve pra gerar um df de interações valido
#seguindo os dados captados do arquivo original:
# IDs alunos: min = 1 , max = 100000
# IDs materiais: min = 1 , max = 50000
# Tipos de interação: {'visualizacao', 'leitura'}
# Avaliação: min = 1 , max = 5
# Duração (minutos): min = 5 , max = 240
# Datas: de 2023-01-01 até 2023-12-31

# Parâmetros fixos
ids_alunos = list(range(1, 9))          # alunos de 1 a 8
ids_materiais = list(range(1, 11))      # materiais de 1 a 10
tipos_interacao = ['visualizacao', 'leitura']
avaliacoes = [1, 2, 3, 4, 5]
min_duracao = 5
max_duracao = 240
inicio_data = datetime(2023, 1, 1)
fim_data = datetime(2023, 12, 31)

# Quantidade de interações falsas
qtd_interacoes = 100

with open('interacoes_geradas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_interacao', 'id_aluno', 'id_material', 'tipo_interacao', 'avaliacao', 'duracao_minutos', 'data'])

    for i in range(1, qtd_interacoes + 1):
        id_aluno = random.choice(ids_alunos)
        id_material = random.choice(ids_materiais)
        tipo = random.choice(tipos_interacao)
        avaliacao = random.choice(avaliacoes)
        duracao = random.randint(min_duracao, max_duracao)
        dias_random = random.randint(0, (fim_data - inicio_data).days)
        data = (inicio_data + timedelta(days=dias_random)).strftime('%Y-%m-%d')

        writer.writerow([i, id_aluno, id_material, tipo, avaliacao, duracao, data])
