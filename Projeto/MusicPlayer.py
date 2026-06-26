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
    controla a reprodução com pygame (play, pause, stop, restart).
    """

    def __init__(self, settings=None):
        self._pausado        = False  # true quando a reprodução está pausada
        self._tocando        = False  # true quando a reprodução está ativa
        self._processo       = None
    # ──────────────────────────────────────────────────────────────────────
    # controles de reprodução
    # ──────────────────────────────────────────────────────────────────────

    def play(self) -> None:

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

    def stop(self) -> None:

        if self._processo is not None:
            self._processo.terminate()
            self._processo.wait()
            self._processo = None

            self._tocando = False
            self._pausado = False
    print("reprodução parada.")

    def pause(self):
        print("Pausa não suportada no Linux usando timidity.")

    def restart(self):
        self.stop()
        self.play()

    def esta_tocando(self):

        if self._processo is None:
            return False

        return self._processo.poll() is None

    def aguardar_fim(self) -> None:
        """
        bloqueia até a música terminar por completo.
        útil em scripts simples que não têm interface gráfica.
        """
        while self.esta_tocando():
            time.sleep(0.5)

    def encerrar(self):
        self.stop()

    # ──────────────────────────────────────────────────────────────────────
    # métodos privados
    # ──────────────────────────────────────────────────────────────────────

