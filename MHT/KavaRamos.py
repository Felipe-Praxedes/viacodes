repetições = 10
qtd = 500
multiplicador = 1.05
parametro = 10

for i in range(1, repetições):
   nova_qtd = qtd * multiplicador
   nova_qtd = int(nova_qtd)
   print(nova_qtd)
   qtd = qtd * multiplicador