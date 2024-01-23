import pandas as pd

Grau_Instr_Bibl = {'Categoria': ['Analfabeto', 'Até 5ª Incompleto', '5ª Completo Fundamental', '6ª a 9ª Fundamental', 'Fundamental Completo', 'Médio Incompleto', 'Médio Completo', 'Superior Incompleto', 'Superior Completo', 'MESTRADO', 'DOUTORADO', 'IGNORADO'],
                   'Valores na fonte': ['1','2','3','4','5','6','7','8','9','10','11','-1']
                  }

dataset_original = pd.DataFrame({'Grau de instrucao': ['1','2','3','4','5','6','7','8','9','10','11','-1']})
Grau_Instr_Bibli = pd.DataFrame(data=Grau_Instr_Bibl)

s = Grau_Instr_Bibli.set_index('Valores na fonte')['Categoria']

dataset_original['GrauNovo'] = dataset_original['Grau de instrucao'].map(s)

print(dataset_original)