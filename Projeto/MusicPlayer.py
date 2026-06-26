import time
import subprocess

# importações com tratamento de erro para permitir rodar os testes
# sem precisar das bibliotecas instaladas no ambiente de teste
try:
    import mido
except ImportError:
    mido = None  # type: ignore


# nome do arquivo midi temporário usado por todos os módulos do projeto
ARQUIVO_TEMP = "faixa_gerada.mid"

# duração de cada nota em ticks midi (480 ticks equivale a 1 batida no padrão midi)
DURACAO_NOTA_TICKS = 480


class MusicPlayer:
    """
    Controla a reprodução do arquivo MIDI utilizando o TiMidity.
    """

    def __init__(self, settings=None):
        self._pausado = False
        self._tocando = False
        self._processo = None

    # ──────────────────────────────────────────────────────────────────────
    # controles de reprodução
    # ──────────────────────────────────────────────────────────────────────

    def play(self) -> None:
        """
        Inicia ou retoma a reprodução.
        """

        if self._tocando:
            print("já está tocando.")
            return

        try:
            self._processo = subprocess.Popen(["timidity", ARQUIVO_TEMP])
            self._tocando = True
            self._pausado = False
            print("reprodução iniciada.")
        except Exception as e:
            print(f"erro ao tocar o arquivo: {e}")

    def pause(self) -> None:
        """
        Pausa a reprodução.
        """

        if self._processo is None:
            print("não está tocando.")
            return

        self._processo.send_signal(subprocess.signal.SIGSTOP)
        self._pausado = True
        self._tocando = False
        print("reprodução pausada.")

    def stop(self) -> None:
        """
        Para a reprodução.
        """

        if self._processo is not None:
            self._processo.terminate()
            self._processo.wait()
            self._processo = None

        self._tocando = False
        self._pausado = False
        print("reprodução parada.")

    def restart(self) -> None:
        """
        Reinicia a reprodução.
        """

        self.stop()
        self.play()

    def resume(self) -> None:
        """
        Retoma a reprodução após uma pausa.
        """

        if self._processo is None:
            self.play()
            return

        self._processo.send_signal(subprocess.signal.SIGCONT)
        self._tocando = True
        self._pausado = False
        print("reprodução retomada.")

    def esta_tocando(self) -> bool:
        """
        Retorna True se a música estiver tocando.
        """

        if self._processo is None:
            return False

        return self._processo.poll() is None

    def aguardar_fim(self) -> None:
        """
        Aguarda o término da reprodução.
        """

        while self.esta_tocando():
            time.sleep(0.5)

    def encerrar(self) -> None:
        """
        Encerra o player.
        """

        self.stop()