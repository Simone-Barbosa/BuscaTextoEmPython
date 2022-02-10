import re               # regular expressions
import nltk             # natural language tolkit
#nltk.download()        # pos download, linha pode ser desativada do código.

stop2 = nltk.corpus.stopwords.words('portuguese')   # esse banco palavras é com todas palavras minusculas
stop2.append('é')

splitter = re.compile('\\W+') # W busca caracteres que não são palavras
lista_palavras = []
lista = [p for p in splitter.split("Este lugar é apavorante a b c++ d") if p != ""]   #p de palavra | splitter.split vai quebrar quando achar no texto a condição \\W+, se p for diferente de vazio "" | \\W+ não pega ++
for p in lista:
    if p.lower() not in stop2:                   #Prof recomenda escolher padrão, minusculo (.lower) ou maiusculo
        if len(p) > 1:                          #para não armazenar letras isoladas
            lista_palavras.append(p.lower())      #inclui cada palavra escrita em minuscula na lista_palavras

print("Lista_palavras = ", lista_palavras)
#print(len(stop2))



