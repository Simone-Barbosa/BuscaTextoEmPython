import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin        #para corrigir links que não tem https
import re
import nltk
import pymysql

def inserePalavra(palavra):
    conexao = pymysql.connect(host = 'localhost', user = 'root', passwd= 'C0br@$t@r', db= 'indice', autocommit= True)
    cursor = conexao.cursor()
    cursor.execute('insert into palavras (palavra) values (%s)', palavra)
    idpalavra = cursor.lastrowid
    
    cursor.close()
    conexao.close()

    return idpalavra

#t4 = inserePalavra('teste2')
#print("Teste função inserePalavra = ", t4)

def palavraIndexada(palavra):       # aula 18
    retorno = -1    # caso não exista a palavra no índice
    conexao = pymysql.connect(host = 'localhost', user = 'root', passwd= 'C0br@$t@r', db= 'indice')
    cursor = conexao.cursor()
    cursor.execute('select idpalavra from palavras where palavra = %s', palavra)
    if cursor.rowcount > 0:
        #print("Palavra já cadastrada")
        retorno = cursor.fetchone()[0]      # retorna o id da palavra
    #else:
        #print("Palavra não cadastrada")

    cursor.close()
    conexao.close()
    return retorno

#t3 = palavraIndexada("Linguage")
#print("Teste função palavraIndexada = ", t3)

def inserePagina(url):      #aula 17
    conexao = pymysql.connect(host = 'localhost', user = 'root', passwd= 'C0br@$t@r', db= 'indice', autocommit= True)   # se não colocar autocommit=True ele não guarda/registra nova url
    cursor = conexao.cursor()
    cursor.execute('insert into urls (url) values (%s)', url)
    idpagina = cursor.lastrowid     # Pega o id que acabou de ser inserido na base de dados / Usar lastrowid só quando tem só 1 pessoa usando banco dados, em rede local.
    cursor.close()
    conexao.close()
    return idpagina

#t2 = inserePagina('teste2')
#print('teste função inserePagina = ', t2)

def paginaIndexada(url):                # Adicionado aula 16, Verifica se já existe a url
    retorno = -1                        # caso não exista a página
    conexao = pymysql.connect(host='localhost', user = 'root', passwd= 'C0br@$t@r', db= 'indice')
    cursorUrl = conexao.cursor()        # permite comandos do sql aqui dentro
    cursorUrl.execute('select idurl from urls where url = %s', url)
    
    if cursorUrl.rowcount > 0:
        #print("Url cadastrada")
        idurl = cursorUrl.fetchone()[0]     #buscar udurl | fetchone pega 1 registro | [0] posição q vou pegar (=id)
        cursorPalavra = conexao.cursor()
        cursorPalavra.execute('select idurl from palavra_localizacao where idurl = %s', idurl)

        if cursorPalavra.rowcount > 0:
            #print("Url com palavras")
            retorno = -2                    # caso exista a página com palavras cadastradas
        else:
            print("Url sem palavras")
            retorno = idurl                 # caso exista a página sem palavras, então retorna o ID da página
        cursorPalavra.close()
    #else:
        #print("Url não cadastrada")

    cursorUrl.close()
    conexao.close()
    return retorno
    
#t = paginaIndexada('teste')
#print("t = ", t)

def separaPalavras(texto):              # adicionado aula 15
    stop = nltk.corpus.stopwords.words('portuguese')
    stemmer = nltk.stem.RSLPStemmer()
    splitter = re.compile('\\W+')
    lista_palavras = []
    lista = [p for p in splitter.split(texto) if p != '']
    for p in lista:
        if p.lower() not in stop:
            if len(p) > 1:
                lista_palavras.append(stemmer.stem(p).lower())
    return lista_palavras
    

def getTexto(sopa):
    for tags in sopa(['script','style']):
        tags.decompose()
    return ' '.join(sopa.stripped_strings)    

def crawl(paginas, profundidade):       # adicionado aula 9
    #urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    #desabilitar
    
    for i in range(profundidade):

        novas_paginas = set()       # set() é um conjunto q nao permite elementos repetidos

        for pagina in paginas:      # for adicionado para usar função em uma lista de paginas

            http = urllib3.PoolManager()
            
            #Tratamento de erro, caso o link não abr
            try:                                
                dados_pagina = http.request('GET', pagina)
            except:
                print('Erro ao abrir a página ' + pagina)
                continue

            sopa = BeautifulSoup(dados_pagina.data, "html.parser")      #parser do linux, diferente do professor
            links = sopa.find_all('a')

            contador = 1        # Variável criada para contar qtos links são válidos (q tem href) # deveria ser = 0? aguardando resp. prof.

            for link in links:
                #print(str(link.contents) + " - " + str(link.get('href')))
                #print(link.attrs)       #imprime todos os atributos do link
                #print("\n")

                if('href' in link.attrs):

                    url = urljoin(pagina,str(link.get('href')))     #para corrigir links que não tem https

                    #if url != link.get('href'):                    # if feito só para mostrar a correção dos links
                        #print("Link corrigido = ", url)
                        #print("Link original sem correção = ",link.get('href'))

                    if url.find("'") != -1:     # diferente de -1 sig. que encontrou uma url / ("'") = url vazio
                        continue                # não executa mais nada pra baixo e passa para próxima url

                    #print("Url original = ",url)
                    url = url.split('#')[0]     # vai quebrar url quando achar o # e desprezar o que vem depois #  / [0] = 1 posição
                    #print("Url quebrada no # :", url)
                    #print("\n")

                    if url[0:4] == 'http':      #verificação adicional para add paginas
                        novas_paginas.add(url)
                                
                    contador = contador + 1

            paginas = novas_paginas

            #print("contador de páginas = ",contador)
            #print("O numero de links dentro da página é: ",len(links))
        print("nº paginas = ", len(paginas))
        print("nº novas_paginas = ", len(novas_paginas))

    print("FIM nº paginas = ", len(paginas))
    print("FIM nº novas_paginas = ", len(novas_paginas))

#crawl("https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o")      

listapaginas = ["https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o"]

#crawl(listapaginas,1)      # 2 = profundidade, busca os links dentro de cada link (396) que estava no link origem (1º)
                            # NOTA: prof.falou que profundidade = 2 nos testes dele levou 10h pra processar os dados!

#teste = separaPalavras('Este lugar é apavorante')
#print("teste = ",teste)



