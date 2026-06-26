from Settings import Settings

# ==========================
# Instrumentos
# ==========================

PIANO = 0
CRAVO = 6
TUBULAR_BELLS = 15
ORGAO = 20
HARMONICA = 22
BANDONEON = 24
FAGOTE = 70
GAITA_DE_FOLES = 110
ONDAS_MAR = 123
AGOGO = 114

# ==========================
# Notas
# ==========================

LA = 45
SI = 47
DO = 36
RE = 38
MI = 40
FA = 41
SOL = 43

SEMITOM = 1
DURACAO_NOTA = 480

# ==========================
# Configurações
# ==========================

OITAVA_INICIAL = 36
TAMANHO_OITAVA = 12
OITAVA_MAXIMA = 73

VOLUME_INICIAL = 100
VOLUME_MAXIMO = 127

BPM_INICIAL = 120

DECRESCIMO_BPM = -10
ACRESCIMO_BPM = 10

CICLO_VOZES = 4


class MusicEvent:

    def __init__(
        self,
        nota,
        instrumento,
        oitava,
        volume,
        tempo_de_atraso,
        bpm,
        faixa,
        indice
    ):

        self.nota = nota
        self.instrumento = instrumento
        self.oitava = oitava
        self.volume = volume
        self.tempo_de_atraso = tempo_de_atraso
        self.bpm = bpm
        self.faixa = faixa
        self.indice = indice


class BPM:

    def __init__(
        self,
        aumenta_bpm,
        faixa_novo_bpm,
        posicao_novo_bpm,
        novoBPM
    ):

        self.aumenta_bpm = aumenta_bpm
        self.faixa_novo_bpm = faixa_novo_bpm
        self.posicao_novo_bpm = posicao_novo_bpm
        self.novoBPM = novoBPM


class MusicInterpreter:
    """
    Converte texto em eventos musicais.
    """

    def __init__(self, user_settings=None):

        self.notaAtual = 0
        self.instrumentoAtual = 0
        self.volumeAtual = 0
        self.oitavaAtual = 0

        self.tempo_de_atraso = 0

        self.bpmAtual = 0

        self.faixaAtual = 0
        self.numero_faixas = 0

        self.lista_de_eventos = []
        self.lista_alteracoes = []

        if user_settings is None:
            self.user_settings = Settings()
        else:
            self.user_settings = user_settings

    def converteCaractere(self, texto):

        # limpa completamente os dados da geração anterior

        self.lista_de_eventos = []
        self.lista_alteracoes = []

        self.faixaAtual = 0
        self.numero_faixas = 0

        self.novaLinha()

        indice_evento = 0

        caractereAnterior = ""

        valor_atraso = ""

        atraso = False

        for i, caractereAtual in enumerate(texto):

            silence = False

            match caractereAtual.upper():

                case 'A':
                    self.notaAtual = LA + self.oitavaAtual

                case 'B':
                    self.notaAtual = SI + self.oitavaAtual

                case 'C':
                    self.notaAtual = DO + self.oitavaAtual

                case 'D':
                    self.notaAtual = RE + self.oitavaAtual

                case 'E':
                    self.notaAtual = MI + self.oitavaAtual

                    if i + 1 < len(texto) and texto[i + 1] == 'b':
                        self.notaAtual = (MI - SEMITOM) + self.oitavaAtual

                case 'F':
                    self.notaAtual = FA + self.oitavaAtual

                case 'G':
                    self.notaAtual = SOL + self.oitavaAtual

                case 'H':
                    self.notaAtual = (SI - SEMITOM) + self.oitavaAtual

                # ------------------------
                # Oitava
                # ------------------------

                case 'V':
                    self.oitavaAtual -= TAMANHO_OITAVA
                    silence = True

                case '?' | '.':
                    if self.oitavaAtual + TAMANHO_OITAVA < OITAVA_MAXIMA:
                        self.oitavaAtual += TAMANHO_OITAVA
                    else:
                        self.oitavaAtual = OITAVA_INICIAL

                    silence = True

                # ------------------------
                # Instrumentos
                # ------------------------

                case 'O' | 'I' | 'U':
                    self.instrumentoAtual = GAITA_DE_FOLES
                    silence = True

                case '!':
                    self.instrumentoAtual = HARMONICA
                    silence = True

                case ';':
                    self.instrumentoAtual = TUBULAR_BELLS
                    silence = True

                case ',':
                    self.instrumentoAtual = ORGAO
                    silence = True

                case c if c.isdigit():

                    numero = int(c)

                    if numero % 2 == 0:
                        self.instrumentoAtual = numero
                    else:
                        self.instrumentoAtual = TUBULAR_BELLS

                    silence = True

                # ------------------------
                # Volume
                # ------------------------

                case ' ':

                    self.volumeAtual = min(
                        self.volumeAtual * 2,
                        VOLUME_MAXIMO
                    )

                    silence = True

                # ------------------------
                # BPM
                # ------------------------

                case '>':

                    self.bpmAtual += ACRESCIMO_BPM
                    silence = True

                case '<':

                    self.bpmAtual += DECRESCIMO_BPM
                    silence = True

                # ------------------------
                # Nova linha
                # ------------------------

                case '\n':

                    self.faixaAtual += 1
                    indice_evento = 0

                    self.novaLinha()

                    silence = True

                # ------------------------
                # Atraso
                # ------------------------

                case '[':

                    atraso = True
                    valor_atraso = ""
                    silence = True

                case ']':

                    if valor_atraso:

                        self.tempo_de_atraso = DURACAO_NOTA * int(valor_atraso)
                        indice_evento += int(valor_atraso)

                    atraso = False
                    silence = True

                case c if atraso and c.isdigit():

                    valor_atraso += c
                    silence = True

                # ------------------------
                # Letras sem nota
                # ------------------------

                case c if 'i' < c.lower() <= 'z':

                    self.tempo_de_atraso += DURACAO_NOTA
                    indice_evento += 1
                    silence = True

                case c if 'a' <= c <= 'h':

                    if not (c == 'b' and caractereAnterior == 'E'):
                        self.tempo_de_atraso += DURACAO_NOTA
                        indice_evento += 1

                    silence = True

                case _:

                    self.tempo_de_atraso += DURACAO_NOTA
                    indice_evento += 1
                    silence = True

            caractereAnterior = caractereAtual

            self.numero_faixas = self.faixaAtual + 1

                        # ------------------------------------------------------
            # Cria o evento musical
            # ------------------------------------------------------

            if not silence:

                indice_evento += 1

                evento = MusicEvent(
                    nota=self.notaAtual,
                    instrumento=self.instrumentoAtual,
                    oitava=self.oitavaAtual,
                    volume=self.volumeAtual,
                    tempo_de_atraso=self.tempo_de_atraso,
                    bpm=self.bpmAtual,
                    faixa=self.faixaAtual,
                    indice=indice_evento
                )

                self.lista_de_eventos.append(evento)

                # zera o atraso após tocar a nota
                self.tempo_de_atraso = 0

        return self.lista_de_eventos

    # ------------------------------------------------------
    # Inicializa uma nova linha/faixa
    # ------------------------------------------------------

    def novaLinha(self):

        resto = self.faixaAtual % CICLO_VOZES

        voz = self.user_settings.vozes[resto]

        self.bpmAtual = self.user_settings.bpmAtual
        self.instrumentoAtual = voz.instrumento
        self.volumeAtual = voz.volume
        self.oitavaAtual = voz.oitava

        self.tempo_de_atraso = voz.atraso