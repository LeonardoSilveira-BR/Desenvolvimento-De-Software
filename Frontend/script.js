const volume = document.getElementById("volume");
const valor = document.getElementById("valorVolume");

volume.oninput = () => {
    valor.innerHTML = volume.value + "%";
};

document.getElementById("help").onclick = () => {
    alert("Digite um texto ou anexe um arquivo.\nEscolha Instrumento, BPM, Oitava e Volume.\nClique em GERAR MÚSICA.");
};

document.getElementById("gerar").onclick = () => {
    alert("Música gerada (simulação).");
};

document.getElementById("play").onclick = () => {
    console.log("Play");
};

document.getElementById("pause").onclick = () => {
    console.log("Pause");
};

document.getElementById("resume").onclick = () => {
    console.log("Retomar");
};

document.getElementById("stop").onclick = () => {
    console.log("Stop");
};

document.getElementById("salvar").onclick = () => {
    alert("Arquivo salvo (simulação).");
};

document.getElementById("reiniciar").onclick = () => {
    location.reload();
};

document.getElementById("sair").onclick = () => {
    alert("Fechando o programa...");
    window.close();
};