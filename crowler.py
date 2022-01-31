import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin        #para corrigir links que não tem https

# -----------------------------AULA 7.Crawler - Busca de Documentos II ---------------------------------
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

# -----------------------------AULA 8.Crawler - Busca de Documentos III ---------------------------------

listapaginas = ["https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o"]

crawl(listapaginas,1)      # 2 = profundidade, busca os links dentro de cada link (396) que estava no link origem (1º)

# NOTA: professor falou que profundidade = 2 nos testes dele levou 10h pra processar os dados!



