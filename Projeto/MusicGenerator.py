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
        """
        converte a lista de musicevent em um arquivo .mid e salva em disco.

        usa as configurações de cada voz (instrumento, volume, oitava, atraso)
        para configurar as faixas.

        para cada evento, adiciona quatro mensagens na faixa midi:
            set_tempo      — atualiza o bpm naquele instante
            program_change — define o instrumento general midi
            note_on        — inicia a nota (time = silêncio antes de soar)
            note_off       — encerra a nota após duracao_nota_ticks ticks
        """
        interpretador = MusicInterpreter(user_settings)
        self.partitura = interpretador.converteCaractere(texto)
        if not self.partitura:
            raise ValueError("Nenhum evento musical foi gerado.")
            return  
    # ──────────────────────────────────────────────────────────────────────
    # geração do midi
    # ──────────────────────────────────────────────────────────────────────
        arquivo_mid = mido.MidiFile() 
        lista_de_faixas = {}
        for faixa_id in range(0, interpretador.numero_faixas):          # processa as faixas em ordem (0, 1, 2...)    
            lista_de_faixas[f"faixa{faixa_id}"] = mido.MidiTrack()
            arquivo_mid.tracks.append( lista_de_faixas[f"faixa{faixa_id}"])

            for evento in self.partitura:
                if evento.faixa == faixa_id:

                    tempo = mido.bpm2tempo(evento.bpm)     # converte bpm para microssegundos por batida (formato exigido pelo midi)
                                                                    # usa o bpm do settings se disponível, senão usa o do evento
                    lista_de_faixas[f"faixa{faixa_id}"].append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))  
                                                                                                
                    lista_de_faixas[f"faixa{faixa_id}"].append(mido.Message('program_change', program=evento.instrumento, time=0)) 
                                                                                                 # troca o instrumento antes de tocar a nota
                    lista_de_faixas[f"faixa{faixa_id}"].append(mido.Message('note_on', note=evento.nota, velocity= evento.volume, time=evento.tempo_de_atraso))    
                                                                                                 # note_on: tempo_de_atraso é o silêncio acumulado
                    lista_de_faixas[f"faixa{faixa_id}"].append(mido.Message('note_off', note=evento.nota, velocity=100, time=DURACAO_NOTA))    
                                                                                                 # note_off: solta a nota após duracao_nota_ticks; velocity=0 é padrão midi
        arquivo_mid.save(ARQUIVO_TEMP)
        self._arquivo_gerado = True     #atualiza a flag para indicar que há um arquivo pronto para tocar
        print(f"arquivo midi gerado: {ARQUIVO_TEMP}")
