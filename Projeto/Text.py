class TextLoadFile:
    """
    Classe responsável por carregar arquivos TXT.
    """

    def __init__(self, path: str = ""):
        self.path = path

    def loadFile(self) -> str:
        """
        Carrega e retorna o conteúdo do arquivo.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo não encontrado: {self.path}"
            )


class TextReader:
    """
    Classe responsável por ler e percorrer o texto.
    """

    def __init__(self, texto: str = ""):
        self.texto = texto
        self.currentIndex = 0

    def readText(self, texto: str) -> None:
        """
        Recebe o texto digitado pelo usuário.
        """
        self.texto = texto
        self.currentIndex = 0

    def getText(self) -> str:
        """
        Retorna todo o texto armazenado.
        """
        return self.texto

    def getNextCharacter(self) -> str | None:
        """
        Retorna o próximo caractere do texto.
        Retorna None quando chegar ao final.
        """
        if self.currentIndex >= len(self.texto):
            return None

        character = self.texto[self.currentIndex]
        self.currentIndex += 1

        return character

    def getLines(self) -> list[str]:
        """
        Retorna as linhas do texto.
        Cada linha representa uma voz na Fase 2.
        """
        return self.texto.splitlines()