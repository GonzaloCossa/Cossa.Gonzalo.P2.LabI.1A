import pygame
from jugador import Jugador
from arma import Arma
from enemigo import Enemigo
from configuracion import *

class Juego:
    def __init__(self):
        # Iniciando pygame y estableciendo la pantalla, fondo y nombre
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode(TAMANIO_PANTALLA)
        self.fondo = pygame.transform.scale(pygame.image.load("assets/images/fondo.png").convert_alpha(), TAMANIO_PANTALLA)
        pygame.display.set_caption("Master Galaxy")

        # Reloj y banderas
        self.clock = pygame.time.Clock()
        self.jugando = False
        self.derrota = False
        self.victoria = False

        # Botones para la parte de los menus
        self.boton_jugar_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50)
        self.boton_salir_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 110, 200, 50)
        self.boton_reiniciar_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50)
        self.boton_nivel_1_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 100, 200, 50)
        self.boton_nivel_2_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2, 200, 50)
        self.boton_nivel_3_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50)

        # Fuente de texto del programa
        self.fuente = pygame.font.Font("assets/fonts/fuente_arcade.ttf", TAMANIO_FUENTE)

        # Grupos con los sprites
        self.todos_los_sprites = pygame.sprite.Group()  # Grupo de sprites
        self.enemigos = pygame.sprite.Group()

        # Carga de los diferentes sonidos
        self.sonido_disparo = pygame.mixer.Sound("assets/sounds/sonido_disparo.mp3")
        self.sonido_explosion = pygame.mixer.Sound("assets/sounds/sonido_explosion.mp3")

        # Creacion de niveles y dificultad
        self.num_filas = 0
        self.num_columnas = 0
        self.velocidad_enemigo = 0

        # Creacion de nave y su respectiva arma
        self.arma = Arma(ROJO, BALAS_MAXIMAS, self.sonido_disparo)
        self.nave_uno = Jugador("assets/images/nave.png", TAMANIO_NAVE, self.arma)
        
        # Añadiendo a los sprites la nave y estableciendo el puntaje del juego 
        self.todos_los_sprites.add(self.nave_uno)
        self.puntaje = 0

    def comenzar(self):
        """comenzar Comienza mostrando el menu principal del juego
        """        
        self.mostrar_menu_principal()

    def iniciar_juego(self):
        """iniciar_juego Establece el inicio del juego y la creacion de enemigos junto a la iteración del bucle principal del juego
        """        
        self.jugando = True
        self.crear_enemigos()
        self.ejecutar()

    def ejecutar(self):
        """ejecutar Es el bucle principal del juego, mientras se esté jugando se establece el tick y se realiza el resto de manejos
        """        
        while self.jugando:
            self.clock.tick(FPS)
            self.manejo_eventos()
            if self.jugando and not self.derrota and not self.victoria: # Actualizar y dibujar solo si no hay derrota y sigue jugando
                self.update()
                self.dibujar()
        pygame.quit()

    def manejo_eventos(self):
        """manejo_eventos Se encarga del manejo principal de eventos dentro de la ventana, en caso de cerrar la ventana deja de seguir jugando
        y en caso de tocar el boton de reiniciar, reinicia el juego
        """        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.derrota:
                if self.boton_reiniciar_rect.collidepoint(event.pos):
                    self.reiniciar_juego()
    
    def update(self):
        # Actualizaciones lógicas del juego
        self.todos_los_sprites.update()
        self.detectar_colisiones_jugador()
        self.detectar_colisiones_bala()

    def dibujar(self):
        # Dibujar elementos del juego
        self.pantalla.blit(self.fondo, ORIGIN)  # Dibujar fondo
        # Dibujar informacion del jugador
        self.mostrar_informacion_jugador()
        # Dibujar balas
        self.arma.dibujar_balas(self.pantalla)
        # Dibujo el resto de sprites
        self.todos_los_sprites.draw(self.pantalla)
        # Muestro en caso de derrota o victoria el respectivo mensaje
        self.mostrar_mensaje_derrota()
        self.mostrar_mensaje_victoria()
        # Actualizo la pantalla 
        pygame.display.flip()
    
    def mostrar_menu_principal(self):
        """mostrar_menu_principal Muestra el menú principal del juego con las opciones Jugar o Salir
        """        
        menu_principal = True
        # Manejo de eventos del menú
        while menu_principal:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_principal = False
                    self.jugando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_jugar_rect.collidepoint(event.pos):
                        menu_principal = False
                        self.mostrar_menu_niveles()
                    elif self.boton_salir_rect.collidepoint(event.pos):
                        menu_principal = False

            if menu_principal:
                # Agrego el fondo a la pantalla
                self.pantalla.blit(self.fondo, ORIGIN)

                # Dibujo los 2 rectangulos con los cuales valido que el usuario haga click
                pygame.draw.rect(self.pantalla, VERDE, self.boton_jugar_rect)
                pygame.draw.rect(self.pantalla, ROJO, self.boton_salir_rect)

                # Agrego los textos de cada botón
                texto_jugar = self.fuente.render("Jugar", True, NEGRO)
                texto_salir = self.fuente.render("Salir", True, NEGRO)

                # Muevo los textos sobre los botones
                posicion_texto_jugar = texto_jugar.get_rect(center = self.boton_jugar_rect.center)
                posicion_texto_salir = texto_salir.get_rect(center = self.boton_salir_rect.center)
                
                # Agrego en la pantalla los textos sobre los botones
                self.pantalla.blit(texto_jugar, posicion_texto_jugar)
                self.pantalla.blit(texto_salir, posicion_texto_salir)

                # Actualizo la pantalla
                pygame.display.flip()

    def mostrar_menu_niveles(self):
        """mostrar_menu_niveles Muestra el menú de los 3 niveles disponibles 
        """        
        menu_niveles = True
        while menu_niveles:
            # Manejo de eventos del menú
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_niveles = False
                    self.jugando = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_nivel_1_rect.collidepoint(event.pos):
                        self.num_filas = 2
                        self.num_columnas = 4
                        self.velocidad_enemigo = 1
                        self.iniciar_juego()
                        menu_niveles = False
                    elif self.boton_nivel_2_rect.collidepoint(event.pos):
                        self.num_filas = 3
                        self.num_columnas = 6
                        self.velocidad_enemigo = 2
                        self.iniciar_juego()
                        menu_niveles = False
                    elif self.boton_nivel_3_rect.collidepoint(event.pos):
                        self.num_filas = 4
                        self.num_columnas = 8
                        self.velocidad_enemigo = 2
                        self.iniciar_juego()
                        menu_niveles = False

            if menu_niveles:
                # Agrego el fondo a la pantalla
                self.pantalla.blit(self.fondo, ORIGIN)

                # Dibujo los 3 rectangulos con los cuales valido que el usuario haga click
                pygame.draw.rect(self.pantalla, VERDE, self.boton_nivel_1_rect)
                pygame.draw.rect(self.pantalla, AMARILLO, self.boton_nivel_2_rect)
                pygame.draw.rect(self.pantalla, ROJO, self.boton_nivel_3_rect)

                # Agrego el titulo y los textos de los 3 niveles
                texto_titulo = self.fuente.render("Selecciona un nivel", True, ROJO)
                texto_nivel_1 = self.fuente.render("Facil", True, NEGRO)
                texto_nivel_2 = self.fuente.render("Medio", True, NEGRO)
                texto_nivel_3 = self.fuente.render("Dificil", True, NEGRO)

                # Posiciono todos los textos
                posicion_texto_titulo = texto_titulo.get_rect(center = (ANCHO // 2, ALTO // 2 - 150))
                posicion_texto_nivel_1 = texto_nivel_1.get_rect(center = self.boton_nivel_1_rect.center)
                posicion_texto_nivel_2 = texto_nivel_2.get_rect(center = self.boton_nivel_2_rect.center)
                posicion_texto_nivel_3 = texto_nivel_3.get_rect(center = self.boton_nivel_3_rect.center)
                
                # Añado los textos a la pantalla
                self.pantalla.blit(texto_titulo, posicion_texto_titulo)
                self.pantalla.blit(texto_nivel_1, posicion_texto_nivel_1)
                self.pantalla.blit(texto_nivel_2, posicion_texto_nivel_2)
                self.pantalla.blit(texto_nivel_3, posicion_texto_nivel_3)

                # Actualizo la pantalla
                pygame.display.flip()

    def crear_enemigos(self):
        # Calcular la posición inicial de la formación
        posicion_inicial_x = (ANCHO - (self.num_columnas * (TAMANIO_ENEMIGO[0] + ESPACIO_ENTRE_ENEMIGOS))) // 2
        posicion_inicial_y = 25

        # Crear enemigos y agregarlos al grupo de enemigos
        for fila in range(self.num_filas):
            for columna in range(self.num_columnas):
                x = posicion_inicial_x + columna * (TAMANIO_ENEMIGO[0] + ESPACIO_ENTRE_ENEMIGOS)
                y = posicion_inicial_y + fila * (TAMANIO_ENEMIGO[1] + ESPACIO_ENTRE_ENEMIGOS)
                enemigo = Enemigo("assets/images/nave_enemigo.png", (x, y), TAMANIO_ENEMIGO, self.velocidad_enemigo)
                self.enemigos.add(enemigo)
                self.todos_los_sprites.add(enemigo)

    def reiniciar_juego(self):
        """reiniciar_juego Se encarga de reiniciar todos los valores de las flags y eliminar todos los sprites y volviendolos a crear
        """        
        self.derrota = False
        self.jugando = True
        self.victoria = False
        self.nave_uno.salud = SALUD_JUGADOR
        self.todos_los_sprites.empty()
        self.enemigos.empty()
        self.nave_uno.arma.eliminar_balas()
        self.nave_uno = Jugador("assets/images/nave.png", TAMANIO_NAVE, self.arma)
        self.todos_los_sprites.add(self.nave_uno)
        self.crear_enemigos() 
    
    def detectar_colisiones_jugador(self):
        """detectar_colisiones_jugador Revisa si ha habido un choque entre la nave y cualquier enemigo, en caso de haberlo se le resta
        una vida a la nave, en caso de que las vidas lleguen a 0, se pierde la partida
        """        
        colisiones_jugador = pygame.sprite.spritecollide(self.nave_uno, self.enemigos, True)
        if colisiones_jugador:
            # Se ha producido una colisión con un enemigo
            self.nave_uno.salud -= 1  # Resta 1 a la salud del jugador
            self.sonido_explosion.play()
            if self.nave_uno.salud <= 0:        
                self.derrota = True

    def detectar_colisiones_bala(self):
        """detectar_colisiones_bala Revisa si ha habido un choque entre el disparo de la nave y cualquier enemigo, en caso de haberlo 
        se elimina la nave y la bala, se suma 10 puntos y en caso de que ya no haya enemigos se declara la victoria del nivel
        """        
        colisiones_balas_enemigos = pygame.sprite.groupcollide(self.arma.balas, self.enemigos, True, True)
        for bala, enemigos_colisionados in colisiones_balas_enemigos.items():
            self.sonido_explosion.play()
            self.puntaje += 10
            if len(self.enemigos) == 0:
                self.victoria = True

    def mostrar_mensaje_derrota(self):
        """mostrar_mensaje_derrota En caso de haber derrota muestra el mensaje y la respectiva opcion de reiniciar la partida
        """        
        if self.derrota:
            # Declaro los mensajes
            mensaje_derrota = "Has Perdido"
            mensaje_reiniciar = "Reiniciar"

            # Creo la superficie de los mensajes
            texto_derrota = self.fuente.render(mensaje_derrota, True, ROJO)
            texto_reiniciar = self.fuente.render(mensaje_reiniciar, True, NEGRO)

            # Posiciono las superficies
            posicion_derrota = texto_derrota.get_rect(center = CENTER)
            posicion_reiniciar = texto_reiniciar.get_rect(center = self.boton_reiniciar_rect.center)

            # Añado a la pantalla el respectivo mensaje y el botón de reiniciar
            self.pantalla.blit(texto_derrota, posicion_derrota)
            pygame.draw.rect(self.pantalla, ROJO, self.boton_reiniciar_rect)
            self.pantalla.blit(texto_reiniciar, posicion_reiniciar)
    
    def mostrar_mensaje_victoria(self):
        """mostrar_mensaje_victoria En caso de haber victoria muestra el mensaje y la respectiva opcion de salir de la partida
        """ 
        # Declaro los mensajes       
        mensaje_victoria = "Ganaste"
        mensaje_salir = "Salir"

        # Creo la superficie de los mensajes
        texto_victoria = self.fuente.render(mensaje_victoria, True, VERDE)
        texto_salir = self.fuente.render(mensaje_salir, True, NEGRO)

        # Acomodo las superficies en la pantalla
        posicion_victoria = texto_victoria.get_rect(center = CENTER)
        posicion_salir = texto_salir.get_rect(center = self.boton_salir_rect.center)

        # Mientras haya victoria 
        while self.victoria:
            # Realizo el manejo de eventos para que pueda cerrar la ventana o usar el botón de salir
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.victoria = False
                    self.jugando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_salir_rect.collidepoint(event.pos):
                        self.victoria = False
                        self.jugando = False

            # Añado el fondo a la pantalla y el texto de victoria
            self.pantalla.blit(self.fondo, ORIGIN)
            self.pantalla.blit(texto_victoria, posicion_victoria)
            
            # Muestro el botón de salir y actualizo la pantalla
            pygame.draw.rect(self.pantalla, ROJO, self.boton_salir_rect)
            self.pantalla.blit(texto_salir, posicion_salir)
            pygame.display.flip()

    def mostrar_informacion_jugador(self):
        """mostrar_informacion_jugador De forma constante se encarga de mostrar la salud y puntaje actual del personaje
        """  
        # Mensajes que mostrará la informacion      
        mensaje_vidas = f"Vidas {self.nave_uno.salud}"
        mensaje_puntaje = f"Puntaje {self.puntaje}"

        # Superficies con la informacion
        texto_vidas = self.fuente.render(mensaje_vidas, True, BLANCO)
        texto_puntaje = self.fuente.render(mensaje_puntaje, True, BLANCO)

        # Muestro en la parte superior de la pantalla la informacion
        self.pantalla.blit(texto_vidas, (CENTER_X * 0.5, 5))
        self.pantalla.blit(texto_puntaje, (CENTER_X * 1.25, 5))