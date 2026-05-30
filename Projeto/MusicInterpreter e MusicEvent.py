import mido

#constantes
BANDONEON = 24
GAITA_DE_FOLES = 110
TUBULAR_BELLS = 15
ONDAS_MAR = 123
AGOGO = 114

TAMANHO_OITAVA = 12
OITAVA_MAXIMA = 49
LA = 69
SI = 71
DO = 60
RE = 62
MI = 64
FA = 65
SOL = 67
SEMITOM = 1
#constantes

class MusicEvent:
    def __init__(self, nota, instrumento, oitava, volume, tempo_de_atraso, bpm, faixa):
        self.nota = nota
        self.instrumento = instrumento
        self.oitava = oitava
        self.volume = volume
        self.tempo_de_atraso = tempo_de_atraso
        self.bpm = bpm
        self.faixa = faixa
class MusicInterpreter:
    def __init__(self, notaAtual, instrumentoAtual, volumeAtual, oitavaAtual, tempo_de_atraso, bpmAtual, faixaAtual):
        self.notaAtual = notaAtual
        self.instrumentoAtual = instrumentoAtual
        self.volumeAtual = volumeAtual
        self.oitavaAtual = oitavaAtual
        self.tempo_de_atraso = tempo_de_atraso
        self.bpmAtual = bpmAtual
        self.faixaAtual = faixaAtual

    def converteCaractere(self, texto):
        lista_de_eventos: list[MusicEvent] = []
        self.volumeAtual = 70 #inicial
        self.bpmAtual = 120 #inicial #(vai estar em outro lugar?)
        caractereAnterior = 0
        silence = False
        for caractereAtual in texto:
            silence = False
            match caractereAtual:
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
                case 'F':
                    self.notaAtual = FA + self.oitavaAtual
                case 'G':
                    self.notaAtual = SOL + self.oitavaAtual
                case 'H':
                    self.notaAtual = (SI - SEMITOM) + self.oitavaAtual
                case 'M':
                    self.notaAtual = (MI - SEMITOM) + self.oitavaAtual
                case c if 'i' < c.lower() <= 'z':
                    if 'A' <= caractereAnterior <= 'H':
                        pass
                    else:
                        silence = True
                case '!':
                    self.instrumentoAtual = BANDONEON
                    silence = True
                case 'O'|'o'|'I'|'i'|'U'|'u':
                    self.instrumentoAtual = GAITA_DE_FOLES
                    silence = True
                case c if 'a' <= c <= 'h':
                    self.tempo_de_atraso += 480          #tem que ser o mesmo tempo que a nota fica ligada
                    silence = True
                case '?'|'.':
                    if (self.oitavaAtual + 12) < OITAVA_MAXIMA:
                        self.oitavaAtual += TAMANHO_OITAVA          
                    else:
                        self.oitavaAtual = 0            
                    silence = True
                case '\n':
                    #self.instrumentoAtual = ONDAS_MAR    
                    #troca a faixa e re      
                    silence = True
                case c if  c == ';' or ord(c)%2 != 0:
                    self.instrumentoAtual = TUBULAR_BELLS
                    silence = True
                case c if c.isdigit() and ord(c) % 2 == 0:
                    self.instrumentoAtual += ord(c) 
                    silence = True
                case ',':
                    self.instrumentoAtual = AGOGO
                    silence = True
                case ' ':
                    if (self.volumeAtual * 2) > 127:
                        self.volumeAtual = 127
                        silence = True
                    else:
                        self.volumeAtual *= 2
                        silence = True
                case '>':
                    self.bpmAtual += 10
                    silence = True
                case '<':
                    self.bpmAtual -= 10
                    silence = True
            caractereAnterior = caractereAtual 
            if (silence == False ):    #cria evento na lista apenas no caso de mudança de nota 
                evento = MusicEvent(nota = self.notaAtual, instrumento=self.instrumentoAtual,volume= self.volumeAtual, oitava=self.oitavaAtual, tempo_de_atraso=self.tempo_de_atraso, bpm= self.bpmAtual, faixa = self.faixaAtual)
                lista_de_eventos.append(evento)  
                self.tempo_de_atraso = 0           #retira o silencio entre notas 
        return lista_de_eventos

#aqui pra baixo é em outra classe

#teste
texto = 'GaaFAEaDGC '   
interpretador = MusicInterpreter(0,0,0,-2,0,0,0)
partitura = interpretador.converteCaractere(texto)

#PRODUZ O MID E SALVA 
arquivoMid = mido.MidiFile() 
faixa1 = mido.MidiTrack()
arquivoMid.tracks.append(faixa1)
for evento in partitura:
    tempo = mido.bpm2tempo(evento.bpm)
    faixa1.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

    faixa1.append(mido.Message('program_change', program=evento.instrumento, time=0))  #program é o insrumento

    faixa1.append(mido.Message('note_on', note=evento.nota, velocity= evento.volume, time=evento.tempo_de_atraso))

    faixa1.append(mido.Message('note_off', note=evento.nota, velocity=100, time=480))    #note_off, o time é o tempo que dura a nota


mid = mido.MidiFile('testeLogica.mid')
arquivoMid.save('testeLogica.mid')





