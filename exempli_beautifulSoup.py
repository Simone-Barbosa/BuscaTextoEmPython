from bs4 import BeautifulSoup
import urllib3

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    #link da aula deu warning, esse é comando para desabilitar

http = urllib3.PoolManager()
pagina = http.request('GET', 'https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o')

statusPagina = pagina.status
print(statusPagina)

sopa = BeautifulSoup(pagina.data, "html.parser")    #parser é uma analisador de sintaxe, serve pra organizar o texto

#print(sopa)                #imprime todo cod da pagina com a organizaçõa parser
#print(sopa.title)          #imprime o título com as tags html
print(sopa.title.string)    #tira as tags, deixa só texto limpo

links = sopa.find_all('a')      # O 'a' é identificação de direcionamento de links na pagina

print("O numero de links dentro da página é: ",len(links))

# for cadaLink in links:
#     print(cadaLink.get('href'))       #imprime o link
#     print(cadaLink.contents)          #imprime o titulo do link



