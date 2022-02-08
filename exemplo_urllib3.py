import urllib3

http = urllib3.PoolManager()
pagina = http.request('GET', 'http://www.iaexpert.com.br')

statusPagina = pagina.status
dadosPagina = pagina.data                   #Retorna todo codigo fonte da página
dadosPaginaLimitado = pagina.data[0:50]     #Retorna os primeiros 50 caracteres do cod fonte da pagina

print("Este é o status da página: ",statusPagina)
#print(dadosPagina)
print("Primeiros 50 caracteres da página: ", dadosPaginaLimitado)

#print("Código integrado com GitHub Desktop no Linux!")
