import pygame
from configuracion import *

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, path_imagen, ubicacion, tamanio: tuple, velocidad: int) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path_imagen).convert_alpha(), tamanio)
        self.rect = self.image.get_rect()
        self.rect.center = ubicacion
        self.velocidad = velocidad
    
    def update(self):
        """update Actualiza constantemente a los enemigos
        """        
        self.mover_enemigo()
        
    def mover_enemigo(self):
        """mover_enemigo Se encarga de hacer que los enemigos caigan y en caso de salir de la pantalla vuelven a aparece arriba
        """        
        self.rect.y += self.velocidad
        if self.rect.y > PANTALLA_BOTTOM:
            self.rect.y = PANTALLA_TOP
