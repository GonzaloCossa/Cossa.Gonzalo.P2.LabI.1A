import pygame
from bala import Bala
from configuracion import *

class Arma:
    def __init__(self, color_bala: tuple, maximo_balas: int, sonido_disparo: pygame.mixer.Sound):
        self.color_bala = color_bala
        self.maximo_balas = maximo_balas
        self.sonido_disparo = sonido_disparo
        self.balas = pygame.sprite.Group()
        self.disparando = False

    def disparar(self, ubicacion: tuple, tamanio_bala: tuple, direccion: int):
        """disparar Se encargar de hacaer disparar una bala del arma

        Args:
            ubicacion (tuple): Punto de origen de donde se origina el salto
            tamanio_bala (tuple): Tamaño de la bala
            direccion (int): Dirección para donde va a ser disparada la bala (-1) dispara para arriba
        """        
        if not self.disparando and len(self.balas) < self.maximo_balas:
            bala = Bala(ubicacion, tamanio_bala, self.color_bala, direccion)
            self.balas.add(bala)
            self.sonido_disparo.play()
            self.disparando = True

    def reiniciar_balas(self):
        """reiniciar_balas Vuelve la cantidad de balas que disparó a 0
        """        
        self.balas_disparadas = 0

    def eliminar_balas(self):
        """eliminar_balas Elimina todas las balas en la pantalla
        """        
        self.balas.empty()
    
    def mover_balas(self):
        """mover_balas Se encarga del movimiento vertical de la bala, si sobre pasa el limite del top de la pantalla, se elimina
        """        
        for bala in self.balas:
            bala.mover(VELOCIDAD_BALA)
            if bala.rect.bottom < 0:
                self.balas.remove(bala)

    def update(self):
        """update Actualiza la posicion de las balas
        """        
        self.mover_balas()

    def dibujar_balas(self, pantalla: pygame.surface.Surface):
        """dibujar_balas Dibuja las balas en la pantalla

        Args:
            pantalla (Surface): Pantalla principal del juego
        """        
        self.balas.draw(pantalla)

