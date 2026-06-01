from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flasgger import Swagger

from Text import TextReader, TextLoadFile
from Settings import Settings
from MusicInterpreter import MusicInterpreter
from MusicGenerator import MusicGenerator
from MusicPlayer import MusicPlayer
from SaveAudio import SaveAudio

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# ==================================================
# OBJETOS GLOBAIS
# ==================================================

texto_reader = TextReader()
settings = Settings()
player = MusicPlayer()
generator = MusicGenerator()

eventos_gerados = []


# ==================================================
# TEXT
# ==================================================

@app.route('/Text', methods=['GET'])
def GetText():
    """
    Retorna o texto atualmente carregado.
    """
    return jsonify({
        "text": texto_reader.getText()
    }), 200


@app.route('/Text', methods=['PUT'])
def UpdateText():
    """
    Atualiza o texto armazenado.
    """

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "erro": "Campo 'text' não informado."
        }), 400

    texto_reader.readText(data["text"])

    return jsonify({
        "mensagem": "Texto atualizado com sucesso."
    }), 200


@app.route('/Text', methods=['DELETE'])
def ClearText():
    """
    Limpa o texto armazenado.
    """

    texto_reader.readText("")

    return jsonify({
        "mensagem": "Texto removido."
    }), 200


@app.route('/Text/Load', methods=['POST'])
def LoadText():
    """
    Carrega um arquivo TXT.
    """

    arquivo = request.files.get("file")

    if not arquivo:
        return jsonify({
            "erro": "Arquivo não enviado."
        }), 400

    caminho = "temp.txt"
    arquivo.save(caminho)

    try:
        loader = TextLoadFile(caminho)
        texto = loader.loadFile()

        texto_reader.readText(texto)

        return jsonify({
            "text": texto
        }), 200

    except Exception as e:
        return jsonify({
            "erro": str(e)
        }), 400


# ==================================================
# SETTINGS
# ==================================================

@app.route('/Settings', methods=['GET'])
def GetSettings():
    """
    Retorna as configurações atuais.
    """

    return jsonify({
        "bpm": settings.bpmAtual,
        "voices": [
            {
                "numero": voz.numero,
                "oitava": voz.oitava,
                "volume": voz.volume,
                "instrumento": voz.instrumento,
                "atraso": voz.atraso
            }
            for voz in settings.vozes
        ]
    }), 200


@app.route('/Settings', methods=['PUT'])
def UpdateSettings():
    """
    Atualiza BPM e volume geral.
    """

    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "Dados inválidos."
        }), 400

    if "bpm" in data:
        settings.setBPM(data["bpm"])

    if "volumeGeral" in data:
        settings.setVolumeGeral(data["volumeGeral"])

    return jsonify({
        "mensagem": "Configurações atualizadas."
    }), 200


# ==================================================
# VOICE
# ==================================================

@app.route('/Voice', methods=['GET'])
def GetVoices():
    """
    Retorna todas as vozes.
    """

    return jsonify([
        {
            "numero": voz.numero,
            "oitava": voz.oitava,
            "volume": voz.volume,
            "instrumento": voz.instrumento,
            "atraso": voz.atraso
        }
        for voz in settings.vozes
    ]), 200


@app.route('/Voice/<int:voice_id>', methods=['GET'])
def GetVoice(voice_id):
    """
    Retorna uma voz específica.
    """

    if voice_id < 0 or voice_id >= len(settings.vozes):
        return jsonify({
            "erro": "Voz não encontrada."
        }), 404

    voz = settings.vozes[voice_id]

    return jsonify({
        "numero": voz.numero,
        "oitava": voz.oitava,
        "volume": voz.volume,
        "instrumento": voz.instrumento,
        "atraso": voz.atraso
    }), 200


@app.route('/Voice/<int:voice_id>', methods=['PUT'])
def UpdateVoice(voice_id):
    """
    Atualiza uma voz específica.
    """

    if voice_id < 0 or voice_id >= len(settings.vozes):
        return jsonify({
            "erro": "Voz não encontrada."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "erro": "Dados inválidos."
        }), 400

    voz = settings.vozes[voice_id]

    if "volume" in data:
        voz.setVolume(data["volume"])

    if "oitava" in data:
        voz.setOitava(data["oitava"])

    if "instrumento" in data:
        voz.setInstrumento(data["instrumento"])

    if "atraso" in data:
        voz.setAtraso(data["atraso"])

    return jsonify({
        "mensagem": f"Voz {voice_id} atualizada."
    }), 200


