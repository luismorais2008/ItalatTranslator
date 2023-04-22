from django.shortcuts import render
from django.http import HttpResponse
import json 
import sys
from enum import Enum
import requests 
import html2text
from ftfy import fix_text
from unidecode import unidecode
import html
from statistics import mean
from math import ceil 
import numpy as np 

def translate(request):
    return HttpResponse("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bruno+Ace+SC&display=swap');

body{
    background-color: #000;
    color:white;
    font-family: 'Bruno Ace SC', cursive;
}

article{
    margin-top: 100px;
    margin: 100px;
    margin-bottom: 200px; 
}

div .input{
    float: left; 
    background-color: white;
}

.board{
    border: 0ch;
    color:black;
    width: 450px; 
    height: 200px;
    border-radius: 10px;
}

footer{
    margin-top: 40%; 
    text-align: center;
}

div .output{
    float: right; 
    background-color: white;
}

h1{
    overflow: hidden; 
    border-right: .15em solid white; 
    white-space: nowrap; 
    text-align:center;
    width: 60%;
    margin: 0 auto; 
    animation: 
      typing 3.5s steps(40, end),
      blink-caret .75s step-end infinite;
}

.translation{
    margin-top: 10%;
}
  
  @keyframes typing {
    from { width: 0 }
    to { width: 60% } 
  }
  
  @keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: white; }
  }

.main{
    position: fixed;
    top: 50%;
    left: 50%;
    height: 1px;
    width: 1px;
    background-color: #fff;
    border-radius: 50%;
    box-shadow: -24vw -44vh 2px 2px #fff,38vw -4vh 0px 0px #fff,-20vw -48vh 1px 2px #fff,-39vw 38vh 3px 1px #fff,-42vw -11vh 0px 3px #fff,12vw 15vh 3px 3px #fff,42vw 6vh 3px 2px #fff,-8vw 9vh 0px 2px #fff,34vw -38vh 1px 0px #fff,-17vw 45vh 3px 1px #fff,22vw -36vh 3px 2px #fff,-42vw 1vh 1px 0px #fff;
    animation: zoom 10s alternate infinite;
}

@keyframes zoom {
    0%{
        transform: scale(1);
    }
    100%{
        transform: scale(1.5);
    }
}
    </style>
    <title>Tradutor de Italat</title>
</head>
<body>
    <div class="translation">
    <h1>Tradutor de português para italat</h1>
    <article>
        <div class="input board" style="padding: 40px">
            <textarea onclick="audio()" class="board"></textarea>
        </div>
        <div class="output board" style="padding: 40px ">
            <p style="padding-right: 40px; font-size: auto; text-align: justify;" class="board"></p>
        </div>
    </article>
    </div>
    <div class="main">
    </div>
    <script type="text/javascript">
        function randomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min
}

const STAR_COUNT = 200
let result = ""

for(let i = 0; i < STAR_COUNT; i++){
    result += `${randomNumber(-50, 50)}vw ${randomNumber(-50, 50)}vh ${randomNumber(0, 3)}px ${randomNumber(0, 3)}px #fff,`
}

console.log(result.substring(0, result.length - 1))

function audio(){
    const audio = new Audio('universal.mp3');
    audio.play();
}

async function get_translation(text) {
    const response = await fetch('http://127.0.0.1:8000/?text=' + String(text));
    // waits until the request completes...
    txt = String(await response.text())
    console.log(txt)
    const paragraph = document.getElementsByTagName("p")[0]
    paragraph.innerText = txt
}

document.addEventListener('keyup', (event) => {
    if(String(event.key) === "Enter"){
    const textArea = document.getElementsByTagName("textarea")[0]
    get_translation(textArea.value)
    }
  }, false);

    </script>
    <footer>
        &copy; Luís Morais e Carina Sousa 2023
    </footer>
</body>
</html>""")

def index(request):
    if(request.method == "GET"): 
        try: 
            return HttpResponse(texto_portuguese_to_italat(fix_text(str(request.GET['text']))))
        except Exception:  
            pass 
    return HttpResponse("<h1>Sorry, something went wrong. Try agarin in a few ages.</h1>")

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
        "aprender" : "discete",
        "ensinar" : "docere",
        "aos" : "aux", 
        "às" : "aux", 
        "no" : "nel", 
        "na" : "nel", 
        "num" : "nun",
        "nada" : "rien",
        "pensar" : "cogitare",
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
        "saber" : "sapere",
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

sinal_de_pontuacao = [",", "...", "!", "?", "\"", "'", "(", ")", ";", ".", ":"]

def texto_portuguese_to_italat(text): #dividir o texto em orações
    for sp in sinal_de_pontuacao:
        if sp in text:
            text = text.replace(sp, " " + sp)
    s = text.split()
    c = []
    translation = ""
    for i in range(len(s)): 
        if "conjun\\xc3\\xa7\\xc3\\xa3o" in priberam_search(s[i]) or s[i] in sinal_de_pontuacao:
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
    palavras = []
    verb = False 
    for p in text.split(): 
        data = word_data(p)
        translation = word_portuguese_to_italat(data)
        if len(palavras) > 0 and data['classe'] == Palavra.VERBO and not verb: 
            verb = not verb 
            ar = [word_portuguese_to_italat(data)]
            if palavras[len(palavras) - 1].lower() == "nó":
                palavras = np.delete(palavras, [len(palavras) - 1])
                ar.append( "non")
            elif  palavras[len(palavras)-2].lower() == "nó": 
                palavras = np.delete(palavras, [len(palavras) - 2])
                ar.append("non")
                ar.append(palavras(len(palavras)-1))
            palavras = np.concatenate((ar, palavras), axis = None)
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
    try: 
        if palavra["infinitivo"] in palavras_irregulares.keys():
            return palavras_irregulares[palavra["infinitivo"]]
    except KeyError: 
        pass 
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
        l = palavra["silabas"][len(palavra["silabas"])-3]
        if "z" == l[len(l)-1]: 
            palavra["silabas"][len(palavra["silabas"])-3] = l.replace("z", "")
        for i in palavra["silabas"][0:len(palavra["silabas"])-2]: 
            traducao+=i
        traducao += "mice"
    elif palavra["classe"] is Palavra.LOGIA: 
        for i in palavra["silabas"][0:len(palavra["silabas"]-1)]: 
            traducao+=i
        traducao += "um"
    elif palavra["classe"] is Palavra.VERBO: 
         if len(palavra["silabas"])>1:
              s = silabas(palavra["infinitivo"])
              for i in s[0:len(s)-1]: 
                    traducao += i 
              for c in ['ar', 'er', 'ir', 'or']: 
                    terminacao = "cus" 
                    if c != 'ir': 
                        terminacao =  "re"
                    if c in s[len(s)-1]:
                        traducao += terminacao         
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
        print(priberam)
        palavra["infinitivo"] = priberam[a:b]
    if "adv\\xc3\\xa9rbio" in priberam and "mente" in palavra["origem"]: 
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
    try: 
        link = "https://dicionario.priberam.org/{word}".format(word = word)
        data = str(requests.get(link).content)
        data = data[data.index("<div id=\"resultados\""):data.index('</article')] 
        priberam = html.escape(str(html2text.html2text(data)).replace("\\n", "").replace("#", "").replace("\\r", ""))
    except ValueError: 
        return "not found"
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
  
