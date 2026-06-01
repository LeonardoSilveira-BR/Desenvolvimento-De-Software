from http import HTTPStatus
from flask import Flask, request, send_file
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)=


# =========================
# TEXTO
# =========================

@app.route('/text', methods=['GET'])
def GetText():
    """
    Get current text
    ---
    responses:
      200:
        description: Current text
    """
    pass


@app.route('/text', methods=['PUT'])
def UpdateText():
    """
    Update text
    ---
    parameters:
      - in: body
        name: body
        required: true
    responses:
      204:
        description: Success
      400:
        description: Invalid data
    """
    pass


@app.route('/text/load', methods=['POST'])
def LoadTextFile():
    """
    Load TXT file
    ---
    consumes:
      - multipart/form-data
    responses:
      200:
        description: File loaded
      400:
        description: Invalid file
    """
    pass


@app.route('/text/save', methods=['POST'])
def SaveTextFile():
    """
    Save TXT file
    ---
    responses:
      204:
        description: Success
    """
    pass


# =========================
# CONFIGURAÇÕES
# =========================

@app.route('/settings', methods=['GET'])
def GetSettings():
    """
    Get current settings
    ---
    responses:
      200:
        description: Settings
    """
    pass


@app.route('/settings', methods=['PUT'])
def UpdateSettings():
    """
    Update settings
    ---
    responses:
      204:
        description: Success
      400:
        description: Invalid data
    """
    pass


# =========================
# INSTRUMENTOS GM
# =========================

@app.route('/instruments', methods=['GET'])
def GetInstruments():
    """
    Get General MIDI instruments
    ---
    responses:
      200:
        description: Instrument list
    """
    pass


@app.route('/instruments/<int:instrument_id>', methods=['GET'])
def GetInstrument(instrument_id: int):
    """
    Get instrument
    ---
    parameters:
      - name: instrument_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Instrument
      404:
        description: Not found
    """
    pass


# =========================
# VOZES (FASE 2)
# =========================

@app.route('/voices', methods=['GET'])
def GetVoices():
    """
    Get all voices
    ---
    responses:
      200:
        description: Voice list
    """
    pass


@app.route('/voices/<int:voice_id>', methods=['GET'])
def GetVoice(voice_id: int):
    """
    Get voice
    ---
    parameters:
      - name: voice_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Voice
      404:
        description: Not found
    """
    pass


# =========================
# INTERPRETADOR
# =========================

@app.route('/interpreter/parse', methods=['POST'])
def ParseText():
    """
    Parse text into music events
    ---
    responses:
      200:
        description: Parsed events
      400:
        description: Invalid text
    """
    pass


@app.route('/interpreter/events', methods=['GET'])
def GetEvents():
    """
    Get generated events
    ---
    responses:
      200:
        description: Event list
    """
    pass


# =========================
# FUGA
# =========================

@app.route('/fugue/process', methods=['POST'])
def ProcessFugue():
    """
    Process voices as fugue
    ---
    responses:
      200:
        description: Fugue generated
      400:
        description: Invalid text
    """
    pass


@app.route('/fugue/preview', methods=['GET'])
def PreviewFugue():
    """
    Preview generated fugue
    ---
    responses:
      200:
        description: Fugue preview
    """
    pass


# =========================
# PARTITURA
# =========================

@app.route('/music/score', methods=['GET'])
def GetScore():
    """
    Get score
    ---
    responses:
      200:
        description: Score
    """
    pass


@app.route('/music/generate', methods=['POST'])
def GenerateMusic():
    """
    Generate music
    ---
    responses:
      200:
        description: Music generated
      400:
        description: Invalid text
    """
    pass


@app.route('/music/score', methods=['DELETE'])
def ClearScore():
    """
    Clear score
    ---
    responses:
      204:
        description: Success
    """
    pass


# =========================
# PLAYER
# =========================

@app.route('/player/play', methods=['POST'])
def Play():
    """
    Start playback
    ---
    responses:
      204:
        description: Success
    """
    pass


@app.route('/player/pause', methods=['POST'])
def Pause():
    """
    Pause playback
    ---
    responses:
      204:
        description: Success
    """
    pass


@app.route('/player/resume', methods=['POST'])
def Resume():
    """
    Resume playback
    ---
    responses:
      204:
        description: Success
    """
    pass


@app.route('/player/stop', methods=['POST'])
def Stop():
    """
    Stop playback
    ---
    responses:
      204:
        description: Success
    """
    pass


@app.route('/player/restart', methods=['POST'])
def Restart():
    """
    Restart playback
    ---
    responses:
      204:
        description: Success
    """
    pass


@app.route('/player/end', methods=['POST'])
def End():
    """
    End playback
    ---
    responses:
      204:
        description: Success
    """
    pass


@app.route('/player/status', methods=['GET'])
def GetPlayerStatus():
    """
    Get player status
    ---
    responses:
      200:
        description: Player state
    """
    pass


# =========================
# MIDI
# =========================

@app.route('/midi/generate', methods=['POST'])
def GenerateMidi():
    """
    Generate MIDI file
    ---
    responses:
      200:
        description: MIDI generated
      400:
        description: Invalid data
    """
    pass


@app.route('/midi/download', methods=['GET'])
def DownloadMidi():
    """
    Download MIDI file
    ---
    responses:
      200:
        description: MIDI file
      404:
        description: Not found
    """
    pass


@app.route('/midi/save', methods=['POST'])
def SaveMidi():
    """
    Save MIDI file
    ---
    responses:
      204:
        description: Success
    """
    pass


if __name__ == '__main__':
    app.run(debug=True)