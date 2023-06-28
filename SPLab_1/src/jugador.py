import pygame
from arma import Arma
from configuracion import *

class Jugador(pygame.sprite.Sprite):
    """Jugador Clase Jugador

    Args:
        pygame (Sprite): Hereda los atributos de un Sprite
    """    
    def __init__(self, path_imagen, tamanio: tuple, arma: Arma):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path_imagen).convert_alpha(), tamanio)
        self.rect = self.image.get_rect()
        self.rect.midbottom = PUNTO_ORIGEN_NAVE
        self.arma = arma
        self.salud = SALUD_JUGADOR
        self.disparando = False
    
    def moverse(self):
        """moverse Este atributo de la clase Jugador se encarga de realizar los movimientos de la nave
        """        
        teclas_presionadas = pygame.key.get_pressed()

        if teclas_presionadas[pygame.K_a] and self.rect.x - VELOCIDAD_JUGADOR > PANTALLA_LEFT + 15:  # IZQUIERDA
            self.rect.x -= VELOCIDAD_JUGADOR
        if teclas_presionadas[pygame.K_d] and self.rect.x + VELOCIDAD_JUGADOR + self.rect.width < ANCHO - 15:  # DERECHA
            self.rect.x += VELOCIDAD_JUGADOR
        if teclas_presionadas[pygame.K_w] and self.rect.y - VELOCIDAD_JUGADOR > PANTALLA_TOP + 15:  # ARRIBA
            self.rect.y -= VELOCIDAD_JUGADOR
        if teclas_presionadas[pygame.K_s] and self.rect.y + VELOCIDAD_JUGADOR + self.rect.height < ALTO - 15:  # ABAJO
            self.rect.y += VELOCIDAD_JUGADOR

        if teclas_presionadas[pygame.K_LSHIFT]:
            if not self.disparando:  # Disparar solo si no se está disparando actualmente
                self.disparar_arma()
                self.disparando = True
        else:
            self.disparando = False
    
    def disparar_arma(self):
        """disparar_arma Dispara el arma que lleva el juegador, validando que no esté disparando en ese momento y que las balas que 
        ya disparó sean una cantidad menor a las maximas posibles
        """        
        if not self.arma.disparando and len(self.arma.balas) < BALAS_MAXIMAS:
            self.arma.disparar(self.rect.midtop, TAMANIO_BALA, DISPARAR_ARRIBA)
    
    def validar_disparo(self):
        """validar_disparo Este atributo se encarga de validar que no haya error al momento de disparar y restablece self.disparando
        para poder volver a disparar
        """        
        if self.disparando and len(self.arma.balas) < BALAS_MAXIMAS:
            self.disparar_arma()
        elif not self.disparando:
            self.arma.disparando = False  # Restablecer el atributo "disparando" en el objeto "arma"
    
    def update(self):
        """update Se encarga de actualizar todos los metodos del jugador para luego poder dibujarlos en pantalla
        """        
        self.moverse()
        self.validar_disparo()
        self.arma.update()
    
    def dibujar(self, pantalla: pygame.surface.Surface):
        """dibujar Se encarga de dibujar en la pantalla las nuevas actualizaciones

        Args:
            pantalla (Surface): Pantalla principal del programa
        """        
        self.arma.dibujar_balas(pantalla)