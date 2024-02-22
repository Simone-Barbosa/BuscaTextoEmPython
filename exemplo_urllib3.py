import urllib3

http = urllib3.PoolManager()
pagina = http.request('GET', 'http://www.iaexpert.com.br')

statusPagina = pagina.status
dadosPagina = pagina.data
dadosPaginaLimitado = pagina.data[0:50]

print("Este é o status da página: ",statusPagina)

print("Primeiros 50 caracteres da página: ", dadosPaginaLimitado)