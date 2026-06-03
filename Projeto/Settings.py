import sys
sys.dont_write_bytecode = True  # Impede o Python de criar a pasta __pycache__

from Voice import Voice

# CONSTANTES
BPM_INICIAL = 120
VOLUME_INICIAL = 70
ATRASO_INICIAL = 0

# Maximos e minimos
VOLUME_MIN = 0
VOLUME_MAX = 127
BPM_MIN = 20
BPM_MAX = 300

# Registros vocais
SOPRANO = 6  # Voz 0
ALTO = 5     # Voz 1
TENOR = 4    # Voz 2
BAIXO = 3    # Voz 3

# Volumes iniciais
VOL_SOPRANO = 100  # Voz 0
VOL_ALTO = 80      # Voz 1
VOL_TENOR = 60     # Voz 2
VOL_BAIXO = 40     # Voz 3

# Instrumentos sugeridos
CRAVO = 6   # Voz 0
ORGAO = 20  # Voz 1
PIANO = 0   # Voz 2
FAGOTE = 70  # Voz 3


class Settings:
    def __init__(self):

        self.bpmAtual = BPM_INICIAL

        self.defaultInstrumentos = [CRAVO, ORGAO, PIANO, FAGOTE]

        self.vozes = [
            Voice(0, SOPRANO, VOL_SOPRANO, CRAVO, ATRASO_INICIAL),
            Voice(1, ALTO, VOL_ALTO, ORGAO, ATRASO_INICIAL),
            Voice(2, TENOR, VOL_TENOR, PIANO, ATRASO_INICIAL),
            Voice(3, BAIXO, VOL_BAIXO, FAGOTE, ATRASO_INICIAL)
        ]

    # ------------- Métodos para BPM -------------

    def resetBPM(self):
        self.bpmAtual = BPM_INICIAL

    # Recebe bpm escolhido na interface
    def setBPM(self, novo_bpm):
        if BPM_MIN <= novo_bpm <= BPM_MAX:
            self.bpmAtual = novo_bpm
        else:
            print(
                f"Erro: BPM {novo_bpm} inválido. Deve ser entre {BPM_MIN} e {BPM_MAX}.")

    # ------------- Métodos para volume geral (todas as vozes) -------------

    def resetVolumeGeral(self):
        for i in range(len(self.vozes)):
            self.vozes[i].setVolume(VOLUME_INICIAL)

    def setVolumeGeral(self, novo_volume):
        if VOLUME_MIN <= novo_volume <= VOLUME_MAX:
            for i in range(len(self.vozes)):
                self.vozes[i].setVolume(novo_volume)
        else:
            print(
                f"Erro: Volume {novo_volume} inválido. Deve ser entre {VOLUME_MIN} e {VOLUME_MAX}.")

    def increaseVolumeGeral(self):
        for i in range(len(self.vozes)):
            volume_atual = self.vozes[i].getVolume()
            if volume_atual < VOLUME_MAX:
                self.vozes[i].setVolume(volume_atual + 1)
            else:
                print(f"Voz {i} já está no volume máximo ({VOLUME_MAX}).")

    def decreaseVolumeGeral(self):
        for i in range(len(self.vozes)):
            volume_atual = self.vozes[i].getVolume()
            if volume_atual > VOLUME_MIN:
                self.vozes[i].setVolume(volume_atual - 1)
            else:
                print(f"Voz {i} já está no volume mínimo ({VOLUME_MIN}).")

    # ------------- Métodos para volume individual (cada voz) -------------
    def setVolumeVoz(self, voz, novo_volume):
        if 0 <= voz < len(self.vozes):
            if VOLUME_MIN <= novo_volume <= VOLUME_MAX:
                self.vozes[voz].setVolume(novo_volume)
            else:
                print(
                    f"Erro: Volume {novo_volume} inválido. Deve ser entre {VOLUME_MIN} e {VOLUME_MAX}.")
        else:
            print(
                f"Erro: Número de voz {voz} inválido. Deve ser entre 0 e {len(self.vozes)-1}.")

    def increaseVolumeVoz(self, voz):
        if 0 <= voz < len(self.vozes):
            volume_atual = self.vozes[voz].getVolume()
            if volume_atual < VOLUME_MAX:
                self.vozes[voz].setVolume(volume_atual + 1)
            else:
                print(f"Voz {voz} já está no volume máximo ({VOLUME_MAX}).")
        else:
            print(
                f"Erro: Número de voz {voz} inválido. Deve ser entre 0 e {len(self.vozes)-1}.")

    def decreaseVolumeVoz(self, voz):
        if 0 <= voz < len(self.vozes):
            volume_atual = self.vozes[voz].getVolume()
            if volume_atual > VOLUME_MIN:
                self.vozes[voz].setVolume(volume_atual - 1)
            else:
                print(f"Voz {voz} já está no volume mínimo ({VOLUME_MIN}).")
        else:
            print(
                f"Erro: Número de voz {voz} inválido. Deve ser entre 0 e {len(self.vozes)-1}.")

    # Método caso o usuário resete os intrumentos padrões (1 botão na interface)
    def resetInstrumentos(self):

        for i in range(len(self.vozes)):
            self.vozes[i].setInstrumento(self.defaultInstrumentos[i])

    # Método chamado quando o usuário troca o instrumento de uma das vozes (4 botões na interface?)
    def trocarInstrumento(self, voz, novo_instrumento):

        # Caso botões separados, botão passa qual voz e qual instrumento
        # self.vozes[voz].setInstrumento(novo_instrumento)

        if 0 <= voz < len(self.vozes):
            self.vozes[voz].setInstrumento(novo_instrumento)
        else:
            print(
                f"Erro: Número de voz {voz} inválido. Deve ser entre 0 e {len(self.vozes)-1}.")

    def settings(self):
        while True:
            print("\n1 - Alterar BPM")
            print("2 - Alterar volume geral")
            print("3 - Trocar instrumento")
            print("4 - Mostrar vozes")
            print("0 - Sair")
            print(f"instrumento escolhido: {self.vozes[0].instrumento}")
            opcao = input("Escolha: ")

            if opcao == "1":
                bpm = int(input("Novo BPM: "))
                self.setBPM(bpm)

            elif opcao == "2":
                volume = int(input("Novo volume Geral: "))
                self.setVolumeGeral(volume)

            elif opcao == "3":
                print("opcao3")
                voz = int(input("Voz (0-3): "))
                instrumento = int(input("Instrumento GM: "))
                self.trocarInstrumento(voz, instrumento)


            elif opcao == "4":
                print(f"\nBPM Atual: {self.bpmAtual}")
                for i in range(len(self.vozes)):
                    v = self.vozes[i]
                    # Ajustado para usar as funções getVolume() e o atributo correto do instrumento
                    print(f"Voz {i} | Vol={v.getVolume()} | Inst={v.instrumento}")

            elif opcao == "0":
                break


