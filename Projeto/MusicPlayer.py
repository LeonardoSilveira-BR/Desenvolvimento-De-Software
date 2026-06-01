import time

# importações com tratamento de erro para permitir rodar os testes
# sem precisar das bibliotecas instaladas no ambiente de teste
try:
    import mido
except ImportError:
    mido = None  # type: ignore

try:
    import pygame
except ImportError:
    pygame = None  # type: ignore


# nome do arquivo midi temporário usado por todos os módulos do projeto
ARQUIVO_TEMP = "faixa_gerada.mid"

# duração de cada nota em ticks midi (480 ticks equivale a 1 batida no padrão midi)
DURACAO_NOTA_TICKS = 480


class MusicPlayer:
    """
    recebe a lista de eventos gerada pelo musicinterpreter,
    converte para um arquivo .mid usando mido e controla
    a reprodução com pygame (play, pause, stop, restart).

    integra com settings e voice: usa as configurações de cada voz
    (oitava, volume, instrumento, atraso) para montar as faixas midi.
    """

    def __init__(self, settings=None):
        # settings é opcional — se não for passado, usa os valores dos eventos diretamente
        self._settings = settings
        self._arquivo_gerado = False  # true depois que gerar_midi() for chamado
        self._pausado        = False  # true quando a reprodução está pausada
        self._tocando        = False  # true quando a reprodução está ativa

    # ──────────────────────────────────────────────────────────────────────
    # geração do midi
    # ──────────────────────────────────────────────────────────────────────

    def gerar_midi(self, lista_de_eventos: list) -> None:
        """
        converte a lista de musicevent em um arquivo .mid e salva em disco.

        se settings foi passado no construtor, usa as configurações de cada
        voz (instrumento, volume, oitava, atraso) para configurar as faixas.

        para cada evento, adiciona quatro mensagens na faixa midi:
            set_tempo      — atualiza o bpm naquele instante
            program_change — define o instrumento general midi
            note_on        — inicia a nota (time = silêncio antes de soar)
            note_off       — encerra a nota após duracao_nota_ticks ticks
        """
        if not lista_de_eventos:
            print("erro: lista de eventos vazia. interprete o texto primeiro.")
            return

        # separa os eventos pelo número da faixa para suportar múltiplas vozes
        # cada faixa vira uma track independente dentro do arquivo midi
        faixas: dict[int, list] = {}
        for evento in lista_de_eventos:
            if evento.faixa not in faixas:
                faixas[evento.faixa] = []
            faixas[evento.faixa].append(evento)

        arquivo_mid = mido.MidiFile()

        # processa as faixas em ordem (0, 1, 2...) para manter a sequência correta
        for faixa_id, eventos_da_faixa in sorted(faixas.items()):
            faixa = mido.MidiTrack()
            arquivo_mid.tracks.append(faixa)

            # se settings foi fornecido, aplica as configurações da voz correspondente
            # isso permite que a interface gráfica controle volume/instrumento por voz
            if self._settings and faixa_id < len(self._settings.vozes):
                voz = self._settings.vozes[faixa_id]
                instrumento_inicial = voz.getInstrumento()
                atraso_inicial      = voz.getAtraso()

                # define o instrumento inicial da voz antes de qualquer nota
                faixa.append(mido.Message('program_change',
                                          program=instrumento_inicial,
                                          time=0))

                # insere o atraso inicial da voz (entrada defasada da fuga)
                if atraso_inicial > 0:
                    faixa.append(mido.Message('note_on',
                                              note=0,
                                              velocity=0,
                                              time=atraso_inicial))

            for evento in eventos_da_faixa:
                # converte bpm para microssegundos por batida (formato exigido pelo midi)
                # usa o bpm do settings se disponível, senão usa o do evento
                bpm_atual = self._settings.bpmAtual if self._settings else evento.bpm
                tempo = mido.bpm2tempo(bpm_atual)

                faixa.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

                # troca o instrumento antes de tocar a nota
                faixa.append(mido.Message('program_change',
                                          program=evento.instrumento,
                                          time=0))

                # note_on: tempo_de_atraso é o silêncio acumulado pelas letras minúsculas a-h
                faixa.append(mido.Message('note_on',
                                          note=evento.nota,
                                          velocity=evento.volume,
                                          time=evento.tempo_de_atraso))

                # note_off: solta a nota após duracao_nota_ticks; velocity=0 é padrão midi
                faixa.append(mido.Message('note_off',
                                          note=evento.nota,
                                          velocity=0,
                                          time=DURACAO_NOTA_TICKS))

        arquivo_mid.save(ARQUIVO_TEMP)

        # atualiza os flags para indicar que há um arquivo pronto para tocar
        self._arquivo_gerado = True
        self._pausado        = False
        self._tocando        = False
        print(f"arquivo midi gerado: {ARQUIVO_TEMP}")

    # ──────────────────────────────────────────────────────────────────────
    # controles de reprodução
    # ──────────────────────────────────────────────────────────────────────

    def play(self) -> None:
        """
        inicia ou retoma a reprodução.

        - sem arquivo gerado : exibe mensagem de erro
        - pausado            : retoma do ponto onde parou
        - já tocando         : ignora a chamada
        - parado / novo      : carrega o arquivo e começa do início
        """
        if not self._arquivo_gerado:
            print("erro: gere o midi primeiro chamando gerar_midi().")
            return

        if self._pausado:
            # unpause retoma exatamente de onde o pause ocorreu
            pygame.mixer.music.unpause()
            self._pausado = False
            self._tocando = True
            print("reprodução retomada.")
            return

        if self._tocando:
            print("já está tocando.")
            return

        # inicializa o mixer apenas se necessário para não sobrescrever configurações
        self._inicializar_pygame()

        try:
            pygame.mixer.music.load(ARQUIVO_TEMP)
            pygame.mixer.music.play()
            self._tocando = True
            self._pausado = False
            print("reprodução iniciada.")
        except pygame.error as e:
            print(f"erro ao tocar o arquivo: {e}")

    def pause(self) -> None:
        """
        pausa a reprodução no ponto atual.
        chame play() para retomar do mesmo lugar.
        """
        if not self._tocando or self._pausado:
            print("não está tocando.")
            return

        pygame.mixer.music.pause()
        self._pausado = True
        self._tocando = False
        print("reprodução pausada.")

    def stop(self) -> None:
        """
        para a reprodução completamente.
        a próxima chamada a play() recomeça do início.
        """
        if not self._tocando and not self._pausado:
            print("não está tocando.")
            return

        pygame.mixer.music.stop()
        self._tocando = False
        self._pausado = False
        print("reprodução parada.")

    def restart(self) -> None:
        """para e reinicia a reprodução do início."""
        self.stop()
        self._pausado = False  # garante que play() não tente retomar do meio
        self.play()

    def esta_tocando(self) -> bool:
        """retorna true se o pygame ainda está reproduzindo áudio no momento."""
        return pygame.mixer.music.get_busy()

    def aguardar_fim(self) -> None:
        """
        bloqueia até a música terminar por completo.
        útil em scripts simples que não têm interface gráfica.
        """
        while self.esta_tocando():
            time.sleep(0.5)

    def encerrar(self) -> None:
        """
        libera os recursos de áudio do pygame.
        deve ser chamado quando o programa for fechado.
        """
        pygame.mixer.quit()
        self._tocando = False
        self._pausado = False
        print("player encerrado.")

    # ──────────────────────────────────────────────────────────────────────
    # métodos privados
    # ──────────────────────────────────────────────────────────────────────

    def _inicializar_pygame(self) -> None:
        """inicializa o mixer do pygame somente se ainda não estiver ativo."""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
