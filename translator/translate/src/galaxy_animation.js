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
    const response = await fetch('http://149.90.143.191/translate?text=' + String(text));
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
