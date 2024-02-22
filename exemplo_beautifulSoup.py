from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()
pagina = http.request('GET', 'https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o')

statusPagina = pagina.status
print(statusPagina)

sopa = BeautifulSoup(pagina.data, "html.parser")

#print(sopa)               
#print(sopa.title)         
print(sopa.title.string)
links = sopa.find_all('a')

print("O numero de links dentro da página é: ",len(links))



