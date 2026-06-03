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
    controla a reprodução com pygame (play, pause, stop, restart).
    """

    def __init__(self, settings=None):
        self._pausado        = False  # true quando a reprodução está pausada
        self._tocando        = False  # true quando a reprodução está ativa
        
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
