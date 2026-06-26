import mido
from MusicInterpreter import MusicInterpreter, DURACAO_NOTA

# nome do arquivo midi temporário usado por todos os módulos do projeto
ARQUIVO_TEMP = "faixa_gerada.mid"

class MusicGenerator:
    """ recebe a lista de eventos gerada pelo musicinterpreter, 
    converte para um arquivo.mid usando mido
    """
    def __init__(self):
        self.partitura = ''
        self._arquivo_gerado = False

    def produz_MIDI(self, texto, user_settings):

        interpretador = MusicInterpreter(user_settings)
        self.partitura = interpretador.converteCaractere(texto)

        if not self.partitura:
            raise ValueError("Nenhum evento musical foi gerado.")

        arquivo_mid = mido.MidiFile()

        for faixa_id in range(interpretador.numero_faixas):

            track = mido.MidiTrack()
            arquivo_mid.tracks.append(track)

            eventos = [
                e for e in self.partitura
                if e.faixa == faixa_id
            ]

            if not eventos:
                continue

        primeiro = eventos[0]

        # BPM da faixa
        track.append(
            mido.MetaMessage(
                "set_tempo",
                tempo=mido.bpm2tempo(primeiro.bpm),
                time=0
            )
        )

        # Instrumento da faixa
        track.append(
            mido.Message(
                "program_change",
                program=primeiro.instrumento,
                time=0
            )
        )

        tempo_acumulado = 0

        for evento in eventos:

            tempo_acumulado += evento.tempo_de_atraso

            track.append(
                mido.Message(
                    "note_on",
                    note=evento.nota,
                    velocity=evento.volume,
                    time=tempo_acumulado
                )
            )

            track.append(
                mido.Message(
                    "note_off",
                    note=evento.nota,
                    velocity=0,
                    time=DURACAO_NOTA
                )
            )

            tempo_acumulado = 0

            arquivo_mid.save(ARQUIVO_TEMP)

            self._arquivo_gerado = True

            print(f"arquivo midi gerado: {ARQUIVO_TEMP}")
    # ──────────────────────────────────────────────────────────────────────
    # geração do midi
    # ──────────────────────────────────────────────────────────────────────
        arquivo_mid = mido.MidiFile() 
        lista_de_faixas = {}
        for faixa_id in range(0, interpretador.numero_faixas):          # processa as faixas em ordem (0, 1, 2...)    
            lista_de_faixas[f"faixa{faixa_id}"] = mido.MidiTrack()
            arquivo_mid.tracks.append( lista_de_faixas[f"faixa{faixa_id}"])

            ultimo_bpm = None
            ultimo_instrumento = None

            for evento in self.partitura:

                if evento.faixa != faixa_id:
                    continue

                if evento.bpm != ultimo_bpm:
                    lista_de_faixas[f"faixa{faixa_id}"].append(
                        mido.MetaMessage(
                'set_tempo',
                tempo=mido.bpm2tempo(evento.bpm),
                time=0
            )
        )
                ultimo_bpm = evento.bpm

                if evento.instrumento != ultimo_instrumento:
                    lista_de_faixas[f"faixa{faixa_id}"].append(
            mido.Message(
                'program_change',
                program=evento.instrumento,
                time=0
            )
        )
                ultimo_instrumento = evento.instrumento

                lista_de_faixas[f"faixa{faixa_id}"].append(
                mido.Message(
            'note_on',
            note=evento.nota,
            velocity=evento.volume,
            time=evento.tempo_de_atraso
        )
    )

            lista_de_faixas[f"faixa{faixa_id}"].append(
                mido.Message(
            'note_off',
            note=evento.nota,
            velocity=100,
            time=DURACAO_NOTA
        )
    )                                                             # note_off: solta a nota após duracao_nota_ticks; velocity=0 é padrão midi
        arquivo_mid.save(ARQUIVO_TEMP)
        self._arquivo_gerado = True     #atualiza a flag para indicar que há um arquivo pronto para tocar
        print(f"arquivo midi gerado: {ARQUIVO_TEMP}")
