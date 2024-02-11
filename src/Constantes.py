#Archivo para declarar constantes de la aplicacion

TITULO_INTERFAZ = "Othello"
TITULO = "OTHELLO"

#Dimensiones
VENTANA_LARGO = 700 
VENTANA_ANCHO = 1100

ORIGEN_MARGO = {'x':30,'y':30}
ORIGEN_TABLERO = {'x':117,'y':117}
FIN_MARCO = {'x':667,'y':667}
FIN_TABLERO = {'x':583,'y':583}
DIM_TABLERO = FIN_TABLERO['x']-ORIGEN_TABLERO['x']
CELDAS = 8
DIM_CELDA = DIM_TABLERO / CELDAS
DIM_FICHA = DIM_CELDA

#Turno 
TURNO = "Turno:"
DIM_FICHA_TURNO = DIM_FICHA/1.5

LOCALIZACION_CENTRO_DERECHA =  FIN_MARCO['x'] + ((VENTANA_ANCHO - FIN_MARCO['x']) //2 )

#Fuentes
FUENTE = "../Fuentes/KarmaSuture.ttf"
FUENTE_TITULO = "../Fuentes/KarmaSuture.ttf"
ESPACIADO_TITULO = 2
ESPACIADO_TURNO = 1
ESPACIADO_BOTONES = 1

#Imagenes
IMG_TABLERO = "../Assets/Board-othello.png"
IMG_FICHA_BLANCA = "../Assets/Pieza-blanca.png"
IMG_FICHA_NEGRA = "../Assets/Pieza-negra.png"
IMG_FONDO_MENU_PRINCIPAL = "../Assets/Fondo-Menu-Tablero.png"
IMG_FONDO_JUEGO = "../Assets/Fondo-Menu.png"
IMG_BOTON = "../Assets/Boton.png"
IMG_BOTON_ENCIMA = "../Assets/Boton-Encima.png"

#Botones
ANCHURA_BOTON = 250
ALTURA_BOTON = 100
TEXTO_BOTON_IA = "1 VS IA"
TEXTO_BOTON_JUGADORES = "1 VS 1"

#Colores RGB
BLANCO_RGB = (255,255,255)
NEGRO_RGB = (0,0,0)
MARRON_RGB = (104,68,53)
VERDE_RGB = (45,86,50)

#Jugadores
BLANCO = 2
NEGRO = 1
P1 = 1
P2 = 2

#Tablero (hacer con un enumerado)
A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6 
H = 7
