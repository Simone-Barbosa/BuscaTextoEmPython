# criar um consulta simples de uma palavra (ex; Economia), dentro de um site
from hashlib import scrypt
import urllib3
from bs4 import BeautifulSoup

linkPagina = "https://braziljournal.com/chuvas-inesperadas-podem-aliviar-inflacao-juros-podem-ceder-com-novo-tom-do-governo"

http = urllib3.PoolManager()
pagina = http.request('GET',linkPagina)
statusPagina = pagina.status
sopaPagina = BeautifulSoup(pagina.data, "html.parser")

# PRIMEIRO TRATAMENTO DE TEXTO: Remoção das tags SCRIPT E STYLE
def extraiTexto(sopa):
    for tags in sopa(['script','style']):
        tags.decompose()                    # decompose remove o tag e conteudo da tag
    return ' '.join(sopa.stripped_strings) 

textoPagina = extraiTexto(sopaPagina)
linkDentroPagina = sopaPagina.find_all('a')

# revisar essa função
def separaPalavras(textoPag):              # adicionado aula 15
    stop = nltk.corpus.stopwords.words('portuguese')
    stemmer = nltk.stem.RSLPStemmer()
    splitter = re.compile('\\W+')

    lista_palavras = []
    lista = [p for p in splitter.split(textoPag) if p != '']

    for p in lista:

        if p.lower() not in stop:
            if len(p) > 1:
                lista_palavras.append(stemmer.stem(p).lower())

    return lista_palavras




print("\n Status da página: ", statusPagina)
#print("\n SOPA: \n\n", sopaPagina)         # imprime todo cod fonte original da pagina
#print("\n LINKS DENTRO DA PAGINA: \n\n", linkDentroPagina)
print("\n QUANTIDADE DE LINKS: ", len(linkDentroPagina))
print("\n TEXTO DENTRO DA PÁGINA:\n\n", textoPagina)






#todosDadosPagina = pagina.data
#print("Todo conteúdo da página é = \n", todosDadosPagina)


'''
for tags in sopaPagina(['script','style']):
    tags.decompose()                           
conteudoPaginaTeste = '********'.join(sopaPagina.stripped_strings)
#print("\n SOPA SEM SCRIPT E STYLE: \n\n", conteudoPaginaTeste)

# SEGUNDO TRATAMENTO TEXTO: Após o for, ALGUMAS palavras ficaram grudadas, .join coloca um espaço entre elas
conteudoPagina = ' '.join(sopaPagina.stripped_strings)
#print("\n O conteúdo escrito da pagina é:\n\n ", conteudoPagina)
'''
