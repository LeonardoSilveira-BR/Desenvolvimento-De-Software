import mido

#constantes
PIANO = 0                           #instrumentos
CRAVO = 6
ORGAO = 20
BANDONEON = 24
FAGOTE = 70
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

VOLUME_INICIAL = 100 
DECRESCIMO_VOLUME = 20
OITAVA_INICIAL = 6
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
    def __init__(self):
        self.notaAtual = 0
        self.instrumentoAtual = 0
        self.volumeAtual = 0
        self.oitavaAtual = 0
        self.tempo_de_atraso = 0
        self.bpmAtual = 0
        self.faixaAtual = 0

    def novaLinha(self):                #private    
        resto = self.faixaAtual % 4       #resto da divisão da linha por 4, para manter as vozes nos 4 casos
        match resto:
            case 0:
                self.oitavaAtual = OITAVA_INICIAL
                self.volumeAtual = VOLUME_INICIAL
                self.instrumentoAtual = CRAVO      # = getInstrumentoInicial()
            case 1:
                self.oitavaAtual -= 1
                self.volumeAtual -= DECRESCIMO_VOLUME
                self.instrumentoAtual = ORGAO
            case 2:
                self.oitavaAtual -= 1
                self.volumeAtual -= DECRESCIMO_VOLUME
                self.instrumentoAtual = PIANO
            case 3:
                self.oitavaAtual -= 1
                self.volumeAtual -= DECRESCIMO_VOLUME
                self.instrumentoAtual = FAGOTE  
    def alteraBPM(self):            #######!!!!!!!!!
        pass

    def converteCaractere(self, texto):              
        lista_de_eventos: list[MusicEvent] = []
        self.bpmAtual = 120 #inicial ###########!!!!!
        self.novaLinha()    #inicial
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
                    self.faixaAtual += 1
                    self.novaLinha()
                    silence = True 
                case c if caractereAnterior == '[' and c.isdigit():
                    self.tempo_de_atraso = 480 * int(c)                
                    silence = True 
                case c if c == '[' or c == ']':               #########!!!!!
                    silence = True              
                case c if  c == ';' or (c.isdigit() and int(c)%2 != 0):           
                    self.instrumentoAtual = TUBULAR_BELLS
                    silence = True
                case c if c.isdigit() and int(c) % 2 == 0:             
                    self.instrumentoAtual += int(c) 
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


class MusicGenerator:
    def __init__(self):
        self.partitura = ''
    def produzMIDI(self, texto):
        interpretador = MusicInterpreter()
        self.partitura = interpretador.converteCaractere(texto)
        arquivoMid = mido.MidiFile() 
        lista_de_faixas = {}
        for i in range(0, 4):    # 4 -> quantidade_vozes + 1    ######!!!!!!!!!
            lista_de_faixas[f"faixa{i}"] = mido.MidiTrack()            
            arquivoMid.tracks.append( lista_de_faixas[f"faixa{i}"])
            for evento in self.partitura:
                if evento.faixa == i:                    #verifica se o número da faixa corresponde ao numero na lista_de_faixas
                    tempo = mido.bpm2tempo(evento.bpm)
                    lista_de_faixas[f"faixa{i}"].append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))     

                    lista_de_faixas[f"faixa{i}"].append(mido.Message('program_change', program=evento.instrumento, time=0))  #program é o insrumento

                    lista_de_faixas[f"faixa{i}"].append(mido.Message('note_on', note=evento.nota, velocity= evento.volume, time=evento.tempo_de_atraso))    #em note_on, time = tempo para iniciar a nota

                    lista_de_faixas[f"faixa{i}"].append(mido.Message('note_off', note=evento.nota, velocity=100, time=480))    #em note_off, o time é o tempo que dura a nota

        arquivoMid.save('testeLogica.mid')


#teste
class TextReader:
    def __init__(self):
        self.texto = 'A\nA\nCB'
    def getText(self):
        return self.texto
    
#teste
leitor = TextReader()
texto = leitor.getText()   

musica = MusicGenerator()
musica.produzMIDI(texto)



