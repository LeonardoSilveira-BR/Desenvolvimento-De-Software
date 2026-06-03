
#FOI SEPARADO EM DIFERENTES ARQUIVOS!!

import mido

#instrumentos
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

#notas
LA = 45
SI = 47
DO = 36        
RE = 38
MI = 40
FA = 41
SOL = 43
SEMITOM = 1
DURACAO_NOTA = 480

OITAVA_INICIAL = 36     #oitava 6 = 36
TAMANHO_OITAVA = 12                       
OITAVA_MAXIMA = 73
VOLUME_INICIAL = 100 
VOLUME_MAXIMO = 127
DECRESCIMO_VOLUME = 20
BPM_INICIAL = 120
DECRESCIMO_BPM = -10
ACRESCIMO_BPM = 10

CICLO_VOZES = 4

class MusicEvent:
    def __init__(self, nota, instrumento, oitava, volume, tempo_de_atraso, bpm, faixa, indice):
        self.nota = nota
        self.instrumento = instrumento
        self.oitava = oitava
        self.volume = volume
        self.tempo_de_atraso = tempo_de_atraso
        self.bpm = bpm
        self.faixa = faixa
        self.indice = indice      

class BPM:
    def __init__(self, aumenta_bpm, faixa_novo_bpm, posicao_novo_bpm, novoBPM):
        self.aumenta_bpm = aumenta_bpm
        self.faixa_novo_bpm = faixa_novo_bpm
        self.posicao_novo_bpm = posicao_novo_bpm
        self.novoBPM = novoBPM

