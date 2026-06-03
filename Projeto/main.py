from Text import TextReader
from MusicGenerator import MusicGenerator
from MusicPlayer import MusicPlayer
from Settings import Settings


# ----Testes ----
texto = "[0] > > C D E F G A G \n[4] > G A H C D E F "
leitor = TextReader()
leitor.readText(texto) 

user_settings = Settings()
Settings.settings(user_settings)

musica = MusicGenerator()
musica.produz_MIDI(texto, user_settings)

if musica._arquivo_gerado:
    player = MusicPlayer()
    player.play()
    player.aguardar_fim()
    player.encerrar()
else: 
    print(f"arquivo midi não foi gerado!")
