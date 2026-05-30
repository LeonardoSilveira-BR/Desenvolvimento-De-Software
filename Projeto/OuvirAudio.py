#ouvir o audio

import time
import pygame
pygame.mixer.init()
try:
    pygame.mixer.music.load('testeLogica.mid')
    print("Tocando: {testeLogica.mid}")
    pygame.mixer.music.play()
except pygame.error as e:
        print(f"Erro!!!")
while pygame.mixer.music.get_busy():
    time.sleep(5)
pygame.mixer.quit()