class MusicInterpreter:
    def __init__(self):
        self.notaAtual = 0
        self.instrumentoAtual = 0
        self.volumeAtual = 0
        self.oitavaAtual = 0
        self.tempo_de_atraso = 0
        self.bpmAtual = 0
        self.faixaAtual = 0
        self.numero_faixas = 0
        self.lista_de_eventos: list[MusicEvent] = []
        self.lista_alteracoes: list[BPM] = []

    def novaLinha(self):                   
        self.bpmAtual = BPM_INICIAL         #getBPM()  pega bpm estabelecido no inicio, pelo usuario
        resto = self.faixaAtual % CICLO_VOZES      #resto da divisão da linha por 4, para manter as vozes nos 4 casos
        match resto:
            case 0:
                self.oitavaAtual = OITAVA_INICIAL
                self.volumeAtual = VOLUME_INICIAL
                self.instrumentoAtual = PIANO      # = getInstrumentoInicial()
            case 1:
                self.oitavaAtual -= TAMANHO_OITAVA
                self.volumeAtual -= DECRESCIMO_VOLUME
                self.instrumentoAtual = ORGAO      # = getInstrumentoInicial()
            case 2:
                self.oitavaAtual -= TAMANHO_OITAVA
                self.volumeAtual -= DECRESCIMO_VOLUME
                self.instrumentoAtual = PIANO      # = getInstrumentoInicial()
            case 3:
                self.oitavaAtual -= TAMANHO_OITAVA
                self.volumeAtual -= DECRESCIMO_VOLUME
                self.instrumentoAtual = FAGOTE      # = getInstrumentoInicial()

    def converteCaractere(self, texto):              
        indice_evento = 0
        self.novaLinha()    
        caractereAnterior = 0
        valor_atraso = " "
        atraso = False
        bpm = BPM(False, 0,0,0)
        for i, caractereAtual in enumerate(texto):
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
                    if i + 1 < len(texto) and texto[i + 1] == 'b':
                        self.notaAtual = (MI - SEMITOM) + self.oitavaAtual
                case 'F':
                    self.notaAtual = FA + self.oitavaAtual
                case 'G':
                    self.notaAtual = SOL + self.oitavaAtual
                case 'H':
                    self.notaAtual = (SI - SEMITOM) + self.oitavaAtual
                case 'V':
                    self.oitavaAtual -= TAMANHO_OITAVA  
                    silence = True
                case 'O'|'o'|'I'|'i'|'U'|'u':
                    self.instrumentoAtual = GAITA_DE_FOLES
                    silence = True
                case c if 'i' < c.lower() <= 'z':
                    if 'A' <= caractereAnterior <= 'H':
                        silence = False
                    else:
                        self.tempo_de_atraso += DURACAO_NOTA    
                        silence = True
                        indice_evento += 1       #contabiliza o silencio na ordem dos eventos de cada faixa/voz
                case '!':
                    self.instrumentoAtual = HARMONICA
                    silence = True

                case c if 'a' <= c <= 'h':
                    silence = True
                    if  c == 'b' and caractereAnterior == 'E':              #caso de Eb
                        pass
                    else:
                        self.tempo_de_atraso += DURACAO_NOTA         
                        indice_evento += 1      
                case '?'|'.':
                    if (self.oitavaAtual + TAMANHO_OITAVA) < OITAVA_MAXIMA:             
                        self.oitavaAtual += TAMANHO_OITAVA          
                    else:
                        self.oitavaAtual = OITAVA_INICIAL            
                    silence = True
                case '\n': 
                    silence = True   
                    self.faixaAtual += 1
                    indice_evento = 0
                    self.novaLinha()
                case c if atraso == True and c.isdigit():
                    valor_atraso += c
                    silence = True
                    if i + 1 < len(texto) and not texto[i+1].isdigit():                
                        self.tempo_de_atraso = 480 * int(valor_atraso) 
                        atraso = False
                        indice_evento += int(valor_atraso)         
                case c if c == '[':              
                    atraso = True                       
                    silence = True 
                case c if c == ']':
                    valor_atraso = ' '
                    silence = True       
                case c if  c == ';' or (c.isdigit() and int(c)%2 != 0):           
                    self.instrumentoAtual = TUBULAR_BELLS
                    silence = True
                case c if c.isdigit() and int(c) % 2 == 0:             
                    self.instrumentoAtual += int(c) 
                    silence = True
                case ',':
                    self.instrumentoAtual = ORGAO
                    silence = True
                case ' ':
                    if (self.volumeAtual * 2) > VOLUME_MAXIMO:
                        self.volumeAtual = VOLUME_MAXIMO
                        silence = True
                    else:
                        self.volumeAtual *= 2
                        silence = True
                case c if c == '>' or c == '<':
                    if caractereAtual == '>':
                        bpm = BPM(True, faixa_novo_bpm = self.faixaAtual, posicao_novo_bpm = indice_evento, novoBPM = ACRESCIMO_BPM)
                    if caractereAtual == '<':
                        bpm = BPM(False, faixa_novo_bpm = self.faixaAtual, posicao_novo_bpm = indice_evento, novoBPM = DECRESCIMO_BPM)
                    self.lista_alteracoes.append(bpm)
                    silence = True
                case _:
                    if 'A' <= caractereAnterior <= 'H':
                        silence = False
                    else:
                        self.tempo_de_atraso += DURACAO_NOTA    
                        silence = True
                        indice_evento += 1  
            caractereAnterior = caractereAtual 
            self.numero_faixas = self.faixaAtual + 1
            if (silence == False ):    #cria evento na lista apenas no caso de mudança de nota 
                indice_evento += 1      #contabiliza as notas na ordem dos eventos de cada faixa/voz
                evento = MusicEvent(nota = self.notaAtual, instrumento=self.instrumentoAtual,volume= self.volumeAtual, oitava=self.oitavaAtual, tempo_de_atraso=self.tempo_de_atraso, bpm= self.bpmAtual, faixa = self.faixaAtual, indice = indice_evento)
                self.lista_de_eventos.append(evento)  
                self.tempo_de_atraso = 0           #retira o silencio entre notas 
        self.altera_bpm(bpm)
        return self.lista_de_eventos    
    
    def altera_bpm(self, bpm):
        for alteracao in self.lista_alteracoes:
            for evento in self.lista_de_eventos:
                if (evento.faixa < alteracao.faixa_novo_bpm or evento.faixa == alteracao.faixa_novo_bpm) and (evento.indice > alteracao.posicao_novo_bpm):
                        evento.bpm = evento.bpm + alteracao.novoBPM 
                if evento.faixa > alteracao.faixa_novo_bpm and (evento.indice >alteracao.posicao_novo_bpm):
                        evento.bpm = evento.bpm + alteracao.novoBPM 

class MusicGenerator:
    def __init__(self):
        self.partitura = ''
    def produzMIDI(self, texto):
        interpretador = MusicInterpreter()
        self.partitura = interpretador.converteCaractere(texto)
        arquivoMid = mido.MidiFile() 
        lista_de_faixas = {}
        for i in range(0, interpretador.numero_faixas):    
            lista_de_faixas[f"faixa{i}"] = mido.MidiTrack()
            arquivoMid.tracks.append( lista_de_faixas[f"faixa{i}"])
            for evento in self.partitura:
                if evento.faixa == i:
                    tempo = mido.bpm2tempo(evento.bpm)
                    lista_de_faixas[f"faixa{i}"].append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))       #se estabelecer o bpm pra uma faixa ja muda nas outras

                    lista_de_faixas[f"faixa{i}"].append(mido.Message('program_change', program=evento.instrumento, time=0))  #program é o insrumento

                    lista_de_faixas[f"faixa{i}"].append(mido.Message('note_on', note=evento.nota, velocity= evento.volume, time=evento.tempo_de_atraso))    #aqui o time é o tempo para iniciar a nota

                    lista_de_faixas[f"faixa{i}"].append(mido.Message('note_off', note=evento.nota, velocity=100, time=DURACAO_NOTA))    

        arquivoMid.save('faixa_gerada.mid')
