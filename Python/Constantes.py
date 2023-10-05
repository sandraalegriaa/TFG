#Archivo para declarar constantes de la aplicacion

TITULO_INTERFAZ = "Othello"

#Dimensiones
VENTANA_LARGO = 700
VENTANA_ANCHO = 700

ORIGEN_TABLERO = {'x':117,'y':117}
FIN_TABLERO = {'x':583,'y':583}
DIM_TABLERO = FIN_TABLERO['x']-ORIGEN_TABLERO['x']
CELDAS = 8
DIM_CELDA = DIM_TABLERO / CELDAS
DIM_FICHA = DIM_CELDA

#Imagenes
IMG_TABLERO = "./Assets/Board-othello.png"
IMG_FICHA_BLANCA = "./Assets/Pieza-blanca.png"
IMG_FICHA_NEGRA = "./Assets/Pieza-negra.png"

#Colores RGB
BLANCO = (255,255,255)
NEGRO = (0,0,0)

#Jugadores
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
