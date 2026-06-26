const API = "http://127.0.0.1:5000";

const volume = document.getElementById("volume");
const valor = document.getElementById("valorVolume");
const textarea = document.querySelector("textarea");

volume.oninput = () => {
    valor.textContent = volume.value + "%";
};

// ===============================
// AJUDA
// ===============================

document.getElementById("help").onclick = () => {
    alert(
`1 - Digite um texto ou anexe um arquivo TXT.
2 - Escolha BPM e Volume.
3 - Clique em GERAR MÚSICA.
4 - Utilize os controles para reproduzir.`
    );
};

// ===============================
// GERAR MÚSICA
// ===============================

document.getElementById("gerar").onclick = async () => {

    try {

        // Atualiza o texto
        await fetch(API + "/Text", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: textarea.value
            })
        });

        // Atualiza as configurações
        await fetch(API + "/Settings", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                bpm: Number(document.getElementById("bpm").value),
                volumeGeral: Number(volume.value)
            })
        });

        // Interpreta o texto
        await fetch(API + "/MusicInterpreter/Parse", {
            method: "POST"
        });

        // Gera o MIDI
        const resposta = await fetch(API + "/MusicGenerator/Generate", {
            method: "POST"
        });

        const dados = await resposta.json();

        if (resposta.ok) {

            alert("Música gerada com sucesso!");

        } else {

            alert(dados.erro);

        }

    } catch (erro) {

        console.error(erro);
        alert("Não foi possível conectar na API.");

    }

};

// ===============================
// CARREGAR ARQUIVO
// ===============================

document.getElementById("arquivo").addEventListener("change", async (e) => {

    const arquivo = e.target.files[0];

    if (!arquivo) return;

    const form = new FormData();

    form.append("file", arquivo);

    const resposta = await fetch(API + "/Text/Load", {
        method: "POST",
        body: form
    });

    const dados = await resposta.json();

    textarea.value = dados.text;

});

// ===============================
// PLAY
// ===============================

document.getElementById("play").onclick = async () => {

    await fetch(API + "/MusicPlayer/Play", {

        method: "POST"

    });

};

// ===============================
// PAUSE
// ===============================

document.getElementById("pause").onclick = async () => {

    await fetch(API + "/MusicPlayer/Pause", {

        method: "POST"

    });

};

// ===============================
// RETOMAR
// ===============================

document.getElementById("resume").onclick = async () => {

    await fetch(API + "/MusicPlayer/Resume", {

        method: "POST"

    });

};

// ===============================
// STOP
// ===============================

document.getElementById("stop").onclick = async () => {

    await fetch(API + "/MusicPlayer/Stop", {

        method: "POST"

    });

};

// ===============================
// SALVAR MIDI
// ===============================

document.getElementById("salvar").onclick = async () => {

    const resposta = await fetch(API + "/SaveAudio", {

        method: "POST"

    });

    const dados = await resposta.json();

    alert(dados.mensagem);

};

// ===============================
// REINICIAR PLAYER
// ===============================

document.getElementById("reiniciar").onclick = async () => {

    await fetch(API + "/MusicPlayer/Restart", {

        method: "POST"

    });

};

// ===============================
// SAIR
// ===============================

document.getElementById("sair").onclick = async () => {

    await fetch(API + "/MusicPlayer/End", {

        method: "POST"

    });

    alert("Player encerrado.");

};

// ===============================
// CARREGA CONFIGURAÇÕES
// ===============================

async function carregarConfiguracoes() {

    try {

        const resposta = await fetch(API + "/Settings");

        const dados = await resposta.json();

        document.getElementById("bpm").value = dados.bpm;

        valor.innerHTML = volume.value + "%";

    } catch (e) {

        console.log(e);

    }

}

// ===============================
// CARREGA TEXTO
// ===============================

async function carregarTexto() {

    try {

        const resposta = await fetch(API + "/Text");

        const dados = await resposta.json();

        textarea.value = dados.text;

    } catch (e) {

        console.log(e);

    }

}

carregarTexto();
carregarConfiguracoes();