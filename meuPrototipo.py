from hashlib import scrypt
import urllib3
from bs4 import BeautifulSoup

linkPagina = "https://braziljournal.com/chuvas-inesperadas-podem-aliviar-inflacao-juros-podem-ceder-com-novo-tom-do-governo"

http = urllib3.PoolManager()
pagina = http.request('GET',linkPagina)
statusPagina = pagina.status
sopaPagina = BeautifulSoup(pagina.data, "html.parser")

def extraiTexto(sopa):
    for tags in sopa(['script','style']):
        tags.decompose()
    return ' '.join(sopa.stripped_strings) 

textoPagina = extraiTexto(sopaPagina)
linkDentroPagina = sopaPagina.find_all('a')

def separaPalavras(textoPag):
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
print("\n QUANTIDADE DE LINKS: ", len(linkDentroPagina))
print("\n TEXTO DENTRO DA PÁGINA:\n\n", textoPagina)