# ==================================================
# MUSIC INTERPRETER
# ==================================================

@app.route('/MusicInterpreter/Parse', methods=['POST'])
def ParseText():
    """
    Converte texto em eventos musicais.
    """

    global eventos_gerados

    texto = texto_reader.getText()

    if not texto:
        return jsonify({
            "erro": "Texto vazio."
        }), 400

    interpretador = MusicInterpreter(settings)

    eventos_gerados = interpretador.converteCaractere(texto)

    return jsonify({
        "eventosGerados": len(eventos_gerados)
    }), 200


@app.route('/MusicInterpreter/Events', methods=['GET'])
def GetEvents():
    """
    Retorna os eventos gerados.
    """

    return jsonify([
        {
            "nota": evento.nota,
            "instrumento": evento.instrumento,
            "oitava": evento.oitava,
            "volume": evento.volume,
            "tempo_de_atraso": evento.tempo_de_atraso,
            "bpm": evento.bpm,
            "faixa": evento.faixa,
            "indice": evento.indice
        }
        for evento in eventos_gerados
    ]), 200


# ==================================================
# MUSIC GENERATOR
# ==================================================

@app.route('/MusicGenerator/Generate', methods=['POST'])
def GenerateMusic():
    """
    Gera o arquivo MIDI.
    """

    texto = texto_reader.getText()

    if not texto:
        return jsonify({
            "erro": "Texto vazio."
        }), 400

    try:
        generator.produz_MIDI(
            texto=texto,
            user_settings=settings
        )

        return jsonify({
            "mensagem": "MIDI gerado com sucesso.",
            "arquivo": "faixa_gerada.mid"
        }), 200

    except Exception as e:
        return jsonify({
            "erro": str(e)
        }), 500


@app.route('/MusicGenerator/Download', methods=['GET'])
def DownloadMidi():
    """
    Download do arquivo MIDI.
    """

    return send_file(
        "faixa_gerada.mid",
        as_attachment=True
    )


# ==================================================
# SAVE AUDIO
# ==================================================

@app.route('/SaveAudio', methods=['POST'])
def SaveGeneratedAudio():
    """
    Salva o arquivo MIDI gerado.
    """

    try:
        salvador = SaveAudio()
        salvador.salvar_com_local()

        return jsonify({
            "mensagem": "Arquivo salvo com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "erro": str(e)
        }), 500


# ==================================================
# MUSIC PLAYER
# ==================================================

@app.route('/MusicPlayer/Play', methods=['POST'])
def Play():
    """
    Inicia a reprodução.
    """

    player.play()

    return jsonify({
        "mensagem": "Reprodução iniciada."
    }), 200


@app.route('/MusicPlayer/Pause', methods=['POST'])
def Pause():
    """
    Pausa a reprodução.
    """

    player.pause()

    return jsonify({
        "mensagem": "Reprodução pausada."
    }), 200


@app.route('/MusicPlayer/Resume', methods=['POST'])
def Resume():
    """
    Retoma a reprodução.
    """

    player.play()

    return jsonify({
        "mensagem": "Reprodução retomada."
    }), 200


@app.route('/MusicPlayer/Stop', methods=['POST'])
def Stop():
    """
    Para a reprodução.
    """

    player.stop()

    return jsonify({
        "mensagem": "Reprodução parada."
    }), 200


@app.route('/MusicPlayer/Restart', methods=['POST'])
def Restart():
    """
    Reinicia a reprodução.
    """

    player.restart()

    return jsonify({
        "mensagem": "Reprodução reiniciada."
    }), 200


@app.route('/MusicPlayer/End', methods=['POST'])
def End():
    """
    Encerra o player.
    """

    player.encerrar()

    return jsonify({
        "mensagem": "Player encerrado."
    }), 200


@app.route('/MusicPlayer/Status', methods=['GET'])
def GetPlayerStatus():
    """
    Retorna o estado atual do player.
    """

    return jsonify({
        "tocando": player.esta_tocando()
    }), 200


# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )