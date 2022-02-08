import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
pagina = http.request('GET', 'https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o')

sopa = BeautifulSoup(pagina.data, "html.parser")        #parser (do prof é só 'lxml')

for tags in sopa(['script','style']):       # tags a remover: script e style
    tags.decompose()                        # decompose remove o tag e conteudo da tag

conteudo = ' '.join(sopa.stripped_strings)      # esse comando junta o espaço ' ' com cada palavra do texto, do contrario tudo ficaria grudado

print()
print("O CONTEÚDO DA PÁGINA É: ", conteudo)

