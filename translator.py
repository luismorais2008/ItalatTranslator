from enum import Enum
import requests 
import html2text
from unidecode import unidecode
import html
from statistics import mean
from math import ceil 
import numpy as np 

palavras_irregulares = dict({
        "água" : "acqua",
        "caneta" : "pen", 
        "jantar" : "cena", 
        "jantares" : "ceni",
        "almoço" : "pranzo",
        "almoços": "pranzi",  
        "cena" : "ato", 
        "cenas" : "ato",
        "lugar": "locus",
        "lugares" : "loce",
        "pessoa" : "persona",
        "pessoas" : "persone", 
        "vez" : "phois",
        "vezes" : "phois",
        "ação" : "actio",
        "ações" : "actio",
        "casa" : "domus", 
        "cama" : "bechusi",
        "dia" : "diem", 
        "dias" : "diem",
        "camas" : "beche",
        "o" : {"determinante":"li", "pronome" : "lo"}, 
        "os" : "il", 
        "a" : "la", 
        "as" : "le",
        "um" : "uno", 
        "uns" : "uni", 
        "uma" : "una", 
        "umas" : "une",
        "porque" : "sance", 
        "assim" : "cossa", 
        "mas" : "perus",
        "eu" : "io", 
        "ele" : "lui", 
        "ela" : "lei", 
        "nós" : "noi", 
        "vós" : "voi", 
        "eles" : "loro", 
        "elas" : "loro", 
        "me" : "mi", 
        "te" : "ti", 
        "se" : {"fs" : "la", "ms" : "le", "p" : "gi"},
        "lhe" : "la", 
        "nos" : "ni",
        "vos" : "vi", 
        "meu" : "mio", 
        "minha" : "mia", 
        "meus": "mí",
        "minhas" : "mie", 
        "teu" : "tuo", 
        "tua" : "tua", 
        "teus" : "tui", 
        "tuas" : "tue", 
        "seu" : "sio", 
        "sua" : "sia", 
        "seus" : "sí",
        "suas" : "sie", 
        "nosso" : "nostrio",
        "nossa" : "nostria",
        "nossos" : "nostri",  
        "nossas" : "nostrie", 
        "vosso" : "vio", 
        "vossa" : "via", 
        "vossos" : "ví", 
        "vossas" : "vie", 
        "este" : "quescus", 
        "isto" : "quescus",
        "esta" : "quescusi", 
        "aquele" : "quod", 
        "aquela" : "quod", 
        "aquilo" : "quod", 
        "esse" : "quod", 
        "essa" : "quod", 
        "estes" : "quesci", 
        "estas" : "quesce", 
        "aqui" : "ci", 
        "ali" : "la", 
        "aí" : "la", 
        "agora" : "hora", 
        "não" : "nó", 
        "sim" : "só",
        "só" : "seulemice", 
        "sozinho" : "seul",
        "sozinha" : "seule", 
        "o que" : "iqui", 
        "depois" : "puis",
        "sobre" : "sur", 
        "obrigado" : "prego", 
        "obrigadíssimo" : "tábua", 
        "por" : "per",
        "com" : "cith", 
        "sem" : "sout", 
        "para" : "al",
        "ao" : "al", 
        "à" : "ai", 
        "aos" : "aux", 
        "às" : "aux", 
        "no" : "nel", 
        "na" : "nel", 
        "num" : "nun",
        "numa" : "nun",
        "estar" : "tar", 
        "sendo" : "sí", 
        "sido" : "sí", 
        "achar" : "char", 
        "querer" : "quercusi", 
        "decidir" : "deciquis", 
        "que" : "qui", 
        "como" : "come", 
        "quando" : "cum", 
        "onde" : "ubi", 
        "quem" : "chi", 
        "quanto" : "quanti", 
        "bom" : "buon", 
        "boa": "buonna", 
        "bons" : "boni", 
        "boas" : "bone", 
        "e" : "et"
    })

class Palavra(Enum): 
    ESTRANGEIRISMO=-1,
    NORMAL = 0,
    VERBO = 1,  
    ADVERBIO = 2, 
    LOGIA = 3 

def texto_portuguese_to_italat(text): #dividir o texto em orações
    s = text.split()
    c = []
    translation = ""
    for i in range(len(s)): 
        if "conjun\\xc3\\xa7\\xc3\\xa3o" in priberam_search(s[i]):
            c.append(i)
    try: 
        translation += oracao_portuguese_to_italat(' '.join(s[0:c[0]])) + " "
        for i in range(len(c)-1):
            translation += word_portuguese_to_italat(s[c[i]]) + " " + oracao_portuguese_to_italat(' '.join(s[c[i]+1:c[i+1]])) + " "
        translation += word_portuguese_to_italat(word_data(s[c[len(c)-1]])) + " " + oracao_portuguese_to_italat(' '.join(s[c[len(c)-1]+1:len(s)]))
    except: 
        translation = oracao_portuguese_to_italat(' '.join(s[0:len(s)-1])) 
    return translation


