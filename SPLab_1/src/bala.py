import pygame
from configuracion import *

class Bala(pygame.sprite.Sprite):
    def __init__(self, ubicacion: tuple, tamanio: tuple, color: tuple, direccion: int):
        super().__init__()
        self.image = pygame.Surface(tamanio)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.midbottom = ubicacion
        self.direccion = direccion

    def mover(self, velocidad: int):
        """mover Se encarga de mover con una dirección la bala en cuestión

        Args:
            velocidad (int): Velocidad a la cual se va a mover la bala
        """        
        self.rect.y += velocidad * self.direccion

    def update(self):
        pass

    def dibujar(self, pantalla: pygame.surface.Surface):
        """dibujar Se encarga de dibujar la bala creada

        Args:
            pantalla (Surface): Pantalla principal del juego
        """        
        pantalla.blit(self.image, self.rect)
