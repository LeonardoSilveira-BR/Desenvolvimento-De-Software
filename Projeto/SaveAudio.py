import shutil
import tkinter as tk
from tkinter import filedialog


class SaveAudio:
    def salvar_com_local(self):
        # configuração do tkinter para abrir a janela escondendo o fundo
        root = tk.Tk()
        root.withdraw()

        # força a janela a aparecer na frente de tudo
        root.attributes("-topmost", True)

        print("Abrindo janela para escolher o local e o nome do arquivo")

        # abre a janela "salvar Como"
        caminho_completo = filedialog.asksaveasfilename(
            initialfile='minha_musica.mid',
            defaultextension=".mid",
            filetypes=[("Arquivos MIDI", "*.mid"),
                       ("Todos os arquivos", "*.*")],
            title="Escolha onde salvar sua música"
        )

        if caminho_completo:
            try:
                shutil.copy("faixa_gerada.mid", caminho_completo)
                print(f"Música salva com sucesso em: {caminho_completo}")
            except FileNotFoundError:
                print("Erro: O arquivo 'faixa_gerada.mid' não foi encontrado.")
        else:
            print("Operação de salvamento cancelada pelo usuário.")

    '''def salvar_pelo_terminal(self):
        nome_arquivo = input("Digite o nome do arquivo para salvar: ")

        # Se o usuário não digitar nada, define um nome padrão para não dar erro
        if not nome_arquivo.strip():
            nome_arquivo = "musica_final"

        # 3. Garante que o nome termine com a extensão .mid caso o usuário esqueça
        if not nome_arquivo.endswith(".mid"):
            nome_arquivo += ".mid"

        # 4. Faz a cópia do arquivo temporário para o novo nome
        try:
            shutil.copy("faixa_gerada.mid", nome_arquivo)
            print(f"Música salva com sucesso como: {nome_arquivo}")
        except FileNotFoundError:
            print("Erro: O arquivo 'faixa_gerada.mid' não foi encontrado na pasta.")
'''


# testa
salvador = SaveAudio()
salvador.salvar_com_local()