def oracao_portuguese_to_italat(text): #organizar a sintaxe da oração e dividir a oração em palavras
    text = text.replace("-", "")
    palavras = list([])
    for p in text.split(): 
        data = word_data(p)
        translation = word_portuguese_to_italat(data)
        if len(palavras) > 0 and data['classe'] == Palavra.VERBO: 
            if palavras[len(palavras) - 1].lower() == "nó": 
                palavras[len(palavras) - 1] = "non"
            palavras = np.concatenate(([word_portuguese_to_italat(data)], palavras), axis = None)
        elif p.lower() in palavras_irregulares.keys(): 
            if type(palavras_irregulares[p.lower()]) == dict: 
                palavras = np.append(palavras, p.lower())
                continue 
            palavras = np.append(palavras, palavras_irregulares[p.lower()])
        else:
            palavras = np.append(palavras, translation)
    r = ""
    for p in range(len(palavras)):
        if palavras[p] == 'o': 
            try:
              if p == 0 and 'nome' in priberam_search(palavras[p+1]): 
                  r += 'li'
              else: 
                  r += 'lo '
            except: 
                continue 
        elif palavras[p] =='se':
                d = palavras_irregulares["se"]
                d1 = word_data(palavras[p-1])
                d2 = word_data(palavras[p-2])
                opt = list()
                opt.append(d['fs'], d['ms'])
                opt.append(d['p'])
                r += opt[ceil(mean([d1['número'], d2['número']]))][ceil(mean(d1['género'], d2['género']))] + " "
        else: 
            r += palavras[p] + " "

    r = r[0:len(r) - 1] 
    return r 

def word_portuguese_to_italat(palavra): #traduzir a palavra
    traducao = ""
    if palavra["origem"] in palavras_irregulares.keys(): 
        return palavras_irregulares[palavra["origem"]]
    elif palavra["classe"] is Palavra.NORMAL and len(palavra["silabas"])>1:
        for i in palavra["silabas"][0:len(palavra["silabas"])-1]: 
            traducao+=i
        if palavra["género"] == 0 and palavra["número"] == 0: 
            traducao+="cusi"
        elif palavra["género"] == 1 and palavra["número"] == 1: 
            traducao+="ci"
        elif palavra["género"] == 0 and palavra["número"] == 1: 
            traducao+="ce"
        else: 
            traducao+="cus"
    elif palavra["classe"] is Palavra.ADVERBIO: 
        for i in palavra["silabas"][0:len(palavra["silabas"]-2)]: 
            traducao+=i
        traducao += "mice"
    elif palavra["classe"] is Palavra.LOGIA: 
        for i in palavra["silabas"][0:len(palavra["silabas"]-1)]: 
            traducao+=i
        traducao += "um"
    elif palavra["classe"] is Palavra.VERBO: 
         if len(palavra["silabas"])>1:
              s = silabas(palavra["infinitivo"])
              conjugacao = s[len(s) - 1] 
              for i in s[0:len(s)-1]: 
                    traducao += i 
              for c in ['ar', 'er', 'ir', 'or']: 
                    terminacao = "cusi" 
                    if c == 'ir': 
                        terminacao = 'cus'
                    if c in conjugacao:
                        traducao += conjugacao.replace('ir', '') + terminacao         
         else:
              traducao = palavra["infinitivo"]
    else: 
        traducao = palavra["origem"]
    return traducao


def word_data(word): #recolher informação sobre uma palavra
    palavra = dict({"origem":word, "silabas":[], "classe": Palavra.NORMAL, "género": 0, "número": 0})
    priberam = priberam_search(palavra['origem'])
    palavra["silabas"] = silabas(palavra['origem'])
    if "Palavra n\\xc3\\xa3o encontrada" in priberam: 
        palavra["classe"] = Palavra.ESTRANGEIRISMO
    if "verbo" in priberam: 
        palavra["classe"] = Palavra.VERBO
        a = priberam.index("[")+1
        b = priberam.index("]")
        b = ceil((a+b)/2)
        palavra["infinitivo"] = priberam[a:b]
    if "adv\\xc3\\xa9rbio" in priberam: 
        palavra["classe"] = Palavra.ADVERBIO 
    if "logia" in palavra["origem"]:
        palavra["classe"] = Palavra.LOGIA
    if palavra["classe"] == Palavra.NORMAL: 
        if  "dois g\\xc3\\xa9neros" in priberam: 
            palavra["género"] = 0
        elif "masculino" in priberam: 
            palavra["género"] = 1
        if "pl." in priberam:
            palavra["número"] = 1  
    return palavra

def priberam_search(word): #pesquisar a palavra no priberam e recolher toda a informação disponível
    link = "https://dicionario.priberam.org/{word}".format(word = word)
    data = str(requests.get(link).content)
    data = data[data.index("<div id=\"resultados\""):data.index('</article')] 
    priberam = html.escape(str(html2text.html2text(data)).replace("\\n", "").replace("#", "").replace("\\r", ""))
    return priberam

def silabas(word): #fazer a divisão silábica da palavra
    link = "https://www.separaremsilabas.com/index.php?lang=index.php&p={word}&button=Separa%C3%A7%C3%A3o+das+s%C3%ADlabas".format(word = unidecode(word))
    data = str(requests.get(link).content)
    silabas = html2text.html2text(data)
    a = silabas.index("Por favor escreva a palavra **de forma correta**.") + 49
    b = silabas.index("Mais informa\\xc3\\xa7\\xc3\\xb5es")
    silabas = html.escape(silabas[a:b]).replace("\\n", "").replace("#", "").replace("\\r", "")
    silabas = silabas[0:silabas.index("* Quantas")].replace("\n", "").replace(" **", "").replace("** ", "").replace(" ", "").split("-")
    return silabas
  
texto_portuguese_to_italat('Eu sou o Luis e tu és a Carina')
